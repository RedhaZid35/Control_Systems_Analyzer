import numpy as np
import asyncio
class ResponseAnalyser:
    def __init__(self, data, delta = 0.05, error_factor = 1, **kwargs):
        self.data = data
        self.delta = delta
        self.error_factor = error_factor
        # self.stability = self.is_stable()
        self.vf = data[1][-1]
        self.te = self._get_settling_time()
        self.tm, self.vm = self._get_tm_vm()

    # def _find_sums_diff(self):
    #     sums_diff = []
    #     for i in range(len(self.data[1])):
    #         sum_diff = 0
    #         idx = 1
    #         for j in range(len(self.data[1])):
    #             diff = abs(self.data[1][i] - self.data[1][j])
    #             sum_diff += diff
    #             idx += 1
    #         if idx != 0: 
    #             sums_diff.append(self.error_factor * sum_diff/idx)
    #         else: 
    #             sums_diff.append(self.error_factor * sum_diff)
    #     minv = min(sums_diff)
    #     for i in sums_diff:
    #         i -= minv
    #     return sums_diff

    # def _get_diff_between_response_mins_maxs(self,data):
    #     arr = []
    #     arr_of_ep = []
    #     for i in range(2, len(data[1])-1):
    #         if data[1][i] > data[1][i-1] and data[1][i] > data[1][i+1]:
    #             arr.append(data[1][i])
    #         elif data[1][i] < data[1][i-1] and data[1][i] < data[1][i+1]:
    #             arr.append(data[1][i])
    #     for i in range(0, len(arr)-1):
    #         arr_of_ep.append(abs(arr[i]-arr[i+1]))
    #     return arr_of_ep    

    # def _get_diff_mins_maxs(self):
    #     sums_diff = self._find_sums_diff()
    #     max_id_arr = []
    #     min_id_arr = []
    #     for i in range(2, len(sums_diff)-1):
    #         if sums_diff[i] > sums_diff[i-1] and sums_diff[i] > sums_diff[i+1]:
    #             max_id_arr.append(i)
    #         elif sums_diff[i] < sums_diff[i-1] and sums_diff[i] < sums_diff[i+1]:
    #             min_id_arr.append(i)
    #     return min_id_arr, max_id_arr

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


    # def is_stable(self):
    #     arr_of_ep = self._get_diff_between_response_mins_maxs(self.data)
    #     if len(arr_of_ep) != 0:
    #         for i in range(2, len(arr_of_ep)):
    #             if arr_of_ep[i] > arr_of_ep[i-1] and arr_of_ep[i] > self.delta:
    #                 return False
    #     return True

    # def find_vf(self):
    #     if self.stability:
    #         diff_mins, diff_maxs = self._get_diff_mins_maxs()
    #         sum_vfs = 0
    #         if len(diff_mins) !=0 :
    #             for i in range(0, len(diff_mins)):
    #                 sum_vfs += self.data[1][diff_mins[i]]
                
    #             return sum_vfs / len(diff_mins)
    #     return 0 

    # def find_ssv(self, InfValue):
    #     settled = np.where(abs((self.data[1]/InfValue)-1) <= self.delta)[0][0]
    #     print(settled)
    #     if settled < len(self.data[0]):
    #         settling_time = self.data[0][settled]
    #     return settling_time
