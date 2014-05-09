#!/usr/bin/python2.6

'''
@author: Yogesh Kumar
@since: 4-Oct-2011
@date: 4-Oct-2011
@version: 0.1
@note: In this File There are many classes i.e. CommandType: [which gives you the type of commands to execute sql query], MySQLConnectionState: [to check the connection state], MySQLConnection:[to create open close and perform other operations],MySQLHelper:[gives you function to execute the queries(insert,update,delete,select)]
@organization: Codescape Consultants Pvt. Ltd.
@copyright: 2011 Yogesh Kumar for Codescape Consultants Pvt. Ltd.
@see: http://www.codescape.in
'''

import MySQLdb


class CommandType(object):
    '''
    @requires: Nothing
    @param object: object class to inherit
    @var stored_procedure: A Query type
    @var text: A Query type
    @precondition: no pre-conditions
    @note: This Class use to define sql Query Type
    '''
    stored_procedure = "stored_procedure"
    text = "text"


class MySQLConnectionState(object):
    '''
    @requires: none
    @var open: Database status for open connection
    @var text: Database status for close connection
    @precondition: no pre-conditions
    @note: This Class use to define Database connection states i.e. Open and Close.
    '''
    open = 1
    close = 0


class MySQLConnection(object):
    '''
    @requires: mysql credentials in form of tuple (host-name,user-name,password,database-name)
    @var mysql_credentials: mysql credentials in form of tuple (host-name,user-name,password,database-name)
    @precondition: MySQLdb module
    '''

    mysql_credentials = ()      # declare as a empty tuple

    def __init__(self, mysql_credentials):
        self.mysql_credentials = mysql_credentials      # receive tuple as a parameter then assign with instance variable
        self.set_connection(mysql_credentials)
        # connect with database using set_connction method

    def get_connection(self):
        '''
        @requires: Nothing
        @return: connection Object
        @rtype: MySQLdb Object
        @precondition: MySQLdb module
        @note: get the connection object
        '''
        return self._connection                         # get connection object [getter method]

    def set_connection(self, mysql_credentials):         # set connection object [setter method]
        '''
        @requires: mysql credentials in form of tuple (host-name,user-name,password,database-name)
        @return: Nothing
        @rtype: Nothing
        @precondition: MySQLdb module
        @note: set the connection object
        '''
        self._connection = MySQLdb.connect(
            *mysql_credentials)      # calling of MySQLdb.connect method to connect with database

    connection = property(get_connection, set_connection)
    # define connection property

    def close_connection(self):                         # call this method to close database connection
        '''
        @requires: Nothing
        @return: Nothing
        @rtype: Nothing
        @precondition: MySQLdb module
        @note:call this method to close database connection
        '''
        self.connection.close(
        )                         # calling of MySQLdb's close() method

    def connection_state(self):                         # call this method to check status of database
        '''
        @requires: Nothing
        @return: connection state
        @rtype: 0/1    [1 for open state and 0 for close state]
        @precondition: MySQLdb module
        @note: call this method to check status of database
        '''
        return self.connection.open                     # calling of MySQLdb open variable

    def reopen_connection(self):                        # call this method to reopen the connection
        '''
        @requires: Nothing
        @return: connection state
        @rtype: 0/1    [1 for open state and 0 for close state]
        @precondition: MySQLdb module
        @note: call this method to reopen the connection
        '''
        self.set_connection(self.mysql_credentials)
        # calling of set_connection to recreate object

    def connection_cursor(self):                        # call this method to get database cursor
        '''
        @requires: Nothing
        @return: MySQldb cursor object
        @rtype: cursor Object
        @precondition: MySQLdb module
        @note: call this method to get database cursor
        '''
        return self.connection.cursor()                 # calling of MySQldb's cursor method to create cursor object

    def db_commit(self):                                # call this method to commit the database changes
        '''
        @requires: Nothing
        @return: Nothing
        @rtype: Nothing
        @precondition: MySQLdb module
        @node: call this method to commit the database changes
        '''
        self.connection.commit(
        )                        # calling of MySQLdb's commit method

    def db_rollback(self):                              # call this method to rollback the database changes
        '''
        @requires: Nothing
        @return: Nothing
        @rtype: Nothing
        @precondition: MySQLdb module
        @node: call this method to rollback the database changes
        '''
        self.connection.rollback(
        )                      # calling of MySQLdb's rollback method


