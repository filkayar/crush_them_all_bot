import wx
import wx.xrc
import wx.grid
import mouse


class ScreenDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(
            self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(-1, -1),
            style=wx.DEFAULT_DIALOG_STYLE
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        sd_container = wx.FlexGridSizer(0, 1, 0, 0)
        sd_container.SetFlexibleDirection(wx.BOTH)
        sd_container.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        screen_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText128 = wx.StaticText(self, wx.ID_ANY, u"Зона скриншотов", wx.DefaultPosition, wx.Size(300, -1),
                                             0)
        self.m_staticText128.Wrap(-1)

        screen_block.Add(self.m_staticText128, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_screen_zone = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        screen_block.Add(self.set_screen_zone, 0, wx.ALL | wx.EXPAND, 5)

        screen_coord = wx.GridSizer(2, 2, 0, 0)

        self.sz_x0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        screen_coord.Add(self.sz_x0, 0, wx.ALL | wx.EXPAND, 5)

        self.sz_y0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        screen_coord.Add(self.sz_y0, 0, wx.ALL | wx.EXPAND, 5)

        self.sz_x1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        screen_coord.Add(self.sz_x1, 0, wx.ALL | wx.EXPAND, 5)

        self.sz_y1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        screen_coord.Add(self.sz_y1, 0, wx.ALL | wx.EXPAND, 5)

        screen_block.Add(screen_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(screen_block, 1, wx.EXPAND, 5)

        self.m_staticline17 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline17, 0, wx.EXPAND | wx.ALL, 5)

        exit_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"Зона поиска выхода", wx.DefaultPosition,
                                            wx.Size(300, -1), 0)
        self.m_staticText12.Wrap(-1)

        exit_block.Add(self.m_staticText12, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        sb_sizer1 = wx.BoxSizer(wx.VERTICAL)

        sb_sizer1.SetMinSize(wx.Size(100, -1))
        self.set_exit_zone = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        sb_sizer1.Add(self.set_exit_zone, 1, wx.ALL | wx.EXPAND, 5)

        self.clear_exit_zone = wx.Button(self, wx.ID_ANY, u"CLEAR", wx.DefaultPosition, wx.DefaultSize, 0)
        sb_sizer1.Add(self.clear_exit_zone, 1, wx.ALL | wx.EXPAND, 5)

        exit_block.Add(sb_sizer1, 0, wx.EXPAND, 5)

        sb_sizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Список зон поиска"), wx.VERTICAL)

        sb_sizer1.SetMinSize(wx.Size(300, 150))
        self.find_zones = wx.grid.Grid(sb_sizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size(250, -1), 0)

        # Grid
        self.find_zones.CreateGrid(0, 4)
        self.find_zones.EnableEditing(False)
        self.find_zones.EnableGridLines(True)
        self.find_zones.EnableDragGridSize(False)
        self.find_zones.SetMargins(0, 0)

        # Columns
        self.find_zones.SetColSize(0, 50)
        self.find_zones.SetColSize(1, 50)
        self.find_zones.SetColSize(2, 50)
        self.find_zones.SetColSize(3, 50)
        self.find_zones.EnableDragColMove(False)
        self.find_zones.EnableDragColSize(True)
        self.find_zones.SetColLabelValue(0, u"x0")
        self.find_zones.SetColLabelValue(1, u"y0")
        self.find_zones.SetColLabelValue(2, u"x1")
        self.find_zones.SetColLabelValue(3, u"y1")
        self.find_zones.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Rows
        self.find_zones.AutoSizeRows()
        self.find_zones.EnableDragRowSize(True)
        self.find_zones.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Label Appearance

        # Cell Defaults
        self.find_zones.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        self.find_zones.SetMinSize(wx.Size(-1, 120))

        sb_sizer1.Add(self.find_zones, 0, wx.ALL | wx.EXPAND, 5)

        exit_block.Add(sb_sizer1, 1, wx.EXPAND, 5)

        sd_container.Add(exit_block, 1, wx.EXPAND, 5)

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        chest_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText121 = wx.StaticText(self, wx.ID_ANY, u"Зона поиска сундуков", wx.DefaultPosition,
                                             wx.Size(300, -1), 0)
        self.m_staticText121.Wrap(-1)

        chest_block.Add(self.m_staticText121, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_chest_zone = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        chest_block.Add(self.set_chest_zone, 0, wx.ALL | wx.EXPAND, 5)

        chest_coord = wx.GridSizer(2, 2, 0, 0)

        self.ctz_x0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                  0)
        chest_coord.Add(self.ctz_x0, 0, wx.ALL | wx.EXPAND, 5)

        self.ctz_y0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                  0)
        chest_coord.Add(self.ctz_y0, 0, wx.ALL | wx.EXPAND, 5)

        self.ctz_x1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                  0)
        chest_coord.Add(self.ctz_x1, 0, wx.ALL | wx.EXPAND, 5)

        self.ctz_y1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                  0)
        chest_coord.Add(self.ctz_y1, 0, wx.ALL | wx.EXPAND, 5)

        chest_block.Add(chest_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(chest_block, 1, wx.EXPAND, 5)

        self.m_staticline11 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline11, 0, wx.EXPAND | wx.ALL, 5)

        play_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1211 = wx.StaticText(self, wx.ID_ANY, u"Зона воспроизведения", wx.DefaultPosition,
                                              wx.Size(300, -1), 0)
        self.m_staticText1211.Wrap(-1)

        play_block.Add(self.m_staticText1211, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_play_zone = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        play_block.Add(self.set_play_zone, 0, wx.ALL | wx.EXPAND, 5)

        play_coord = wx.GridSizer(2, 2, 0, 0)

        self.pz_x0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        play_coord.Add(self.pz_x0, 0, wx.ALL | wx.EXPAND, 5)

        self.pz_y0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        play_coord.Add(self.pz_y0, 0, wx.ALL | wx.EXPAND, 5)

        self.pz_x1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        play_coord.Add(self.pz_x1, 0, wx.ALL | wx.EXPAND, 5)

        self.pz_y1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        play_coord.Add(self.pz_y1, 0, wx.ALL | wx.EXPAND, 5)

        play_block.Add(play_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(play_block, 1, wx.EXPAND, 5)

        self.m_staticline111 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline111, 0, wx.EXPAND | wx.ALL, 5)

        end_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText122 = wx.StaticText(self, wx.ID_ANY, u"Зона получения", wx.DefaultPosition, wx.Size(300, -1),
                                             0)
        self.m_staticText122.Wrap(-1)

        end_block.Add(self.m_staticText122, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_end_zone = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        end_block.Add(self.set_end_zone, 0, wx.ALL | wx.EXPAND, 5)

        end_coord = wx.GridSizer(2, 2, 0, 0)

        self.ez_x0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        end_coord.Add(self.ez_x0, 0, wx.ALL | wx.EXPAND, 5)

        self.ez_y0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        end_coord.Add(self.ez_y0, 0, wx.ALL | wx.EXPAND, 5)

        self.ez_x1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        end_coord.Add(self.ez_x1, 0, wx.ALL | wx.EXPAND, 5)

        self.ez_y1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                 0)
        end_coord.Add(self.ez_y1, 0, wx.ALL | wx.EXPAND, 5)

        end_block.Add(end_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(end_block, 1, wx.EXPAND, 5)

        self.m_staticline12 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline12, 0, wx.EXPAND | wx.ALL, 5)

        check_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText123 = wx.StaticText(self, wx.ID_ANY, u"Зона проверки экрана", wx.DefaultPosition,
                                             wx.Size(300, -1), 0)
        self.m_staticText123.Wrap(-1)

        check_block.Add(self.m_staticText123, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_check_zone = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        check_block.Add(self.set_check_zone, 0, wx.ALL | wx.EXPAND, 5)

        check_coord = wx.GridSizer(2, 2, 0, 0)

        self.ckz_x0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                  0)
        check_coord.Add(self.ckz_x0, 0, wx.ALL | wx.EXPAND, 5)

        self.ckz_y0 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                  0)
        check_coord.Add(self.ckz_y0, 0, wx.ALL | wx.EXPAND, 5)

        self.ckz_x1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                  0)
        check_coord.Add(self.ckz_x1, 0, wx.ALL | wx.EXPAND, 5)

        self.ckz_y1 = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                  0)
        check_coord.Add(self.ckz_y1, 0, wx.ALL | wx.EXPAND, 5)

        check_block.Add(check_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(check_block, 1, wx.EXPAND, 5)

        self.m_staticline13 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline13, 0, wx.EXPAND | wx.ALL, 5)

        icon_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText125 = wx.StaticText(self, wx.ID_ANY, u" - ИКОНКА ПРИЛОЖЕНИЯ", wx.DefaultPosition,
                                             wx.Size(300, -1), 0)
        self.m_staticText125.Wrap(-1)

        icon_block.Add(self.m_staticText125, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_icon_zone = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        icon_block.Add(self.set_icon_zone, 0, wx.ALL | wx.EXPAND, 5)

        icon_coord = wx.GridSizer(2, 2, 0, 0)

        self.iz_x = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                0)
        icon_coord.Add(self.iz_x, 0, wx.ALL | wx.EXPAND, 5)

        self.iz_y = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000,
                                0)
        icon_coord.Add(self.iz_y, 0, wx.ALL | wx.EXPAND, 5)

        icon_block.Add(icon_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(icon_block, 1, wx.EXPAND, 5)

        self.m_staticline14 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline14, 0, wx.EXPAND | wx.ALL, 5)

        back_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText126 = wx.StaticText(self, wx.ID_ANY, u" - НАЗАД", wx.DefaultPosition, wx.Size(300, -1), 0)
        self.m_staticText126.Wrap(-1)

        back_block.Add(self.m_staticText126, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_BACK = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        back_block.Add(self.set_BACK, 0, wx.ALL | wx.EXPAND, 5)

        back_coord = wx.GridSizer(2, 2, 0, 0)

        self.b_x = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000, 0)
        back_coord.Add(self.b_x, 0, wx.ALL | wx.EXPAND, 5)

        self.b_y = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000, 0)
        back_coord.Add(self.b_y, 0, wx.ALL | wx.EXPAND, 5)

        back_block.Add(back_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(back_block, 1, wx.EXPAND, 5)

        self.m_staticline15 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline15, 0, wx.EXPAND | wx.ALL, 5)

        apps_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText127 = wx.StaticText(self, wx.ID_ANY, u" - ФОНОВЫЕ ПРИЛОЖЕНИЯ", wx.DefaultPosition,
                                             wx.Size(300, -1), 0)
        self.m_staticText127.Wrap(-1)

        apps_block.Add(self.m_staticText127, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_APPS = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        apps_block.Add(self.set_APPS, 0, wx.ALL | wx.EXPAND, 5)

        apps_coord = wx.GridSizer(2, 2, 0, 0)

        self.a_x = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000, 0)
        apps_coord.Add(self.a_x, 0, wx.ALL | wx.EXPAND, 5)

        self.a_y = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000, 0)
        apps_coord.Add(self.a_y, 0, wx.ALL | wx.EXPAND, 5)

        apps_block.Add(apps_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(apps_block, 1, wx.EXPAND, 5)

        self.m_staticline16 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        sd_container.Add(self.m_staticline16, 0, wx.EXPAND | wx.ALL, 5)

        clear_block = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText124 = wx.StaticText(self, wx.ID_ANY, u" - ОЧИСТИТЬ", wx.DefaultPosition, wx.Size(300, -1), 0)
        self.m_staticText124.Wrap(-1)

        clear_block.Add(self.m_staticText124, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.set_CLEAR = wx.Button(self, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        clear_block.Add(self.set_CLEAR, 0, wx.ALL | wx.EXPAND, 5)

        clear_coord = wx.GridSizer(2, 2, 0, 0)

        self.c_x = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000, 0)
        clear_coord.Add(self.c_x, 0, wx.ALL | wx.EXPAND, 5)

        self.c_y = wx.SpinCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10000, 0)
        clear_coord.Add(self.c_y, 0, wx.ALL | wx.EXPAND, 5)

        clear_block.Add(clear_coord, 1, wx.ALIGN_CENTER, 5)

        sd_container.Add(clear_block, 1, wx.EXPAND, 5)

        self.SetSizer(sd_container)
        self.Layout()
        sd_container.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.set_screen_zone.Bind(wx.EVT_BUTTON, self.set_zone_screen)
        self.set_exit_zone.Bind(wx.EVT_BUTTON, self.set_zone_exit)
        self.clear_exit_zone.Bind(wx.EVT_BUTTON, self.clear_exit_zone)
        self.set_chest_zone.Bind(wx.EVT_BUTTON, self.set_zone_chest)
        self.set_play_zone.Bind(wx.EVT_BUTTON, self.set_zone_play)
        self.set_end_zone.Bind(wx.EVT_BUTTON, self.set_zone_end)
        self.set_check_zone.Bind(wx.EVT_BUTTON, self.set_zone_check)
        self.set_icon_zone.Bind(wx.EVT_BUTTON, self.set_zone_icon)
        self.set_BACK.Bind(wx.EVT_BUTTON, self.set_zone_back)
        self.set_APPS.Bind(wx.EVT_BUTTON, self.set_zone_apps)
        self.set_CLEAR.Bind(wx.EVT_BUTTON, self.set_zone_clear)

        self.parent = parent
        self.counter = 0

    def __del__(self):
        pass

    def clear_exit_zone_f(self):
        n = self.find_zones.GetNumberRows()
        if n > 0:
            self.find_zones.DeleteRows(numRows=n)

    def clear_exit_zone(self, event):
        self.clear_exit_zone_f()
        event.skip()

    def set_zone_exit(self, event):
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
        event.skip()

    def set_zone_chest(self, event):
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
        event.skip()

    def set_zone_play(self, event):
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
        event.skip()

    def set_zone_end(self, event):
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
        event.skip()

    def set_zone_check(self, event):
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
        event.skip()

    def set_zone_icon(self, event):
        self.counter = 0

        def on_click():
            x, y = mouse.get_position()
            if self.counter == 0:
                self.iz_x.SetValue(x)
                self.iz_y.SetValue(y)
                mouse.unhook_all()
            self.counter += 1

        mouse.on_click(on_click)
        event.skip()

    def set_zone_screen(self, event):
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
        event.skip()

    def set_zone_back(self, event):
        self.counter = 0

        def on_click():
            x, y = mouse.get_position()
            if self.counter == 0:
                self.b_x.SetValue(x)
                self.b_y.SetValue(y)
                mouse.unhook_all()
            self.counter += 1

        mouse.on_click(on_click)
        event.skip()

    def set_zone_apps(self, event):
        self.counter = 0

        def on_click():
            x, y = mouse.get_position()
            if self.counter == 0:
                self.a_x.SetValue(x)
                self.a_y.SetValue(y)
                mouse.unhook_all()
            self.counter += 1

        mouse.on_click(on_click)
        event.skip()

    def set_zone_clear(self, event):
        self.counter = 0

        def on_click():
            x, y = mouse.get_position()
            if self.counter == 0:
                self.c_x.SetValue(x)
                self.c_y.SetValue(y)
                mouse.unhook_all()
            self.counter += 1

        mouse.on_click(on_click)
        event.skip()
