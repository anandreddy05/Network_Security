import sys
from network_security.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        # (exc_type, exc_value, exc_traceback)
        _, _, exc_tb = error_details.exc_info()
        
        # Handle case where exc_tb is None
        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            # Fallback when no active exception context
            import inspect
            frame = inspect.currentframe().f_back
            self.lineno = frame.f_lineno
            self.file_name = frame.f_code.co_filename
    
    def __str__(self):
        return f"Error Occured in [{self.file_name}] at line [{self.lineno}] Error Message: [{self.error_message}]"