import wx


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

        name_t = wx.TextCtrl(self, validator=InputValidator(input_data, "Name"), size=(200, 25))  # , value=name)
        comment_t = wx.TextCtrl(self, validator=InputValidator(input_data, "Comment"),
                                size=(200, 25))  # , value=comment)

        ok = wx.Button(self, wx.ID_OK)
        ok.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)

        fgs = wx.FlexGridSizer(2, 2, 5, 5)
        fgs.Add(name_l, 1, wx.ALIGN_RIGHT)
        fgs.Add(name_t, 1, wx.EXPAND, 25)
        fgs.Add(comment_l, 1, wx.ALIGN_RIGHT)
        fgs.Add(comment_t, 1, wx.EXPAND)
        sizer.Add(fgs, 1, wx.EXPAND | wx.ALL, 5)

        buttons = wx.StdDialogButtonSizer()
        buttons.AddButton(ok)
        buttons.AddButton(cancel)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(sizer)
        self.ShowModal()


class CodeSelection(wx.Frame):
    def __init__(self, parent, title, list_items):
        style = wx.SYSTEM_MENU | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent, title=title, style=style)
        self.SetIcon(wx.Icon("app_logo.png"))
        self.SetTitle(title)
        self.__names = {"Name": "", "Comment": ""}
        self.__list_items = list_items

        self.InitUI()

    def InitUI(self):
        h_box = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self)

        self.list = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list.InsertColumn(0, 'Имя', width=100)
        self.list.InsertColumn(1, 'Комментарий', width=200)

        list_index = 0
        for item in self.__list_items:
            current_list_index = self.list.InsertItem(list_index, item[0])  # Добавить имя
            self.list.SetItem(current_list_index, 1, item[1])  # Добавить комментарий
            list_index += 1

        h_box.Add(self.list, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, 5)

        button_panel = wx.Panel(panel)
        v_box = wx.BoxSizer(wx.VERTICAL)
        select_btn = wx.Button(button_panel, wx.ID_ANY, 'Выбрать', size=(100 + 100, 30))
        new_btn = wx.Button(button_panel, wx.ID_ANY, 'Новый', size=(100 + 100, 30))
        rename_btn = wx.Button(button_panel, wx.ID_ANY, 'Изменить', size=(100 + 100, 30))
        delete_btn = wx.Button(button_panel, wx.ID_ANY, 'Удалить', size=(100 + 100, 30))
        search_field = wx.TextCtrl(button_panel, -1, "", size=(100 + 100, 30))

        quote = wx.StaticText(button_panel, label="Поиск")

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=new_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnRename, id=rename_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delete_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=select_btn.GetId())
        self.Bind(wx.EVT_TEXT, self.OnChar, id=search_field.GetId())

        v_box.Add(quote, 0, wx.LEFT, 10)
        v_box.Add(search_field, 0, wx.LEFT)
        v_box.Add(select_btn, 0, wx.TOP, 10)
        v_box.Add(new_btn, 0, wx.TOP, 10)
        v_box.Add(rename_btn, 0, wx.TOP, 10)
        v_box.Add(delete_btn, 0, wx.TOP, 10)

        button_panel.SetSizer(v_box)
        h_box.Add(button_panel, 1, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)
        panel.SetSizer(h_box)

        self.Centre()
        self.Show()

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
            # Debug ---> print(f"Selected ITEM: {text}, index: {selected_item}")
            # TODO: Сохранение выбранного элемента, модифицированного входного списка
            self.Close(True)  # Close the frame

    def OnDelete(self, event):
        selected_item = self.list.GetFirstSelected()
        if selected_item != -1:
            self.list.DeleteItem(selected_item)
            if self.list.GetItemCount() > 0:
                self.list.Select(selected_item - 1)
