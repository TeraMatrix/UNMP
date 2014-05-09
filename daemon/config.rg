###########

## VNL unicast Discovery Server CONFIGURATION FILE

## Author : Rahul Gautam 

## This is a very sensitive file, Please only change it if you know what you are doing Otherwise it will cause failure for Server 

###########

### config_responce variable consists FTP server information and SNMP details
### Please fill each value appropriately 
### for config_responce every value must be in "" i quotes 


config_responce = {'2077':"@@SERVERIP@@",				#FTP_SERVER_IP
   		'2072':"unmpftp",					#FTP_USER_NAME
		'2073':"unmpftp@123",					#FTP_USER_PASSWORD
		'2075':"/unmpftp",			        	#USER_FTP_HOME
		'2071':"private",					#SNMP_WRITE_COMMUNITY_PREFIX
		'2070':"public",					#SNMP_READ_COMMUNITY_PREFIX
		'2069':"162",						#SNMP_TRAP_PORT
		'2068':"161"						#SNMP_REQUEST_PORT
	}		

###### My SQL parameters #### used by all files that resides in /omd/daemon folder

hostname = "@@HOSTNAME@@"
username = "@@USERNAME@@"
password = "@@PASSWORD@@"
schema = "@@SCHEMA@@"

###############
				
#thread_count = 105 						# change this variable if you want to spawn more than 100 threads from server (maximum is 185)
								# value 105 means your Server can serve 100 devices at a time 
								# (** IT DOESN'T MEAN THAT YOUR "SERVER" RESTRICT TO SERVE 100 DEVICES, YOUR SERVER CAN SERVE 1000 DEVICES WITHIN 30 MINS **)
								# this server can serve 10000 devices ( for more than 1000 devices thread_count must set to its maximum limit ).
								# in our next version we are making our server to serve 1000 devices in 200 seconds only  
								# if you set it more than 185 then it's default value is picked by Daemon that is 105
												
nms_ip = '127.0.0.1'             				# nms ip address used for nagios plugin that checks health of discovery server

server_ip_addr = '@@SERVERIP@@'                                  # server ip address
# '10.113.247.69'				
