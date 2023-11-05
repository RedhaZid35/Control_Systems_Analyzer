# matplotlib.use('WXAgg')
import asyncio

import matplotlib.pyplot as plt
import numpy as np
import wx
import wx.lib.plot as wxplot
from control import rootlocus_pid_designer
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import \
    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure

from API.api import MyAPI


class MyFrame (wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Control_PID", pos=wx.DefaultPosition, size=wx.Size(
            1280, 720), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.rbtn_checked: str

        self.SetSizeHints(wx.Size(1280, 720), wx.Size(1920, 1080))
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        # Sizers --------------------------------------------------
        Main_sizer = wx.BoxSizer(wx.VERTICAL)
        Header = wx.BoxSizer(wx.HORIZONTAL)
        _G_sizer = wx.BoxSizer(wx.VERTICAL)
        _H_sizer = wx.BoxSizer(wx.VERTICAL)
        _Loop_sizer = wx.StaticBoxSizer(wx.StaticBox(
            self, wx.ID_ANY, "Choose Loop Type "), wx.VERTICAL)
        _Button_sizer = wx.BoxSizer(wx.VERTICAL)

        Body = wx.BoxSizer(wx.HORIZONTAL)
        _Body_left = wx.BoxSizer(wx.VERTICAL)
        __Status_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Status"), wx.VERTICAL)
        __PID_Sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "PID"), wx.VERTICAL)

        U_val_sizer = wx.BoxSizer(wx.HORIZONTAL)
        Time_sizer = wx.BoxSizer(wx.HORIZONTAL)

        U_val_sizer_parent = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "Select Step Value"), wx.VERTICAL)

        ___P_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ___I_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ___D_sizer = wx.BoxSizer(wx.HORIZONTAL)

        _Body_right = wx.BoxSizer(wx.VERTICAL)
        self.__Plot_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, u"Plots"), wx.VERTICAL)

        # Components ----------------------------------------------
        self.G_lable = wx.StaticText(
            self, wx.ID_ANY, u"G(s)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.G_num_txt = wx.TextCtrl(
            self, wx.ID_ANY, "5", wx.DefaultPosition, wx.DefaultSize, 0)
        self.G_den_txt = wx.TextCtrl(
            self, wx.ID_ANY, "1 3 2 0", wx.DefaultPosition, wx.DefaultSize, 0)

        self.H_lable = wx.StaticText(
            self, wx.ID_ANY, u"H(s)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.H_num_txt = wx.TextCtrl(
            self, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, 0)
        self.H_den_txt = wx.TextCtrl(
            self, wx.ID_ANY, "1", wx.DefaultPosition, wx.DefaultSize, 0)

        self.OLTF = wx.RadioButton(_Loop_sizer.GetStaticBox(
        ), wx.ID_ANY, "OLTF", wx.DefaultPosition, wx.DefaultSize, 0)
        self.CLTFUF = wx.RadioButton(_Loop_sizer.GetStaticBox(
        ), wx.ID_ANY, "CLTFUF", wx.DefaultPosition, wx.DefaultSize, 0)
        self.CLTF = wx.RadioButton(_Loop_sizer.GetStaticBox(
        ), wx.ID_ANY, "CLTF", wx.DefaultPosition, wx.DefaultSize, 0)

        self.Auto_timing = wx.CheckBox(
            self, wx.ID_ANY, "Auto Timing", wx.DefaultPosition, wx.DefaultSize, 0)

        self.Time_lbl = wx.StaticText(
            self, wx.ID_ANY, "Simulation time", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Time_txt = wx.TextCtrl(
            self, wx.ID_ANY, "1", wx.DefaultPosition, wx.DefaultSize, 0)

        self.U_val_lbl = wx.StaticText(
            self, wx.ID_ANY, u"Step Value", wx.DefaultPosition, wx.DefaultSize, 0)
        self.U_val_txt = wx.TextCtrl(
            self, wx.ID_ANY, "10", wx.DefaultPosition, wx.DefaultSize, 0)

        self.U_check = wx.CheckBox(
            self, wx.ID_ANY, "Plot Input", wx.DefaultPosition, wx.DefaultSize, 0)

        self.P_check = wx.CheckBox(__PID_Sizer.GetStaticBox(
        ), wx.ID_ANY, "Kp", wx.DefaultPosition, wx.DefaultSize, 0)
        self.P_txt = wx.TextCtrl(__PID_Sizer.GetStaticBox(
        ), wx.ID_ANY, "1", wx.DefaultPosition, wx.DefaultSize, 0)

        self.I_check = wx.CheckBox(__PID_Sizer.GetStaticBox(
        ), wx.ID_ANY, "Ki", wx.DefaultPosition, wx.DefaultSize, 0)
        self.I_txt = wx.TextCtrl(__PID_Sizer.GetStaticBox(
        ), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)

        self.D_check = wx.CheckBox(__PID_Sizer.GetStaticBox(
        ), wx.ID_ANY, "Kd", wx.DefaultPosition, wx.DefaultSize, 0)
        self.D_txt = wx.TextCtrl(__PID_Sizer.GetStaticBox(
        ), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)

        self.my_lables = {
            "Stability": wx.StaticText(__Status_sizer .GetStaticBox(), wx.ID_ANY, "Stability : ", wx.DefaultPosition, wx.DefaultSize, 0),
            "Steady State Value": wx.StaticText(__Status_sizer .GetStaticBox(), wx.ID_ANY, "Steady State Value : ", wx.DefaultPosition, wx.DefaultSize, 0),
            "Settling Time": wx.StaticText(__Status_sizer .GetStaticBox(), wx.ID_ANY, "Settling Time : ", wx.DefaultPosition, wx.DefaultSize, 0),
            "Rise Time": wx.StaticText(__Status_sizer .GetStaticBox(), wx.ID_ANY, "Rise Time : ", wx.DefaultPosition, wx.DefaultSize, 0),
            "Peak": wx.StaticText(__Status_sizer .GetStaticBox(), wx.ID_ANY, "Peak : ", wx.DefaultPosition, wx.DefaultSize, 0)
        }

# todo : ploooooot
        self.fig = Figure(figsize=(1, 1))
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()
        self.canvas = FigureCanvas(self, -1, self.fig)
        self.toolbar = NavigationToolbar(self.canvas)

        # self.toolbar.Bind(wx.EVT_TOOL, self.on_clear, id=wx.ID_ANY)
# todo : plllllloooooot

        self.Simulate_button = wx.Button(
            self, wx.ID_ANY, u"Simulate", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Implement_PID_button = wx.Button(
            __PID_Sizer.GetStaticBox(), wx.ID_ANY, u"Implement PID controller", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Plot_bode_button = wx.Button(
            self, wx.ID_ANY, u"Plot Bode Diagramme", wx.DefaultPosition, wx.DefaultSize, 0)

        self.Clear_canvas_button = wx.Button(
            self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0)

        # Sets ---------------------------------------------
        self.G_lable.SetFont(wx.Font(20, 70, 90, 92, False))
        self.H_lable.SetFont(wx.Font(20, 70, 90, 92, False))

        self.G_num_txt.SetMinSize(wx.Size(290, -1))
        self.G_den_txt.SetMinSize(wx.Size(290, -1))
        self.H_num_txt.SetMinSize(wx.Size(290, -1))
        self.H_den_txt.SetMinSize(wx.Size(290, -1))
        self.U_val_txt.SetMinSize(wx.Size(75, -1))
        self.Time_txt.SetMinSize(wx.Size(48, -1))
        self.P_check.SetMinSize(wx.Size(35, 20))
        self.P_txt.SetMinSize(wx.Size(230, -1))
        self.I_check.SetMinSize(wx.Size(35, 20))
        self.I_txt.SetMinSize(wx.Size(230, -1))
        self.D_check.SetMinSize(wx.Size(35, 20))
        self.D_txt.SetMinSize(wx.Size(230, -1))

        self.P_txt.Disable()
        self.I_txt.Disable()
        self.D_check.Disable()
        self.D_txt.Disable()
        self.H_num_txt.Disable()
        self.H_den_txt.Disable()
        self.Implement_PID_button.Disable()
        # Bindings -------------------------------------------
        self.G_num_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.G_den_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.H_num_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.H_den_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.Time_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.U_val_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.P_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.I_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.D_txt.Bind(wx.EVT_CHAR, self.on_char)
        self.OLTF.Bind(wx.EVT_RADIOBUTTON, self.on_radio_btn_check)
        self.CLTFUF.Bind(wx.EVT_RADIOBUTTON, self.on_radio_btn_check)
        self.CLTF.Bind(wx.EVT_RADIOBUTTON, self.on_radio_btn_check)
        self.P_check.Bind(wx.EVT_CHECKBOX, self.on_check_p)
        self.I_check.Bind(wx.EVT_CHECKBOX, self.on_check_i)
        self.D_check.Bind(wx.EVT_CHECKBOX, self.on_check_d)
        self.U_check.Bind(wx.EVT_CHECKBOX, self.plot_u)
        self.Auto_timing.Bind(wx.EVT_CHECKBOX, self.auto_time)

        self.Simulate_button.Bind(wx.EVT_BUTTON, self.on_Simulate)
        self.Implement_PID_button.Bind(wx.EVT_BUTTON, self.implement_pid)
        self.Plot_bode_button.Bind(wx.EVT_BUTTON, self.on_bode)
        self.Clear_canvas_button.Bind(wx.EVT_BUTTON, self.on_clear)

        # Rendering ------------------------------------------
        _G_sizer.Add(self.G_lable, 0, wx.ALL, 5)
        _G_sizer.Add(self.G_num_txt, 0, wx.LEFT |
                     wx.BOTTOM | wx.RIGHT | wx.EXPAND, 5)
        _G_sizer.Add(self.G_den_txt, 0, wx.LEFT |
                     wx.BOTTOM | wx.RIGHT | wx.EXPAND, 5)

        _H_sizer.Add(self.H_lable, 0, wx.ALL, 5)
        _H_sizer.Add(self.H_num_txt, 0, wx.LEFT |
                     wx.BOTTOM | wx.RIGHT | wx.EXPAND, 5)
        _H_sizer.Add(self.H_den_txt, 0, wx.LEFT |
                     wx.BOTTOM | wx.RIGHT | wx.EXPAND, 5)

        _Loop_sizer.Add(self.OLTF, 0, wx.ALL, 5)
        _Loop_sizer.Add(self.CLTFUF, 0, wx.ALL, 5)
        _Loop_sizer.Add(self.CLTF, 0, wx.ALL, 5)

        _Button_sizer.Add(self.Simulate_button, 0, wx.EXPAND |
                          wx.RIGHT | wx.LEFT | wx.TOP, 10)
        _Button_sizer.Add(self.Plot_bode_button, 0, wx.EXPAND |
                          wx.RIGHT | wx.LEFT | wx.TOP, 10)
        _Button_sizer.Add(self.Clear_canvas_button, 0,
                          wx.EXPAND | wx.RIGHT | wx.LEFT | wx.TOP, 10)

        U_val_sizer.Add(self.U_val_lbl, 0, wx.ALL, 5)
        U_val_sizer.Add(self.U_val_txt, 0, wx.LEFT | wx.RIGHT, 5)
        U_val_sizer.Add(self.U_check, 0, wx.ALL, 5)

        Time_sizer.Add(self.Time_lbl, 0, wx.ALL, 5)
        Time_sizer.Add(self.Time_txt, 0, wx.LEFT | wx.RIGHT, 5)
        Time_sizer.Add(self.Auto_timing, 0, wx.ALL, 5)

        U_val_sizer_parent.Add(Time_sizer, 0, wx.ALL, 5)
        U_val_sizer_parent.Add(U_val_sizer, 0, wx.ALL, 5)

        ___P_sizer.Add(self.P_check, 0, wx.ALL, 5)
        ___P_sizer.Add(self.P_txt, 0, wx.ALL, 5)

        ___I_sizer.Add(self.I_check, 0, wx.ALL, 5)
        ___I_sizer.Add(self.I_txt, 0, wx.ALL, 5)

        ___D_sizer.Add(self.D_check, 0, wx.ALL, 5)
        ___D_sizer.Add(self.D_txt, 0, wx.ALL, 5)

        __PID_Sizer.Add(___P_sizer, 0, 0, 5)
        __PID_Sizer.Add(___I_sizer, 0, 0, 5)
        __PID_Sizer.Add(___D_sizer, 0, 0, 5)
        __PID_Sizer.Add(self.Implement_PID_button, 0, wx.EXPAND | wx.ALL, 5)

        for i in self.my_lables:
            __Status_sizer .Add(self.my_lables[i], 0, wx.ALL, 5)

        _Body_left.Add(__PID_Sizer, 1, wx.EXPAND, 5)
        _Body_left.Add(__Status_sizer, 0, wx.EXPAND, 5)
# todo : plooot
        self.__Plot_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        self.__Plot_sizer.Add(self.toolbar, 0, wx.EXPAND | wx.ALL, 5)

        _Body_right.Add(self.__Plot_sizer, 1, wx.EXPAND |
                        wx.LEFT | wx.RIGHT, 5)

        Header.Add(_G_sizer, 1, wx.ALL | wx.EXPAND, 5)
        Header.Add(_H_sizer, 1, wx.ALL | wx.EXPAND, 5)
        Header.Add(_Loop_sizer, 0, wx.ALL | wx.EXPAND, 5)
        Header.Add(U_val_sizer_parent, 1, wx.ALL | wx.EXPAND, 5)
        Header.Add(_Button_sizer, 1, wx.ALL | wx.EXPAND, 5)

        Body.Add(_Body_left, 0, wx.EXPAND)
        Body.Add(_Body_right, 1, wx.EXPAND)

        Main_sizer.Add(Header, 0, wx.ALL | wx.EXPAND, 10)
        Main_sizer.Add(Body, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 20)

        self.CreateStatusBar()
        self.SetStatusText("Welcome...")
        self.SetSizer(Main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def auto_time(self, event):
        if self.Auto_timing.IsChecked():
            self.Time_txt.Disable()
        else:
            self.Time_txt.Enable()

    def __del__(self):
        pass

    def plot_u(self, event):
        if self.U_check.IsChecked():
            U_val = abs([float(i) for i in str(
                self.U_val_txt.GetValue()).strip().split()][0])
            pass
        else:
            pass

    def on_char(self, event):
        keycode = event.GetKeyCode()
        if keycode < wx.WXK_SPACE or keycode == wx.WXK_DELETE or keycode > 255:
            event.Skip()
            return
        if chr(keycode).isdigit() or chr(keycode).isspace() or chr(keycode) in ('-', '+', '.'):
            event.Skip()
        else:
            return

    def on_check_p(self, event):
        if self.P_check.IsChecked():
            self.P_txt.Enable()
            self.D_check.Enable()
            self.Implement_PID_button.Enable()
        else:
            self.P_txt.Disable()
            self.D_check.Disable()
            if not self.I_check.IsChecked():
                self.Implement_PID_button.Disable()

    def on_check_i(self, event):
        if self.I_check.IsChecked():
            self.I_txt.Enable()
            self.Implement_PID_button.Enable()
        else:
            self.I_txt.Disable()
            if not self.P_check.IsChecked():
                self.Implement_PID_button.Disable()

    def on_check_d(self, event):
        if self.P_check.IsChecked() and self.D_check.IsChecked():
            self.D_txt.Enable()
        else:
            self.D_txt.Disable()

    def on_radio_btn_check(self, event):
        self.Simulate_button.Enable()
        radio_button = event.GetEventObject()
        self.rbtn_checked = radio_button.GetLabel()
        if self.rbtn_checked == "CLTF":
            self.H_num_txt.Enable()
            self.H_den_txt.Enable()
        else:
            self.H_num_txt.Disable()
            self.H_den_txt.Disable()
        self.Update()

    def on_Simulate(self, event):
        try:
            self.SetStatusText("Simulation...")
            # Get values from the TxtCrls and clean them
            g_num = [float(i)
                     for i in str(self.G_num_txt.GetValue()).strip().split()]
            g_den = [float(i)
                     for i in str(self.G_den_txt.GetValue()).strip().split()]
            h_num = [float(i)
                     for i in str(self.H_num_txt.GetValue()).strip().split()]
            h_den = [float(i)
                     for i in str(self.H_den_txt.GetValue()).strip().split()]

            # Check if the oreder of the numenator is less than or equal to the order of the denumenator
            if len(g_num) > len(g_den) or len(h_num) > len(h_den):
                wx.MessageBox(
                    "The order of the numenator must be less than or equal to the order of the denumenator  ")
                self.SetStatusText("Error!!!")
                return

            # Check the type of the loop and create the system
            if self.rbtn_checked == "CLTF":
                self.my_system = MyAPI(g_num, g_den, num2=h_num, den2=h_den)
            elif self.rbtn_checked == "CLTFUF":
                self.my_system = MyAPI(g_num, g_den, num2=1)
            else:
                self.my_system = MyAPI(g_num, g_den)

            t, y, U_val, test = self.calculate_step_r(self.my_system)
            self.plot(event, t, y, U_val)
            self.update_lbls(self.my_system, test)
            self.SetStatusText("Completed")
            self.Update()
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
            self.SetStatusText("Error!!!")

    def on_bode(self, event):
        self.my_system.plot_bode_diagramme()
        pass

# todo ploooooootototot
    def on_clear(self, event):
        try:
            self.ax.clear()
            self.ax.grid()
            self.canvas.draw()
            for i in self.my_lables:
                self.my_lables[i].SetLabel(i + " : ")
            self.Update()
        except:
            wx.MessageBox(
                Exception)
            self.SetStatusText("Error!!!")
            return

    def plot(self, event, t, y, U_val, lable="output"):
        try:
            if self.U_check.IsChecked():
                U = U_val*(np.ones_like(t))
                self.ax.plot(t, U, label="input")
            self.ax.plot(t, y, label=lable)
            self.ax.legend()
            self.canvas.draw()
            self.Update()
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
            self.SetStatusText("Error!!!")

    def implement_pid(self, event):
        try:
            self.SetStatusText("Simulation...")
            Kp = [float(i) for i in str(self.P_txt.GetValue()).strip().split()]
            Ki = [float(i) for i in str(self.I_txt.GetValue()).strip().split()]
            Kd = [float(i) for i in str(self.D_txt.GetValue()).strip().split()]
            lable = ""

            if not (self.P_check.IsChecked() or self.I_check.IsChecked() or self.D_check.IsChecked()):
                wx.MessageBox(
                    "No parameter provided. \nPlease check at least one of the PID parameters (Kp, Ki or Kd)")
                self.SetStatusText("Error!!!")
                return
                pass

            if len(Kp) == 0 and self.P_check.IsChecked():
                wx.MessageBox("HEY, you forgot the Kp parameter")
                self.SetStatusText("Error!!!")
                return
            if len(Ki) == 0 and self.I_check.IsChecked():
                wx.MessageBox("HEY, you forgot the Ki parameter")
                self.SetStatusText("Error!!!")
                return
            if len(Kd) == 0 and self.D_check.IsChecked():
                wx.MessageBox("HEY, you forgot the Kd parameter")
                self.SetStatusText("Error!!!")
                return

            if self.P_check.IsChecked():
                lable += "P"
            if self.I_check.IsChecked():
                lable += "I"
            if self.D_check.IsChecked():
                lable += "D"

            new_system = self.my_system.pid_version(
                Kp=Kp[0] if self.P_check.IsChecked() and Kp else 1,
                Ki=Ki[0] if self.I_check.IsChecked() and Ki else 0,
                Kd=Kd[0] if self.D_check.Enabled and self.D_check.IsChecked() and Kd else 0,
            )

            t, y, U_val, test = self.calculate_step_r(new_system)
            self.plot(0, t, y, U_val, lable="With "+lable)
            self.update_lbls(new_system, test)
            self.SetStatusText("Completed")
            self.Update()
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
            self.SetStatusText("Error!!!")

    def update_lbls(self, sys, test):
        self.my_lables["Stability"].SetLabel(
            f"Stability : {sys.is_stable_by_poles_method()}")
        if sys.is_stable_by_poles_method():
            for i in test:
                self.my_lables[i].SetLabel(i + " : " + str(test[i]))
        else:
            for i in test:
                self.my_lables[i].SetLabel(i + " : " + "Not available")

    def calculate_step_r(self, sys):
        U_val = abs([float(i)
                    for i in str(self.U_val_txt.GetValue()).strip().split()][0])
        time = [float(i)
                for i in str(self.Time_txt.GetValue()).strip().split()]
        if not self.Auto_timing.IsChecked():
            if not len(time) > 0:
                wx.MessageBox(
                    "You forgot to provide the simulation time")
                self.SetStatusText("Error!!!")
                return
            if time[0] <= 0:
                wx.MessageBox(
                    "Hey fool, is there any non positive time ??????")
                self.SetStatusText("Error!!!")
                return
            t, y, test = sys._get_step_response(U_val=U_val, end_time=time[0])
        else:
            t, y, test = sys._get_step_response(U_val=U_val)
        return t, y, U_val, test


if __name__ == '__main__':
    app = wx.App()
    frm = MyFrame(None)
    frm.Show()
    app.MainLoop()
