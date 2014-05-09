#!/usr/bin/python2.6

import uuid
from nms_config import open_database_sqlalchemy_connection
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base

def rename_tablename(tablename):
    try:
        ss=""
        idx = tablename.index("_")
        ss = tablename[0:idx] + tablename[idx+1].upper() + tablename[idx+1+1:]
        ss=ss[0].upper() + ss[1:]
        return ss
    except Exception as e:
        return 1

def make_table_array(like_filter):
    db_connect=create_engine("mysql://root:root@localhost/information_schema")
    db = db_connect.connect() 
    table_array = []
    try:
        db_connect.echo=False
        metadata = MetaData(db_connect)
        result = db.execute("Select table_name from tables where table_name like '%s%%%%'" % like_filter)
        for row in result:
            table_array.append(row["table_name"])
        message = make_table_class_strucuture(table_array)
        db.close()
        return message
    except Exception as e:
        print str(e)

def make_table_class_strucuture(table_array):
    try:
        classes = ""
        mappers = ""
        for i in range(0,len(table_array)):
            c ,m = class_structure(table_array[i])
            classes += c
            mappers += m
        file = open('./odu_model.py','a')
        ##file.write(classes+ "\n\n")
        ##file.write(mappers)
        file.close()
        return "files write successfully"
    except Exception as e:
        return str(e[-1])
def class_structure(tablename):
    # Create A Database Connection
    table_rename = rename_tablename(tablename)
    if table_rename == 1:
        table_rename = tablename.capitalize()
    db_connect=create_engine("mysql://root:root@localhost/information_schema")
    db = db_connect.connect()
    mappers = "\n"
    class_structure_style ="\n\n"
    class_structure_style += "class %s(Base):\n\t__tablename__= \"%s\"\n" % (table_rename,tablename) 
    try:
        db_connect.echo=False
        metadata = MetaData(db_connect)
        result = db.execute("SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s'"%(tablename))
        for row in result:
            class_structure_style +="\t%s = Column(%s%s)\n" %(row['column_name'],row['column_type'].upper(),(",primary_key=True"if((row['column_key']) =="PRI" ) else ""))
        result = db.execute("SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s'"%(tablename))
        class_structure_style +="\n\tdef __init__(self"
        for row in result:
            class_structure_style +=",%s"%(row['column_name'])
        class_structure_style +="):\n\t\t"
        result = db.execute("SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s'"%(tablename))
        for row in result:
            class_structure_style +="self.%s = %s\n\t\t"%(row['column_name'],row['column_name'])
        class_structure_style +="\n\tdef __repr__(self):\n\t\t"
        class_structure_style += "return \"<%s("%(table_rename)
        result = db.execute("SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s'"%(tablename))
        for row in result:
            class_structure_style += "\'%s\',"
        class_structure_style = class_structure_style[0:len(class_structure_style)-1]
        class_structure_style += ")>\" %("
        result = db.execute("SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s'"%(tablename))
        for row in result:
            class_structure_style += "self.%s," %(row['column_name'])
        class_structure_style = class_structure_style[0:len(class_structure_style)-1]
        class_structure_style +=")"
        mappers += "mapper(%s,%s.__table__)"%(table_rename,table_rename)
        db.close()
        return class_structure_style , mappers
    except Exception as e:
        return str(e[-1])

#print class_structure('set_odu16_sys_omc_registration_table ')
print make_table_array("oi")
#make_table_class_strucuture(['odu100_eswATUConfigTable','odu100_eswBadFramesTable'])






