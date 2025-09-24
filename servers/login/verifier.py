import sys 
sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

from path_storage_info import request_path
from servers.login import id_generator
from data_tools import json_tool

def register_login(user_name :str , passcode : str , role :str , scale : str , country :str ,
                    state : str,phone_number : str, bank_account :str , bank_passcode : str , bank_name : str):
    
    
    role_1 = 0
    if role.lower() == "famer":
        role_1 = "frm"
    elif role.lower() == "buyer":
        role_1 = "byer"

    if scale.lower() == "small":
        scale_1 = "sml"
    elif scale.lower() == "large":
        scale_1 = "lrg"
    
    user_id = id_generator.make_id(user_name=user_name , role=role_1 , scale=scale_1 , state=state ,
                                    country=country , phone_number=phone_number)

    buyer_codex_path = request_path.get_path("buyer_codex")
    farmer_codex_path= request_path.get_path("farmer_codex")

    buyer_details_path = request_path.get_path(path_name='buyer_details')
    farmer_details_path = request_path.get_path(path_name="farmer_details")

    buyer_bank_details = request_path.get_path(path_name="buyer_transaction_bank")

    if role_1 == "byer":
        print("registering buyer")
        json_tool.append_json(file_path=buyer_codex_path , append_dict_list=[{user_id : passcode}])

        json_tool.update_json(buyer_bank_details , key="bank_name" , new_value=bank_name)
        json_tool.update_json(buyer_bank_details , key="ac_no" , new_value=bank_account)
        json_tool.update_json(buyer_bank_details , key="passcode" , new_value=bank_passcode)

    if role_1 == "frm":
        print("registering farmer")
        json_tool.append_json(file_path=farmer_codex_path , append_dict_list=[{user_id : passcode}])

# register_login(user_name="vaibhavaa" , passcode="vaibhav123" , role="buyer" , scale="large" , country="India" , state="uttar pradesh" ,
#                 bank_account="1234567890" , bank_passcode="bank123" , bank_name="Sate Bank of India" , phone_number="1234567890")





    
    





