import pprint

trap_devices = ["storage", "otaf"] #, "smsspam", "smsspamclear"]

trap_identification = map(lambda x : x + "Trap", trap_devices)

# def template_objects():

nocout = {
    "severity": { "type" : "integer", "values" : {'major': 4, 'clear': 0, 'warning': 2, 'critical': 5, 'informational': 1, 'minor': 3}, 
    "m2m" : "serevity" },
    "eventType": { "type" : "integer", "values" : {} , "m2m" : "trap_event_type" },
    "eventId": { "type" : "string", "values" : {}, "m2m" : "trap_event_id"},
    "managedObjectType": {"type" :"integer", "values" : {}, "m2m" : "manage_obj_name" },
    "managedObjectID": { "type" : "string", "values" : {} , "m2m" : "manage_obj_id" }, 
    "componentType" : { "type" : "integer", "values" : {"nocout-poller": 200, "nocout-application": 202}, "m2m" : "agent_id" },
    "componentID": { "type" : "string", "values" : {}, "m2m" : "component_id" },
    "eventDesc": { "type" : "string", "values" : {}, "m2m" : "description"},
    "trapTimeStamp": { "type" : "string", "values" : {}, "m2m": "timestamp"} 
}


# print ("="*20)
# pprint.pprint(nocout)
# print ("="*20)

otaf =  {
    "alarmType": {
        "type": "string",
        "values": [],
        "nocout": "eventId",
        "index" : 0
    },
    "alarmCategory": {
        "type": "string",
        "values": [],
        "nocout": "eventType",
        "index" : 1
    },
    "alarmSeverity": {
        "type": "string",
        "values": [
            "Warning",
            "Minor",
            "Major",
            "Critical",
            "CLEAR"
        ],
        "nocout": "severity",
        "index" : 2
    },
    "alarmPcause": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 3
    },
    "alarmDataTimeStamp": {
        "type": "string",
        "values": [],
        "nocout": "trapTimeStamp",
        "index" : 4
    },
    "alarmDescription": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 5
    },
    "alarmAdditioanlInfo": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 6
    },
    "alarmManualAutoClear": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 7
    },
    "alarmServiceImpact": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 8
    }
}

storage = {
    "deviceName": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 0
    },
    "alertLevel": {
        "type": "integer",
        "values": ['clear', 'minor', 'major', 'critical', 'down'],
        "nocout": "severity",
        "index" : 1
    },
    "message": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 2
    },
    "gridId": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 3
    },
    "deviceId": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 4
    },
    "componentName": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 5
    },
    "componentId": {
        "type": "string",
        "values": [],
        "nocout": "eventDesc",
        "index" : 6
    },
    "eventId": {
        "type": "string",
        "values": [],
        "nocout": "eventId",
        "index" : 7
    },
    "eventName": {
        "type": "string",
        "values": [],
        "nocout": "eventType",
        "index" : 8
    }
}

nocout_machine_map = {}

#create the mapping table to identify all the fields going in DB

for td in trap_devices:
    nocout_device_map = {
        "severity": [],
        "eventType": [],
        "eventId": [],
        "managedObjectType": [],
        "managedObjectID": [], 
        "componentType" : [],
        "componentID": [],
        "eventDesc": [],
        "trapTimeStamp": []
    }
    what_type = eval(td)
    nocout_machine_map[td] = []
    for keys in nocout_device_map:
        for key in what_type:
            if keys == what_type[key]["nocout"]:
                nocout_device_map[what_type[key]["nocout"]].append(key)
        nocout_machine_map[td] = nocout_device_map

# print ("="*20)
# pprint.pprint(nocout_machine_map)
# print ("="*20)


#read values from snmptt

def map_severity(severity):
    if lower(severity) == "clear":
        return "0"
    elif lower(severity) == "informational":
        return "1"
    elif lower(severity) == "minor":
        return "2"
    elif lower(severity) == "major":
        return "3"
    elif lower(severity) == "warning":
        return "4"
    elif lower(severity) == "critical":
        return "5"
    else:
        return "1"

def map_severity_storage(severity):
    if lower(str(severity)) == "0":
        return "0"
    elif lower(severity) == "informational":
        return "5"
    elif lower(str(severity)) == "1":
        return "1"
    elif lower(str(severity)) == "2":
        return "2"
    elif lower(str(severity)) == "3":
        return "3"
    elif lower(str(severity)) == "4":
        return "4"
    else:
        return "1"


def insert_values(device_type, format_line):

    m2m = {
        "serevity": "",
        "trap_event_id": "",
        "trap_event_type": "",
        "manage_obj_id": "",
        "manage_obj_name": "",
        "component_id": "",
        "trap_ip": "",
        "description": "",
    }

    print ("="*20)
    pprint.pprint(m2m)
    print ("="*20)


    mapped_objects = nocout_machine_map
    pprint.pprint(mapped_objects)
    
    fl = format_line.split("|")

    ret_str = ""

    if device_type == "storageTrap":
        ret_str += map_severity_storage(fl[1])
        ret_str += "|"
        ret_str += fl[7]
        ret_str += "|"
        ret_str += fl[8]
        ret_str += "|"
        ret_str += "200"
        ret_str += "|"
        ret_str += "nocout-application"
        ret_str += "|"
        ret_str += "storage"
        ret_str += "|"
        ret_str += fl[0]
        ret_str += "|"
        ret_str += "deviceName = "
        ret_str += fl[0]
        ret_str += "deviceId = "
        ret_str += fl[4]
        ret_str += "componentName = "
        ret_str += fl[5]
        ret_str += "componentId = "
        ret_str += fl[6]
        ret_str += "gridId = "
        ret_str += fl[3]
        ret_str += "message = "
        ret_str += fl[2]

        return ret_str

    elif device_type == "otafTrap":
        ret_str += map_severity(fl[2])
        ret_str += "|"
        ret_str += fl[0]
        ret_str += "|"
        ret_str += fl[1]
        ret_str += "|"
        ret_str += "200"
        ret_str += "|"
        ret_str += "nocout-application"
        ret_str += "|"
        ret_str += "otaf"
        ret_str += "|"
        ret_str += ""
        ret_str += "|"
        ret_str += "alarmPcause "
        ret_str += " "
        ret_str += fl[3]
        ret_str += "alarmDataTimeStamp "
        ret_str += " "
        ret_str += fl[4]
        ret_str += "alarmDescription "
        ret_str += " "
        ret_str += fl[5]
        ret_str += "alarmAdditioanlInfo "
        ret_str += " "
        ret_str += fl[6]
        ret_str += "alarmManualAutoClear "
        ret_str += " "
        ret_str += fl[7]
        ret_str += "alarmServiceImpact "
        ret_str += " "
        ret_str += fl[8]
        
    else:
        return "|||||||"