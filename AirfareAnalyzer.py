# coding=utf-8

import json
import time
import os
import commands
# local path
path = "/home/qings2329/airfareAnalyze/"
# remote path
# path = "/data/nfs/horse3/logs/api-web/"


# read test data
# f = open(path + "bjs-par-ML", "r")
# jsonstr = f.read().decode("utf-8")
# print jsonstr


# invoke grep, get jsonstr
# 远程脚本
# 执行失败，字符转义的问题，如何解决？
# shell = 'ssh usere@bjop.sjbly.cn "zgrep -aE \\"\"from_city_code\":\"BJS\",\"to_city_code\":\"PAR\",(.*?)\"from_city_code\":\"PAR\",\"to_city_code\":\"BJS\"\" ' + path + "flight_connect.20151030.tgz\""
# shell = 'ssh usere@bjop.sjbly.cn "zgrep -aE \\"\\"from_city_code\\":\\"BJS\\",\\"to_city_code\\":\\"PAR\\",(.*?)\\"from_city_code\\":"PAR\\",\\"to_city_code\\":\\"BJS\\"\\" ' + path + "flight_connect.20151030.tgz\""

#
# 可运行成功的远程脚本原文
#        ssh usere@bjop.sjbly.cn "grep -Ec \"dep_date=2016-02-05(.*?)3710457111429024\" /data/nfs/horse3/logs/api-web/stdout_fighter.log.20151030"
# shell = 'ssh usere@bjop.sjbly.cn "grep -Ec \\"dep_date=2016-02-05(.*?)3710457111429024\\" ' + path + 'stdout_fighter.log.20151030"'


# shell = 'zgrep -aE \""from_city_code":"BJS","to_city_code":"PAR",(.*?)"from_city_code":"PAR","to_city_code":"BJS"\" ' + path + "flight_connect.20151030.tgz"


# print shell
# (status, ret) = commands.getstatusoutput(shell)

# 这种做法一开始的返回值ret是查询结果，后来就变成状态码，什么原因
# ret = os.system(shell)
all_result = {}
flight_no_query_date_chart = {}
query_date_list = ["20151027", "20151028", "20151029", "20151030", "20151031", "20151101", "20151102", "20151103", "20151104", "20151105", "20151106", "20151107", "20151108", "20151109", "20151110", "20151111", "20151112", "20151113", "20151114", "20151115", "20151116", "20151117"]
# query_date_list = ["20151118"]
# query_date_list = ["20151116"]
qdl_index = 0
total_available_flights = 0
# query_date = "2015-10-30"
start_time_stamp = time.time()
for query_date in query_date_list:
    print 'Analyzing...'
    ret = open(path + query_date + "-all-bjs-par-ML", "r").read()
    # ret = ""
    # print ret

    lines = ret.split("\n")
    for ln in lines:
            separator = ln.find("@@")
            if separator > -1:
                separator += 2
            else:
                continue
            space_index = ln.find(" {\"extra\":")
            seqId = ln[:space_index]
            query_param = json.loads(ln[space_index + 1:separator - 2])
            uuid = query_param.get("uuid")
            # if uuid != "3849963113316037":
            # if uuid != "3849230225793704":
            #     continue

            p_type = query_param.get("plane_type")
            if p_type == "RT":
                journey_type = 0
            elif p_type == "OW":
                journey_type = 1
            elif p_type == "ML":
                journey_type = 2

            avs = json.loads(ln[separator:])
            fareList = avs["fareList"]
            # print fareList[0]["route"].items()
            total_available_flights += avs["count"]
            for item in fareList:
                fare = {"seqId": seqId}
                if journey_type == 0 or journey_type == 1:
                    go_trip = item.get("go")
                    return_trip = item.get("return")
                else:
                    go_trip = item.get("ml").get("1")
                    return_trip = item.get("ml").get("2")

                dep_date = time.localtime(go_trip["start_time"])
                fare["dep_date"] = time.strftime("%Y-%m-%d", dep_date)
                if return_trip:
                    return_date = time.localtime(return_trip["start_time"])
                    fare["ret_date"] = time.strftime("%Y-%m-%d", return_date)
                else:
                    fare["ret_date"] = ""

                fare["amount_adt"] = item["amount_adt"]
                fare["tax_adt"] = item["tax_adt"]
                fare["total_adt"] = item["amount_adt"] + item["tax_adt"]

                fare["amount_chd"] = item["amount_chd"]
                fare["tax_chd"] = item["tax_chd"]
                fare["total_chd"] = item["amount_chd"] + item["tax_chd"]

                if any(item["ml"]):
                    fare["flight_no"] = item["ml"]["1"]["no_link"] + "-" + item["ml"]["2"]["no_link"]
                else:
                    fare["flight_no"] = item["go"]["no_link"]

                if any(item["return"]):
                    fare["flight_no"] = fare["flight_no"] + "-" + item["return"]["no_link"]

                # 如果航班号对应的信息为空，则添加
                query_date_dict = all_result.get(fare["flight_no"])
                if not query_date_dict:
                    query_date_dict = {}
                    all_result[fare["flight_no"]] = query_date_dict

                dep_date_list = query_date_dict.get(query_date)
                if not dep_date_list:
                    dep_date_list = []
                    query_date_dict[query_date] = dep_date_list

                # dep_date_dict[fare["dep_date"]] = fare["total_adt"]
                dep_date_list.append(fare["dep_date"] + "/" + fare["ret_date"] + ":" + str(fare["total_adt"]) + ":" + seqId + "-" + uuid)
                # print fare

                flight_no_and_date = fare["flight_no"] + "@" + fare["dep_date"] + "/" + fare["ret_date"]
                price_list = flight_no_query_date_chart.get(flight_no_and_date)
                if not price_list:
                    price_list = [0] * len(query_date_list)
                    flight_no_query_date_chart[flight_no_and_date] = price_list
                price_list[qdl_index] = fare["total_adt"]

    qdl_index += 1



# 按出发日期排序，看价格变化
# for flight_no in all_result:
#     f_dict = all_result.get(flight_no)
#     for qd in f_dict:
#         f_dict.get(qd).sort()

# analyseResult = json.dumps(all_result, indent=1)
# print analyseResult


# 可以定义成一个函数

# save file
file_name = "-AnalyseResutl"
file_dir = path + file_name
# file_handle = open(file_dir, 'w')
# file_handle.write(analyseResult)
# file_handle.close()

chart_file = open(path + "chart_file_" + str(time.time()), "w+")

print >> chart_file, "%-60s" % " ",
for d in query_date_list:
    print >> chart_file, "%-10s" % d,
print >> chart_file, "\n"
# print query_date_list

fnd_list = flight_no_query_date_chart.keys()
fnd_list.sort()
for fnd in fnd_list:
    print >> chart_file, "%-60s" % fnd,
    for price in flight_no_query_date_chart.get(fnd):
        print >> chart_file, "%-10s" % price,
    print >> chart_file
chart_file.close()
print "\n done, total available flights: " + str(total_available_flights) \
      + ". Time cost :" + str(round(time.time() - start_time_stamp))

