import os

from selection_windows import InputValidator, ValueSetupDialog
import wx
import wx.adv


########################################################################

class TitledPage(wx.adv.WizardPageSimple):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title, list_items):
        """Constructor"""
        wx.adv.WizardPageSimple.__init__(self, parent)

        self.__names = {"Name": "", "Comment": ""}
        self.__list_items = list_items
        self.__title = title
        self.__init_UI()

    def __init_UI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, self.__title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        self.list = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list.InsertColumn(0, 'Имя', width=160)
        self.list.InsertColumn(1, 'Комментарий', width=300)
        list_index = 0
        for item in self.__list_items:
            current_list_index = self.list.InsertItem(list_index, item[0])  # Добавить имя
            self.list.SetItem(current_list_index, 1, item[1])  # Добавить комментарий
            list_index += 1

        h_box.Add(self.list, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)

        button_panel = wx.Panel(self)
        v_box = wx.BoxSizer(wx.VERTICAL)
        select_btn = wx.Button(button_panel, wx.ID_ANY, 'Выбрать', size=(200, 30))
        new_btn = wx.Button(button_panel, wx.ID_ANY, 'Новый', size=(200, 30))
        rename_btn = wx.Button(button_panel, wx.ID_ANY, 'Изменить', size=(200, 30))
        delete_btn = wx.Button(button_panel, wx.ID_ANY, 'Удалить', size=(200, 30))
        search_field = wx.TextCtrl(button_panel, wx.ID_ANY, "", size=(200, 30))

        quote = wx.StaticText(button_panel, label="Поиск")
        v_box.Add(quote, 0, wx.LEFT, 10)
        v_box.Add(search_field, 0, wx.LEFT)
        v_box.Add(select_btn, 0, wx.TOP, 10)
        v_box.Add(new_btn, 0, wx.TOP, 10)
        v_box.Add(rename_btn, 0, wx.TOP, 10)
        v_box.Add(delete_btn, 0, wx.TOP, 10)
        button_panel.SetSizer(v_box)
        h_box.Add(button_panel, 0, wx.RIGHT | wx.LEFT, 5)

        sizer.Add(h_box, proportion=1, flag=wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=new_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnRename, id=rename_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delete_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=select_btn.GetId())
        self.Bind(wx.EVT_TEXT, self.OnChar, id=search_field.GetId())

    def OnChar(self, event):
        typed_chars = event.GetString()
        possible_idx = self.list.FindItem(start=-1, str=typed_chars, partial=True)

        if possible_idx != wx.NOT_FOUND:
            # Debug ---> print(possible_idx, self.list.GetItemText(possible_idx, col=0))
            self.list.Select(possible_idx)

    def OnRename(self, event):
        selected_item = self.list.GetFirstSelected()
        if selected_item != -1:
            self.__names['Name'] = self.list.GetItemText(selected_item, col=0)
            self.__names['Comment'] = self.list.GetItemText(selected_item, col=1)
            # Debug ---> print(f"Selected ITEM: {self.names['Name']}, {self.names['Comment']}")
            ex = ValueSetupDialog("Переименовать элемент", input_data=self.__names)

            self.list.SetItem(selected_item, 0, self.__names['Name'])  # Изменить имя
            self.list.SetItem(selected_item, 1, self.__names['Comment'])  # Изменить комментарий

            self.__names['Name'] = ""
            self.__names['Comment'] = ""
            ex.Destroy()

    def NewItem(self, event):
        ex = ValueSetupDialog("Создание нового элемента", input_data=self.__names)

        # Debug ---> print(f"Имя: {self.__names['Name']}\nКомментарий: {self.__names['Comment']}")

        if len(self.__names['Name']) and len(self.__names['Comment']):
            index = self.list.GetItemCount()
            temp = self.list.InsertItem(index, self.__names['Name'])  # Добавить имя
            self.list.SetItem(temp, 1, self.__names['Comment'])  # Добавить комментарий

            self.__names['Name'] = ""
            self.__names['Comment'] = ""

        ex.Destroy()

    def OnSelect(self, event):
        selected_item = self.list.GetFirstSelected()
        if selected_item != -1:
            text = self.list.GetItemText(selected_item, col=0)
            # Debug --->
            print(f"Selected ITEM: {text}, index: {selected_item}")
            # TODO: Сохранение выбранного элемента, модифицированного входного списка
            #self.Close(True)  # Close the frame

    def OnDelete(self, event):
        selected_item = self.list.GetFirstSelected()
        if selected_item != -1:
            self.list.DeleteItem(selected_item)
            if self.list.GetItemCount() > 0:
                self.list.Select(selected_item - 1)


def main():
    app = wx.App()

    data = [('TFT', 'TFT дисплеи'), ('LCD', 'ЖКИ'),
            ('DOT', 'Точечные индикаторы'), ('GPI', 'Имитатор протоколов СУЛ'),
            ('MODB', 'Modbus to CAN конвертер')]

    wizard = wx.adv.Wizard(None, -1, "Software S/N Gen v1.0")
    page1 = TitledPage(wizard, "Выбор обозначения", data)
    page2 = TitledPage(wizard, "Выбор размера дисплея", data)
    page3 = TitledPage(wizard, "Выбор типа матрицы", data)

    wizard.FitToPage(page1)
    wizard.Centre()
    # Set the initial order of the pages
    page1.SetNext(page2)
    page2.SetPrev(page1)
    page2.SetNext(page3)
    page3.SetPrev(page2)

    wizard.GetPageAreaSizer().Add(page1)
    wizard.RunWizard(page1)
    wizard.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    main()
