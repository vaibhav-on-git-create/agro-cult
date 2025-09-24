import sys

def bridge_to_all():
    data = open('../agro-cult/system_bridge/bridge_data.txt' , 'r').read().split(',')
    data_lst = []
    for i in data:
        data_lst.append(i.strip())
    for j in data_lst:
        sys.path.insert(1,j)