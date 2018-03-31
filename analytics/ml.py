from .models import LoggedDeviceData, LoggedRoomData
from devices.models import Device
from django.shortcuts import get_object_or_404
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier

def transf(string):
    res = []
    for char in string:
        res.append(ord(char))
    return res

def parse_time(timestamp):
    hours_mins = int(datetime.fromtimestamp(timestamp).strftime("%H %M")
    split_hm = hours_mins.split()
    return int(split_hm[0]) + int(split_hm[1])/60

def convert_device_to_lists(req_data):
    device_id = req_data[0].device.device_id
    device_id = transf(device_id)
    cleaned_list = []
    for datum in req_data:
        newlist = device_id
        tstamp = datum.get('timestamp', 0)
        tstamp = parse_time(tstamp)
        value = datum.value
        state = datum.state
        newlist.extend([tstamp, value, state])
        cleaned_list.append(newlist)
    return cleaned_list

def preprocess(dataset):
    let ret_vals = []
    for datum in dataset:
        val = []
        val.extend(transf(datum.get('device', None).device_id))
        val.append(parse_time(datum.get('timestamp', 0)))
        val.append(datum.get('state', 'on'))
        ret_vals.append(val)
    return ret_vals


def generate_device_data(device_id):
    device = get_object_or_404(Device, device_id=device_id)
    req_data_obj = list(LoggedRoomData.objects.filter(device=device))
    req_data = [model_to_dict(obj) for obj in req_data_obj]
    cleaned_data = convert_device_to_lists(req_data)

def do_knn_on_dataset(dataset, device_id):
    train_values = generate_device_data(device_id)
    dataset = preprocess(dataset)
    train_inputs = [datum[:-1] for datum in train_values]
    train_results = [datum[-1] for datum in train_values]
    neigh = KNeighborsClassifier(n_neighbors = 10, algorithm='auto', weights='distance')
    neigh.fit(train_inputs, train_results)
    data_ins = [datum[:-1] for datum in dataset]
    data_outs = [datum[-1] for datum in dataset]
    accuracy = neigh.score(data_ins, data_outs)
    return accuracy

