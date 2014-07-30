
import pickle
def load_collector():
	collector = None
	with open('stats_collector.pkl', 'rb') as input:
			collector = pickle.load(input)
	return collector

collector = load_collector()
# collector = advisor.load_collector()
# print collector.container_stats