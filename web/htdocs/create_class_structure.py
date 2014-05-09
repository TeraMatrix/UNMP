#!/usr/bin/python2.6

import pprint
import os.path
import sys
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base


def rename_tablename(tablename):
    try:
        ss = ""
        idx = tablename.index("_")
        ss = tablename[0:idx] + tablename[idx + 1].upper(
        ) + tablename[idx + 1 + 1:]
        ss = ss[0].upper() + ss[1:]
        return ss
    except Exception as e:
        return 1


def make_table_array(like_filter):
    db_connect = create_engine(
        "mysql://root:root@localhost/information_schema")
    db = db_connect.connect()
    table_array = []
    try:
        db_connect.echo = False
        metadata = MetaData(db_connect)
        # result = db.execute("SELECT table_name FROM tables WHERE table_schema
        # = 'nms' AND table_name like '%s%%%%'" % like_filter)
        result = db.execute("SELECT table_name FROM tables WHERE table_schema = '%s' AND table_name like '%%%%%s%%%%'" %
                            (database_name, like_filter))
        for row in result:
            table_array.append(row["table_name"])

        print " Tables matches like %s in database %s " % (like_filter, database_name)
        pprint.pprint(table_array)
        print " File that is going to write is : %s " % (file_to_write)
        answer = raw_input(" Do you want to continue : yes/no  ")
        if answer == 'yes':
            message = make_table_class_strucuture(table_array)
        else:
            message = " Quit"

        db.close()
        return message
    except Exception as e:
        print str(e)


def make_table_class_strucuture(table_array):
    try:
        classes = ""
        mappers = ""
        for i in range(0, len(table_array)):
            c, m = class_structure(table_array[i])
            classes += c
            mappers += m
            # print
            # print c
            # print
            # print m
            # print
        f = open(file_to_write, 'a+')
        f.write(classes + "\n\n")
        f.write(mappers)
        f.close()
        return "\n-------------\n Files write successfully"
    except Exception as e:
        return str(e[-1])


def class_structure(tablename):
    # Create A Database Connection
    table_rename = rename_tablename(tablename)
    if table_rename == 1:
        table_rename = tablename.capitalize()
    db_connect = create_engine(
        "mysql://root:root@localhost/information_schema")
    db = db_connect.connect()
    mappers = "\n"
    class_structure_style = "\n\n"
    class_structure_style += "class %s(Base):\n\t__tablename__= \"%s\"\n" % (
        table_rename, tablename)
    try:
        db_connect.echo = False
        metadata = MetaData(db_connect)
        result = db.execute(
            "SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s' AND table_schema = '%s'" % (
            tablename, database_name))
        for row in result:
            class_structure_style += "\t%s = Column(%s%s)\n" % (row['column_name'], row['column_type'].upper(
            ), (",primary_key=True" if ((row['column_key']) == "PRI") else ""))

        result = db.execute(
            "SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s' AND table_schema = '%s'" % (
            tablename, database_name))
        class_structure_style += "\n\tdef __init__(self"
        for row in result:
            class_structure_style += ",%s" % (row['column_name'])

        class_structure_style += "):\n\t\t"
        result = db.execute(
            "SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s' AND table_schema = '%s'" % (
            tablename, database_name))
        for row in result:
            class_structure_style += "self.%s = %s\n\t\t" % (
                row['column_name'], row['column_name'])

        class_structure_style += "\n\tdef __repr__(self):\n\t\t"
        class_structure_style += "return \"<%s(" % (table_rename)
        result = db.execute(
            "SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s' AND table_schema = '%s'" % (
            tablename, database_name))
        for row in result:
            class_structure_style += "\'%s\',"

        class_structure_style = class_structure_style[0:len(
            class_structure_style) - 1]

        class_structure_style += ")>\" %("
        result = db.execute(
            "SELECT COLUMN_NAME , COLUMN_TYPE , COLUMN_KEY FROM COLUMNS WHERE table_name = '%s' AND table_schema = '%s'" % (
            tablename, database_name))
        for row in result:
            class_structure_style += "self.%s," % (row['column_name'])

        class_structure_style = class_structure_style[0:len(
            class_structure_style) - 1]

        class_structure_style += ")"
        mappers += "mapper(%s,%s.__table__)" % (table_rename, table_rename)
        db.close()
        return class_structure_style, mappers
    except Exception as e:
        return str(e[-1])


"""
TODO: class structure doesn't contains information of PRIMARY_KEY and RELATIONS
    For Now, that should be added by developer manually.
    And talking about manually i don't know how to define primary_key mapper
    althogh i do know FORIGN_KEY mapper
    See FixMe section below


File has two main variables

    database_name: specify which database you want to use, in which your db tables lies

    file_to_write: in which file you want to write generated class structure


File has 3 main functions

##class_structure('name_of_table')

    Note: will return and generate SqlAlchemy class strucure from argument table

    Usage:
        class_structure('hosts')

##make_table_class_strucuture([_list_of_db_tables_seperated_by_comma])

    Note: will generate class strucure for list of db tables specfied in argument,
            And write the class structure in file (file_to_write)
            this function will open the file in `append mode`
            so file should be present at specfied location

    Usage:
        make_table_class_strucuture(['odu100_7_2_29_oids','odu100_7_2_29_oids_multivalues'])

##make_table_array(like_filter)

    Note: Assume you have too many tables that contains string `XYZ`,
            And you want to create class structure for all of them
            and you don't what to write these table name's as a argument
            to any of the above function, then this one for you.

            replace like_filter to 'XYZ'

    Usage:
        you have tables odu100_7_2_29_oids, odu100_7_2_29_oids_multivalues, odu100_7_2_29_oid_table
        you found your like filter that is _7_2_29
        that's it
        make_table_array('_7_2_29')

"""

