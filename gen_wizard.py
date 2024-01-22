import wx
import wx.adv
from gen_dialog import ValueSetupDialog
from usr_data import ParametersDataBase


class CodeGenerationWizard(wx.adv.Wizard):
    def __init__(self, parent, wiz_id, title):
        wx.adv.Wizard.__init__(self, parent, wiz_id)
        self.SetTitle(title)
        self.SetIcon(wx.Icon("app_logo.png"))
        self.Centre()
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.on_page_changing)

        self.prev_btn = self.FindWindowById(wx.ID_BACKWARD)
        self.prev_btn.SetLabel("Назад")
        self.next_btn = self.FindWindowById(wx.ID_FORWARD)
        self.cancel_btn = self.FindWindowById(wx.ID_CANCEL)
        self.cancel_btn.SetLabel("Отмена")

    def on_page_changing(self, event):
        page = event.GetPage()

        # Debug -->print(f"Page state state: {page.selection_was_made}, page: {page.get_page_number()}")

        if not page.selection_was_made:
            page.FindWindowById(wx.ID_FORWARD).Disable()
        else:
            page.FindWindowById(wx.ID_FORWARD).Enable()

        self.next_btn.SetLabel("Далее")

        if page.GetNext() is None:
            self.next_btn.SetLabel("Готово")
            # Debug --->print("Последняя страница!")

    def GenerationFinished(self, event):
        pass
        # Debug ---> page = event.GetPage()
        # Debug ---> print(f"Номер версии ПО:    {'.'.join(self.__data_class.get_software_code())}")
        # Debug ---> if page.GetNext() is None:
        # Debug ---> self.__last_page = page
        # Debug ---> print("Последняя страница!")


class CodeGenerationWizardPage(wx.adv.WizardPage):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title, data_base_instance, page_number):
        """Constructor"""
        wx.adv.WizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.selection_was_made = False
        self.__names = {"Name": "", "Comment": ""}
        self.__data_class = data_base_instance

        if not isinstance(self.__data_class, ParametersDataBase):
            raise SystemExit(f"Объекту {self} передан некорректный объект {ParametersDataBase}")

        self.__list_items = data_base_instance.get_user_data(title)
        self.__title = title
        self.__init_UI()
        self.__page_number = page_number
        self.__cur_sel_item = 0

    def __init_UI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, self.__title)
        title.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
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
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDoubleClick, id=self.list.GetId())

    def get_page_number(self):
        return self.__page_number
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

            self.__data_class.set_user_data(self.__title, selected_item,
                                            (self.__names['Name'], self.__names['Comment']), append=False)


            # Debug ---> self.__data_class.show_user_data(self.__title)
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

            self.__data_class.set_user_data(self.__title, -1, (self.__names['Name'], self.__names['Comment']))
            # Debug --->
            self.__data_class.show_user_data(self.__title)

            self.__names['Name'] = ""
            self.__names['Comment'] = ""

        ex.Destroy()

    def OnDoubleClick(self, event):
        self.OnSelect(event)

    def OnSelect(self, event):
        # Снятие выделения с ранее выбранного элемента
        if self.__cur_sel_item < self.list.GetItemCount():
            self.list.SetItemTextColour(self.__cur_sel_item, wx.Colour("black"))

        selected_item = self.list.GetFirstSelected()
        self.__cur_sel_item = selected_item

        if self.__cur_sel_item != -1:
            # Активировать кнопку "Далее"
            self.FindWindowById(wx.ID_FORWARD).Enable()

            self.__cur_sel_item = selected_item
            text = self.list.GetItemText(self.__cur_sel_item, col=0)
            # Debug --->print(f"Selected ITEM: {text}, index: {self.__cur_sel_item}")
            # Выделение выбранного элемента
            self.list.SetItemTextColour(self.__cur_sel_item, wx.Colour("red"))

            # Добавление очередной части кода
            self.__data_class.add_part_to_software_code(self.__page_number, text)

            self.selection_was_made = True
            # Debug --->print(f"code:{self.__data_class.get_software_code()}")
        else:
            self.FindWindowById(wx.ID_FORWARD).Disable()

    def OnDelete(self, event):
        selected_item = self.list.GetFirstSelected()
        if selected_item != -1:
            self.list.DeleteItem(selected_item)
            self.__data_class.delete_user_data(self.__title, selected_item)

            # Debug --->
            self.__data_class.show_user_data(self.__title)
            if self.list.GetItemCount() > 0:
                self.list.Select(selected_item - 1)

    def SetNext(self, next):
        self.next = next

    # ----------------------------------------------------------------------
    def SetPrev(self, prev):
        self.prev = prev

    # ----------------------------------------------------------------------
    def GetNext(self):
        return self.next

    # ----------------------------------------------------------------------
    def GetPrev(self):
        return self.prev
