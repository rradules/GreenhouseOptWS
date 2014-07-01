#import com.xhaus.jyson.JysonCodec as json
import cookielib
import json
import httplib
import urllib
import urllib2

def compute_efficiency(beta1, beta2, cT, T_opt, T_pred, T_0, max_T_heat, cB, B_opt, B_pred, max_B_light, pred_dt, json=False):
	alpha = 0.4
	dt = 1./6
	max_t = pred_dt * len(T_pred)
	max_T_heat = max_T_heat * dt
	T = [T_0]
	T_cost = [0]
	T_pred_full = [T_pred[0]]

	B = [B_pred[0]]
	B_cost = [0]
	B_pred_full = [B_pred[0]]

	t = [0]
	while t[-1] <= max_t:
		T_pred_t = T_pred[int(t[-1] / pred_dt)]
		T_pred_full.append(T_pred_t)
		T_heat = max(min((T_opt - T[-1]) * beta1, max_T_heat), -max_T_heat)
		if (T[-1] <= T_pred_t) != (T[-1] <= T_opt):
			T_heat -= (T_pred_t - T[-1]) * alpha
		T.append(T[-1] + ((T_pred_t - T[-1]) * alpha + T_heat) * dt)
		T_cost.append(cT*abs(T_heat))

		B_pred_t = B_pred[int(t[-1] / pred_dt)]
		B_pred_full.append(B_pred_t)
		B_light = max(0, min((B_opt - B_pred_t) * beta2, max_B_light))
		B.append(B_pred_t + B_light)
		B_cost.append(cB*B_light)

		t.append(t[-1] + dt)
	T_efficiency = [cT*(T_opt - x)**2 for x in T]
	B_efficiency = [cB*(B_opt - x)**2 for x in B]

	total_T_cost = sum(T_cost) * dt
	total_B_cost = sum(B_cost) * dt
	total_T_efficiency = sum(T_efficiency) * dt
	total_B_efficiency = sum(B_efficiency) * dt
	total_cost = total_T_cost + total_B_cost
	total_efficiency = total_T_efficiency + total_B_efficiency
	
	if json:
		results = {
			"T": T,
			"B": B,
			"T_predicted": T_pred_full,
			"B_predicted": B_pred_full,
			"T_cost": T_cost,
			"B_cost": B_cost,
			"total_T_cost": total_T_cost,
			"total_B_cost": total_B_cost,
			"total_cost": total_cost,
			"T_efficiency": T_efficiency,
			"B_efficiency": B_efficiency,
			"total_B_efficiency": total_B_efficiency,
			"total_T_efficiency": total_T_efficiency,
			"total_efficiency": total_efficiency,
			"t": t
		}
		return results
	else:
		return (total_T_efficiency, total_T_cost), (total_B_efficiency, total_B_cost)

def get_predictions():
	"""
	Returns the predictions over 5 days per 3 hours.
	"""
	def cloudiness_to_light(clouds, dt):
		return 500 + (100 - clouds) * 10 if 7 <= dt / 3600 % 24 <= 19 else 0
	
	conn = httplib.HTTPConnection("api.openweathermap.org")
	conn.request("GET", "/data/2.5/forecast?q=Brussels,be&mode=json")
	res = conn.getresponse()
	json_res = json.loads(res.read())

	dt = [x['dt'] for x in json_res['list']]
	assert(len(dt) >= 2)
	return [round(x['main']['temp'] - 273.15, 2) for x in json_res['list']], [cloudiness_to_light(x['clouds']['all'], x['dt']) for x in json_res['list']], (dt[1] - dt[0]) / 3600.

def get_greenhouse_temperature():
	"""
	Returns the current greenhouse temperature.
	"""
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.open('http://www.nassist-test.com/api/auth', urllib.urlencode({'UserName':'vubgreenhouse', 'Password':'vubgreenhouse'}))
	res = opener.open('http://www.nassist-test.com/api/sensors/4Noks_77000000-0000-0000-0000-000000000077_ZED_THL_16_Temperature_6/values?format=json&PageSize=1&PageId=1')
	json_res = json.loads(res.read())
	return json_res['Values'][1]['Value']
	
def termination_condition(beta1_interval, beta2_interval):
	return beta1_interval[1] - beta1_interval[0] < 0.01 and beta2_interval[1] - beta2_interval[0] < 0.01

def run(wT, wB, T_opt, B_opt, budget, max_T_heat, max_B_light):
	cT = 2;
	cB = 0.005;

	T_0 = get_greenhouse_temperature()
	T_pred, B_pred, pred_dt = get_predictions()
	beta1_interval = [0.0, max_T_heat / min(map(lambda x: abs(x - T_opt), T_pred))]
	beta2_interval = [0.0, max_B_light / min(map(lambda x: abs(x - B_opt), B_pred))]
	while not termination_condition(beta1_interval, beta2_interval):
		#print beta1_interval, beta2_interval
		beta1, beta2 = (beta1_interval[1] + beta1_interval[0]) / 2, (beta2_interval[1] + beta2_interval[0]) / 2
		(efficiency_T, cost_T), (efficiency_B, cost_B) = compute_efficiency(beta1, beta2, cT, T_opt, T_pred, T_0, max_T_heat, cB, B_opt, B_pred, max_B_light, pred_dt)
		#print beta1, efficiency_T, cost_T, beta2, efficiency_B, cost_B
		if cost_T > wT*budget: beta1_interval[1] = beta1
		else: beta1_interval[0] = beta1
		if cost_B > wB*budget: beta2_interval[1] = beta2
		else: beta2_interval[0] = beta2

	result = compute_efficiency(beta1_interval[0], beta2_interval[0], cT, T_opt, T_pred, T_0, max_T_heat, cB, B_opt, B_pred, max_B_light, pred_dt, True)
	#print beta1_interval[0], beta2_interval[0], result["total_T_efficiency"], result["total_B_efficiency"]	
	return result

def main(wT, wB, T_opt, B_opt, budget, max_T_heat, max_B_light):
	return json.dumps(run(wT, wB, T_opt, B_opt, budget, max_T_heat, max_B_light), sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf8')

if __name__ == "__main__":
	f = open('cost_efficiency.json', 'w')
	f.write(main(0.7, 0.3, 22.0, 1000, 904, 4.0, 750))
	f.close()