class MySQLHelper(object):
    '''
    @requires: Nothing
    @return: Nothing
    @precondition: MySQLdb module
    '''
    inserted_row_id = None                  # this variable stores newly inserted row's auto generated id
    effected_row = 0                        # this variable stores total effected row after query execution

    def __init__(self):
        __version__ = 0.1
        __info__ = "fetch your data from database"
        __author__ = "Yogesh Kumar"

    def execute_non_query(self, mysql_credentials, command_type, command_text, sql_parameter=None):
        '''
        @requires: mysql_credentials,command_type,command_text,sql_parameter [Default Value is None]
        @var mysql_credentials: this is a tuple of mysql credentials
        @var command_type: this defines the type of command
        @var command_text: this defines the command text or sql query
        @var sql_parameter: this is define to create dynamic query
        @return: True/Flase
        @rtype: Boolean
        @precondition: MySQLdb module
        @node: call this method to execute non queries like insert delete update etc.
        '''
        mysql_connection = MySQLConnection(
            mysql_credentials)           # create mysql database connection
        cursor, self.effected_row = self.execute_command(
            mysql_connection, command_type, command_text, sql_parameter, True)  # execute mysql command
        self.inserted_row = cursor.lastrowid                            # get the last row id which is inserted
        if self.effected_row > 0:                                       # compare number of effected row with your query.
            return True
        else:
            return False

    def execute_all_query(self, mysql_credentials, command_type, command_text, sql_parameter=None):
        '''
        @requires: mysql_credentials,command_type,command_text,sql_parameter [Default Value is None]
        @var mysql_credentials: this is a tuple of mysql credentials
        @var command_type: this defines the type of command
        @var command_text: this defines the command text or sql query
        @var sql_parameter: this is define to create dynamic query
        @return: Query Result
        @rtype: 2D - tuple
        @precondition: MySQLdb module
        @node: call this method to execute all queries like select query [fetch multiple records].
        '''
        mysql_connection = MySQLConnection(
            mysql_credentials)           # create mysql database connection
        cursor, self.effected_row = self.execute_command(
            mysql_connection, command_type, command_text, sql_parameter)   # execute mysql command
        return cursor.fetchall()                                        # fetch all the data from cursor

    def execute_many_query(self, mysql_credentials, command_type, rows, command_text, sql_parameter=None):
        '''
        @requires: mysql_credentials,command_type,command_text,sql_parameter [Default Value is None]
        @var mysql_credentials: this is a tuple of mysql credentials
        @var command_type: this defines the type of command
        @var rows: number of rows that you want in your mysql query result
        @var command_text: this defines the command text or sql query
        @var sql_parameter: this is define to create dynamic query
        @return: Query Result
        @rtype: 2D - tuple
        @precondition: MySQLdb module
        @node: call this method to execute all queries like select query [fetch specific records].
        '''
        mysql_connection = MySQLConnection(
            mysql_credentials)           # create mysql database connection
        cursor, self.effected_row = self.execute_command(
            mysql_connection, command_type, command_text, sql_parameter)   # execute mysql command
        return cursor.fetchmany(rows)                                   # fetch specific records

    def execute_single_query(self, mysql_credentials, command_type, command_text, sql_parameter=None):
        '''
        @requires: mysql_credentials,command_type,command_text,sql_parameter [Default Value is None]
        @var mysql_credentials: this is a tuple of mysql credentials
        @var command_type: this defines the type of command
        @var command_text: this defines the command text or sql query
        @var sql_parameter: this is define to create dynamic query
        @return: Query Result
        @rtype: tuple
        @precondition: MySQLdb module
        @node: call this method to execute all queries like select query [fetch single record].
        '''
        mysql_connection = MySQLConnection(
            mysql_credentials)           # create mysql database connection
        cursor, self.effected_row = self.execute_command(
            mysql_connection, command_type, command_text, sql_parameter)   # execute mysql command
        return cursor.fetchone()                                        # fetch single record

    def execute_command(self, mysql_connection, command_type, command_text, sql_parameter, do_commit=False):
        '''
        @requires: mysql_connection,command_type,command_text,sql_parameter [Default Value is None]
        @var mysql_connection: this is a object of MySQLConnection class
        @var command_type: this defines the type of command
        @var command_text: this defines the command text or sql query
        @var sql_parameter: this is define to create dynamic query
        @return: cursor and number of effected row
        @rtype: cursor object and int
        @precondition: MySQLdb module
        @node: call this method to execute query
        '''
        effected_row = 0                                                        # default value of effected row [value is 0]
        if mysql_connection.connection_state() != MySQLConnectionState.open:    # check the connection is open or closed
            mysql_connection.reopen_connection(
            )                                # if connection is closed the reopen it

        cursor = mysql_connection.connection_cursor(
        )                           # create cursor object

        if command_type == CommandType.text:                                    # check the command type is text or not
            if sql_parameter != None and len(sql_parameter) > 0:                # check the parameter
                command_text = command_text % sql_parameter                     # prepare command for execution
            effected_row = cursor.execute(command_text)
            # execute command then get the number
            # of rows effected
        elif command_text == CommandType.stored_procedure:                      # check the command type is stored procedure or not
            effected_row = cursor.callproc(
                command_text, sql_parameter)          # execute stored procedure the get number of row  effected
        if do_commit == True:                                                   # check do_commit is True or False
            mysql_connection.db_commit(
            )                                        # if do_commit is True the Commit the database

        mysql_connection.close_connection(
        )                                     # close the mysql connection
        return cursor, effected_row                                              # return cursor object and effected row


# ============
# How to Use
# ============
# command_text = "Update staudent_details SET student_name = '%(name)s' WHERE roll_number = %(roll_no)s"
# sql_parameter = {'name':"Yogesh","result":"pass","roll_no":8}

# command_text = "SELECT * FROM staudent_details"

# mysql = ("localhost","root","root","student")
# myhelper = MySQLHelper()
# print myhelper.execute_many_query(mysql, CommandType.text, 3, command_text)
# print myhelper.effected_row

# import datetime

# mysql = ("localhost","root","root","nms")
# myhelper = MySQLHelper()
# command_text = "ap_interface_graph"
# sql_parameter = ("now()","now() - INTERVAL 20 MINUTE",1,'eth0','172.22.0.101')
# refresh_time  = 1
# now = datetime.datetime.now()
# now2 = now + datetime.timedelta(minutes = - 60*int(refresh_time))

# sql_parameter = (now.strftime('%Y-%m-%d
# %H:%M:%S'),now2.strftime('%Y-%m-%d %H:%M:%S'),
# refresh_time,"eth0","172.22.0.101")

# print command_text
# print sql_parameter

# print myhelper.execute_all_query(mysql,CommandType.stored_procedure,command_text,sql_parameter)
# print myhelper.effected_row
