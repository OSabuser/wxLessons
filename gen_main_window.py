from gen_wizard import wx, MainWizardClass
from dec_window import DecodeFrame


class MainFrame(wx.Frame):
    def __init__(self, parent, title, path_to_icon, path_to_database, version):
        style = wx.SYSTEM_MENU | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX

        wx.Frame.__init__(self, parent, title=title, style=style, size=(480, 180))

        self.path_to_file = path_to_database
        self.path_to_icon = path_to_icon
        self.title = title

        self.__version = version
        version_size = wx.Window.GetTextExtent(self, self.__version)

        self.SetIcon(wx.Icon(self.path_to_icon))

        self.status_bar = self.CreateStatusBar(2)

        self.status_bar.SetStatusWidths([-1, version_size.width])

        self.SetStatusText('ООО "МЮ"', 0)
        self.SetStatusText(self.__version, 1)

        self.Centre()
        self.__panel = MainPanel(self)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.control = wx.TextCtrl(self, size=(250, 32), style=wx.TE_CENTER)
        self.control.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))

        static_text = wx.StaticText(self, label="Серийный номер")
        static_text.SetFont(wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL))

        button_panel = wx.Panel(self)
        decode_btn = wx.Button(button_panel, wx.ID_ANY, 'РАСШИФРОВАТЬ', size=(200, 36))
        generate_btn = wx.Button(button_panel, wx.ID_ANY, 'СОЗДАТЬ', size=(200, 36))

        generate_btn.SetFocus()  # Кнопка "Сгенерировать" выделена по умолчанию

        button_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_horizontal_sizer.Add(generate_btn, 0, wx.RIGHT, 20)
        button_horizontal_sizer.Add(wx.StaticLine(button_panel, wx.ID_ANY, style=wx.LI_VERTICAL), 0, wx.EXPAND, 0)
        button_horizontal_sizer.Add(decode_btn, 0, wx.LEFT, 20)
        button_panel.SetSizer(button_horizontal_sizer)

        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_box_sizer.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND | wx.TOP, 5)
        vertical_box_sizer.Add(static_text, 0, wx.CENTER | wx.TOP, 5)
        vertical_box_sizer.Add(self.control, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
        vertical_box_sizer.Add(button_panel, 0, wx.CENTER | wx.TOP, 0)

        self.Bind(wx.EVT_BUTTON, self.OnGenerateTouch, id=generate_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDecodeTouch, id=decode_btn.GetId())

        self.SetSizer(vertical_box_sizer)
        self.Centre()

    def OnGenerateTouch(self, event):
        test = MainWizardClass(self, self.parent.path_to_file)

    def OnDecodeTouch(self, event):
        serial_number_to_decode = self.control.GetValue()
        if len(serial_number_to_decode) > 0:
            decode_frame = DecodeFrame(self, self.parent.title, path_to_icon=self.parent.path_to_icon,
                                       serial_number=serial_number_to_decode,
                                       path_to_database=self.parent.path_to_file)
            decode_frame.Show()
        else:
            wx.MessageBox(f"Поле серийного номера не должно быть пустым!", "Ошибка", wx.ICON_ERROR)
