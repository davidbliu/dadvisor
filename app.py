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
# 
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
			if container_name not in charts:
				charts.append(container_name)
	# print data
	# print data
	# print 'that was data'
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
	app.run(port=5555, host=host)