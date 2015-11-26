# coding=utf-8
import commands

remote_path = "/data/nfs/horse3/logs/api-web/"
seq_id = "61545896596056127"
query_date = "20151123"
# 搜索所有的查询记录
# 远程执行awk 命令，$等特殊字符需要转义
# shell = 'ssh usere@bjop.sjbly.cn "grep fighter_search ' + remote_path + 'stdout_fighter.log* | head -n100 | awk \'{print \$11}\'" '

shell = 'ssh usere@bjop.sjbly.cn "zgrep -aE \\"' + seq_id + '(.*?)response=\\" ' + remote_path + "flight_request." + query_date + ".tgz\""

print shell
print 'Running...'
executeRet = (status, ret) = commands.getstatusoutput(shell)
# print "返回结果： " + ret

index = ret.find("response=") + "response=".__len__()
response = ret[index:]
# print(response)

file_name = seq_id + "_zhf_response"
file_dir = "/home/qings2329/ZhfTestData/" + file_name
file_handle = open(file_dir, 'w')
file_handle.write(response)
file_handle.close()

print 'Done ! Save In: ' + file_dir

