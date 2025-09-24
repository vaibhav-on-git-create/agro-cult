import sys
sys.path.insert(1,"../agro-cult")
from system_bridge import bridge
bridge.bridge_to_all()

from data_tools import env_tool

path_storage = env_tool.get_env_value("storage")

def get_path(path_name : str):
    parent_path = env_tool.get_env_value(file_path=path_storage , key="parent_path")
    path_name_address = env_tool.get_env_value(file_path=path_storage , key=path_name)

    if path_name == "parent":
        return parent_path

    else:
        final_path = str(parent_path) + "/" +str(path_name_address)
        return final_path

# for i in env_tool.list_env_keys(path_storage):
#     print(get_path(path_name=i))
# print(get_path(path_name="parent"))



    

    