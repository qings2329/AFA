# coding=utf-8
import commands

remote_path = "/data/nfs/horse3/logs/api-web/"

# 搜索所有的查询记录
shell = 'ssh usere@bjop.sjbly.cn "grep fighter_search ' + remote_path + 'stdout_fighter.log | head -n1 | awk \'{print \$11}\'" '
print shell
print 'Running...'
executeRet = (status, ret) = commands.getstatusoutput(shell)
file_name = "all-airfare-searchX"
file_dir = "/home/qings2329/airfareAnalyze/" + file_name
file_handle = open(file_dir, 'w')
file_handle.write(ret)
file_handle.close()

print 'Done !'
