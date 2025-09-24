import sys
sys.path.insert(1, '../agro-cult') # this is the path to the system bridge module. It is used to send and recive data from all the modules in the system.
from system_bridge import bridge 
bridge.bridge_to_all()
#---------------------------------------------------------------------------------------------
import os
from data_tools import env_tool as env_modes
from uitility import printer
#---------------------------------------------------------------------------------------------
path_storage = env_modes.get_env_value('storage')

#---------------------------------------------------------------------------------------------
def change_setting(setting , new_val):
    
    printer.t_print(f"acessing : [{env_modes.get_env_value(path_storage, 'setting')}]")
    printer.t_print(f"updating : [{setting}] to [{new_val}]")
    printer.t_print(f"current value : [{env_modes.get_env_value(env_modes.get_env_value(path_storage, 'setting'),setting)}]")
    printer.t_print('updating setting...')
    env_modes.update_env_variable(env_modes.get_env_value(path_storage, 'setting'), setting, new_val)
    print('Setting updated successfully!')
#---------------------------------------------------------------------------------------------

