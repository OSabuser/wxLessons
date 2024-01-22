import os
from gen_wizard import wx, CodeGenerationWizard, CodeGenerationWizardPage
from usr_data import DataTest

def main():
    app = wx.App()

    data = [('TFT', 'TFT дисплеи'), ('LCD', 'ЖКИ'),
            ('DOT', 'Точечные индикаторы'), ('GPI', 'Имитатор протоколов СУЛ'),
            ('MODB', 'Modbus to CAN конвертер')]

    data2 = [('4', 'TFT'), ('7', 'TFT'),
            ('8', 'TFT'), ('10', 'TFT'),
            ('32', 'LCD'), ('54', 'LCD')]
    tester = DataTest()
    tester.add_user_data("ОБОЗНАЧЕНИЕ", data)
    tester.add_user_data("РАЗМЕР", data2)

    tester.set_user_data("РАЗМЕР", -1, ("Для тестов", "TFT77"))
    tester.set_user_data("ОБОЗНАЧЕНИЕ", 2, ("111", "222"), append=False)

   # tester.show_user_data("ОБОЗНАЧЕНИЕ")
   # tester.show_user_data("РАЗМЕР")

    wizard = CodeGenerationWizard(None, wx.ID_ANY, "Software S/N Gen v1.0")
    page1 = CodeGenerationWizardPage(wizard, "ОБОЗНАЧЕНИЕ", tester)
    page2 = CodeGenerationWizardPage(wizard, "РАЗМЕР", tester)
    #page3 = CodeGenerationWizardPage(wizard, "Выбор типа матрицы", data)

    wizard.FitToPage(page1)

    # Set the initial order of the pages
    page1.SetNext(page2)
    page2.SetPrev(page1)
    #page2.SetNext(page3)
    #page3.SetPrev(page2)

    wizard.GetPageAreaSizer().Add(page1)
    wizard.RunWizard(page1)
    wizard.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    main()
