# TODO : provide a precision and check stability 
# TODO : analyse precision, depacement, rise time, estblisment time 

from MyApp import MyFrame
from wx import App

if __name__ == '__main__':
    app = App()
    frm = MyFrame(None)
    frm.Show()
    app.MainLoop()


