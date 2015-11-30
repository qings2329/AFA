# coding=utf-8
import commands
import os

# remote path
remote_path = "/data/nfs/horse3/logs/api-web/"
remote_echo = "ssh usere@bjop.sjbly.cn echo -e "

dep_city1 = "BJS"
arrive_city1 = "SYD"
dep_city2 = "MEL"
arrive_city2 = "BJS"
line_type = "ML"

dep_city1 = "BJS"
arrive_city1 = "HNL"
dep_city2 = "HNL"
arrive_city2 = "BJS"
line_type = "RT"

dep_city1 = "BJS"
arrive_city1 = "AKL"
dep_city2 = "AKL"
arrive_city2 = "BJS"
line_type = "RT"

dep_city1 = "BJS"
arrive_city1 = "PAR"
dep_city2 = "ROM"
arrive_city2 = "BJS"
line_type = "ML"

dep_city1 = "BJS"
arrive_city1 = "ROM"
dep_city2 = "MIL"
arrive_city2 = "BJS"
line_type = "ML"


# 字符串格式化
date_template = "201511"
for i in range(6, 27):
        suffix = ""
        if i < 10:
                suffix = "0" + str(i)
        else:
                suffix = str(i)
        query_date = date_template + suffix
        # shell = 'ssh usere@bjop.sjbly.cn "grep -Ec \\"dep_date=2016-02-05(.*?)3710457111429024\\" ' + path + 'stdout_fighter.log.20151030"'

        # 需要密码 why? 写错域名了 bjop.sjb.ly.cn
        # shell = 'ssh usere@bjop.sjbly.cn "zgrep -aEc \\"\\\\\\"from_city_code\\\\\\"\\" ' + path + "flight_connect.20151030.tgz\""

        # shell = 'ssh usere@bjop.sjbly.cn "zgrep -aEc \\"\\\"fromX_city_code(.*?)BJS\\" ' + path + 'flight_connect.20151030.tgz"'

        # 能执行成功
        # 搜索 bjs - par 的机票查询记录
        # shell = 'ssh usere@bjop.sjbly.cn "zgrep -aE \\"\\\\\\"from_city_code\\\\\\":\\\\\\"BJS\\\\\\",\\\\\\"to_city_code\\\\\\":\\\\\\"PAR\\\\\\",(.*?)\\\\\\"from_city_code\\\\\\":\\\\\\"PAR\\\\\\",\\\\\\"to_city_code\\\\\\":\\\\\\"BJS\\\\\\"\\" ' \
        #         + remote_path + "flight_connect." + query_date + ".tgz\""

        shell = 'ssh usere@bjop.sjbly.cn "zgrep -aE \\"\\\\\\"from_city_code\\\\\\":\\\\\\"' + dep_city1 + '\\\\\\",\\\\\\"to_city_code\\\\\\":\\\\\\"' + arrive_city1 + '\\\\\\",(.*?)\\\\\\"from_city_code\\\\\\":\\\\\\"' + dep_city2 + '\\\\\\",\\\\\\"to_city_code\\\\\\":\\\\\\"' + arrive_city2 + '\\\\\\"\\" ' \
                + remote_path + "flight_connect." + query_date + ".tgz\""


        shell = 'ssh usere@bjop.sjbly.cn "grep \'fighter_search http\' ' + remote_path + 'stdout_fighter.log.' + query_date + ' |' \
                                                                        'awk -v target=6 \'{split(\$11, ret, \\"|\\"); if(length(ret) == 8) target = 7; print substr(ret[target], 11, 6) , substr(ret[target], 28, 6) , substr(ret[target + 1], index(ret[target + 1], \\",\\") + 1, 2) }\' | sort | uniq -c | sort -nr" '

        print '\n Running...'
        print shell
        # continue
        exit()
        executeRet = (status, ret) = commands.getstatusoutput(shell)
        # print executeRet

        # save file
        # file_name = query_date + "-airline"
        # file_dir = "/home/qings2329/airfareAnalyze/airlines/" + file_name

        file_name = query_date + "-search"
        file_dir = "/home/qings2329/airfareAnalyze/search/" + dep_city1 + arrive_city1 + dep_city2 + arrive_city2 + line_type
        if not os.path.isdir(file_dir):
                os.mkdir(file_dir)


        file_handle = open(file_dir + "/" +file_name, 'w')
        file_handle.write(ret)
        file_handle.close()

print 'Done !'
