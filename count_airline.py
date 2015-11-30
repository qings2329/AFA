# coding=utf-8
import os


file_direct = "/home/qings2329/airfareAnalyze/airlines/"
airline_dir = {}

for parent, dirnames, filenames in os.walk(file_direct):
    for fn in filenames:
        path = os.path.join(parent, fn)
        file_handle = open(path, 'r')
        lines = file_handle.readlines()
        for ln in lines:
            arr = ln.split(' ')
            length = len(arr)
            key = arr[length - 3] + ' ' + arr[length - 2] + ' ' + arr[length - 1][:2]
            value = airline_dir.get(key)
            if value:
                value += int(arr[length - 4])
            else:
                value = int(arr[length - 4])
            airline_dir[key] = value

file_name = "airline-list"
file_dir = "/home/qings2329/airfareAnalyze/airlines/" + file_name
file_handle = open(file_dir, 'w')

# rank_list = []
for key in airline_dir:
    # rank_list.append(str(airline_dir.get(key)) + " " + key)
    print >> file_handle, str(airline_dir.get(key)) + " " + key

# rank_list.sort()
# print rank_list

file_handle.close()
