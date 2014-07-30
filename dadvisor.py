import os
import time
from random import randint
import docker
import pickle
import threading
root_dir = os.environ.get('CROOT')
if not root_dir:
	root_dir = '/sys/fs'

class StatsCollector:
	def __init__(self):
		self.container_stats = {}
	def dump(self):
		with open('stats_collector.pkl', 'wb') as output:
			pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
	def clean(self):
		# print 'cleaning'
		# containers = docker_client.containers()
		# container_ids = map(lambda x: x['Id'], containers)
		container_ids = get_docker_ids(root_dir)
		# print container_ids
		for key in self.container_stats.keys():
			if key not in container_ids:
				self.container_stats.pop(key, None)
	def print_stats(self):
		for key in self.container_stats.keys():
			print key
			c_stats = self.container_stats[key]
			for s_key in c_stats.stats.keys():
				print '\t'+s_key+' length '+str(len(c_stats.stats[s_key]))

class ContainerStats:
	def __init__(self,container_id):
		self.id = container_id
		self.stats = {}

def load_collector():
	try:
		collector = None
		with open('stats_collector.pkl', 'rb') as input:
			collector = pickle.load(input)
		return collector
	except Exception as failure:
		print failure
		return StatsCollector()
#
# gets docker ids from docker daemon
#
def get_docker_ids_with_daemon():
	try:
		docker_client = docker.Client(base_url='unix://var/run/docker.sock',
	                  version='1.10',
	                  timeout=10)
	except:
		docker_client = docker.Client(base_url='unix://var/run/docker.sock',
	                  version='1.10',
	                  timeout=10)
	containers = docker_client.containers()
	container_ids = map(lambda x: x['Id'], containers)
	# print container_ids
	return container_ids
#
# gets docker ids from roaming around in cgroups
#
def get_docker_ids(root_dir = '/sys/fs'):
	# print 'monitoring'
	docker_ids = []
	for root, dirs, files in os.walk(root_dir+"/cgroup"):
		dir_split = root.split('/')
		if dir_split[len(dir_split)-2] == 'docker':
			d_id = dir_split[-1]
			if d_id not in docker_ids:
				docker_ids.append(dir_split[-1])
	return docker_ids

def get_container_data(container_id, root_path = '/sys/fs' ):
	memory_stat_path = root_path+'/cgroup/memory/docker/'+container_id+'/memory.stat'
	cpuacct_stat_path = root_path+'/cgroup/cpuacct/docker/'+container_id+'/cpuacct.stat'
	rand_i = int(randint(0,5))
	rss_stat = rand_i
	swap_stat = rand_i
	cache_stat = rand_i
	user_cpuacct_stats = rand_i
	system_cpuacct_stats = rand_i
	try:
		with open(memory_stat_path, 'r') as datafile:
			data = datafile.read()
			stats_split = data.split('\n')
			# print stats_split
			for split in stats_split:
				if 'rss '==split[0:4]:
					rss_stat = split.split(' ')[1]
				if 'swap ' == split[0:5]:
					swap_stat = split.split(' ')[1]
				if 'cache ' == split[0:6]:
					cache_stat = split.split(' ')[1]
	except Exception as failure:
		print failure
	try:
		with open(cpuacct_stat_path, 'r') as datafile:
			data = datafile.read()
			stats_split = data.split('\n')
			user_cpuacct_stats = stats_split[0].split(' ')[1]
			system_cpuacct_stats = stats_split[1].split(' ')[1]
	except Exception as failure:
		print failure


	
	rss_stat = int(rss_stat) + rand_i
	swap_stat = int(swap_stat) + rand_i
	cache_stat = int(cache_stat) + rand_i
	user_cpuacct_stats = int(user_cpuacct_stats) + rand_i
	system_cpuacct_stats = int(system_cpuacct_stats) + rand_i
	
	return {'rss_stat':int(rss_stat), 
			'swap_stat':int(swap_stat),
			'cache_stat':int(cache_stat), 
			'user_cpuacct_stats':int(user_cpuacct_stats), 
			'system_cpuacct_stats':int(system_cpuacct_stats)}


def update_collector(root_path = '/sys/fs'):
	collector = load_collector()
	# 
	# collect stats for each container and update collector
	# 
	containers = get_docker_ids_with_daemon()
	for container_id in containers:
		container_data = get_container_data(container_id, root_path)
		c_stat = collector.container_stats.get(container_id)
		if c_stat is None:
			container_stat = ContainerStats(container_id)
			container_stat.stats = {}
			container_stat.stats['memory_rss'] = [container_data['rss_stat']]
			container_stat.stats['memory_swap'] = [container_data['swap_stat']]
			container_stat.stats['memory_cache'] = [container_data['cache_stat']]
			container_stat.stats['cpuacct_user'] = [container_data['user_cpuacct_stats']]
			container_stat.stats['cpuacct_system'] = [container_data['system_cpuacct_stats']]
			collector.container_stats[container_id] = container_stat
		else:
			collector.container_stats[container_id].stats['memory_rss'].append(container_data['rss_stat'])
			collector.container_stats[container_id].stats['memory_swap'].append(container_data['swap_stat'])
			collector.container_stats[container_id].stats['memory_cache'].append(container_data['cache_stat'])
			collector.container_stats[container_id].stats['cpuacct_user'].append(container_data['user_cpuacct_stats'])
			collector.container_stats[container_id].stats['cpuacct_system'].append(container_data['system_cpuacct_stats'])
	#
	# save collector
	#
	collector.dump()


#
# long running process that updates collector
#
def collect():
	while True:
		update_collector(root_dir)
		collector = load_collector()
		collector.clean()
		time.sleep(5)
		# 
		# TODO variable collect interval
		# 

class ThreadClass(threading.Thread):
	def run(self):
		print 'thread is starting to collect data'
		print 'collecting on this root '+str(root_dir)
		collect()

	
def threaded_collect():
	t=ThreadClass()
	t.daemon=True
	t.start()
if __name__ == "__main__":
	# collect()
	get_docker_ids_with_daemon()
