import sys
from network_security.logging import logger

# defining a custom exception class
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message = error_message
        # (exc_type, exc_value, exc_traceback)
        # This traceback object gives access to the call stack where the exception was 
        _,_,exc_tb = error_details.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
    def __str__(self):
        return f"Error Occured in [{self.file_name}] at line [{self.lineno}] Error Message: [{self.error_message}]"

