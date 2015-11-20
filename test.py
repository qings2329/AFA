# coding=utf-8
import time
import traceback

path = "/home/qings2329/airfareAnalyze/"
# 默认文件操作模式是read，不能写文件
test_file = open(path + "test")
test_file.write("23434")
test_file.close()

print "done, total available flights : %d" % 124, " . Time cost : %.2f" % 1.235
exit()

try:
    1/0
except Exception, e:
    print "###################"
    print traceback.format_exc()
    print "###################"
    print e
    print "###################"

print int(round(5.58357300758))

print time.time()

print "%-50s" %'TK021/TK1827-TK1830/TK020@2016-02-20/2016-02-28', '[19848]'

# about dict
dict = {}
dict["q1"] = 123


# 判断是否存在某个key
print not dict.get("q12")
print dict.has_key("q1")
print "q13" in dict.keys()

if dict["q1"]:
    print(dict["q1"])
else:
    print("null")

# about list
list = []
list.append("qq")

print list