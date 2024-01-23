from gen_main_window import wx
from usr_data import ParametersDataBase


class DecodeFrame(wx.Frame):
    def __init__(self, parent, title, path_to_icon, serial_number, path_to_database):
        style = wx.SYSTEM_MENU | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX

        wx.Frame.__init__(self, parent, title=title, style=style, size=(490, 250))

        self.SetIcon(wx.Icon(path_to_icon))
        self.path_to_file = path_to_database
        self.Centre()
        self.__panel = DecodePanel(self, serial_number)


class DecodePanel(wx.Panel):
    def __init__(self, parent, serial_number):
        wx.Panel.__init__(self, parent)

        self.parent = parent
        self.database_instance = ParametersDataBase(self.parent.path_to_file)

        if not self.database_instance.is_everything_ok:
            wx.MessageBox(f"Не найден файл {self.parent.path_to_file}!", "Ошибка", wx.ICON_ERROR)
            self.parent.Destroy()
        else:
            # TODO: ОПРЕДЕЛИТЬ ТОЧНЫЙ ФОРМАТ СЕРИЙНОГО НОМЕРА
            if serial_number.count(".") < 1:
                wx.MessageBox(f"Задан неверный формат серийного номера!", "Ошибка", wx.ICON_ERROR)
                self.parent.Destroy()
            else:
                self.__list_items = []
                number_to_decode = serial_number.split(".")
                print(number_to_decode)
                checked_keys = list(self.database_instance.get_all_keys())
                print(checked_keys)
                is_match_found = False

                for idx, key in enumerate(self.database_instance.get_all_keys()):
                    if idx < len(number_to_decode):
                        for element in self.database_instance.get_user_data(key):
                            is_match_found = False

                            if element[0] == number_to_decode[idx]:
                                self.__list_items.append((element[0], element[1]))
                                is_match_found = True
                                break

                        if not is_match_found:
                            self.__list_items.append((f"{number_to_decode[idx]}", "Элемент кода не распознан"))

                    else:
                        self.__list_items.append(("None", "Элемент кода не распознан"))

                static_text_1 = wx.StaticText(self, label="Расшифровка серийного номера")
                static_text_1.SetFont(wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.NORMAL))

                # Введённый пользователем номер
                static_text_2 = wx.StaticText(self, label=serial_number)
                static_text_2.SetFont(wx.Font(16, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.BOLD))

                self.list = wx.ListCtrl(self, wx.ID_ANY,
                                        style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES | wx.LC_HRULES)
                self.list.InsertColumn(0, 'Элемент шифра', width=160)
                self.list.InsertColumn(1, 'Комментарий', width=300)

                list_index = 0
                for item in self.__list_items:
                    current_list_index = self.list.InsertItem(list_index, item[0])  # Добавить имя
                    self.list.SetItem(current_list_index, 1, item[1])  # Добавить комментарий
                    self.list.SetItemFont(current_list_index, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
                    list_index += 1

                vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)
                vertical_box_sizer.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND | wx.TOP, 5)
                vertical_box_sizer.Add(static_text_1, 0, wx.CENTER | wx.TOP, 5)
                vertical_box_sizer.Add(static_text_2, 0, wx.CENTER | wx.TOP, 5)
                vertical_box_sizer.Add(self.list, 0, wx.CENTER | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 5)
                vertical_box_sizer.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND | wx.TOP, 5)
                self.SetSizer(vertical_box_sizer)
                self.Centre()

