import com.xhaus.jyson.JysonCodec as json
import cookielib
#import json
import httplib
import urllib
import urllib2

def compute_efficiency(beta, T_opt, T_pred, T_pred_dt, T_0, max_T_heat, json=False):
	alpha = 0.4
	dt = 1./6
	max_t = T_pred_dt * len(T_pred)
	max_T_heat = max_T_heat * dt
	T = [T_0]
	cost = [0]
	result = [{"temperature": T_0, "cost": 0, "efficiency": 0, "t": 0}]

	t = [0]
	while t[-1] <= max_t:
		T_pred_t = T_pred[int(t[-1] / T_pred_dt)]
		T_heat = max(min((T_opt - T[-1]) * beta, max_T_heat), -max_T_heat)
		if (T[-1] <= T_pred_t) != (T[-1] <= T_opt):
			T_heat -= (T_pred_t - T[-1]) * alpha
		
		T.append(T[-1] + ((T_pred_t - T[-1]) * alpha + T_heat) * dt)
		cost.append(abs(T_heat))
		t.append(t[-1] + dt)
	print len(T), len(T_pred)
	efficiency = [(T_opt - x)**2 for x in T]

	total_cost = sum(cost) * dt
	total_efficiency = sum(efficiency) * dt
	
	if json:
		results = {
			"temperature": T,
			"cost": cost,
			"efficiency": efficiency,
			"total_cost": total_cost,
			"total_efficiency": total_efficiency,
			"t": t
		}
		return results
	else:
		return total_efficiency, total_cost

def get_predictions():
	"""
	Returns the predictions over 5 days per 3 hours.
	"""
	conn = httplib.HTTPConnection("api.openweathermap.org")
	conn.request("GET", "/data/2.5/forecast?q=Brussels,be&mode=json")
	res = conn.getresponse()
	json_res = json.loads(res.read())

	dt = [x['dt'] for x in json_res['list']]
	assert(len(dt) >= 2)
	return [round(x['main']['temp'] - 273.15, 2) for x in json_res['list']], (dt[1] - dt[0]) / 3600. #first entry is current weather

def get_greenhouse_temperature():
	"""
	Returns the current greenhouse temperature.
	"""
	return 10 ###
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.open('http://www.nassist-test.com/api/auth', urllib.urlencode({'UserName':'vubgreenhouse', 'Password':'vubgreenhouse'}))
	res = opener.open('http://www.nassist-test.com/api/sensors/4Noks_77000000-0000-0000-0000-000000000077_ZED_THL_16_Temperature_6/values?format=json&PageSize=1&PageId=1')
	json_res = json.loads(res.read())
	return json_res['Values'][1]['Value']
	
def termination_condition(beta_interval):
	return beta_interval[1] - beta_interval[0] < 0.01

def run(T_opt, budget, max_T_heat):	
	T_0 = get_greenhouse_temperature()
	T_pred, T_pred_dt = get_predictions()
	beta_interval = [0, max_T_heat / abs(max(T_pred) - T_opt)]
	while not termination_condition(beta_interval):
		print beta_interval
		beta = (beta_interval[1] + beta_interval[0]) / 2
		efficiency, cost = compute_efficiency(beta, T_opt, T_pred, T_pred_dt, T_0, max_T_heat)
		print efficiency, beta, cost
		if cost > budget: beta_interval[1] = beta
		else: beta_interval[0] = beta

	print beta_interval[0], compute_efficiency(beta_interval[0], T_opt, T_pred, T_pred_dt, T_0, max_T_heat) ###
	
	return compute_efficiency(beta_interval[0], T_opt, T_pred, T_pred_dt, T_0, max_T_heat, True)

def main(T_opt, budget, max_T_heat):
	return json.dumps(run(T_opt, budget, max_T_heat), sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":
	f = open('temperature.json', 'w')
	f.write(main(22.0, 904, 4.0))
	f.close()

