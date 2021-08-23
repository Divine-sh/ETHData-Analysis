import time

t = time.time() - 60*60*24*30
time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
print(time_string)
