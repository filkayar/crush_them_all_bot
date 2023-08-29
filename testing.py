import os

import cv2
import wx
import wx.xrc
from PIL import Image

###########################################################################
## Class TestingDialog
###########################################################################

class TestingDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.Size( -1,-1 ) )

		TD_container = wx.FlexGridSizer( 3, 1, 0, 0 )
		TD_container.SetFlexibleDirection( wx.BOTH )
		TD_container.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		TD_path_container = wx.BoxSizer( wx.HORIZONTAL )

		self.test_image_path = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		TD_path_container.Add( self.test_image_path, 1, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.td_TEST = wx.Button( self, wx.ID_ANY, u"ТЕСТ", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.td_TEST.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.td_TEST.SetMinSize( wx.Size( 150,-1 ) )

		TD_path_container.Add( self.td_TEST, 0, wx.ALL, 5 )


		TD_container.Add( TD_path_container, 1, wx.EXPAND, 5 )

		TD_setting_container = wx.FlexGridSizer( 0, 2, 0, 0 )
		TD_setting_container.SetFlexibleDirection( wx.BOTH )
		TD_setting_container.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		TD_setting_parameters_container = wx.BoxSizer( wx.VERTICAL )

		TD_setting_parameters_container.SetMinSize( wx.Size( 400,-1 ) )
		td_WBlvl_block = wx.BoxSizer( wx.HORIZONTAL )

		self.td_WBlvl = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 110,-1 ), wx.SP_ARROW_KEYS, 0, 255, 0 )
		td_WBlvl_block.Add( self.td_WBlvl, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText43 = wx.StaticText( self, wx.ID_ANY, u" - Порог градации цвета", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )

		td_WBlvl_block.Add( self.m_staticText43, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		TD_setting_parameters_container.Add( td_WBlvl_block, 1, wx.EXPAND, 5 )

		td_SizeCon_block = wx.BoxSizer( wx.HORIZONTAL )

		self.td_SizeCon_min = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		td_SizeCon_block.Add( self.td_SizeCon_min, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.td_SizeCon_max = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.SP_ARROW_KEYS, 0, 10000, 0 )
		td_SizeCon_block.Add( self.td_SizeCon_max, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.m_staticText44 = wx.StaticText( self, wx.ID_ANY, u" - Разброс размеров искомого контура", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )

		td_SizeCon_block.Add( self.m_staticText44, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		TD_setting_parameters_container.Add( td_SizeCon_block, 1, wx.EXPAND, 5 )


		TD_setting_container.Add( TD_setting_parameters_container, 1, wx.EXPAND, 5 )

		TD_setting_buttons_container = wx.BoxSizer( wx.VERTICAL )


		TD_setting_container.Add( TD_setting_buttons_container, 1, 0, 5 )


		TD_container.Add( TD_setting_container, 1, wx.EXPAND, 5 )


		self.SetSizer( TD_container )
		self.Layout()
		TD_container.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.td_TEST.Bind( wx.EVT_BUTTON, self.Test_image )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def Test_image( self, event ):
		# Получение пути к выбранному файлу изображения
		image_path = self.test_image_path.GetPath()
		# Получение радиуса окружности с числового поля
		min_radius = self.td_SizeCon_min.GetValue()
		max_radius = self.td_SizeCon_max.GetValue()

		# Загрузка изображения с использованием OpenCV
		image = cv2.imread(image_path)

		# Преобразование изображения в черно-белую палитру
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# Получение значения порога с числового поля
		threshold = self.td_WBlvl.GetValue()

		# Бинаризация изображения с использованием порога
		_, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
		image2 = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

		height, width = binary_image.shape[:2]
		for radius in range(min_radius,max_radius+1,1):
			for y in range(radius, height - radius):
				for x in range(radius, width - radius):
					_x = binary_image[y, x]
					_a = binary_image[y - radius, x - radius]
					_b = binary_image[y - radius, x + radius]
					_c = binary_image[y + radius, x - radius]
					_d = binary_image[y + radius, x + radius]
					_e = binary_image[y + radius, x]
					_f = binary_image[y - radius, x]
					_g = binary_image[y, x + radius]
					_h = binary_image[y, x - radius]
					if (  # белый крест
							_x == 255 and
							_a == 255 and _b == 255 and _c == 255 and _d == 255 and
							_e == 0 and _f == 0 and _g == 0 and _h == 0
					) or (  # черный крест
							_x == 0 and
							_a == 0 and _b == 0 and _c == 0 and _d == 0 and
							_e == 255 and _f == 255 and _g == 255 and _h == 255
					) or (  # белый next
							_x == 255 and
							_a == 255 and _b == 0 and _c == 255 and _d == 0 and
							_e == 0 and _f == 0 and _h == 0
					):
						cv2.circle(image2, (int(x), int(y)), radius, (0, 255, 0), 1)


		# Создание временного файла для сохранения обработанного изображения
		temp_image_path = "temp_image.jpg"
		cv2.imwrite(temp_image_path, image2)

		# Открытие и отображение обработанного изображения с помощью PIL
		img = Image.open(temp_image_path)
		img.show()

		# Удаление временного файла
		os.remove(temp_image_path)