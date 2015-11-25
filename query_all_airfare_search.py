# coding=utf-8
import commands

remote_path = "/data/nfs/horse3/logs/api-web/"

# 搜索所有的查询记录
# 远程执行awk 命令，$等特殊字符需要转义
# shell = 'ssh usere@bjop.sjbly.cn "grep fighter_search ' + remote_path + 'stdout_fighter.log* | head -n100 | awk \'{print \$11}\'" '
shell = 'ssh usere@bjop.sjbly.cn "grep fighter_search ' + remote_path + 'stdout_fighter.log.20151104 | awk \'{split(\$11, ret, \\"|\\"); ' \
                                                                        'print substr(ret[7], 11, 6) , substr(ret[7], 28, 6) , substr(ret[8], index(ret[8], \\",\\") + 1, 2)  }\'| sort | uniq -c | sort -nr" '
print shell
print 'Running...'
executeRet = (status, ret) = commands.getstatusoutput(shell)
# print ret

file_name = "airfare-search-statistics"
file_dir = "/home/qings2329/airfareAnalyze/" + file_name
file_handle = open(file_dir, 'w')
file_handle.write(ret)
file_handle.close()

print 'Done !'
