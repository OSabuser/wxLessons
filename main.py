import os.path

import wx


class TextEditorFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(480, 272))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        # Setting up the menu
        file_menu = wx.Menu()
        menuOpen = file_menu.Append(wx.ID_OPEN, "&Open File", "Открыть файл")
        file_menu.AppendSeparator()
        menuAbout = file_menu.Append(wx.ID_ABOUT, "&About", "О программе")
        file_menu.AppendSeparator()
        menuExit = file_menu.Append(wx.ID_EXIT, "&Exit", "Выход из программы")

        properties_menu = wx.Menu()
        menuProperties = properties_menu.Append(wx.ID_PROPERTIES, "&Config", "Конфигурация")

        # Create the menu bar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(properties_menu, "&Properties")
        self.SetMenuBar(menu_bar)

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)

        self.nested_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0,6):
            self.buttons.append(wx.Button(self, -1, f"Button &{i}"))
            self.nested_sizer.Add(self.buttons[i], 1, wx.EXPAND)

        urgent_button = self.buttons[2]
        self.Bind(wx.EVT_BUTTON, self.OnButton2Click, urgent_button)

        self.parent_sizer = wx.BoxSizer(wx.VERTICAL)
        self.parent_sizer.Add(self.control, 1, wx.EXPAND)
        self.parent_sizer.Add(self.nested_sizer, 0, wx.EXPAND)

        self.SetSizer(self.parent_sizer)
        self.SetAutoLayout(1)
        self.parent_sizer.Fit(self)

        self.Show(True)

    def OnButton2Click(self, e):
        print("Button2 was pressed!")


    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A small TE", "Title")
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        self.Close(True)

    def OnOpen(self, e):
        # Открытие файла
        self.dir_name = ""
        dlg = wx.FileDialog(self, "Выберите файл: ", self.dir_name, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_name = dlg.GetFilename()
            self.dir_name = dlg.GetDirectory()
            f = open(os.path.join(self.dir_name, self.file_name), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()


app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
myFrame = TextEditorFrame(None, "Текстовый редактор")
app.MainLoop()
