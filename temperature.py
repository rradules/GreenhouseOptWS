import com.xhaus.jyson.JysonCodec as json

def func():
	T_0 = 10.0
	T_opt = 22.0
	T_pred = [23.0] * 8 * 5
	T_pred_dt = 3

	T_heat = 0

	alpha = 0.4

	dt = 1./6

	max_t = 24 * 5

	T = [T_0]
	cost = [0]

	t = 0
	while t <= max_t:
		T.append(T[-1] + ((T_pred[int(t / T_pred_dt)] - T[-1]) * alpha + T_heat) * dt)
		cost.append(T_heat**2)
		t += dt

	efficiency = [(T_opt - x)**2 for x in T]

	total_cost = sum(cost) * dt
	total_efficiency = sum(efficiency) * dt

	output = {
		'temperature': T,
		'cost': cost,
		'efficiency': efficiency,
		'total_cost': total_cost,
		'total_efficiency': total_efficiency,
		'dt': dt
	}

	f = open('temperature.json', 'w')
	json.dump(output, f, sort_keys=True, indent=4, separators=(',', ': '))
	f.close()

def main(T_opt, budget):
	print T_opt, budget
	return '{"test": 1}'

