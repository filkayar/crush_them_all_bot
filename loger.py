import wx
import wx.xrc

###########################################################################
## Class LogDialog
###########################################################################


class LogDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 671,487 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		L_sizer = wx.BoxSizer( wx.HORIZONTAL )

		self.LOG = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 600,400 ), wx.TE_LEFT|wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP|wx.VSCROLL )
		self.LOG.SetMinSize( wx.Size( 600,400 ) )

		L_sizer.Add( self.LOG, 1, wx.ALL|wx.EXPAND, 5 )

		self.SetSizer( L_sizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass