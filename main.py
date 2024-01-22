import os
from gen_wizard import wx, CodeGenerationWizard, CodeGenerationWizardPage
from usr_data import ParametersDataBase


def main():
    app = wx.App()

    data = [('TFT', 'TFT дисплеи'), ('LCD', 'ЖКИ'),
            ('DOT', 'Точечные индикаторы'), ('GPI', 'Имитатор протоколов СУЛ'),
            ('MODB', 'Modbus to CAN конвертер')]

    data2 = [('4', 'TFT'), ('7', 'TFT'),
             ('8', 'TFT'), ('10', 'TFT'),
             ('32', 'LCD'), ('54', 'LCD')]

    data3 = [('01', 'Короткий шлейф'), ('02', 'Длинный шлейф'),
             ('NN', 'Не имеет значения')]

    tester = ParametersDataBase()
    tester.add_user_data("ОБОЗНАЧЕНИЕ", data)
    tester.add_user_data("РАЗМЕР", data2)
    tester.add_user_data("ТИП МАТРИЦЫ", data3)

    tester.set_user_data("РАЗМЕР", -1, ("Для тестов", "TFT77"))
    tester.set_user_data("ОБОЗНАЧЕНИЕ", 2, ("111", "222"), append=False)

    tester.show_user_data("ОБОЗНАЧЕНИЕ")
    tester.show_user_data("РАЗМЕР")

    tester.delete_user_data("ОБОЗНАЧЕНИЕ", 2)
    tester.show_user_data("ОБОЗНАЧЕНИЕ")

    wizard = CodeGenerationWizard(None, wx.ID_ANY, "Software S/N Gen v1.0")
    page1 = CodeGenerationWizardPage(wizard, "ОБОЗНАЧЕНИЕ", tester, 0)
    page2 = CodeGenerationWizardPage(wizard, "РАЗМЕР", tester, 1)
    page3 = CodeGenerationWizardPage(wizard, "ТИП МАТРИЦЫ", tester, 2)

    wizard.FitToPage(page1)

    # Set the initial order of the pages
    page1.SetNext(page2)
    page2.SetPrev(page1)
    page2.SetNext(page3)
    page3.SetPrev(page2)

    wizard.GetPageAreaSizer().Add(page1)
    state = wizard.RunWizard(page1)

    # Работа объекта wizard завершена!
    if state:
        print(f"Шифр ПО:  {'.'.join(tester.get_software_code())}")

    wizard.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    main()
