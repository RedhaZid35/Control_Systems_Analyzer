import asyncio
import matplotlib.pyplot as plt
import numpy as np

from control import (TransferFunction, bode, feedback, impulse_response, nichols,nyquist_plot,step_response, rootlocus_pid_designer)
from .pid import my_pid_designer
from .RampRes import ramp_response
from .ResponseAnalyzer import ResponseAnalyser



class MyAPI:
    def __init__(self, num, den, num2 = 0, den2 = 1, *args, **kwargs):
        self.num = num
        self.den = den
        self.num2 = num2
        self.den2 = den2
        self.TF = feedback(TransferFunction(self.num,self.den),sys2 = TransferFunction(self.num2, self.den2))
        # self.poles = self.TF.poles()
        # print(self.poles)
        # self.zeros = self.TF.zeros()

    def is_stable_by_poles_method(self):
        real_parts = np.real(self.TF.poles())  # Get the real parts of the poles.
        # Check if all the real parts of the poles are negative.
        print(real_parts)
        if np.all(real_parts <= 0):
            return True
        else:
            return False
    
    
    def _get_step_response(self,U_val, start_time = 0, end_time = 0):
        if end_time:
            if type(end_time) == float and end_time >= 1:
                tu = np.linspace(start_time, end_time, int(300*end_time))
            elif type(end_time) == float and end_time < 1:
                tu = np.linspace(start_time, end_time, 300)
            t,y = step_response(self.TF, E = U_val, T= tu)
        else:
            t,y = step_response(self.TF, E = U_val)
        test = self._get_step_info(t, y)
        return t, y, test
    
    def _get_puls_response(self, start_time = 0, end_time = 10):
        if end_time:
            if type(end_time) == float and end_time >= 1:
                tu = np.linspace(start_time, end_time, int(300*end_time))
            elif type(end_time) == float and end_time < 1:
                tu = np.linspace(start_time, end_time, 300)
        return impulse_response(self.TF, T=tu)
    
    def _get_ramp_response(self, start_time=0, end_time =10, start= 0, stop = 10):
        if end_time:
            if type(end_time) == float and end_time >= 1:
                tu = np.linspace(start_time, end_time, int(300*end_time))
            elif type(end_time) == float and end_time < 1:
                tu = np.linspace(start_time, end_time, 300)
        U = np.linspace(start, stop, len(tu))
        return ramp_response(self.TF, T=tu, U = U)
    
    def _get_step_info(self, t, y):
        data = [list(t), list(y)]
        return ResponseAnalyser(data).get_result()
    
    def plot_res(self, func):
        t,y = func()
        plt.plot(t, y)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('Step response')
        plt.grid()
        plt.show()    

    def plot_bode_diagramme(self):
        mag, phase, w = bode(self.TF)
        plt.show()

    def plot_nichols_dlagrame(self):
        nichols(self.TF)
        plt.show()

    def pid_version(self, Kp=1, Ki=0, Kd=0):
        instance = MyAPI(self.num, self.den, self.num2, self.den2)
        instance.TF = my_pid_designer(self.TF,Kp0=Kp, Ki0=Ki, Kd0= Kd)
        # print(instance.TF)
        return instance

    # def plot_nyquist_diagramme(self):
    #     print(nyquist_plot(self.TF, plot=False))
    #     plt.show()