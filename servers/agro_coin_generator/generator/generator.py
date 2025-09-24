import random
import datetime
import time
import sys 
sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

from path_storage_info import request_path
from data_tools import json_tool
from servers.login import id_generator
from tqdm import tqdm

def generate_serial():
    serial_1 = random.randint(10000000,99999999)
    serial_2 = random.randint(10000000,99999999)

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
        
def alot_serial(crop : str = "WHEAT",user_name : str = ""):

    buyer_id_path = request_path.get_path(path_name="buyer_id_register")
    buyers_list = json_tool.list_json_key(file_path=buyer_id_path)
    buyer_id_data = json_tool.read_json(file_path=buyer_id_path)
 
    if user_name in buyers_list:

        index = buyers_list[buyers_list.index(user_name)]

        date = str(datetime.datetime.now()).replace(":" , "")

        pros_1 = date.replace("-","")
        pros_2 = pros_1.replace(".","")
        pros_3 = pros_2.replace(" ","")

        final_serial = f"{pros_3}-{crop.upper()}-{generate_serial()}-{buyer_id_data[index]}"
        return final_serial


def generate_agro_coin(user_name :str , crop : str = "WHEAT" , coins : int = 1):
    generation_data_set_list = []

    if alot_serial(user_name=user_name , crop=crop) is not None:
        
        for i in tqdm(range(coins) , desc = "Generating Agro-coins"):
                
            generation_histoy_path = request_path.get_path(path_name="agro_coin_generation_history")
            transaction_buyer_path = request_path.get_path(path_name='buyer_transaction_balance')

            date_day = f"{datetime.datetime.now()}||{datetime.datetime.today().strftime('%A')}||{crop.upper()}"

            generation_data_set = {date_day:alot_serial(crop=crop , user_name= user_name)}
            generation_data_set_list.append(generation_data_set)
            time.sleep(0.01)

        json_tool.append_json(file_path=generation_histoy_path , append_dict_list=generation_data_set_list)
        json_tool.append_json(file_path=transaction_buyer_path , append_dict_list=generation_data_set_list)
        
        

# generate_agro_coin(coins=1000 , crop="rice" , user_name="kuldeep_marhaan")


    



    


