from control import TransferFunction
from API.api import MyAPI
from wx import *


class MyFrame(Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)
        self.my_system : TransferFunction
        self.MaxSize = (1280, 720)
        self.MinSize = (1280, 720)
        self.rbtn_checked : str 
        self.stab = ""
        self.vf = 0
        self.vm = 0
        self.et = 0
        self.mt = 0

        pnl = Panel(self)

        # my sizers to manage the layout of child widgets
        outer_sizer = BoxSizer(VERTICAL)
        header = BoxSizer(HORIZONTAL)
        g_sizer = BoxSizer(VERTICAL)
        h_sizer = BoxSizer(VERTICAL)
        r_sizer = StaticBoxSizer(VERTICAL, pnl, label="Select Loop Type")
        pid_sizer = StaticBoxSizer(VERTICAL, pnl, label="Select Loop Type")
        left_body = BoxSizer(VERTICAL)
        right_body = BoxSizer(VERTICAL)
        body = BoxSizer(HORIZONTAL)
        footer = BoxSizer(HORIZONTAL)

        # HEADER ---------------------------------------------------------------------------------------------------
        g_s = StaticText(pnl, label="G(s)")
        h_s = StaticText(pnl, label="H(s)")
        font = g_s.GetFont()
        font.PointSize += 10
        font = font.Bold()
        g_s.SetFont(font)
        h_s.SetFont(font)

        # PUT THE TXT BOXES FOR G(S) AND H(S)
        self.g_num_box = TextCtrl(pnl, value='1',)
        self.g_den_box = TextCtrl(pnl, value='1 1',)
        self.h_num_box = TextCtrl(pnl, 1, value='1',)
        self.h_den_box = TextCtrl(pnl, 2, value='1 1',)

        self.g_num_box.Bind(EVT_CHAR, self.on_char)
        self.g_den_box.Bind(EVT_CHAR, self.on_char)
        self.h_num_box.Bind(EVT_CHAR, self.on_char)
        self.h_den_box.Bind(EVT_CHAR, self.on_char)

        self.h_num_box.Disable()
        self.h_den_box.Disable()

        g_sizer.Add(g_s, SizerFlags().Border(TOP | LEFT, 25))
        g_sizer.Add(self.g_num_box, 1, EXPAND | ALL, 4)
        g_sizer.Add(self.g_den_box, 1, EXPAND | ALL, 4)

        h_sizer.Add(h_s, SizerFlags().Border(TOP | LEFT, 25))
        h_sizer.Add(self.h_num_box, 1, EXPAND | ALL, 4)
        h_sizer.Add(self.h_den_box, 1, EXPAND | ALL, 4)

        r_tfol = RadioButton(pnl, label="TFOL")
        r_tfclwuf = RadioButton(pnl, label="TFCLWUF")
        r_tfcl = RadioButton(pnl, label="TFCL")

        r_tfol.Bind(EVT_RADIOBUTTON, self.on_radio_btn_check)
        r_tfclwuf.Bind(EVT_RADIOBUTTON, self.on_radio_btn_check)
        r_tfcl.Bind(EVT_RADIOBUTTON, self.on_radio_btn_check)

        r_sizer.Add(r_tfol, ALIGN_CENTER)
        r_sizer.Add(r_tfclwuf, ALIGN_CENTER)
        r_sizer.Add(r_tfcl, ALIGN_CENTER)

        header.Add(g_sizer, 1, EXPAND)
        header.Add(h_sizer, 1, EXPAND)
        header.Add(r_sizer, 1, EXPAND | TOP, 26)

        # BODY -------------------------------------------------------------------------------------------------------
        



        self.lables = {
            "stab": StaticText(pnl, label="Stability : NOT AVAILABLE",),
            "vf": StaticText(pnl, label="Final value : NOT AVAILABLE"),
            "vm": StaticText(pnl, label="Max value : NOT AVAILABLE"),
            "et": StaticText(pnl, label="Establishment time : NOT AVAILABLE"),
            "mt": StaticText(pnl, label="Mounting time : NOT AVAILABLE"),
        }

        for lable in self.lables:
            left_body.Add(self.lables[lable], 1)
        
        body.Add(left_body, 1)
        body.Add(right_body, 1)

        # FOOTER-----------------------------------------------------------------------------------------------------
        self.analyse_btn = Button(pnl, label="Analyse")
        self.plt_res_btn = Button(pnl, label="Plot step response")
        self.plt_rmp_btn = Button(pnl, label="Plot ramp response")
        self.plt_bod_btn = Button(pnl, label="Plot bode diagrame")

        self.analyse_btn.Disable()
        self.plt_res_btn.Disable()
        self.plt_rmp_btn.Disable()
        self.plt_bod_btn.Disable()

        self.analyse_btn.Bind(EVT_BUTTON, self.on_analyse_btn_click)
        self.plt_res_btn.Bind(EVT_BUTTON, self.on_plt_res_btn_click)
        self.plt_rmp_btn.Bind(EVT_BUTTON, self.on_plt_rmp_btn_click)
        self.plt_bod_btn.Bind(EVT_BUTTON, self.on_plt_bod_btn_click)

        footer.Add(self.analyse_btn, 1, EXPAND)
        footer.Add(self.plt_res_btn, 1, EXPAND)
        footer.Add(self.plt_rmp_btn, 1, EXPAND)
        footer.Add(self.plt_bod_btn, 1, EXPAND)

        # FINELZE----------------------------------------------------------------------------------------------------
        outer_sizer.Add(header, 0, EXPAND | RIGHT | LEFT, 26)
        outer_sizer.Add(body, 1, EXPAND | ALL, 26)
        outer_sizer.Add(footer, 0, EXPAND | RIGHT |
                        LEFT | BOTTOM, 26, ALIGN_BOTTOM)
        pnl.SetSizer(outer_sizer)

        # create a menu bar
        self.makeMenuBar()
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Systme analyzer")

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                                    "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(ID_EXIT)

        # Now a help menu for the about item
        helpMenu = Menu()
        aboutItem = helpMenu.Append(ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(EVT_MENU, self.OnHello, helloItem)
        self.Bind(EVT_MENU, self.OnExit,  exitItem)
        self.Bind(EVT_MENU, self.OnAbout, aboutItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnHello(self, event):
        """Say hello to the user."""
        MessageBox(
            "Hello, This app was made by  AHMED RIDHA ZIDHANE, An instrumentation student at the INH ")

    def OnAbout(self, event):
        """Display an About Dialog"""
        MessageBox("Hello, This app was made by  AHMED RIDHA ZIDHANE, An instrumentation student at the INH ",
                   "About",
                   OK | ICON_INFORMATION)

    def on_analyse_btn_click(self, event):
        # TODO : satus bar
        self.SetStatusText("Analyzing...")
        g_num = [int(i)
                 for i in str(self.g_num_box.GetValue()).strip().split()]
        g_den = [int(i)
                 for i in str(self.g_den_box.GetValue()).strip().split()]
        h_num = [int(i)
                 for i in str(self.h_num_box.GetValue()).strip().split()]
        h_den = [int(i)
                 for i in str(self.h_den_box.GetValue()).strip().split()]
        # print(type(h_den[0]))
        if len(g_num) > len(g_den) or len(h_num) > len(h_den):
            MessageBox(
                "The order of the numenator must be les than or equal to the order of the denumenator  ")
        # print(self.rbtn_checked)
        if self.rbtn_checked == "TFOL":
            self.my_system = MySystem(g_num, g_den)
        elif self.rbtn_checked == "TFCLWUF":
            self.my_system = MySystem(g_num, g_den, TF_Feed=1)
        elif self.rbtn_checked == "TFCL":
            self.my_system = MySystem(
                g_num, g_den, TF_Feed=TransferFunction(h_num, h_den))
        t, y = self.my_system._get_step_response()
        data = [list(t), list(y)]
        test = ResponseAnalyser(data=data)
        if self.my_system.is_stable_by_poles_method():
            self.lables["stab"].SetLabel(f"Stability : {test.stability}")
            self.lables["vf"].SetLabel(f"Final value : {test.vf}")
            self.lables["vm"].SetLabel(f"Max value : {test.vm}")
            self.lables["et"].SetLabel(f"Establishment time : {test.te} s")
            self.lables["mt"].SetLabel(f"Mounting time : {test.tm} s")

        self.SetStatusText("Completed")
        self.plt_bod_btn.Enable()
        self.plt_res_btn.Enable()
        self.plt_rmp_btn.Enable()
        self.Update()

    def on_plt_res_btn_click(self, event):
        self.my_system.plot_step_response()

    def on_plt_rmp_btn_click(self, event):
        self.my_system.plot_ramp_response()

    def on_plt_bod_btn_click(self, event):
        self.my_system.plot_bode_diagramme()

    def on_radio_btn_check(self, event):
        self.analyse_btn.Enable()
        radio_button = event.GetEventObject()
        self.rbtn_checked = radio_button.GetLabel()
        if self.rbtn_checked == "TFCL":
            self.h_num_box.Enable()
            self.h_den_box.Enable()
        else:
            self.h_num_box.Disable()
            self.h_den_box.Disable()
        self.Update()

    def on_char(self, event):
        keycode = event.GetKeyCode()
        if keycode < WXK_SPACE or keycode == WXK_DELETE or keycode > 255:
            event.Skip()
            return

        if chr(keycode).isdigit() or chr(keycode).isspace() or chr(keycode) in ('-', '+'):
            event.Skip()
        else:
            return

if __name__ == '__main__':
    app = App()
    frm = MyFrame(None, title='Sytems Analyzer')
    frm.Show()
    app.MainLoop()