"""
FixMe: In Response for TODO i have been reached that far
Note: I have found query now i have to know sql alchemy mapper and relationship in SqlAlchemy
        So that i can generate code for that Mapper

    Example:
        For table structure details please have a look at mib_oid.sql

        ==========================
        TABLE : odu100_7_2_29_oids

            Get `KEY_COLUMN_USAGE` of table

                ```
                SELECT COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM  `KEY_COLUMN_USAGE`
                INNER JOIN `REFERENTIAL_CONSTRAINTS`
                WHERE  `TABLE_NAME` =  'odu100_7_2_29_oids'
                    AND `TABLE_SCHEMA` = 'nms'
                ```
                +----------------+------------------------------------+-----------------------+------------------------+
                | COLUMN_NAME    | CONSTRAINT_NAME                    | REFERENCED_TABLE_NAME | REFERENCED_COLUMN_NAME |
                +----------------+------------------------------------+-----------------------+------------------------+
                | oid_id         | PRIMARY                            | NULL                  | NULL                   |
                | device_type_id | FK_odu100_7_2_29_oids              | device_type           | device_type_id         |
                | dependent_id   | FK_odu100_7_2_29_oids_dependant_id | odu100_7_2_29_oids    | oid_id                 |
                +----------------+------------------------------------+-----------------------+------------------------+


            Get `REFERENTIAL_CONSTRAINTS` of table for each `CONSTRAINT_NAME`

                ```
                SELECT UNIQUE_CONSTRAINT_NAME, UPDATE_RULE, DELETE_RULE, REFERENCED_TABLE_NAME
                FROM  `REFERENTIAL_CONSTRAINTS`
                WHERE  `CONSTRAINT_NAME` =  'FK_odu100_7_2_29_oids'
                    AND `TABLE_NAME` =  'odu100_7_2_29_oids'
                    AND `CONSTRAINT_SCHEMA` = 'nms'
                ```
                +------------------------+-------------+-------------+-----------------------+
                | UNIQUE_CONSTRAINT_NAME | UPDATE_RULE | DELETE_RULE | REFERENCED_TABLE_NAME |
                +------------------------+-------------+-------------+-----------------------+
                | PRIMARY                | CASCADE     | CASCADE     | device_type           |
                +------------------------+-------------+-------------+-----------------------+


        =======================================
        TABLE : odu100_7_2_29_oids_multivalues

        ## Get PRIMARY_KEY and FORIGN_KEY details of table
            ```
            SELECT kcu.COLUMN_NAME, kcu.CONSTRAINT_NAME, kcu.REFERENCED_TABLE_NAME, kcu.REFERENCED_COLUMN_NAME,
                rc.UNIQUE_CONSTRAINT_NAME, rc.UPDATE_RULE, rc.DELETE_RULE
            FROM  `KEY_COLUMN_USAGE` AS kcu
            LEFT OUTER JOIN JOIN `REFERENTIAL_CONSTRAINTS` AS rc
            ON rc.`CONSTRAINT_NAME` = kcu.`CONSTRAINT_NAME`
            WHERE  kcu.`TABLE_NAME` =  'odu100_7_2_29_oids_multivalues'
                AND kcu.`TABLE_SCHEMA` = 'nms'
            ```
        +--------------------+-----------------------------------+-----------------------+------------------------+------------------------+-------------+-------------+
        | COLUMN_NAME        | CONSTRAINT_NAME                   | REFERENCED_TABLE_NAME | REFERENCED_COLUMN_NAME | UNIQUE_CONSTRAINT_NAME | UPDATE_RULE | DELETE_RULE |
        +--------------------+-----------------------------------+-----------------------+------------------------+------------------------+-------------+-------------+
        | oids_multivalue_id | PRIMARY                           | NULL                  | NULL                   | NULL                   | NULL        | NULL        |
        | oid_id             | FK_odu100_7_2_29_oids_multivalues | odu100_7_2_29_oids    | oid_id                 | PRIMARY                | CASCADE     | CASCADE     |
        +--------------------+-----------------------------------+-----------------------+------------------------+------------------------+-------------+-------------+

        SqlAlchemy mapper should look like this:

        Its only for FK relation
        ```
        mapper(Odu1007_2_25_oids, Odu1007_2_25_oids.__table__, properties = {
            "odu100_7_2_25_oids_multivalues": relationship(Odu1007_2_25_oids_multivalues, backref="odu100_7_2_25_oids", cascade="all,delete,delete-orphan")
            })
        ```

"""

database_name = 'nms'

file_to_write = './alchemy_model.py'

if not os.path.isfile(file_to_write):
    print " file not present at location : %s " % file_to_write
    sys.exit(1)

#--------
# uncomment function you want to use
#--------

# print class_structure('odu100_7_2_29_oids')
# print
# make_table_class_strucuture(['odu100_7_2_29_oids','odu100_7_2_29_oids_multivalues'])
print make_table_array("7_2_29")
