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
	open_folder, check_screenshot_match, save_or_clear_screenshot


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

		self.m_staticText6111 = wx.StaticText( self, wx.ID_ANY, u"- Выполнять нажатие кнопки \"назад\" при попытке \nпоиска выхода из рекламы", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6111.Wrap( -1 )

		setting_values_container.Add( self.m_staticText6111, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

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

		self.is_click_back = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		setting_values_container.Add( self.is_click_back, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.precision_image = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 100, 0 )
		setting_values_container.Add( self.precision_image, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText61111 = wx.StaticText( self, wx.ID_ANY, u"- Точность сравнения изображений для черного списка (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61111.Wrap( -1 )

		setting_values_container.Add( self.m_staticText61111, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


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

		path_check_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_check = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_check_block.Add( self.path_check, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText272 = wx.StaticText( self, wx.ID_ANY, u"Кнопка меню", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText272.Wrap( -1 )

		path_check_block.Add( self.m_staticText272, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_check_block, 1, wx.EXPAND, 0 )

		path_end_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_end = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_end_block.Add( self.path_end, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText273 = wx.StaticText( self, wx.ID_ANY, u"Получение награды", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText273.Wrap( -1 )

		path_end_block.Add( self.m_staticText273, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_end_block, 1, wx.EXPAND, 0 )

		path_center_block = wx.BoxSizer( wx.HORIZONTAL )

		self.path_center = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_center_block.Add( self.path_center, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText2732 = wx.StaticText( self, wx.ID_ANY, u"Проверка на модальные окна \nпри запуске", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2732.Wrap( -1 )

		path_center_block.Add( self.m_staticText2732, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		right_container.Add( path_center_block, 1, wx.EXPAND, 5 )

		path_center_block1 = wx.BoxSizer( wx.HORIZONTAL )

		self.path_play = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		path_center_block1.Add( self.path_play, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText27321 = wx.StaticText( self, wx.ID_ANY, u"Запуск рекламы", wx.DefaultPosition, wx.DefaultSize, 0 )
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
		self.count_chest = 0

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
		menu_path = self.path_check.GetPath()
		end_path = self.path_end.GetPath()
		end_zone = self.get_end_zone()
		menu_zone = self.get_menu_zone()
		x_rad_min = self.contour_size_min.GetValue()
		x_rad_max = self.contour_size_max.GetValue()
		error_time = self.error_time.GetValue()
		exit_zones = self.get_exit_zones()
		wb_lvl = self.wb_lvl.GetValue()
		bx = self.screen_d.b_x.GetValue()
		by = self.screen_d.b_y.GetValue()
		precision = self.precision.GetValue() / 100
		sleep_time = self.sleep_time.GetValue()
		chest_path = self.path_chest.GetPath()
		chest_zone = self.get_chest_zone()
		ad_time = self.ad_time.GetValue()
		tree_chest_path = self.path_tree_chest.GetPath()
		ax = self.screen_d.a_x.GetValue()
		ay = self.screen_d.a_y.GetValue()
		cx = self.screen_d.c_x.GetValue()
		cy = self.screen_d.c_y.GetValue()
		ix = self.screen_d.iz_x.GetValue()
		iy = self.screen_d.iz_y.GetValue()
		reboot_time = self.reboot_time.GetValue()
		screen_path = self.path_cat_screen.GetPath()
		center_zone = screen_zone = self.get_screen_zone()
		center_path = self.path_center.GetPath()
		click_back = self.is_click_back.GetValue()
		play_path = self.path_play.GetPath()
		play_zone =self.get_play_zone()
		precision_image = self.precision_image.GetValue() / 100

		# Начинаем с того что сундук мы еще не нашли, а выход из рекламы как будто бы нашли
		_found_chest = False
		_found_close = True

		# Чистим буфер черного списка, чтобы не засорять мусором ЧС
		if os.path.exists(screen_path + '/TEMP/screenshot.png'):
			os.remove(screen_path + '/TEMP/screenshot.png')


		self.set_status("Запуск...")
		# Запускаем бесконечный цикл
		while self.running:

			# Ищем главное окно, если не находим пытаемся найти выход и получить награду
			# Если находим ГО, то переходим к поиску сундуков,
			# Если же не находим, а время цикла поиска истекло,
			# то сначала делаем скриншот проблемной области,
			# после чего перезапускаем приложение и начинаем всё сначала

			if self.Find_Close_loop(
				menu_path=menu_path, end_path=end_path, end_zone=end_zone, menu_zone=menu_zone,
				x_rad_min=x_rad_min, x_rad_max=x_rad_max, error_time=error_time, exit_zones=exit_zones, wb_lvl=wb_lvl, bx=bx, by=by,
				precision=precision, click_back=click_back
			):
				# Варианты попадания сюда:
				# 1) Вышли в ГО (старт, перезагрузка, окончание рекламы)

				# Разберемся с прошлым найденным (или не найденным сундуком), добавим рекламу в ЧС либо очистим буфер
				# От альтернативных попаданий в цикл (отсутствия файла) функция защищена.
				result_clear = save_or_clear_screenshot(_found_close, screen_path, *screen_zone)
				if result_clear != "":
					self.set_status(result_clear)

				# Обновляем метку, что выход найден
				_found_close = True

				# Гоняем цикл поиска сундуков, от засыпания он защищен и прекратится только если не сможет работать
				# после засыпания в течение 10 секунд. В этом случае мы выполняем перезагрузку и возвращаемся к началу
				# главного цикла
				_found_chest = self.Find_Chests_loop(
					sleep_time=sleep_time, chest_path=chest_path, chest_zone=chest_zone, precision=precision,
					ad_time=ad_time, menu_path=menu_path, menu_zone=menu_zone, tree_chest_path=tree_chest_path,
					play_path=play_path, play_zone=play_zone, screen_path=screen_path, screen_zone=screen_zone,
					precision_image=precision_image
				)
				if not _found_chest:
					# Плохой выход может быть в следующих случаях:
					# 1) Стоп-сигнал
					# 2) ЧС-ная реклама
					# 3) Ошибка выхода из сна
					# если - №1 то идем на следующую итерацию, что - то же самое, что остановка цикла.

					# В 1-ом варианте перезапуск не нужен, но функция от него защищена
					self.Reboot(
						ax=ax, ay=ay, cx=cx, cy=cy, ix=ix, iy=iy, bx=bx, by=by,
						reboot_time=reboot_time, path_center=center_path,
						center_zone=center_zone, precision=precision, event=event
					)
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
				self.Reboot(
					ax=ax, ay=ay, cx=cx, cy=cy, ix=ix, iy=iy, bx=bx, by=by,
					reboot_time=reboot_time, path_center=center_path,
					center_zone=center_zone, precision=precision, event=event
				)

		self.set_status("Бот остановлен!")



	def Find_Close_loop(self, menu_path, end_path, end_zone, menu_zone, x_rad_min, x_rad_max, error_time, exit_zones, wb_lvl, bx, by,
						precision, click_back):
		self.set_status("Поиск выхода...")

		_now = time_label()
		while stopwatch(_now) < error_time and self.running:
			# Проверим на главный экран
			if find_element(menu_path, *menu_zone, precision=precision, click=False):
				return True

			time.sleep(2)

			# Если мы не в главном экране, то ищем выход, next, или жмем "назад" (если включена опция)
			# Либо реклама могла закончиться сама и тогда ищем кнопку получения награды
			for exit_zone in exit_zones:
				for r in range(x_rad_min, x_rad_max, 1):
					if not self.running:
						return False
					find_x(*exit_zone, radius=r, wb_lvl=wb_lvl, bx=bx, by=by, click_back=click_back)

			# Ищем сбор награды при необходимости
			find_element(end_path, *end_zone, precision=precision, click=True)

		return False



	# Цикл должен быть по сути бесконечный, но если долго не будет сундуков, то приложение заснёт, поэтому периодически
	# требуется проверять заново что мы в главном экране и если это не так, то жмем "назад" пока не выйдем в главное меню для продолжения работы,
	# либо уходим в перезагрузку если "назад" не помогает.
	def Find_Chests_loop(self, sleep_time, chest_path, chest_zone, precision, ad_time, menu_path, menu_zone,
						 tree_chest_path, play_path, play_zone, screen_zone, screen_path, precision_image):
		self.set_status("Поиск сундуков... Найдено: " + str(self.count_chest))
		self.count_chest += 1

		# !!! ИЩЕМ !!!
		_now = time_label()
		_found = False

		while not _found:
			# Это самый долгий цикл в процессе работы и надо постоянно проверять не было ли стоп-сигнала
			if not self.running:
				return False
			# Если время таймаута сна истекло, проверим не ушли ли мы с экрана, если да - то идем на перезагрузку
			# даже если ещё работаем, будем проверять отныне на постоянной основе, пока не уснём или не найдем сундук,
			# чтобы обнулить таймер
			if stopwatch(_now) >= sleep_time:
				if not find_element(menu_path, *menu_zone, precision=precision, click=False):
					return False
			# Ищем золотой сундук, если находим то кликаем Play, засыпаем на заданный отрезок времени и после завершаем функцию
			if find_element(chest_path, *chest_zone, precision=precision, click=True):
				_now = time_label()
				# Нашли золото, нажали - подождали секунду - начинаем искать запуск рекламы
				time.sleep(1)
				_found = find_element(play_path, *play_zone, precision=precision, click=True)

			if find_element(tree_chest_path, *chest_zone, precision=precision, click=True):
				_now = time_label()

		# Если дошли до сюда - значит нашли золото, в любом другом случае - ушли бы к перезагрузке

		# !!! НАШЛИ ЗОЛОТО !!!
		self.set_status("Просмотр рекламы...")
		time.sleep(ad_time)
		self.set_status("Проверка черного списка...")
		# Чтобы не переходить к поиску выхода в безнадежной ситуации, если мы знаем что эта реклама - дерьмо,
		# сразу сверимся с "черным списком" рекламы и в случае чего отправимся сразу на перезагрузку.
		if check_screenshot_match(screen_path, precision_image, *screen_zone):
			return False
		return True



	def Reboot(self, event, ax, ay, cx, cy, ix, iy, reboot_time, path_center, center_zone, precision, bx, by):
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
		_found_main_screen = find_element(path_center, *center_zone, precision=precision, click=False)
		while not _found_main_screen \
				and stopwatch(_now) < 10 \
				and self.running:
			f_click(bx, by)
			time.sleep(1)
			_found_main_screen = find_element(path_center, *center_zone, precision=precision, click=False)

		# Выйти из предыдущего цикла можем в 3 случаях:
		# 1) Стоп-сигнал
		# 2) Превышено время поиска ГО (неудачный перезапуск)
		# 3) Вышли в ГО ( хорошая концовка )

		# Вариант №2
		self.set_status("Ошибка перезапуска...")
		if not _found_main_screen and self.running:
			if self.running:
				self.STOP_handler(event)
			show_error_dialog("Не удалось выйти в главное окно! Цикл остановлен!")




	def RUN_handler( self, event ):
		self.running = True
		self.STOP.Enable(True)
		self.RUN.Disable()
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
		dialog = wx.FileDialog(self, "Выберите файл конфигурации", "", "", "Конфигурационные файлы (*.ini)|*.ini",
							   wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dialog.ShowModal() == wx.ID_OK:
			config_file = dialog.GetPath()
			config = configparser.ConfigParser()
			config.add_section("Settings")

			# Сохранение настроек в файл конфигурации
			config.set("Settings", "exit_zone", self.Zip_exit_zone())

			config.set("Settings", "sz_x0", str(self.screen_d.sz_x0.GetValue()))
			config.set("Settings", "sz_y0", str(self.screen_d.sz_y0.GetValue()))
			config.set("Settings", "sz_x1", str(self.screen_d.sz_x1.GetValue()))
			config.set("Settings", "sz_y1", str(self.screen_d.sz_y1.GetValue()))

			config.set("Settings", "ctz_x0", str(self.screen_d.ctz_x0.GetValue()))
			config.set("Settings", "ctz_y0", str(self.screen_d.ctz_y0.GetValue()))
			config.set("Settings", "ctz_x1", str(self.screen_d.ctz_x1.GetValue()))
			config.set("Settings", "ctz_y1", str(self.screen_d.ctz_y1.GetValue()))

			config.set("Settings", "pz_x0", str(self.screen_d.pz_x0.GetValue()))
			config.set("Settings", "pz_y0", str(self.screen_d.pz_y0.GetValue()))
			config.set("Settings", "pz_x1", str(self.screen_d.pz_x1.GetValue()))
			config.set("Settings", "pz_y1", str(self.screen_d.pz_y1.GetValue()))

			config.set("Settings", "ez_x0", str(self.screen_d.ez_x0.GetValue()))
			config.set("Settings", "ez_y0", str(self.screen_d.ez_y0.GetValue()))
			config.set("Settings", "ez_x1", str(self.screen_d.ez_x1.GetValue()))
			config.set("Settings", "ez_y1", str(self.screen_d.ez_y1.GetValue()))

			config.set("Settings", "ckz_x0", str(self.screen_d.ckz_x0.GetValue()))
			config.set("Settings", "ckz_y0", str(self.screen_d.ckz_y0.GetValue()))
			config.set("Settings", "ckz_x1", str(self.screen_d.ckz_x1.GetValue()))
			config.set("Settings", "ckz_y1", str(self.screen_d.ckz_y1.GetValue()))

			config.set("Settings", "iz_x", str(self.screen_d.iz_x.GetValue()))
			config.set("Settings", "iz_y", str(self.screen_d.iz_y.GetValue()))

			config.set("Settings", "b_x", str(self.screen_d.b_x.GetValue()))
			config.set("Settings", "b_y", str(self.screen_d.b_y.GetValue()))

			config.set("Settings", "a_x", str(self.screen_d.a_x.GetValue()))
			config.set("Settings", "a_y", str(self.screen_d.a_y.GetValue()))

			config.set("Settings", "c_x", str(self.screen_d.c_x.GetValue()))
			config.set("Settings", "c_y", str(self.screen_d.c_y.GetValue()))

			config.set("Settings", "contour_size_max", str(self.contour_size_max.GetValue()))
			config.set("Settings", "contour_size_min", str(self.contour_size_min.GetValue()))
			config.set("Settings", "precision", str(self.precision.GetValue()))
			config.set("Settings", "wb_lvl", str(self.wb_lvl.GetValue()))
			config.set("Settings", "ad_time", str(self.ad_time.GetValue()))
			config.set("Settings", "error_time", str(self.error_time.GetValue()))
			config.set("Settings", "reboot_time", str(self.reboot_time.GetValue()))
			config.set("Settings", "sleep_time", str(self.sleep_time.GetValue()))
			config.set("Settings", "is_click_back", "1" if self.is_click_back.GetValue() else "0")
			config.set("Settings", "precision_image", str(self.precision_image.GetValue()))

			config.set("Settings", "path_cat_screen", self.path_cat_screen.GetPath())
			config.set("Settings", "path_chest", self.path_chest.GetPath())
			config.set("Settings", "path_tree_chest", self.path_tree_chest.GetPath())
			config.set("Settings", "path_check", self.path_check.GetPath())
			config.set("Settings", "path_end", self.path_end.GetPath())
			config.set("Settings", "path_center", self.path_center.GetPath())
			config.set("Settings", "path_play", self.path_play.GetPath())

			with open(config_file, "w") as file:
				config.write(file)

		dialog.Destroy()



	def upload_settings(self, _ds):
		config = configparser.ConfigParser()
		config_file = ""

		if not _ds:
			dialog = wx.FileDialog(self, "Выберите файл конфигурации", "", "", "Конфигурационные файлы (*.ini)|*.ini",
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

			if config.has_option('Settings', 'sz_x0'):
				self.screen_d.sz_x0.SetValue(config.getint("Settings", "sz_x0"))
			if config.has_option('Settings', 'sz_y0'):
				self.screen_d.sz_y0.SetValue(config.getint("Settings", "sz_y0"))
			if config.has_option('Settings', 'sz_x1'):
				self.screen_d.sz_x1.SetValue(config.getint("Settings", "sz_x1"))
			if config.has_option('Settings', 'sz_y1'):
				self.screen_d.sz_y1.SetValue(config.getint("Settings", "sz_y1"))

			if config.has_option('Settings', 'ctz_x0'):
				self.screen_d.ctz_x0.SetValue(config.getint("Settings", "ctz_x0"))
			if config.has_option('Settings', 'ctz_y0'):
				self.screen_d.ctz_y0.SetValue(config.getint("Settings", "ctz_y0"))
			if config.has_option('Settings', 'ctz_x1'):
				self.screen_d.ctz_x1.SetValue(config.getint("Settings", "ctz_x1"))
			if config.has_option('Settings', 'ctz_y1'):
				self.screen_d.ctz_y1.SetValue(config.getint("Settings", "ctz_y1"))

			if config.has_option('Settings', 'pz_x0'):
				self.screen_d.pz_x0.SetValue(config.getint("Settings", "pz_x0"))
			if config.has_option('Settings', 'pz_y0'):
				self.screen_d.pz_y0.SetValue(config.getint("Settings", "pz_y0"))
			if config.has_option('Settings', 'pz_x1'):
				self.screen_d.pz_x1.SetValue(config.getint("Settings", "pz_x1"))
			if config.has_option('Settings', 'pz_y1'):
				self.screen_d.pz_y1.SetValue(config.getint("Settings", "pz_y1"))

			if config.has_option('Settings', 'ez_x0'):
				self.screen_d.ez_x0.SetValue(config.getint("Settings", "ez_x0"))
			if config.has_option('Settings', 'ez_y0'):
				self.screen_d.ez_y0.SetValue(config.getint("Settings", "ez_y0"))
			if config.has_option('Settings', 'ez_x1'):
				self.screen_d.ez_x1.SetValue(config.getint("Settings", "ez_x1"))
			if config.has_option('Settings', 'ez_y1'):
				self.screen_d.ez_y1.SetValue(config.getint("Settings", "ez_y1"))

			if config.has_option('Settings', 'ckz_x0'):
				self.screen_d.ckz_x0.SetValue(config.getint("Settings", "ckz_x0"))
			if config.has_option('Settings', 'ckz_y0'):
				self.screen_d.ckz_y0.SetValue(config.getint("Settings", "ckz_y0"))
			if config.has_option('Settings', 'ckz_x1'):
				self.screen_d.ckz_x1.SetValue(config.getint("Settings", "ckz_x1"))
			if config.has_option('Settings', 'ckz_y1'):
				self.screen_d.ckz_y1.SetValue(config.getint("Settings", "ckz_y1"))

			if config.has_option('Settings', 'iz_x'):
				self.screen_d.iz_x.SetValue(config.getint("Settings", "iz_x"))
			if config.has_option('Settings', 'iz_y'):
				self.screen_d.iz_y.SetValue(config.getint("Settings", "iz_y"))

			if config.has_option('Settings', 'b_x'):
				self.screen_d.b_x.SetValue(config.getint("Settings", "b_x"))
			if config.has_option('Settings', 'b_y'):
				self.screen_d.b_y.SetValue(config.getint("Settings", "b_y"))

			if config.has_option('Settings', 'a_x'):
				self.screen_d.a_x.SetValue(config.getint("Settings", "a_x"))
			if config.has_option('Settings', 'a_y'):
				self.screen_d.a_y.SetValue(config.getint("Settings", "a_y"))

			if config.has_option('Settings', 'c_x'):
				self.screen_d.c_x.SetValue(config.getint("Settings", "c_x"))
			if config.has_option('Settings', 'c_y'):
				self.screen_d.c_y.SetValue(config.getint("Settings", "c_y"))

			if config.has_option('Settings', 'contour_size_max'):
				self.contour_size_max.SetValue(config.getint("Settings", "contour_size_max"))
			if config.has_option('Settings', 'contour_size_min'):
				self.contour_size_min.SetValue(config.getint("Settings", "contour_size_min"))
			if config.has_option('Settings', 'precision'):
				self.precision.SetValue(config.getint("Settings", "precision"))
			if config.has_option('Settings', 'wb_lvl'):
				self.wb_lvl.SetValue(config.getint("Settings", "wb_lvl"))
			if config.has_option('Settings', 'ad_time'):
				self.ad_time.SetValue(config.getint("Settings", "ad_time"))
			if config.has_option('Settings', 'error_time'):
				self.error_time.SetValue(config.getint("Settings", "error_time"))
			if config.has_option('Settings', 'reboot_time'):
				self.reboot_time.SetValue(config.getint("Settings", "reboot_time"))
			if config.has_option('Settings', 'sleep_time'):
				self.sleep_time.SetValue(config.getint("Settings", "sleep_time"))
			if config.has_option('Settings', 'precision_image'):
				self.precision_image.SetValue(config.getint("Settings", "precision_image"))
			if config.has_option('Settings', 'is_click_back'):
				self.is_click_back.SetValue(True if config.getint("Settings", "is_click_back") == 1 else False)

			if config.has_option('Settings', 'path_cat_screen'):
				self.path_cat_screen.SetPath(config.get("Settings", "path_cat_screen"))
			if config.has_option('Settings', 'path_chest'):
				self.path_chest.SetPath(config.get("Settings", "path_chest"))
			if config.has_option('Settings', 'path_tree_chest'):
				self.path_tree_chest.SetPath(config.get("Settings", "path_tree_chest"))
			if config.has_option('Settings', 'path_check'):
				self.path_check.SetPath(config.get("Settings", "path_check"))
			if config.has_option('Settings', 'path_end'):
				self.path_end.SetPath(config.get("Settings", "path_end"))
			if config.has_option('Settings', 'path_center'):
				self.path_center.SetPath(config.get("Settings", "path_center"))
			if config.has_option('Settings', 'path_play'):
				self.path_play.SetPath(config.get("Settings", "path_play"))

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




	def get_end_zone(self):
		x0 = self.screen_d.ez_x0.GetValue()
		y0 = self.screen_d.ez_y0.GetValue()
		x1 = self.screen_d.ez_x1.GetValue()
		y1 = self.screen_d.ez_y1.GetValue()
		return (x0, y0, x1, y1)

	def get_play_zone(self):
		x0 = self.screen_d.pz_x0.GetValue()
		y0 = self.screen_d.pz_y0.GetValue()
		x1 = self.screen_d.pz_x1.GetValue()
		y1 = self.screen_d.pz_y1.GetValue()
		return (x0, y0, x1, y1)

	def get_menu_zone(self):
		x0 = self.screen_d.ckz_x0.GetValue()
		y0 = self.screen_d.ckz_y0.GetValue()
		x1 = self.screen_d.ckz_x1.GetValue()
		y1 = self.screen_d.ckz_y1.GetValue()
		return (x0, y0, x1, y1)

	def get_chest_zone(self):
		x0 = self.screen_d.ctz_x0.GetValue()
		y0 = self.screen_d.ctz_y0.GetValue()
		x1 = self.screen_d.ctz_x1.GetValue()
		y1 = self.screen_d.ctz_y1.GetValue()
		return (x0, y0, x1, y1)

	def get_screen_zone(self):
		x0 = self.screen_d.sz_x0.GetValue()
		y0 = self.screen_d.sz_y0.GetValue()
		x1 = self.screen_d.sz_x1.GetValue()
		y1 = self.screen_d.sz_y1.GetValue()
		return (x0, y0, x1, y1)

	def get_exit_zones(self):
		data = []
		for row in range(self.screen_d.find_zones.GetNumberRows()):
			x0 = int(self.screen_d.find_zones.GetCellValue(row, 0))
			y0 = int(self.screen_d.find_zones.GetCellValue(row, 1))
			x1 = int(self.screen_d.find_zones.GetCellValue(row, 2))
			y1 = int(self.screen_d.find_zones.GetCellValue(row, 3))
			data.append((x0, y0, x1, y1))
		return data


	def Reset_SS(self, event):
		self.screen_d.clear_exit_zone_f()

		self.screen_d.sz_x0.SetValue(0)
		self.screen_d.sz_y0.SetValue(0)
		self.screen_d.sz_x1.SetValue(0)
		self.screen_d.sz_y1.SetValue(0)

		self.screen_d.ctz_x0.SetValue(0)
		self.screen_d.ctz_y0.SetValue(0)
		self.screen_d.ctz_x1.SetValue(0)
		self.screen_d.ctz_y1.SetValue(0)

		self.screen_d.pz_x0.SetValue(0)
		self.screen_d.pz_y0.SetValue(0)
		self.screen_d.pz_x1.SetValue(0)
		self.screen_d.pz_y1.SetValue(0)

		self.screen_d.ez_x0.SetValue(0)
		self.screen_d.ez_y0.SetValue(0)
		self.screen_d.ez_x1.SetValue(0)
		self.screen_d.ez_y1.SetValue(0)

		self.screen_d.ckz_x0.SetValue(0)
		self.screen_d.ckz_y0.SetValue(0)
		self.screen_d.ckz_x1.SetValue(0)
		self.screen_d.ckz_y1.SetValue(0)

		self.screen_d.iz_x.SetValue(0)
		self.screen_d.iz_y.SetValue(0)

		self.screen_d.b_x.SetValue(0)
		self.screen_d.b_y.SetValue(0)

		self.screen_d.a_x.SetValue(0)
		self.screen_d.a_y.SetValue(0)

		self.screen_d.c_x.SetValue(0)
		self.screen_d.c_y.SetValue(0)

	def Set_default_settings(self, event):
		self.contour_size_max.SetValue(0)
		self.contour_size_min.SetValue(0)
		self.precision.SetValue(0)
		self.wb_lvl.SetValue(0)
		self.ad_time.SetValue(0)
		self.error_time.SetValue(0)
		self.reboot_time.SetValue(0)
		self.sleep_time.SetValue(0)
		self.precision_image.SetValue(0)
		self.is_click_back.SetValue(False)

		self.path_cat_screen.SetPath("")
		self.path_chest.SetPath("")
		self.path_tree_chest.SetPath("")
		self.path_check.SetPath("")
		self.path_end.SetPath("")
		self.path_center.SetPath("")
		self.path_play.SetPath("")

	def set_status(self, message, sector=0):
		self.statusbar.SetStatusText(message, sector)  # Обновляем текстовое сообщение в статус-баре
		self.loger.LOG.SetValue(self.loger.LOG.GetValue()  + datetime.now().strftime("%H:%M:%S")  + " -: " +  message + "\n")
