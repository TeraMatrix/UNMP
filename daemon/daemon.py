#!/usr/bin/env python
"""
@summary: A seperate module that daemonize the python script that extends its Daemon class

@author: Rahul Gautam

@date: 20-Aug-2011

@organization: CodeScape Consultants Pvt. Ltd. 

"""

import sys, os, time, atexit
from signal import SIGTERM 

class Daemon:
	"""
	@author: RAHUL GAUTAM
	
	@summary: A generic daemon class that used to make a python class as a deamon service on operating system : this a pythonic way

	@note: Usage inherit the Daemon class and override the run() method

        @note: Final modification at date 28 Nov. 2011
	"""
	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		"""
		Daemon init method takes one active argument that is the process id file name : when you extend that class you must pass a file name to it (don't require the existance of file it will create that for you)
		"""
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
	
	def daemonize(self):
		"""
		do the UNIX double-fork magic
		"""
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit first parent
				sys.exit(0) 
		except OSError, e: 
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
	
		# decouple from parent environment
		os.chdir("/") 
		os.setsid() 
		os.umask(0) 
	
		# do second fork
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit from second parent
				sys.exit(0) 
		except OSError, e: 
			sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1) 
	
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# write pidfile
		atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile,'w+').write("%s\n" % pid)
	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already runs
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	        start_flag = 1
		if pid:
			try:
				procfile = file("/proc/%d/status" % pid, 'r')
				procfile.close()
			except IOError:
				start_flag = 0
				
                        if start_flag == 1:
				message = "  * Daemon Service is already running ? PID is %d \n"
				sys.stderr.write(message % pid)
				sys.exit(1)
		message = "  *Daemon Service is Starting ......				  [42m OK [0m	\n           please confirm with status OR log command\n"
		sys.stderr.write(message)
		# Start the daemon
		self.daemonize()
		self.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
		message = "  stoping ......... Please wait ....... \n"
		sys.stderr.write(message)

		if not pid:
			message = "  *Daemon Service is [91mnot running[0m [1m?[0m\n"
			sys.stderr.write(message)
			return # not an error in a restart

		# Try killing the daemon process	
		try:
			while 1:
				os.kill(pid, SIGTERM)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)
		message = "  *Daemon Service is Stopped				     [42m OK [0m  \n"
		sys.stderr.write(message)

	def restart(self):
		"""
		Restart the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if not pid:
			self.start()
		else:
			self.stop()
			time.sleep(5)
			self.start()
	
	def status(self):
		try:
			pf = file(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		try:
			procfile = file("/proc/%d/status" % pid, 'r')
			procfile.close()
		except IOError:
			sys.stdout.write("  *Probably Daemon Service is not running. There is not a process with the PID specified in PidFile  **try to Start it\n")
			sys.exit(0)
		except TypeError:
			sys.stdout.write("  *Daemon Service is not running. \n")
			sys.exit(0)

		sys.stdout.write("  *Daemon Service with the PID %d is [32mrunning [0m          [42m OK [0m \n" % pid)

	def run(self):
		"""
		@note: You should override this method when you inherit Daemon. It will be called after the process has been
		daemonized by start() or restart().
		"""
