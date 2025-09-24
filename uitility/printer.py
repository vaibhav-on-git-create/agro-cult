import sys
sys.path.insert(1, '../agro-cult') # this is the path to the system bridge module. It is used to send and recive data from all the modules in the system.
from system_bridge import bridge 
bridge.bridge_to_all()
#--------------------------------------------------------------------------------------
from data_tools import env_tool as env_modes
import time
#--------------------------------------------------------------------------------------
path_storage = env_modes.get_env_value("storage")
#--------------------------------------------------------------------------------------
def t_print(text):
    if env_modes.get_env_value(env_modes.get_env_value(path_storage , 'settings'), "flow_tester") == 'Enabled':
        time.sleep(0)
        print(f"{'-'*140}\n>> [{text}]\n{'-'*140}")  
#--------------------------------------------------------------------------------------
