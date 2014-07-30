import argparse
import atexit
import sys
import urlparse
import yaml
from flask import Flask, request, jsonify, render_template
import urllib2
import socket
import os
import shutil
import subprocess
import json
import ast
import dadvisor
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)
# re-initialize later
events = None
event_store = None
#
# graphs data for all containers running on this host
#
@app.route('/', methods=['GET', 'POST'])
def root():
	# print 'loading collector'
	collector = dadvisor.load_collector()
	# print collector
	#
	# provide a dict with {'chart-name':chart-data}
	#
	collector.clean()
	# dadvisor.update_collector()
	# print collector.container_stats
	data = {}
	charts = []
	for key in collector.container_stats.keys():
		container_name = key[0:5]
		stats = collector.container_stats[key].stats
		for s_key in stats.keys():
			chart_name = container_name+'::'+s_key
			data[chart_name] = stats[s_key]
			if 'container_'+container_name not in charts:
				charts.append('container_'+container_name)
	# print data
	# print data
	# print 'that was data'
	return render_template('stat.html', data = json.dumps(data), charts = charts)

@app.route('/container_metrics', methods=['GET', 'POST'])
def get_container_metrics():
	container_id = str(request.args.get('container_id'))
	print 'lol'
	# print container_id
	collector = dadvisor.load_collector()
	collector.clean()
	data = {}
	charts = []
	for key in collector.container_stats.keys():
		container_name = key[0:5]
		print key
		print container_id
		print '....'
		if key == container_id:
			stats = collector.container_stats[key].stats
			for s_key in stats.keys():
				chart_name = container_name+'::'+s_key
				data[chart_name] = stats[s_key]
				if 'container_'+container_name not in charts:
					charts.append('container_'+container_name)
	return render_template('stat.html', data = json.dumps(data), charts = charts)
if __name__ == '__main__':
	
	host='localhost'

	# os.system('printenv')
	# host = socket.gethostbyname(socket.gethostname())
	
	# subprocess.Popen(["python", '-u', "dadvisor.py"])
	print 'running your app'

	# print 'running sshd'
	# os.system("/usr/sbin/sshd -D &")
	# data = dadvisor.get_data()
	# print data
	# print 'that was data'
	dadvisor.threaded_collect()
	app.run(port=5000, host=host)