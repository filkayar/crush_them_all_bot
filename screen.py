import wx
import wx.xrc
import wx.grid
import mouse


class ScreenDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.Size( -1,-1 ) )

		SD_container = wx.FlexGridSizer( 0, 2, 0, 0 )
		SD_container.SetFlexibleDirection( wx.BOTH )
		SD_container.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer10 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer7 = wx.FlexGridSizer( 1, 3, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText123 = wx.StaticText( self, wx.ID_ANY, u"Зона проверки экрана", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText123.Wrap( -1 )

		fgSizer7.Add( self.m_staticText123, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_check_zone = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer7.Add( self.set_check_zone, 0, wx.ALL|wx.EXPAND, 5 )

		check_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.ckz_x0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		check_coord.Add( self.ckz_x0, 0, wx.ALL, 5 )

		self.ckz_y0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		check_coord.Add( self.ckz_y0, 0, wx.ALL, 5 )

		self.ckz_x1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		check_coord.Add( self.ckz_x1, 0, wx.ALL, 5 )

		self.ckz_y1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		check_coord.Add( self.ckz_y1, 0, wx.ALL, 5 )


		fgSizer7.Add( check_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer10.Add( fgSizer7, 1, wx.EXPAND, 5 )

		self.m_staticline12 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer10.Add( self.m_staticline12, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer8 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText122 = wx.StaticText( self, wx.ID_ANY, u"Зона получения", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText122.Wrap( -1 )

		fgSizer8.Add( self.m_staticText122, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_end_zone = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer8.Add( self.set_end_zone, 0, wx.ALL|wx.EXPAND, 5 )

		end_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.ez_x0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		end_coord.Add( self.ez_x0, 0, wx.ALL, 5 )

		self.ez_y0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		end_coord.Add( self.ez_y0, 0, wx.ALL, 5 )

		self.ez_x1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		end_coord.Add( self.ez_x1, 0, wx.ALL, 5 )

		self.ez_y1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		end_coord.Add( self.ez_y1, 0, wx.ALL, 5 )


		fgSizer8.Add( end_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer10.Add( fgSizer8, 1, wx.EXPAND, 5 )

		self.m_staticline17 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer10.Add( self.m_staticline17, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer9 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer9.SetFlexibleDirection( wx.BOTH )
		fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1211 = wx.StaticText( self, wx.ID_ANY, u"Зона воспроизведения", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText1211.Wrap( -1 )

		fgSizer9.Add( self.m_staticText1211, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_play_zone = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer9.Add( self.set_play_zone, 0, wx.ALL|wx.EXPAND, 5 )

		play_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.pz_x0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		play_coord.Add( self.pz_x0, 0, wx.ALL, 5 )

		self.pz_y0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		play_coord.Add( self.pz_y0, 0, wx.ALL, 5 )

		self.pz_x1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		play_coord.Add( self.pz_x1, 0, wx.ALL, 5 )

		self.pz_y1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		play_coord.Add( self.pz_y1, 0, wx.ALL, 5 )


		fgSizer9.Add( play_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer10.Add( fgSizer9, 1, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer10.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer101 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer101.SetFlexibleDirection( wx.BOTH )
		fgSizer101.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1212 = wx.StaticText( self, wx.ID_ANY, u"Зона поиска крылатых сундуков", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText1212.Wrap( -1 )

		fgSizer101.Add( self.m_staticText1212, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_chest3_zone = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer101.Add( self.set_chest3_zone, 0, wx.ALL|wx.EXPAND, 5 )

		chest3_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.ct3z_x0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		chest3_coord.Add( self.ct3z_x0, 0, wx.ALL, 5 )

		self.ct3z_y0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		chest3_coord.Add( self.ct3z_y0, 0, wx.ALL, 5 )

		self.ct3z_x1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		chest3_coord.Add( self.ct3z_x1, 0, wx.ALL, 5 )

		self.ct3z_y1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		chest3_coord.Add( self.ct3z_y1, 0, wx.ALL, 5 )


		fgSizer101.Add( chest3_coord, 1, 0, 5 )


		fgSizer10.Add( fgSizer101, 1, wx.EXPAND, 5 )

		self.m_staticline111 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer10.Add( self.m_staticline111, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer111 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer111.SetFlexibleDirection( wx.BOTH )
		fgSizer111.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText121 = wx.StaticText( self, wx.ID_ANY, u"Зона поиска сундуков", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText121.Wrap( -1 )

		fgSizer111.Add( self.m_staticText121, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_chest_zone = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer111.Add( self.set_chest_zone, 0, wx.ALL|wx.EXPAND, 5 )

		chest_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.ctz_x0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		chest_coord.Add( self.ctz_x0, 0, wx.ALL, 5 )

		self.ctz_y0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		chest_coord.Add( self.ctz_y0, 0, wx.ALL, 5 )

		self.ctz_x1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		chest_coord.Add( self.ctz_x1, 0, wx.ALL, 5 )

		self.ctz_y1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		chest_coord.Add( self.ctz_y1, 0, wx.ALL, 5 )


		fgSizer111.Add( chest_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer10.Add( fgSizer111, 1, wx.EXPAND, 5 )

		self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer10.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer12 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText128 = wx.StaticText( self, wx.ID_ANY, u"Зона скриншотов", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText128.Wrap( -1 )

		fgSizer12.Add( self.m_staticText128, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_screen_zone = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.set_screen_zone, 0, wx.ALL|wx.EXPAND, 5 )

		screen_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.sz_x0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		self.sz_x0.SetMaxSize( wx.Size( 50,-1 ) )

		screen_coord.Add( self.sz_x0, 0, wx.ALL, 5 )

		self.sz_y0 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		screen_coord.Add( self.sz_y0, 0, wx.ALL, 5 )

		self.sz_x1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		screen_coord.Add( self.sz_x1, 0, wx.ALL, 5 )

		self.sz_y1 = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		screen_coord.Add( self.sz_y1, 0, wx.ALL, 5 )


		fgSizer12.Add( screen_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer10.Add( fgSizer12, 1, wx.EXPAND, 5 )


		SD_container.Add( fgSizer10, 1, 0, 5 )

		fgSizer11 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer14 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText125 = wx.StaticText( self, wx.ID_ANY, u" - ИКОНКА ПРИЛОЖЕНИЯ", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText125.Wrap( -1 )

		fgSizer14.Add( self.m_staticText125, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_icon_zone = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer14.Add( self.set_icon_zone, 0, wx.ALL|wx.EXPAND, 5 )

		icon_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.iz_x = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		icon_coord.Add( self.iz_x, 0, wx.ALL, 5 )

		self.iz_y = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 4 )
		icon_coord.Add( self.iz_y, 0, wx.ALL, 5 )


		fgSizer14.Add( icon_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer11.Add( fgSizer14, 1, wx.EXPAND, 5 )

		self.m_staticline16 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer11.Add( self.m_staticline16, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer141 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer141.SetFlexibleDirection( wx.BOTH )
		fgSizer141.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText126 = wx.StaticText( self, wx.ID_ANY, u" - НАЗАД", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText126.Wrap( -1 )

		fgSizer141.Add( self.m_staticText126, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_BACK = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer141.Add( self.set_BACK, 0, wx.ALL|wx.EXPAND, 5 )

		BACK_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.b_x = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		BACK_coord.Add( self.b_x, 0, wx.ALL, 5 )

		self.b_y = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		BACK_coord.Add( self.b_y, 0, wx.ALL, 5 )


		fgSizer141.Add( BACK_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer11.Add( fgSizer141, 1, wx.EXPAND, 5 )

		self.m_staticline163 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer11.Add( self.m_staticline163, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer142 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer142.SetFlexibleDirection( wx.BOTH )
		fgSizer142.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText127 = wx.StaticText( self, wx.ID_ANY, u" - ФОНОВЫЕ ПРИЛОЖЕНИЯ", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText127.Wrap( -1 )

		fgSizer142.Add( self.m_staticText127, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_APPS = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer142.Add( self.set_APPS, 0, wx.ALL|wx.EXPAND, 5 )

		APPS_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.a_x = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		APPS_coord.Add( self.a_x, 0, wx.ALL, 5 )

		self.a_y = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		APPS_coord.Add( self.a_y, 0, wx.ALL, 5 )


		fgSizer142.Add( APPS_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer11.Add( fgSizer142, 1, wx.EXPAND, 5 )

		self.m_staticline14 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer11.Add( self.m_staticline14, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer143 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer143.SetFlexibleDirection( wx.BOTH )
		fgSizer143.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText124 = wx.StaticText( self, wx.ID_ANY, u" - ОЧИСТИТЬ", wx.DefaultPosition, wx.Size( 240,-1 ), 0 )
		self.m_staticText124.Wrap( -1 )

		fgSizer143.Add( self.m_staticText124, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.set_CLEAR = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer143.Add( self.set_CLEAR, 0, wx.ALL|wx.EXPAND, 5 )

		CLEAR_coord = wx.GridSizer( 2, 2, 0, 0 )

		self.c_x = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		CLEAR_coord.Add( self.c_x, 0, wx.ALL, 5 )

		self.c_y = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 70,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		CLEAR_coord.Add( self.c_y, 0, wx.ALL, 5 )


		fgSizer143.Add( CLEAR_coord, 1, wx.ALIGN_CENTER, 5 )


		fgSizer11.Add( fgSizer143, 1, wx.EXPAND, 5 )

		self.m_staticline15 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer11.Add( self.m_staticline15, 0, wx.EXPAND |wx.ALL, 5 )

		fgSizer22 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer22.SetFlexibleDirection( wx.BOTH )
		fgSizer22.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Зона поиска выхода", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText12.Wrap( -1 )

		fgSizer22.Add( self.m_staticText12, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		bSizer35 = wx.BoxSizer( wx.VERTICAL )

		bSizer35.SetMinSize( wx.Size( 100,-1 ) )
		self.set_exit_zone = wx.Button( self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.set_exit_zone, 1, wx.ALL|wx.EXPAND, 5 )

		self.clear_exit_zone = wx.Button( self, wx.ID_ANY, u"CLEAR", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer35.Add( self.clear_exit_zone, 1, wx.ALL|wx.EXPAND, 5 )


		fgSizer22.Add( bSizer35, 0, wx.EXPAND, 5 )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Список зон поиска" ), wx.VERTICAL )

		sbSizer1.SetMinSize( wx.Size( 300,150 ) )
		self.find_zones = wx.grid.Grid( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 250,-1 ), 0 )

		# Grid
		self.find_zones.CreateGrid( 0, 4 )
		self.find_zones.EnableEditing( False )
		self.find_zones.EnableGridLines( True )
		self.find_zones.EnableDragGridSize( False )
		self.find_zones.SetMargins( 0, 0 )

		# Columns
		self.find_zones.SetColSize( 0, 50 )
		self.find_zones.SetColSize( 1, 50 )
		self.find_zones.SetColSize( 2, 50 )
		self.find_zones.SetColSize( 3, 50 )
		self.find_zones.EnableDragColMove( False )
		self.find_zones.EnableDragColSize( True )
		self.find_zones.SetColLabelValue( 0, u"x0" )
		self.find_zones.SetColLabelValue( 1, u"y0" )
		self.find_zones.SetColLabelValue( 2, u"x1" )
		self.find_zones.SetColLabelValue( 3, u"y1" )
		self.find_zones.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.find_zones.AutoSizeRows()
		self.find_zones.EnableDragRowSize( True )
		self.find_zones.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.find_zones.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.find_zones.SetMinSize( wx.Size( -1,120 ) )

		sbSizer1.Add( self.find_zones, 0, wx.ALL|wx.EXPAND, 5 )


		fgSizer22.Add( sbSizer1, 1, wx.EXPAND, 5 )


		fgSizer11.Add( fgSizer22, 1, wx.EXPAND, 5 )


		SD_container.Add( fgSizer11, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( SD_container )
		self.Layout()
		SD_container.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.set_check_zone.Bind( wx.EVT_BUTTON, self.SetZone_check )
		self.set_end_zone.Bind( wx.EVT_BUTTON, self.SetZone_end )
		self.set_play_zone.Bind( wx.EVT_BUTTON, self.SetZone_play )
		self.set_chest3_zone.Bind( wx.EVT_BUTTON, self.SetZone_chest3 )
		self.set_chest_zone.Bind( wx.EVT_BUTTON, self.SetZone_chest )
		self.set_screen_zone.Bind( wx.EVT_BUTTON, self.SetZone_screen )
		self.set_icon_zone.Bind( wx.EVT_BUTTON, self.SetZone_icon )
		self.set_BACK.Bind( wx.EVT_BUTTON, self.SetZone_BACK )
		self.set_APPS.Bind( wx.EVT_BUTTON, self.SetZone_APPS )
		self.set_CLEAR.Bind( wx.EVT_BUTTON, self.SetZone_CLEAR )
		self.set_exit_zone.Bind( wx.EVT_BUTTON, self.SetZone_exit )
		self.clear_exit_zone.Bind( wx.EVT_BUTTON, self.Clear_exit_zone )


		self.parent = parent

	def __del__( self ):
		pass

	def clear_exit_zone_f(self):
		n = self.find_zones.GetNumberRows()
		if n > 0:
			self.find_zones.DeleteRows(numRows=n)

	def Clear_exit_zone(self, event):
		self.clear_exit_zone_f()

	def SetZone_exit( self, event ):
		self.counter = 0
		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				row_count = self.find_zones.GetNumberRows()
				self.find_zones.AppendRows(1)
				self.find_zones.SetCellValue(row_count, 0, str(x))
				self.find_zones.SetCellValue(row_count, 1, str(y))

			elif self.counter == 1:
				row_count = self.find_zones.GetNumberRows() - 1
				self.find_zones.SetCellValue(row_count, 2, str(x))
				self.find_zones.SetCellValue(row_count, 3, str(y))
				mouse.unhook_all()

			self.counter += 1

		mouse.on_click(on_click)

	def SetZone_chest( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.ctz_x0.SetValue(x)
				self.ctz_y0.SetValue(y)
			elif self.counter == 1:
				self.ctz_x1.SetValue(x)
				self.ctz_y1.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)


	def SetZone_chest3( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.ct3z_x0.SetValue(x)
				self.ct3z_y0.SetValue(y)
			elif self.counter == 1:
				self.ct3z_x1.SetValue(x)
				self.ct3z_y1.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)


	def SetZone_play(self, event):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.pz_x0.SetValue(x)
				self.pz_y0.SetValue(y)
			elif self.counter == 1:
				self.pz_x1.SetValue(x)
				self.pz_y1.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)

	def SetZone_end( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.ez_x0.SetValue(x)
				self.ez_y0.SetValue(y)
			elif self.counter == 1:
				self.ez_x1.SetValue(x)
				self.ez_y1.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)

	def SetZone_check( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.ckz_x0.SetValue(x)
				self.ckz_y0.SetValue(y)
			elif self.counter == 1:
				self.ckz_x1.SetValue(x)
				self.ckz_y1.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)

	def SetZone_icon( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.iz_x.SetValue(x)
				self.iz_y.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)

	def SetZone_screen( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.sz_x0.SetValue(x)
				self.sz_y0.SetValue(y)
			elif self.counter == 1:
				self.sz_x1.SetValue(x)
				self.sz_y1.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)

	def SetZone_BACK( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.b_x.SetValue(x)
				self.b_y.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)

	def SetZone_APPS( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.a_x.SetValue(x)
				self.a_y.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)

	def SetZone_CLEAR( self, event ):
		self.counter = 0

		def on_click():
			x, y = mouse.get_position()
			if self.counter == 0:
				self.c_x.SetValue(x)
				self.c_y.SetValue(y)
				mouse.unhook_all()
			self.counter += 1

		mouse.on_click(on_click)