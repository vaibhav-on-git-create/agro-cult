import os
#---------------------------------------------------------------------------------------------
def update_env_variable(file_path, key, new_value):
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        key_found = False
        for line in lines:
            if line.strip().startswith(f"{key} ="):
                file.write(f"{key} = {new_value}\n")
                key_found = True
            else:
                file.write(line)
        
        # If the key doesn't exist, add it
        if not key_found:
            file.write(f"{key} = {new_value}\n")

# Example usage
#update_env_variable(".env", "GREETING", '"hello sir, how are you?"')
#----------------------------------------------------------------------------------------------
def list_env_keys(file_path):
    keys = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key = line.split("=", 1)[0].strip()
                keys.append(key)
    return keys

# Example usage
# keys = list_env_keys("../agro-cult/path_storage_info/path_storage.env")
# print("Available keys:", len(keys))
#----------------------------------------------------------------------------------------------
def get_env_value(file_path, key = None):
    if key is not None:
        with open(file_path,'r') as file:
            for line in file:
                if line.startswith(key):
                    return line.split('=')[1].strip()
                
    elif file_path == 'storage':
        try : 
            return '../agro-cult/path_storage_info/path_storage.env'
        except :
            pass
#example usage
# a = get_env_value("../frost_mind/settings/settings.env", "flow_tester")
# print(a)           
#-----------------------------------------------------------------------------------------------