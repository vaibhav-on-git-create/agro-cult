import sys
sys.path.insert(1, '../agro-cult') # this is the path to the system bridge module. It is used to send and recive data from all the modules in the system.
from system_bridge import bridge 
bridge.bridge_to_all()
#------------------------------------------------------------------------------------------------------------------------
from data_tools import env_tool as env_modes
#------------------------------------------------------------------------------------------------------------------------
path_storage = env_modes.get_env_value("storage")
#------------------------------------------------------------------------------------------------------------------------
def check_setting(setting):
    if env_modes.get_env_value(env_modes.get_env_value(path_storage , 'setting'), setting).strip() == 'Enabled':
        return True
    else:
        return False

def get_setting_val(setting):
    data =  env_modes.get_env_value(env_modes.get_env_value(path_storage , 'setting'), setting).strip()
    try:
        prime_term = int(data)
    except TypeError:
        prime_term = data
        print(f"Error: {setting} is not a valid integer. Using default value instead.")
    return prime_term
        
        

