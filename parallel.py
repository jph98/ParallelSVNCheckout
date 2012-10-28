#!/usr/bin/env python

import os
import os.path
import sys
import subprocess
from multiprocessing import Process

depth="immediates"
repository="http://svn.apache.org/repos/asf/tomcat/trunk"
local_dirname = "tomcat"

checkout_immediates_cmd="svn co --depth=%s %s %s > /dev/null 2>&1" % (depth, repository, local_dirname)
update_dir_cmd="svn update --set-depth infinity"

dir_name_ignores = ".svn"

"""Checkout a skeleton structure for the intermediate directories"""
def checkout_immediates():
	print "Executing %s " % checkout_immediates_cmd
	os.system(checkout_immediates_cmd)

"""Perform directory update"""
def perform_dir_update(dirname):
	command = "cd " + dirname + "; pwd; " + update_dir_cmd + " > /dev/null 2>&1"
	os.system(command)
	print "Process handling [" + dirname + "] exited"

if __name__ == "__main__":

	checkout_immediates()

	jobs = []

	for name in os.listdir(local_dirname):
		potential_directory = os.path.join(local_dirname, name)

		# Filter out svn metadata (e.g. .svn), only process directories
		if os.path.isdir(potential_directory) and dir_name_ignores not in name:
			process = Process(target=perform_dir_update, args=(potential_directory,))
			jobs.append(process)
			process.daemon = True
			process.start()

	# Wait for each daemonized job to finish up
	for job in jobs:
		job.join()