# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame
###########################################################################

class MyFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Control_PID", pos = wx.DefaultPosition, size = wx.Size( 1280,720 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.Size( 1920,1080 ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		Main_sizer = wx.BoxSizer( wx.VERTICAL )
		
		Header = wx.BoxSizer( wx.HORIZONTAL )
		
		G_sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.G_lable = wx.StaticText( self, wx.ID_ANY, u"G(s)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.G_lable.Wrap( -1 )
		self.G_lable.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )
		
		G_sizer.Add( self.G_lable, 0, wx.ALL, 5 )
		
		self.G_num_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		G_sizer.Add( self.G_num_txt, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.G_den_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		G_sizer.Add( self.G_den_txt, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		Header.Add( G_sizer, 1, wx.ALL|wx.EXPAND, 5 )
		
		H_sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.H_lable = wx.StaticText( self, wx.ID_ANY, u"H(s)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.H_lable.Wrap( -1 )
		self.H_lable.SetFont( wx.Font( 20, 70, 90, 92, False, wx.EmptyString ) )
		
		H_sizer.Add( self.H_lable, 0, wx.ALL, 5 )
		
		self.H_num_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		H_sizer.Add( self.H_num_txt, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.H_den_txt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		H_sizer.Add( self.H_den_txt, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		Header.Add( H_sizer, 1, wx.ALL|wx.EXPAND, 5 )
		
		Loop_sizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Choose Loop Type " ), wx.VERTICAL )
		
		self.OLTF = wx.RadioButton( Loop_sizer.GetStaticBox(), wx.ID_ANY, u"OLTF", wx.DefaultPosition, wx.DefaultSize, 0 )
		Loop_sizer.Add( self.OLTF, 0, wx.ALL, 5 )
		
		self.CLTFUF = wx.RadioButton( Loop_sizer.GetStaticBox(), wx.ID_ANY, u"CLTFUF", wx.DefaultPosition, wx.DefaultSize, 0 )
		Loop_sizer.Add( self.CLTFUF, 0, wx.ALL, 5 )
		
		self.CLTF = wx.RadioButton( Loop_sizer.GetStaticBox(), wx.ID_ANY, u"CLTF", wx.DefaultPosition, wx.DefaultSize, 0 )
		Loop_sizer.Add( self.CLTF, 0, wx.ALL, 5 )
		
		
		Header.Add( Loop_sizer, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		Main_sizer.Add( Header, 1, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 10 )
		
		Body = wx.BoxSizer( wx.HORIZONTAL )
		
		Body_left = wx.BoxSizer( wx.VERTICAL )
		
		PID_Sizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"PID" ), wx.VERTICAL )
		
		P_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.P_check = wx.CheckBox( PID_Sizer.GetStaticBox(), wx.ID_ANY, u"P", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.P_check.SetMinSize( wx.Size( 30,20 ) )
		
		P_sizer.Add( self.P_check, 0, wx.ALL, 5 )
		
		self.P_txt = wx.TextCtrl( PID_Sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.P_txt.SetMinSize( wx.Size( 230,-1 ) )
		
		P_sizer.Add( self.P_txt, 0, wx.ALL, 5 )
		
		
		PID_Sizer.Add( P_sizer, 0, 0, 5 )
		
		I_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.I_check = wx.CheckBox( PID_Sizer.GetStaticBox(), wx.ID_ANY, u"I ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.I_check.SetMinSize( wx.Size( 30,20 ) )
		
		I_sizer.Add( self.I_check, 0, wx.ALL, 5 )
		
		self.I_txt = wx.TextCtrl( PID_Sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.I_txt.SetMinSize( wx.Size( 230,-1 ) )
		
		I_sizer.Add( self.I_txt, 0, wx.ALL, 5 )
		
		
		PID_Sizer.Add( I_sizer, 0, 0, 5 )
		
		D_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.D_check = wx.CheckBox( PID_Sizer.GetStaticBox(), wx.ID_ANY, u"D", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.D_check.SetMinSize( wx.Size( 30,20 ) )
		
		D_sizer.Add( self.D_check, 0, wx.ALL, 5 )
		
		self.D_txt = wx.TextCtrl( PID_Sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.D_txt.SetMinSize( wx.Size( 230,-1 ) )
		
		D_sizer.Add( self.D_txt, 0, wx.ALL, 5 )
		
		
		PID_Sizer.Add( D_sizer, 0, 0, 5 )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( PID_Sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		PID_Sizer.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		Body_left.Add( PID_Sizer, 0, wx.EXPAND, 5 )
		
		
		Body.Add( Body_left, 0, wx.EXPAND|wx.LEFT, 10 )
		
		Body_right = wx.BoxSizer( wx.VERTICAL )
		
		
		Body.Add( Body_right, 1, wx.EXPAND, 5 )
		
		
		Main_sizer.Add( Body, 10, wx.ALL|wx.EXPAND, 10 )
		
		Footer  = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Analyze_button = wx.Button( self, wx.ID_ANY, u"Analyze", wx.DefaultPosition, wx.DefaultSize, 0 )
		Footer .Add( self.Analyze_button, 1, wx.ALL, 5 )
		
		self.Plot_step_button = wx.Button( self, wx.ID_ANY, u"Plot Step Response ", wx.DefaultPosition, wx.DefaultSize, 0 )
		Footer .Add( self.Plot_step_button, 1, wx.ALL, 5 )
		
		self.Plot_bode_button  = wx.Button( self, wx.ID_ANY, u"Plot Bode Diagramme", wx.DefaultPosition, wx.DefaultSize, 0 )
		Footer .Add( self.Plot_bode_button , 1, wx.ALL, 5 )
		
		self. = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		Footer .Add( self., 1, wx.ALL, 5 )
		
		
		Main_sizer.Add( Footer , 0, wx.ALIGN_BOTTOM|wx.ALL|wx.EXPAND, 10 )
		
		
		self.SetSizer( Main_sizer )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

