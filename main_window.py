import configparser
import os
from datetime import datetime

import wx.xrc
import threading
import time

from loger import LogDialog
from screen import ScreenDialog
from testing import TestingDialog
from backend import show_error_dialog, time_label, stopwatch, find_element, find_x, f_click, \
	open_folder, check_screenshot_match, save_or_clear_screenshot, save_screenshot


class BotFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CLIP_CHILDREN )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.Size( -1,-1 ) )

		main_container = wx.BoxSizer( wx.HORIZONTAL )

		left_container = wx.FlexGridSizer( 0, 1, 0, 0 )
		left_container.SetFlexibleDirection( wx.BOTH )
		left_container.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		setting_values_container = wx.GridBagSizer( 0, 0 )
		setting_values_container.SetFlexibleDirection( wx.BOTH )
		setting_values_container.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		setting_values_container.SetMinSize( wx.Size( -1,300 ) )
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"- Мин. и макс. радиус контуров перекрестий (пикс.)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		setting_values_container.Add( self.m_staticText1, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"- Световой порог разграничения цвета (0 - 255)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		setting_values_container.Add( self.m_staticText2, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"- Точность поиска объектов (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		setting_values_container.Add( self.m_staticText3, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"- Задержка после начала просмотра рекламы, до начала поиска \nвыхода из неё (с.)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		setting_values_container.Add( self.m_staticText5, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"- Таймаут внештатной ситуации, промежуток между запуском рекламы \nи текущим моментом, пока реклама не закончилась, по истечении которого \nнеобходимо перезапускать приложение (с.)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		setting_values_container.Add( self.m_staticText6, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"- Время ожидания запуска приложения от иконки до загрузки (с.)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )

		setting_values_container.Add( self.m_staticText61, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText611 = wx.StaticText( self, wx.ID_ANY, u" - Временной отрезок бездействия до перехода в спящий режим (с.)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText611.Wrap( -1 )

		setting_values_container.Add( self.m_staticText611, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		contour_size = wx.GridSizer( 0, 2, 0, 0 )

		self.contour_size_min = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 1000, 0 )
		contour_size.Add( self.contour_size_min, 1, wx.ALL, 5 )

		self.contour_size_max = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 1000, 0 )
		contour_size.Add( self.contour_size_max, 1, wx.ALL, 5 )


		setting_values_container.Add( contour_size, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.precision = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 100, 0 )
		setting_values_container.Add( self.precision, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.wb_lvl = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 255, 0 )
		setting_values_container.Add( self.wb_lvl, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.ad_time = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 100000, 29 )
		setting_values_container.Add( self.ad_time, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.error_time = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 100000, 180 )
		setting_values_container.Add( self.error_time, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.reboot_time = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 100000, 0 )
		setting_values_container.Add( self.reboot_time, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.sleep_time = wx.SpinCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 100000, 0 )
		setting_values_container.Add( self.sleep_time, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.precision_image = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 100, 0 )
		setting_values_container.Add( self.precision_image, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText61111 = wx.StaticText( self, wx.ID_ANY, u"- Точность сравнения изображений для черного списка (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61111.Wrap( -1 )

		setting_values_container.Add( self.m_staticText61111, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.is_find_chest3 = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		setting_values_container.Add( self.is_find_chest3, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticText61112 = wx.StaticText( self, wx.ID_ANY, u"- Собирать крылатые сундуки", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61112.Wrap( -1 )

		setting_values_container.Add( self.m_staticText61112, wx.GBPosition( 9, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.is_use_blacklist = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		setting_values_container.Add( self.is_use_blacklist, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticText611121 = wx.StaticText( self, wx.ID_ANY, u"- Использовать черный список", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText611121.Wrap( -1 )

		setting_values_container.Add( self.m_staticText611121, wx.GBPosition( 10, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.find_close_time = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		setting_values_container.Add( self.find_close_time, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText6111211 = wx.StaticText( self, wx.ID_ANY, u"- Задержка между итерациями цикла поиска выхода", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6111211.Wrap( -1 )

		setting_values_container.Add( self.m_staticText6111211, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		left_container.Add( setting_values_container, 1, wx.SHAPED, 5 )

		self.m_staticline17 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		left_container.Add( self.m_staticline17, 0, wx.ALL|wx.EXPAND, 5 )

		button_container = wx.GridSizer( 2, 2, 0, 0 )

		self.RUN = wx.Button( self, wx.ID_ANY, u"Старт", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.RUN.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.RUN.SetBackgroundColour( wx.Colour( 82, 225, 228 ) )

		button_container.Add( self.RUN, 1, wx.ALL|wx.EXPAND, 5 )

		self.STOP = wx.Button( self, wx.ID_ANY, u"Стоп", wx.DefaultPosition, wx.Size( -1,65 ), 0 )
		self.STOP.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.STOP.SetBackgroundColour( wx.Colour( 211, 63, 58 ) )

		button_container.Add( self.STOP, 1, wx.ALL|wx.EXPAND, 5 )

		self.UPLOAD = wx.Button( self, wx.ID_ANY, u"Загрузить", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.UPLOAD.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.UPLOAD.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		button_container.Add( self.UPLOAD, 1, wx.ALL|wx.EXPAND, 5 )

		self.SAVE = wx.Button( self, wx.ID_ANY, u"Сохранить", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.SAVE.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.SAVE.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		button_container.Add( self.SAVE, 1, wx.ALL|wx.EXPAND, 5 )


		left_container.Add( button_container, 1, wx.EXPAND, 5 )


		main_container.Add( left_container, 1, wx.EXPAND, 5 )

		right_container = wx.BoxSizer( wx.VERTICAL )

		path_cat_screen_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_cat_screen = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		path_cat_screen_block.Add( self.path_cat_screen, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"Каталог скриншотов", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )

		path_cat_screen_block.Add( self.m_staticText26, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_cat_screen_block, 1, wx.EXPAND, 0 )

		self.m_staticline162 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		right_container.Add( self.m_staticline162, 0, wx.EXPAND |wx.ALL, 5 )

		path_chest_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_chest = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_chest_block.Add( self.path_chest, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"Золотой сундук", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		path_chest_block.Add( self.m_staticText27, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_chest_block, 1, wx.EXPAND, 0 )

		path_tree_chest_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_tree_chest = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_tree_chest_block.Add( self.path_tree_chest, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText271 = wx.StaticText( self, wx.ID_ANY, u"Деревянный сундук", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText271.Wrap( -1 )

		path_tree_chest_block.Add( self.m_staticText271, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_tree_chest_block, 1, wx.EXPAND, 0 )

		path_chest3_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_chest3 = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_chest3_block.Add( self.path_chest3, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText2711 = wx.StaticText( self, wx.ID_ANY, u"Крылатый сундук с золотом", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText2711.Wrap( -1 )

		path_chest3_block.Add( self.m_staticText2711, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_chest3_block, 1, wx.EXPAND, 5 )

		self.m_staticline163 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		right_container.Add( self.m_staticline163, 0, wx.EXPAND |wx.ALL, 5 )

		path_check_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_check = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_check_block.Add( self.path_check, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText272 = wx.StaticText( self, wx.ID_ANY, u"МЕНЮ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText272.Wrap( -1 )

		path_check_block.Add( self.m_staticText272, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_check_block, 1, wx.EXPAND, 0 )

		path_end_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_end = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_end_block.Add( self.path_end, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText273 = wx.StaticText( self, wx.ID_ANY, u"ПОЛУЧИТЬ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText273.Wrap( -1 )

		path_end_block.Add( self.m_staticText273, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_end_block, 1, wx.EXPAND, 0 )

		path_center_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_center = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_center_block.Add( self.path_center, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText2732 = wx.StaticText( self, wx.ID_ANY, u"Центр ГО", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2732.Wrap( -1 )

		path_center_block.Add( self.m_staticText2732, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_center_block, 1, wx.EXPAND, 5 )

		path_center_block1 = wx.BoxSizer( wx.HORIZONTAL )

		self.path_play = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_center_block1.Add( self.path_play, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText27321 = wx.StaticText( self, wx.ID_ANY, u"PLAY", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27321.Wrap( -1 )

		path_center_block1.Add( self.m_staticText27321, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_center_block1, 1, wx.EXPAND, 5 )

		self.m_staticline16 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		right_container.Add( self.m_staticline16, 0, wx.EXPAND |wx.ALL, 5 )

		dialogs_block = wx.GridSizer( 0, 3, 0, 0 )

		self.cat_screen_button = wx.Button( self, wx.ID_ANY, u"Каталог скриншотов", wx.DefaultPosition, wx.DefaultSize, 0 )
		dialogs_block.Add( self.cat_screen_button, 0, wx.ALL|wx.EXPAND, 5 )

		self.screen_dialog_button = wx.Button( self, wx.ID_ANY, u"Конфигурация экрана", wx.DefaultPosition, wx.DefaultSize, 0 )
		dialogs_block.Add( self.screen_dialog_button, 0, wx.ALL|wx.EXPAND, 5 )

		self.testing_dialog_button = wx.Button( self, wx.ID_ANY, u"Помощник настройки\nкомпьютерного зрения", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
		dialogs_block.Add( self.testing_dialog_button, 0, wx.ALL|wx.EXPAND, 5 )


		right_container.Add( dialogs_block, 1, wx.EXPAND, 0 )


		main_container.Add( right_container, 1, wx.EXPAND, 5 )


		self.SetSizer( main_container )
		self.Layout()
		main_container.Fit( self )
		self.menubar = wx.MenuBar( 0 )
		self.menu = wx.Menu()
		self.reset_screen_setting = wx.MenuItem( self.menu, wx.ID_ANY, u"Сбросить конфигурацию экрана"+ u"\t" + u"ctrl+x", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu.Append( self.reset_screen_setting )

		self.default_settings = wx.MenuItem( self.menu, wx.ID_ANY, u"Сбросить параметры"+ u"\t" + u"ctrl+d", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu.Append( self.default_settings )

		self.OpenLog = wx.MenuItem( self.menu, wx.ID_ANY, u"ЛОГ"+ u"\t" + u"f1", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu.Append( self.OpenLog )

		self.menubar.Append( self.menu, u"Меню" )

		self.SetMenuBar( self.menubar )

		self.statusbar = self.CreateStatusBar( 2, 0, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.RUN.Bind( wx.EVT_BUTTON, self.RUN_handler )
		self.STOP.Bind( wx.EVT_BUTTON, self.STOP_handler )
		self.UPLOAD.Bind( wx.EVT_BUTTON, self.UPLOAD_handler )
		self.SAVE.Bind( wx.EVT_BUTTON, self.SAVE_handler )
		self.cat_screen_button.Bind( wx.EVT_BUTTON, self.Open_cat_screen )
		self.screen_dialog_button.Bind( wx.EVT_BUTTON, self.OpenScreenDialog )
		self.testing_dialog_button.Bind( wx.EVT_BUTTON, self.OpenTestingDialog )
		self.Bind( wx.EVT_MENU, self.Reset_SS, id = self.reset_screen_setting.GetId() )
		self.Bind( wx.EVT_MENU, self.Set_default_settings, id = self.default_settings.GetId() )
		self.Bind( wx.EVT_MENU, self.Open_LogFrame, id = self.OpenLog.GetId() )



		self.testing_d = TestingDialog(parent=self)
		self.screen_d = ScreenDialog(parent=self)
		self.loger = LogDialog(parent=self)

		self.running = False  # Флаг для проверки, выполняется ли цикл
		self.STOP.Enable(False)  # Кнопка будет неактивной до запуска цикла
		self.operation_in_progress = False
		self.statusbar.SetStatusText("")
		self.loger.LOG.SetValue("")

		# На старте счетчики должны быть нулевыми
		self.count_chest = 0
		self.count_tree_chest = 0
		self.count_chest3 = 0

		self.settings = \
			"sz_x0,si;sz_y0,si;sz_x1,si;sz_y1,si;ctz_x0,si;ctz_y0,si;ctz_x1,si;ctz_y1,si;ct3z_x0,si;" \
			"ct3z_y0,si;ct3z_x1,si;ct3z_y1,si;pz_x0,si;pz_y0,si;pz_x1,si;pz_y1,si;ez_x0,si;ez_y0,si;" \
			"ez_x1,si;ez_y1,si;ckz_x0,si;ckz_y0,si;ckz_x1,si;ckz_y1,si;iz_x,si;iz_y,si;b_x,si;b_y,si;" \
			"a_x,si;a_y,si;c_x,si;c_y,si;" + \
			\
			"contour_size_max,i;contour_size_min,i;precision,i;wb_lvl,i;ad_time,i;error_time,i;reboot_time,i;" \
			"sleep_time,i;find_close_time,i;precision_image,i;" + \
			\
			"path_cat_screen,s;path_chest,s;path_chest3,s;path_tree_chest,s;path_check,s;path_end,s;path_center,s;" \
			"path_play,s;" + \
			\
			"is_find_chest3,b;is_use_blacklist,b"

		self.zones = "end,ez;play,pz;menu,ckz;chest,ctz;chest3,ct3z;screen,sz;exit,find_zones"
		self.screen_zone = None
		self.chest3_zone = None
		self.play_zone = None
		self.chest_zone = None
		self.menu_zone = None
		self.end_zone = None
		self.exit_zones = []

		self.Try_upload_config_default()

	def __del__( self ):
		pass

	def OpenScreenDialog( self, event ):
		self.screen_d.ShowModal()

	def OpenTestingDialog( self, event ):
		self.testing_d.ShowModal()

	def Open_LogFrame(self, event):
		self.loger.ShowModal()

	def Try_upload_config_default(self):
		if os.path.isfile("./default_settings.ini"):
			self.upload_settings(True)


	def infinite_loop(self, event):
		# Соберем текущие установки программы
		ad_time = self.ad_time.GetValue()
		screen_path = self.path_cat_screen.GetPath()

		# Начинаем с того что сундук мы еще не нашли, а выход из рекламы как будто бы нашли
		_found_chest = False
		_found_close = True
		self.found_chest3 = False
		self.found_boost = False

		# Чистим буфер черного списка, чтобы не засорять мусором ЧС
		if os.path.exists(screen_path + '/TEMP/screenshot_0.png'):
			os.remove(screen_path + '/TEMP/screenshot_0.png')


		self.set_status("Запуск...")
		# Запускаем бесконечный цикл
		while self.running:

			# Ищем главное окно, если не находим пытаемся найти выход и получить награду
			# Если находим ГО, то переходим к поиску сундуков,
			# Если же не находим, а время цикла поиска истекло,
			# то сначала делаем скриншот проблемной области,
			# после чего перезапускаем приложение и начинаем всё сначала

			if self.Find_Close_loop():
				# Варианты попадания сюда:
				# 1) Вышли в ГО (старт, перезагрузка, окончание рекламы)

				# Разберемся с прошлым найденным (или не найденным сундуком), добавим рекламу в ЧС либо очистим буфер
				# От альтернативных попаданий в цикл (отсутствия файла) функция защищена.
				result_clear = save_or_clear_screenshot(_found_close, screen_path, *self.screen_zone, ad_time=ad_time)
				if result_clear != "":
					self.set_status(result_clear)

				# Считаем найденным сундук, если find_chest его нашел и был найден выход (в отличие от первой итерации)
				self.count_chest += 1 if _found_close and _found_chest and not self.found_chest3 and not self.found_boost else 0

				# Признаки нахождение крылатого сундука идентичны обычному золотому,
				# Поэтому, чтобы разделить счетчики, добавим разделяющий флаг
				self.count_chest3 += 1 if _found_close and _found_chest and self.found_chest3 and not self.found_boost else 0
				self.found_chest3 = False
				self.found_boost = False


				# Обновляем метку, что выход найден
				_found_close = True

				# Гоняем цикл поиска сундуков, от засыпания он защищен и прекратится только если не сможет работать
				# после засыпания в течение 10 секунд. В этом случае мы выполняем перезагрузку и возвращаемся к началу
				# главного цикла
				_found_chest = self.Find_Chests_loop()
				if not _found_chest:
					# Плохой выход может быть в следующих случаях:
					# 1) Стоп-сигнал
					# 2) ЧС-ная реклама
					# 3) Ошибка выхода из сна
					# если - №1 то идем на следующую итерацию, что - то же самое, что остановка цикла.

					# В 1-ом варианте перезапуск не нужен, но функция от него защищена
					self.Reboot(event)
			else:
				# Если не смогли найти выход, то запоминаем это и идем на перезагрузку
				# после перезагрузки и начала новой итерации по флагу определим что изображение из буфера надо сохранить
				# Если стоп-сигнал, то на следующую итерацию мы не пойдем, изображение так и останется в буфере
				# Поэтому мы чистим буфер перед запуском бота
				_found_close = False

				# Варианты попадания сюда:
				# 1) Стоп-сигнал
				# 2) Превышение времени поиска выхода

				# В 1-ом варианте перезапуск не нужен, но функция от него защищена
				self.Reboot(event)

		self.set_status("Бот остановлен!")



	def Find_Close_loop(self):
		menu_path = self.path_check.GetPath()
		end_path = self.path_end.GetPath()
		x_rad_min = self.contour_size_min.GetValue()
		x_rad_max = self.contour_size_max.GetValue()
		error_time = self.error_time.GetValue()
		wb_lvl = self.wb_lvl.GetValue()
		precision = self.precision.GetValue() / 100
		screen_path = self.path_cat_screen.GetPath()
		center_path = self.path_center.GetPath()
		is_use_blacklist = self.is_use_blacklist.GetValue()
		find_close_time = self.find_close_time.GetValue()

		self.set_status("Поиск выхода...")

		_now = time_label()
		while stopwatch(_now) < error_time and self.running:
			time.sleep(find_close_time)

			# Проверим на главный экран
			if find_element(menu_path, *self.menu_zone, precision=precision, click=False):
				self.set_status(" Успех!", type=1)
				return True

			# Если по ошибке нажали на выход после попадания в главное окно, жмем "назад"
			if find_element(center_path, *self.screen_zone, precision=precision, click=False):
				f_click(self.screen_d.ckz_x0.GetValue(),self.screen_d.ckz_y0.GetValue())
				time.sleep(1)
				continue

			# Ищем сбор награды при необходимости
			find_element(end_path, *self.end_zone, precision=precision, click=True)

			# Если мы не в главном экране, то ищем выход, next, или жмем "назад" (если включена опция)
			# Либо реклама могла закончиться сама и тогда ищем кнопку получения награды
			if not self.check_zones(self.exit_zones, x_rad_min, x_rad_max, wb_lvl):
				return False

		# Сохраним проблемный экран для последующего анализа возникавших ошибок
		if stopwatch(_now) >= error_time:
			if is_use_blacklist:
				_screen_error = save_screenshot("ERROR_SCREEN", screen_path, *self.screen_zone)
				self.set_status("Выход не обнаружен! Сохранение проблемного экрана: " + _screen_error, type=1)
			else:
				self.set_status("Выход не обнаружен!", type=1)

		return False

	def check_zones(self, exit_zones, x_rad_min, x_rad_max, wb_lvl):
		for exit_zone in exit_zones:
			for r in range(x_rad_min, x_rad_max, 1):
				if not self.running:
					return False
				if find_x(*exit_zone, radius=r, wb_lvl=wb_lvl):
					return True
		return True


	# Цикл должен быть по сути бесконечный, но если долго не будет сундуков, то приложение заснёт, поэтому периодически
	# требуется проверять заново что мы в главном экране и если это не так, то жмем "назад" пока не выйдем в главное меню для продолжения работы,
	# либо уходим в перезагрузку если "назад" не помогает.
	def Find_Chests_loop(self):
		menu_path = self.path_check.GetPath()
		precision = self.precision.GetValue() / 100
		sleep_time = self.sleep_time.GetValue()
		chest_path = self.path_chest.GetPath()
		ad_time = self.ad_time.GetValue()
		tree_chest_path = self.path_tree_chest.GetPath()
		screen_path = self.path_cat_screen.GetPath()
		play_path = self.path_play.GetPath()
		precision_image = self.precision_image.GetValue() / 100
		chest3_path = self.path_chest3.GetPath()
		is_find_chest3 = self.is_find_chest3.GetValue()
		is_use_blacklist = self.is_use_blacklist.GetValue()

		self.update_state()
		self.set_status("Поиск сундуков...")

		# !!! ИЩЕМ !!!
		_start_find_chests = _now = time_label()
		_found = False

		while not _found:
			# Это самый долгий цикл в процессе работы и надо постоянно проверять не было ли стоп-сигнала
			if not self.running:
				return False

			# Если время таймаута сна истекло, проверим не ушли ли мы с экрана, если да - то идем на перезагрузку
			# даже если ещё работаем, будем проверять отныне на постоянной основе, пока не уснём или не найдем сундук,
			# чтобы обнулить таймер
			if stopwatch(_now) >= sleep_time:
				if not find_element(menu_path, *self.menu_zone, precision=precision, click=False):
					self.set_status("Приложение уснуло, перенаправление на перезагрузку!...")
					return False

			# Ищем золотой сундук, если находим то кликаем Play, засыпаем на заданный отрезок времени и после завершаем функцию
			if find_element(chest_path, *self.chest_zone, precision=precision, click=True):
				if stopwatch(_now) > 3 or _start_find_chests < 3.1:
					# Индикация аналогична предыдущей, только значение отображаем как +1 на опережение
					# т.е. на ЧС мы увидим 1 найденный сундук, но и на следующем мы увидим 1
					self.set_status("\tЗолотой сундук +1 (" + str(self.count_chest + 1) + ")")
				# Нашли золото, нажали - подождали секунду - начинаем искать запуск рекламы
				_now = time_label()
				time.sleep(1.5)
				_found = find_element(play_path, *self.play_zone, precision=precision, click=True)
				time.sleep(3)


			if find_element(tree_chest_path, *self.chest_zone, precision=precision, click=True):
				if stopwatch(_now) > 3 or _start_find_chests < 3.1:
					self.count_tree_chest += 1
					self.set_status("\tДеревянный сундук +1 (" + str(self.count_tree_chest) + ")" )
				_now = time_label()
				self.update_state()

			# Копируем функцию поиска золотого сундука с поправкой, что это опционально
			if is_find_chest3:
				if find_element(chest3_path, *self.chest3_zone, precision=precision, click=True):
					if stopwatch(_now) > 3 or _start_find_chests < 3.1:
						# Индикация аналогична предыдущей, только значение отображаем как +1 на опережение
						# т.е. на ЧС мы увидим 1 найденный сундук, но и на следующем мы увидим 1
						self.set_status("\tКрылатый сундук +1 (" + str(self.count_chest3 + 1) + ")")
						self.found_chest3 = True
					# Нашли золото, нажали - подождали секунду - начинаем искать запуск рекламы
					_now = time_label()
					time.sleep(1.5)
					_found = find_element(play_path, *self.play_zone, precision=precision, click=True)
					time.sleep(3)


		# Если дошли до сюда - значит нашли золото, в любом другом случае - ушли бы к перезагрузке
		# Пока индикатор воспроизведения не исчезнет продолжаем кликать по нему
		while _found:
			_found = find_element(play_path, *self.play_zone, precision=precision, click=True)
			time.sleep(3)

		# !!! НАШЛИ ЗОЛОТО !!!
		self.set_status("Просмотр рекламы...")
		time.sleep(ad_time)
		if is_use_blacklist:
			self.set_status("Проверка черного списка...")
			# Чтобы не переходить к поиску выхода в безнадежной ситуации, если мы знаем что эта реклама - дерьмо,
			# сразу сверимся с "черным списком" рекламы и в случае чего отправимся сразу на перезагрузку.
			if check_screenshot_match(screen_path, precision_image, *self.screen_zone, ad_time=ad_time):
				self.set_status("!!! Обнаружено исключение. Перенаправление на перезапуск !!!...")
				return False
		return True



	def Reboot(self, event):
		bx = self.screen_d.b_x.GetValue()
		by = self.screen_d.b_y.GetValue()
		precision = self.precision.GetValue() / 100
		ax = self.screen_d.a_x.GetValue()
		ay = self.screen_d.a_y.GetValue()
		cx = self.screen_d.c_x.GetValue()
		cy = self.screen_d.c_y.GetValue()
		ix = self.screen_d.iz_x.GetValue()
		iy = self.screen_d.iz_y.GetValue()
		reboot_time = self.reboot_time.GetValue()
		center_path = self.path_center.GetPath()

		if not self.running:
			self.STOP_handler(event)
			return

		self.set_status("Перезапуск приложения...")
		f_click(ax, ay)
		time.sleep(3)
		f_click(cx, cy)
		time.sleep(4)
		f_click(ix, iy)
		time.sleep(reboot_time)

		# Пока не найдем метку главного экрана или не вышло время попыток - жмем "назад"
		# если так и не нашли - значит перезагрузка сработала криво, триггерим ошибку
		self.set_status("Поиск рабочей области...")
		_now = time_label()
		_found_main_screen = find_element(center_path, *self.screen_zone, precision=precision, click=False)
		while not _found_main_screen \
				and stopwatch(_now) < 10 \
				and self.running:
			f_click(bx, by)
			time.sleep(1)
			_found_main_screen = find_element(center_path, *self.screen_zone, precision=precision, click=False)

		# Выйти из предыдущего цикла можем в 3 случаях:
		# 1) Стоп-сигнал
		# 2) Превышено время поиска ГО (неудачный перезапуск)
		# 3) Вышли в ГО ( хорошая концовка )

		# Вариант №2
		if not _found_main_screen and self.running:
			self.set_status("Ошибка перезапуска...")
			if self.running:
				self.STOP_handler(event)
			show_error_dialog("Не удалось выйти в главное окно! Цикл остановлен!")




	def RUN_handler( self, event ):
		self.running = True
		self.STOP.Enable(True)
		self.RUN.Disable()
		self.set_zones()
		threading.Thread(target=self.infinite_loop, args={event}).start()

	def STOP_handler( self, event ):
		self.running = False
		self.STOP.Disable()  # Деактивация кнопки "Остановить цикл"
		self.RUN.Enable()  # Активация кнопки "Запустить цикл"

	def UPLOAD_handler(self, event):
		self.Reset_SS(event)
		self.Set_default_settings(event)
		self.upload_settings(False)

	def SAVE_handler(self, event):
		# Отображение диалогового окна для выбора файла конфигурации
		dialog = wx.FileDialog(self, "Выберите файл конфигурации", "/", "default_settings.ini", "Конфигурационные файлы (*.ini)|*.ini",
							   wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dialog.ShowModal() == wx.ID_OK:
			config_file = dialog.GetPath()
			config = configparser.ConfigParser()
			config.add_section("Settings")

			# Сохранение настроек в файл конфигурации
			config.set("Settings", "exit_zone", self.Zip_exit_zone())

			for s in self.settings.split(";"):
				key = s.partition(",")[2]
				val = s.partition(",")[0]

				match key:
					case "si":
						config.set("Settings", val, str(getattr(self.screen_d, val).GetValue()))
					case "i":
						config.set("Settings", val, str(getattr(self, val).GetValue()))
					case "s":
						config.set("Settings", val, getattr(self, val).GetPath())
					case "b":
						config.set("Settings", val, "1" if getattr(self, val).GetValue() else "0")

			with open(config_file, "w") as file:
				config.write(file)

		dialog.Destroy()



	def upload_settings(self, _ds):
		config = configparser.ConfigParser()
		config_file = ""

		if not _ds:
			dialog = wx.FileDialog(self, "Выберите файл конфигурации", "/", "default_settings.ini", "Конфигурационные файлы (*.ini)|*.ini",
								   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
			if dialog.ShowModal() == wx.ID_OK:
				config_file = dialog.GetPath()
				dialog.Destroy()
		else:
			config_file = "./default_settings.ini"

		if config_file != "":
			config.read(config_file)
			# Восстановление настроек из файла конфигурации
			if config.has_option('Settings', 'exit_zone'):
				self.Unpack_exit_zone(config.get("Settings", "exit_zone"))

			for s in self.settings.split(";"):
				key = s.partition(",")[2]
				val = s.partition(",")[0]

				match key:
					case "si":
						if config.has_option('Settings', val):
							getattr(self.screen_d, val).SetValue(config.getint("Settings", val))
					case "i":
						if config.has_option('Settings', val):
							getattr(self, val).SetValue(config.getint("Settings", val))
					case "s":
						if config.has_option('Settings', val):
							getattr(self, val).SetPath(config.get("Settings", val))
					case "b":
						if config.has_option('Settings', val):
							getattr(self, val).SetValue(True if config.getint("Settings", val) == 1 else False)

	def Zip_exit_zone(self):
		_res = ""
		for row in range(self.screen_d.find_zones.GetNumberRows()):
			x0 = int(self.screen_d.find_zones.GetCellValue(row, 0))
			y0 = int(self.screen_d.find_zones.GetCellValue(row, 1))
			x1 = int(self.screen_d.find_zones.GetCellValue(row, 2))
			y1 = int(self.screen_d.find_zones.GetCellValue(row, 3))
			if _res != "":
				_res += ";"
			_res += str(x0)+","+str(y0)+","+str(x1)+","+str(y1)
		return _res

	def Unpack_exit_zone(self, _str):
		if _str != "":
			zones = _str.split(";")
			for z in zones:
				coord = z.split(",")
				row_count = self.screen_d.find_zones.GetNumberRows()
				self.screen_d.find_zones.AppendRows(1)
				self.screen_d.find_zones.SetCellValue(row_count, 0, coord[0])
				self.screen_d.find_zones.SetCellValue(row_count, 1, coord[1])
				self.screen_d.find_zones.SetCellValue(row_count, 2, coord[2])
				self.screen_d.find_zones.SetCellValue(row_count, 3, coord[3])

	def Open_cat_screen( self, event ):
		open_folder(self.path_cat_screen.GetPath())

	def set_zones(self):
		for s in self.zones.split(";"):
			key = s.partition(",")[2]
			val = s.partition(",")[0]
			if val == "exit":
				setattr(self, val+"_zones", [])
				for row in range(getattr(self.screen_d, key).GetNumberRows()):
					x0 = int(getattr(self.screen_d, key).GetCellValue(row, 0))
					y0 = int(getattr(self.screen_d, key).GetCellValue(row, 1))
					x1 = int(getattr(self.screen_d, key).GetCellValue(row, 2))
					y1 = int(getattr(self.screen_d, key).GetCellValue(row, 3))
					getattr(self, val+"_zones").append((x0, y0, x1, y1))
			else:
				x0 = getattr(self.screen_d, key+"_x0").GetValue()
				y0 = getattr(self.screen_d, key+"_y0").GetValue()
				x1 = getattr(self.screen_d, key+"_x1").GetValue()
				y1 = getattr(self.screen_d, key+"_y1").GetValue()
				setattr(self, val + "_zone", (x0, y0, x1, y1))


	def Reset_SS(self, event):
		self.screen_d.clear_exit_zone_f()
		for s in self.settings.split(";"):
			key = s.partition(",")[2]
			val = s.partition(",")[0]
			if key == "si":
				getattr(self.screen_d, val).SetValue(0)


	def Set_default_settings(self, event):
		for s in self.settings.split(";"):
			key = s.partition(",")[2]
			val = s.partition(",")[0]
			match key:
				case "i":
					getattr(self, val).SetValue(0)
				case "s":
					getattr(self, val).SetPath("")
				case "b":
					getattr(self, val).SetValue(False)

	def set_status(self, message, type=0):
		if type == 0:
			self.statusbar.SetStatusText(message, 1)
		if type == 1:
			b = self.statusbar.GetStatusText(1)
			self.statusbar.SetStatusText(b + message, 1)
		if type == 2:
			self.statusbar.SetStatusText(message, 0)

		if (type != 2):
			_end = "\n" if type == 0 else " "
			_time = datetime.now().strftime("%H:%M:%S")  + " -: " if type == 0 else ""
			self.loger.LOG.SetValue(self.loger.LOG.GetValue() + _end  + _time +  message )

	def update_state(self):
		self.set_status(
			"з:" + str(self.count_chest) + " д:" + str(self.count_tree_chest) + " к:" + str(self.count_chest3), type=2
		)
