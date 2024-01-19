import wx

import wx

data = [('TFT', 'TFT дисплеи'), ('LCD', 'ЖКИ'),
        ('DOT', 'Точечные индикаторы'), ('GPI', 'Имитатор протоколов СУЛ'),
        ('MODB', 'Modbus to CAN конвертер')]


class InputValidator(wx.Validator):
    def __init__(self, value, key):
        wx.Validator.__init__(self)
        self.value = value
        self.key = key

    def Clone(self):
        return InputValidator(self.value, self.key)

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
        # TODO: английские символы + цифры!
        if len(text) == 0:
            wx.MessageBox("Поле не должно быть пустым!", "Ошибка")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        textCtrl.SetValue(self.value.get(self.key, ""))
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.value[self.key] = textCtrl.GetValue()
        return True


class ValueSetupDialog(wx.Dialog):
    def __init__(self, title, input_data):
        wx.Dialog.__init__(self, None, -1, title)
        name_l = wx.StaticText(self, -1, "Имя элемента:")
        comment_l = wx.StaticText(self, -1, "Комментарий:")

        name_t = wx.TextCtrl(self, validator=InputValidator(input_data, "Name"))  # , value=name)
        comment_t = wx.TextCtrl(self, validator=InputValidator(input_data, "Comment"))  # , value=comment)

        ok = wx.Button(self, wx.ID_OK)
        ok.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)

        fgs = wx.FlexGridSizer(2, 2, 5, 5)
        fgs.Add(name_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(name_t, 0, wx.EXPAND)
        fgs.Add(comment_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(comment_t, 0, wx.EXPAND)
        sizer.Add(fgs, 0, wx.EXPAND | wx.ALL, 5)

        buttons = wx.StdDialogButtonSizer()
        buttons.AddButton(ok)
        buttons.AddButton(cancel)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.ShowModal()


class AdvSelection(wx.Frame):
    def __init__(self, parent, title, list_items=None):
        style = wx.SYSTEM_MENU | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent, title=title, style=style)
        self.SetIcon(wx.Icon("app_logo.png"))
        self.SetTitle(title)
        self.InitUI()
        self.names = {"Name" : "", "Comment" : ""}

    def InitUI(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self)

        self.list = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list.InsertColumn(0, 'Имя', width=100)
        self.list.InsertColumn(1, 'Комментарий', width=160)

        idx = 0

        for i in data:
            index = self.list.InsertItem(idx, i[0])  # Добавить имя
            self.list.SetItem(index, 1, i[1])  # Добавить комментарий
            idx += 1

        hbox.Add(self.list, 4, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)

        btnPanel = wx.Panel(panel)
        vbox = wx.BoxSizer(wx.VERTICAL)
        SelBtn = wx.Button(btnPanel, wx.ID_ANY, 'Выбрать', size=(100, 30))
        newBtn = wx.Button(btnPanel, wx.ID_ANY, 'Новый', size=(100, 30))
        renBtn = wx.Button(btnPanel, wx.ID_ANY, 'Изменить', size=(100, 30))
        delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Удалить', size=(100, 30))
        search_expected_results = wx.TextCtrl(btnPanel, -1, "", size=(100, 30))

        quote = wx.StaticText(btnPanel, label="Поиск элемента", pos=(20, 30))

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=newBtn.GetId())
        # self.Bind(wx.EVT_BUTTON, self.OnRename, id=renBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=SelBtn.GetId())
        # self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect)
        self.Bind(wx.EVT_TEXT, self.OnChar, id=search_expected_results.GetId())

        vbox.Add(quote)
        vbox.Add(search_expected_results, 0, wx.LEFT)
        vbox.Add(SelBtn, 0, wx.TOP, 10)
        vbox.Add(newBtn, 0, wx.TOP, 10)
        vbox.Add(renBtn, 0, wx.TOP, 10)
        vbox.Add(delBtn, 0, wx.TOP, 10)

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 2, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show()

    def OnChar(self, event):
        typed_chars = event.GetString()
        possible_idx = self.list.FindItem(start=-1, str=typed_chars, partial=True)

        if possible_idx != wx.NOT_FOUND:
            # Debug ---> print(possible_idx, self.list.GetItemText(possible_idx, col=0))
            self.list.Select(possible_idx)

    def NewItem(self, event):
        ex = ValueSetupDialog("Создание нового элемента", input_data=self.names)
        print(self.names)
        ex.Destroy()

    def OnSelect(self, event):
        selected_item = self.list.GetFirstSelected()
        text = self.list.GetItemText(selected_item, col=0)
        # Debug ---> print(f"Selected ITEM: {text}, index: {selected_item}")
        # TODO: Сохранение выбранного элемента, модифицированного входного списка
        self.Close(True)  # Close the frame

    def OnDelete(self, event):
        selected_item = self.list.GetFirstSelected()
        if selected_item != -1:
            self.list.DeleteItem(selected_item)
            if self.list.GetItemCount() > 0:
                self.list.Select(selected_item - 1)

    # def OnRename(self, event):
    #
    #     selected_item = self.listbox.GetSelection()
    #     text = self.listbox.GetString(selected_item)
    #     new_name = wx.GetTextFromUser('Задайте новое имя элемента', 'Переименовать элемент', text)
    #
    #     if new_name != '':
    #         del self.list_items[selected_item]
    #         self.list_items.append(new_name)
    #         self.list_items = sorted(self.list_items)
    #
    #         self.listbox.Delete(selected_item)
    #
    #         item_id = self.listbox.Append(new_name)
    #         self.listbox.SetSelection(item_id)  # Выделение переименованного эл-та


def main():
    test_lst = ["TFT", "LCD", "GPI_MU", "MODB"]
    app = wx.App()
    ex = AdvSelection(None, "ОБОЗНАЧЕНИЕ")

    print(ex)
    app.MainLoop()


if __name__ == '__main__':
    main()
