from gen_wizard import wx, CodeGenerationWizard, CodeGenerationWizardPage
from usr_data import ParametersDataBase


class MainFrame(wx.Frame):
    def __init__(self, parent, title, size, path_to_icon):
        style = wx.SYSTEM_MENU | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent, title=title, style=style, size=size)

        version = "v. 0.1. (2024-23-01)"
        version_size = wx.Window.GetTextExtent(self, version)

        self.SetIcon(wx.Icon(path_to_icon))

        self.status_bar = self.CreateStatusBar(2)

        self.status_bar.SetStatusWidths([-1, version_size.width])

        self.SetStatusText('ООО "МЮ"', 0)
        self.SetStatusText(version, 1)

        self.Centre()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.control = wx.TextCtrl(self, size=(250, 32), style=wx.TE_CENTER)
        self.control.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))

        #self.control.AppendText("МЮ.TFT.88.01.01.V.N.C.03.03.046.01.v1")

        quote = wx.StaticText(self, label="Серийный номер")
        quote.SetFont(wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL))

        #self.control.SetLabelText("МЮ.TFT.88.01.01.V.N.C.03.03.046.01.v1")

        button_panel = wx.Panel(self)
        decode_btn = wx.Button(button_panel, wx.ID_ANY, 'РАСШИФРОВАТЬ', size=(200, 36))
        generate_btn = wx.Button(button_panel, wx.ID_ANY, 'СГЕНЕРИРОВАТЬ', size=(200, 36))

        generate_btn.SetFocus() # Кнопка "Сгенерировать" выделена по умолчанию

        button_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_horizontal_sizer.Add(generate_btn, 0, wx.RIGHT, 20)
        button_horizontal_sizer.Add(wx.StaticLine(button_panel, wx.ID_ANY, style=wx.LI_VERTICAL), 0, wx.EXPAND, 0)
        button_horizontal_sizer.Add(decode_btn, 0, wx.LEFT, 20)
        button_panel.SetSizer(button_horizontal_sizer)

        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_box_sizer.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND | wx.TOP, 5)
        vertical_box_sizer.Add(quote, 0, wx.CENTER | wx.TOP, 5)
        vertical_box_sizer.Add(self.control, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
        vertical_box_sizer.Add(button_panel, 0, wx.CENTER | wx.TOP, 0)

        self.Bind(wx.EVT_BUTTON, self.OnGenerateTouch, id=generate_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDecodeTouch, id=decode_btn.GetId())

        self.SetSizer(vertical_box_sizer)
        self.Centre()

    def OnGenerateTouch(self, event):
        print(f"Pressed OnGenerate")
    def OnDecodeTouch(self, event):
        print(f"Pressed OnDecode")


def main():
    app = wx.App()

    # tester = ParametersDataBase('code_database.ini')
    # wizard = CodeGenerationWizard(None, wx.ID_ANY, "Software S/N Gen v1.0")
    #
    # pages = []
    # # Создание страниц wx.adv.wizard, заполнение их данными из файла code_database
    # for idx, key in enumerate(tester.get_all_keys()):
    #     pages.append(CodeGenerationWizardPage(wizard, key, tester, idx))
    #
    # wizard.FitToPage(pages[0])
    #
    # # Set the initial order of the pages
    # for number in range(len(pages) - 1):
    #     pages[number].SetNext(pages[number + 1])
    #     pages[number + 1].SetPrev(pages[number])
    #
    # wizard.GetPageAreaSizer().Add(pages[0])
    # state = wizard.RunWizard(pages[0])
    #
    # # Работа объекта CodeGenerationWizard завершена!
    # if state:
    #     print(f"Шифр ПО:  {'.'.join(tester.get_software_code())}")
    #     # debug --> print(tester.show_user_data(config.sections()[0]))
    #     # Запись изменений в файл
    #     tester.save_changes()
    #
    # wizard.Destroy()

    frame = MainFrame(None, title="Software S/N handler", size=(480, 180), path_to_icon="app_logo.png")
    panel = MainPanel(frame)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
