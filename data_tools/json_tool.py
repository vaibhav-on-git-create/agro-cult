import sys 
sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

import json
from uitility import printer

file_master = "../agro-cult/data_tools/test.json"
file_master_1 = "../agro-cult/data_tools/test_1.json"

def read_json(file_path:str) -> dict:
    '''
    **Summary** : this fuction returns the whole json data of the json file using path

    _Agrs_ : file_path --> the path to the json file

    '''
    
    with open(file_path , 'r') as file:
        return json.load(file)



def write_json(file_path:str , write_dict: dict):
    '''
    **Summary** : this fuction write the data dictionary to the provided json file

    _Agrs_ : file_path --> the path to the json file
            write_dict --> the dictionary which will be written to the json file
    
    *Caution* : this will refresh the whole file to write the data

    '''

    with open(file_path , "w") as file:
        json.dump(write_dict , file , indent=4)

def append_json(file_path: str , append_dict_list : list):
    """
    **Summary** : this fuction safely adds the data dictionary to the provided json file

     _Agrs_ : file_path --> the path to the json | | 
    
            write_dict --> the dictionary which will be written to the json file
    
    """
    primary_data = read_json(file_path=file_path)
    for append_dict in append_dict_list:
        primary_data.update(append_dict)

    printer.t_print(f"appending : [\n{primary_data}\n] \n to file -- [{file_path}]")
    write_json(file_path=file_path , write_dict=primary_data)

def update_json(file_path:str , key , new_value):
    """
    **Summary** : this fuction safely adds the data dictionary to the provided json file
    
    _Args_ : file_path --> the path to the json file
            'key' --> key to be changed
            'new_value' --> value to be updated
    
    """

    json_data = read_json(file_path=file_path)
    key_list = []

    for i in json_data:
        key_list.append(i)
    
    if key not in key_list:
        printer.t_print(f"the key [{key}] was not found in : [{file_path}]")

        return None
    
    if key in key_list:
        json_data.update({key : new_value})

        write_json(file_path=file_path , write_dict=json_data)
        printer.t_print(f"[{key}] -- key has been updated to -- value [{new_value}] -- in file [{file_path}]")

def list_json_key(file_path : str) -> list:

    """
    **Summary** : this fuction is to list all the keys present in json file
    _Args_ : file_path --> the file you whos keys are to be listed
    """
    
    read_data = read_json(file_path=file_path)
    return [key for key in read_data]

def transfer_to_json(transfer_file : str , destination_file : str , condition = "k-k" ):

    """
    **Summary** : this fuction is to do [json to json] transfer only -- for matching keys only 
                  in both files

     _Agrs_ : transfer_file --> data will be copied from this file 
            destination_file --> data will be updated into this file

            condition --> the type of tranfer you want like

            k-k --> only matching keys will be updated with respect to the destination file keys.

            add --> this will simply add the new sets of key-values to the destination file also the matching 
                keys will automatically be updated.


    """    

    transfer_data = read_json(file_path=transfer_file)
    destination_file_data = read_json(file_path=destination_file)

    trasfer_key = list_json_key(transfer_file)
    destination_key = list_json_key(destination_file)


    if destination_file_data == {}:
        write_json(file_path=destination_file , write_dict=transfer_data)
    
    if condition == "k-k":
    
        for key_1 in trasfer_key:
            if key_1 in destination_key:
                dict_1 = {key_1 : transfer_data[key_1]}
                printer.t_print(f"tranfering data --[{dict_1}]-- from -- [{transfer_file}] to [{destination_file}]")
                update_json(file_path=destination_file , key = key_1 , new_value= transfer_data[key_1])
                
    if condition == "add":
        append_json(file_path= destination_file , append_dict=transfer_data)
        





        





    

        

        
    

    




