# coding:utf-8
# @Time         : 2019/5/23
# @Author       : xuyouze
# @File Name    : monitor.py

import pynvml
import time

__all__ = ["Monitor"]
class Monitor():
    def __init__(self):
        pynvml.nvmlInit()  # 这里的0是GPU
        self.deviceCount = pynvml.nvmlDeviceGetCount()
        self.wait_time = 0

    def detecting(self):
        gpu_available = False
        gpu_list = None
        while gpu_available is False:
            if self.wait_time > 30000:
                break
            available_count_list = []
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            for i in range(self.deviceCount):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
                print("device:{}:{},current memory:{}m/{}m".format(i, str(pynvml.nvmlDeviceGetName(handle)),
                                                                   int(meminfo.used / 1000000),
                                                                   int(meminfo.total / 1000000)))
                # if meminfo.used / meminfo.total < 0.3:
                if meminfo.used / meminfo.total < 0.1 and len(available_count_list) < 2:
                    available_count_list.append(i)
            if len(available_count_list) > 0:
                gpu_available = True
                gpu_list = available_count_list
            time.sleep(30)
            self.wait_time += 30
        return gpu_list

    def shut_down(self):
        pynvml.nvmlShutdown()

