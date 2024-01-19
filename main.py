import wx

import wx


class Selection(wx.Frame):

    def __init__(self, parent, title, list_items):
        style = wx.SYSTEM_MENU | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, parent, title=title, style=style)
        self.SetIcon(wx.Icon("app_logo.png"))
        self.list_items = sorted(list_items)  # Сортировка в алфавитном порядке
        self.InitUI()

    def InitUI(self):

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.listbox = wx.ListBox(panel, style=wx.LB_SORT)

        if isinstance(self.list_items, list) and len(self.list_items):
            for item in self.list_items:
                self.listbox.Append(item)

        hbox.Add(self.listbox, wx.ID_ANY, wx.EXPAND | wx.ALL, 20)

        btnPanel = wx.Panel(panel)
        vbox = wx.BoxSizer(wx.VERTICAL)
        SelBtn = wx.Button(btnPanel, wx.ID_ANY, 'Выбрать', size=(100, 30))
        newBtn = wx.Button(btnPanel, wx.ID_ANY, 'Новый', size=(100, 30))
        renBtn = wx.Button(btnPanel, wx.ID_ANY, 'Переименовать', size=(100, 30))
        delBtn = wx.Button(btnPanel, wx.ID_ANY, 'Удалить', size=(100, 30))
        search_expected_results = wx.TextCtrl(btnPanel, -1, "", size=(100, 30))

        quote = wx.StaticText(btnPanel, label="Поиск элемента", pos=(20, 30))

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=newBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnRename, id=renBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=delBtn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnSelect, id=SelBtn.GetId())
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect)
        self.Bind(wx.EVT_TEXT, self.OnChar, id=search_expected_results.GetId())

        #vbox.Add((-1, 20))
        vbox.Add(quote)
        vbox.Add(search_expected_results, 0, wx.LEFT)
        vbox.Add(SelBtn, 0, wx.TOP, 5)
        vbox.Add(newBtn, 0, wx.TOP, 5)
        vbox.Add(renBtn, 0, wx.TOP, 5)
        vbox.Add(delBtn, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show()

    def ShowErrorMessage(self, text):
        wx.MessageBox(text, 'Ошибка',
                      wx.OK | wx.ICON_ERROR)

    def OnChar(self, event):
        #self.ShowErrorMessage("Тест!")
        typed_chars = event.GetString()
        print(typed_chars)

        temp = self.listbox.GetStrings()

        for string in temp:
            if typed_chars in string:
                item_id = self.listbox.FindString(string, caseSensitive=False)
                self.listbox.SetSelection(item_id)  # Выделение предполагаемого элемента
                break

    def NewItem(self, event):
        text = wx.GetTextFromUser('Задайте имя нового элемента', 'Добавить новый элемент')
        if text != '':
            self.list_items.append(text)
            self.list_items = sorted(self.list_items)
            self.listbox.Append(text)

    def OnRename(self, event):

        selected_item = self.listbox.GetSelection()
        text = self.listbox.GetString(selected_item)
        new_name = wx.GetTextFromUser('Задайте новое имя элемента', 'Переименовать элемент', text)

        if new_name != '':
            del self.list_items[selected_item]
            self.list_items.append(new_name)
            self.list_items = sorted(self.list_items)

            self.listbox.Delete(selected_item)

            item_id = self.listbox.Append(new_name)
            self.listbox.SetSelection(item_id)  # Выделение переименованного эл-та

    def OnSelect(self, event):
        selected_item = self.listbox.GetSelection()
        text = self.listbox.GetString(selected_item)
        print(f"Selected ITEM: {text}")
        #TODO: Сохранение выбранного элемента, модифицированного входного списка
        self.Close(True)  # Close the frame

    def OnDelete(self, event):
        selected_item = self.listbox.GetSelection()

        if selected_item != -1:
            deleted_element = self.listbox.GetString(selected_item)
            self.list_items.remove(deleted_element)
            self.listbox.Delete(selected_item)
            if len(self.listbox.GetStrings()) > 0:
                self.listbox.SetSelection(selected_item - 1)


def main():
    test_lst = ["TFT", "LCD", "GPI_MU", "MODB"]
    app = wx.App()
    ex = Selection(None, "ОБОЗНАЧЕНИЕ", ["TFT", "LCD", "GPI_MU", "MODB"])
    app.MainLoop()


if __name__ == '__main__':
    main()
