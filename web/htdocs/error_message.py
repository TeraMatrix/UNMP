execfile('/omd/daemon/all_unmp_error_message.rs')


class ErrorMessageClass(object):
    def __init__(self, msg='No Message is defined for this error code.'):
        self.default_msg = msg
        self.default_code_msg = msg

    def get_error_msg(self, code=None):
        try:
        #            # This is check the value pass or not in function.
        #            if msg_type==None:
        #                return 'Please pass the message type in function.'
            if code is None:
                return 'Please pass the code in function.'

            # This is return the message for error.
            if all_error_message[code]['user_msg'] == '':
                if all_error_message[code]['sys_msg'] == '':
                    return default_msg
                else:
                    return all_error_message[code]['sys_msg']
            else:
                return all_error_message[code]['user_msg']

            #            # This is return parsing message.
            #            if int(msg_type)==2:
            #                return all_error_message[code]
        except KeyError:
            return self.default_msg
        except Exception, e:
            return self.default_msg + str(e)


# sprint ErrorMessageClass().get_error_msg(104)
