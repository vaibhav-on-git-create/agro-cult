import random
import datetime
import sys 
sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

from path_storage_info import request_path
from data_tools import json_tool

def generate_serial():
    serial_1 = random.randint(100000000,999999999)
    serial_2 = random.randint(100000000,999999999)

    register = request_path.get_path("registered_serial")
    register_list = open(register).read().strip().split(",")

    if serial_1 != serial_2:

        if str(serial_1) not in register_list:
            open(register,"a").write(f"{str(serial_1)},")
            return serial_1
        
        else:
            if str(serial_2) not in register_list:
                open(register,"a").write(f"{str(serial_2)},")
                return serial_2

    else:

        if str(serial_1) not in register_list:
           open(register,"a").write(f"{str(serial_1)},")
           return serial_1

def generate_id(name : str , role : str , scale : str ,  country : str = 'India' ,state : str = "uttar pradesh"):
    index_list = []
    char_list = []

    id_char_list = []

    for i in enumerate(name):
        index , char = i

        index_list.append(index)
        char_list.append(char)
    
    reverse_index_list = index_list[::-1]

    for j in range(len(index_list)):

        id_char_list.append(reverse_index_list[j])
        id_char_list.append(char_list[j])

    name_id = f'''{role}-{scale}-{"".join([str(chars) for chars in id_char_list])}-{generate_serial()}-{country}-{state}'''


    return name_id
    
# print(generate_id(name="ashish_chanalani" , role="frm" , scale="sml"))

def make_id(user_name : str , phone_number :str ,role: str = 'frm' , scale: str = 'lrg' , 
            country : str = 'India' ,state : str = "uttar pradesh" ,):
    farmer_id_path = request_path.get_path(path_name="farmer_id_register")
    farmer_details_path = request_path.get_path(path_name="farmer_details")

    buyer_details_path = request_path.get_path(path_name="buyer_details")
    buyer_id_path = request_path.get_path(path_name="buyer_id_register")

    codec = {'frm':"farmer" , 'byer':"buyer" , 'lrg':'large' , 'sml':"small"}
    farmer_keys = ["name","id" ,"role" ,"scale" ,"country","state","phone_number"]

    #checking for pre-existence
    if role == "byer":
        file_path = buyer_id_path
    if role == "frm" :
        file_path = farmer_id_path

    famer_user_list = json_tool.list_json_key(file_path=farmer_id_path)
    buyer_and_farmer_user_list = json_tool.list_json_key(file_path=buyer_id_path)

    all_user_list = famer_user_list + buyer_and_farmer_user_list

    users_list = all_user_list
    
    if user_name in users_list:
        print(f"the name : [{user_name}] -- alredy exists")
        pass
    elif user_name not in users_list:

        if role == "frm":
            if scale == "lrg":
                
                generated_id = generate_id(name=user_name, role=role, scale=scale , country=country , state=state)

                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[0] , new_value=user_name)
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[1] , new_value=generated_id)
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[2] , new_value=codec[role])
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[3] , new_value=codec[scale])
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[4] , new_value=country)
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[5] , new_value=state)
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[6] , new_value=phone_number)

                json_tool.append_json(file_path=farmer_id_path , append_dict_list=[{user_name:generated_id}])

                return generated_id

            if scale == "sml":

                generated_id = generate_id(name=user_name, role=role, scale=scale , country=country , state=state)

                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[0] , new_value=user_name)
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[1] , new_value=generated_id)
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[2] , new_value=codec[role])
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[3] , new_value=codec[scale])
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[4] , new_value=country)
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[5] , new_value=state)
                json_tool.update_json(file_path=farmer_details_path , key=farmer_keys[6] , new_value=phone_number)

                json_tool.append_json(file_path=farmer_id_path , append_dict_list=[{user_name:generated_id}])

                return generated_id

        if role == "byer":
            if scale == "lrg":
                
                generated_id = generate_id(name=user_name, role=role, scale=scale , country=country , state=state)

                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[0] , new_value=user_name)
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[1] , new_value=generated_id)
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[2] , new_value=codec[role])
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[3] , new_value=codec[scale])
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[4] , new_value=country)
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[5] , new_value=state)
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[6] , new_value=phone_number)

                json_tool.append_json(file_path=buyer_id_path , append_dict_list=[{user_name:generated_id}])

                return generated_id

            if scale == "sml":

                generated_id = generate_id(name=user_name, role=role, scale=scale , country=country , state=state)

                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[0] , new_value=user_name)
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[1] , new_value=generated_id)
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[2] , new_value=codec[role])
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[3] , new_value=codec[scale])
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[4] , new_value=country)
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[5] , new_value=state)
                json_tool.update_json(file_path=buyer_details_path , key=farmer_keys[6] , new_value=phone_number)

                json_tool.append_json(file_path=buyer_id_path , append_dict_list=[{user_name:generated_id}])

                return generated_id


    
    

# make_id(user_name="kuldeep_marhaan" , role="byer")

        

        

            

            
            


            



    