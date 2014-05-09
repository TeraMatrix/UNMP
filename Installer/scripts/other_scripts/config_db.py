#! /usr/bin/python -tt
try:
	from xml.dom.minidom import parse,Node,Text,Document
	from xml.parsers.expat import ExpatError
	import os.path
	import sys
except ImportError, e:
	print " Import Error Make sure python install ",str(e)
try:
	print len(sys.argv)
	if len(sys.argv) == 7:
		pass
	else:
		print " wrong argument : \n\t\t  use >  python make_xml.py  database_name hostname port username password "
		sys.exit(1)


	file_present = False 
	file_path = sys.argv[6]#'/home/cscape/Desktop/FirstXml.xml'	# change if location changed

	if(os.path.isfile(file_path)):
		file_present = True 		
	else:
		file_present = False

	if(os.path.isfile(file_path)):
		pass
	else:
		print " not able to create file "

	try:
		if file_present == True:
			dom = parse(file_path)

	except ExpatError, e:
		print " creating new file because of parsing error "
		file_present = False

	if file_present == True:
		print "hi"
		dom = parse(file_path)
		ts = dom.getElementsByTagName('mysql')
		ts[0].setAttribute("schema",sys.argv[1])
		ts[0].setAttribute("hostname",sys.argv[2])
		ts[0].setAttribute("port",sys.argv[3])
		ts[0].setAttribute("username",sys.argv[4])
		ts[0].setAttribute("password",sys.argv[5])
		xml_file = open(file_path,'w')
		dom.writexml(xml_file)
		xml_file.close()

	elif file_present == False :
		print " creating new file because file not present at given destination  %s "%sys.argv[6]
		doc = Document()
		nms = doc.createElement("nms")
		doc.appendChild(nms)
		mysql = doc.createElement("mysql")
		nms.appendChild(mysql)
		mysql.setAttribute("schema",sys.argv[1])
		mysql.setAttribute("hostname",sys.argv[2])
		mysql.setAttribute("port",sys.argv[3])
		mysql.setAttribute("username",sys.argv[4])
		mysql.setAttribute("password",sys.argv[5])	
		xml_file = open(file_path,'w')
		xml_file.write(doc.toprettyxml(indent=" "))
		xml_file.close()

	else:
		print " Some error occur "

except Exception, e:
	print " Exception occur : ",str(e)
	

