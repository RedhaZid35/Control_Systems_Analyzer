import numpy as np
import asyncio
class ResponseAnalyser:
    def __init__(self, data, delta = 0.05, error_factor = 1, **kwargs):
        self.data = data
        self.delta = delta
        self.error_factor = error_factor
        self.vf = data[1][-1]
        self.te = self._get_settling_time()
        self.tm, self.vm = self._get_tm_vm()

    def _get_tm_vm(self):
        x1 = 0.1 * self.vf
        x2 = 0.9 * self.vf
        t1 = 0 
        t2 = 0
        vm = 0
        for i in range(0,len(self.data[1])):
            if vm < self.data[1][i]:
                vm = self.data[1][i]
            if x1 - self.data[1][i] < 0 :
                if not t1:
                    if i > 0:
                        t1 = self.data[0][i-1]
                    if i==0:
                        t1 = self.data[0][i]
            if x2 - self.data[1][i] < 0 :
                if not t2:
                    if i > 1:
                        t2 = self.data[0][i-1]
                    if i==1:
                        t2 = self.data[0][i]
        return t2-t1, vm 

    def _get_settling_time(self):
        if self.vf == 0:
            return "Error : Steady state value = 0"        
        for i in self.data[1][::-1]:
            if abs((i/self.vf)-1) > self.delta :
                return self.data[0][self.data[1].index(i)]
    
    def get_result(self):
        test = {
            "Steady State Value":self.vf,
            "Peak":self.vm,
            "Settling Time":self.te,
            "Rise Time":self.tm,
        }
        return test