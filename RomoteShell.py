# coding=utf-8
import commands

# remote path
date_template = "2015111"
for i in range(8, 9):
        query_date = date_template + str(i)
        path = "/data/nfs/horse3/logs/api-web/"
        remoteEcho = "ssh usere@bjop.sjbly.cn echo -e "
        # shell = 'ssh usere@bjop.sjbly.cn "grep -Ec \\"dep_date=2016-02-05(.*?)3710457111429024\\" ' + path + 'stdout_fighter.log.20151030"'

        # 需要密码 why? 写错域名了 bjop.sjb.ly.cn
        # shell = 'ssh usere@bjop.sjbly.cn "zgrep -aEc \\"\\\\\\"from_city_code\\\\\\"\\" ' + path + "flight_connect.20151030.tgz\""

        # shell = 'ssh usere@bjop.sjbly.cn "zgrep -aEc \\"\\\"fromX_city_code(.*?)BJS\\" ' + path + 'flight_connect.20151030.tgz"'

        # 成功
        shell = 'ssh usere@bjop.sjbly.cn "zgrep -aE \\"\\\\\\"from_city_code\\\\\\":\\\\\\"BJS\\\\\\",\\\\\\"to_city_code\\\\\\":\\\\\\"PAR\\\\\\",(.*?)\\\\\\"from_city_code\\\\\\":\\\\\\"PAR\\\\\\",\\\\\\"to_city_code\\\\\\":\\\\\\"BJS\\\\\\"\\" ' \
                + path + "flight_connect." + query_date + ".tgz\""

        print shell
        print 'Running...'
        executeRet = (status, ret) = commands.getstatusoutput(shell)
        # print executeRet

        # save file
        file_name = query_date + "-all-bjs-par-ML"
        file_dir = "/home/qings2329/airfareAnalyze/" + file_name
        file_handle = open(file_dir, 'w')
        file_handle.write(ret)
        file_handle.close()

print 'Done !'
