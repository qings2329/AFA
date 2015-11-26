# coding=utf-8
import commands

remote_path = "/data/nfs/horse3/logs/api-web/"

# 搜索所有的查询记录
# 远程执行awk 命令，$等特殊字符需要转义
# shell = 'ssh usere@bjop.sjbly.cn "grep \'fighter_search http\' ' + remote_path + 'stdout_fighter.log* | head -n100 | awk \'{print \$11}\'" '
shell = 'ssh usere@bjop.sjbly.cn "grep \'fighter_search http\' ' + remote_path + 'stdout_fighter.log |' \
                                                                        'awk -v target=6 \'{split(\$11, ret, \\"|\\"); if(length(ret) > 7) target = 7; print substr(ret[target], 11, 6) , substr(ret[target], 28, 6) , substr(ret[target + 1], index(ret[target + 1], \\",\\") + 1, 2) }\' | sort | uniq -c | sort -nr" '
                                                                        # 'awk \'{split(\$11, ret, \\"|\\"); print substr(ret[7], 11, 6) , substr(ret[7], 28, 6) , substr(ret[8], index(ret[8], \\",\\") + 1, 2)  }\'| sort | uniq -c | sort -nr" '

print shell
print '\n Running...'
# exit()
executeRet = (status, ret) = commands.getstatusoutput(shell)
# print ret

file_name = "airfare-search-statisticsX"
file_dir = "/home/qings2329/airfareAnalyze/" + file_name
file_handle = open(file_dir, 'w')
file_handle.write(ret)
file_handle.close()

print '\n Done !'
