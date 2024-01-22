
from gen_wizard import wx, CodeGenerationWizard, CodeGenerationWizardPage
from usr_data import ParametersDataBase
import configparser


def main():
    tester = ParametersDataBase('code_database.ini')

    pages = []

    app = wx.App()
    wizard = CodeGenerationWizard(None, wx.ID_ANY, "Software S/N Gen v1.0")

    # Создание страниц wx.adv.wizard, заполнение их данными из файла code_database
    for idx, key in enumerate(tester.get_all_keys()):
        pages.append(CodeGenerationWizardPage(wizard, key, tester, idx))

    wizard.FitToPage(pages[0])

    # Set the initial order of the pages
    for number in range(len(pages) - 1):
        pages[number].SetNext(pages[number + 1])
        pages[number + 1].SetPrev(pages[number])

    wizard.GetPageAreaSizer().Add(pages[0])
    state = wizard.RunWizard(pages[0])

    # Работа объекта CodeGenerationWizard завершена!
    if state:
        print(f"Шифр ПО:  {'.'.join(tester.get_software_code())}")
        # debug --> print(tester.show_user_data(config.sections()[0]))

        # Запись изменений в файл
        tester.save_changes()

    wizard.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    main()
