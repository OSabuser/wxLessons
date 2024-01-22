import os
from gen_wizard import wx, CodeGenerationWizard, CodeGenerationWizardPage
from usr_data import ParametersDataBase
import configparser

def main():
    config = configparser.ConfigParser()

    config.read('code_database.ini', encoding="utf-8")

    tester = ParametersDataBase()

    # Считывание данных посекционно в объект - базу-данных tester
    for section in config.sections():
        tester.add_user_data(section, [(key.upper(), config[section][key]) for key in config[section]])

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
        #debug --> print(tester.show_user_data(config.sections()[0]))

        # Запись изменений в файл
        config = configparser.ConfigParser()

        for key in tester.get_all_keys():
            config[key] = {}
            for data in tester.get_user_data(key):
                config[key][data[0]] = data[1]

        with open('code_database.ini', 'w', encoding="utf-8") as configfile:
            config.write(configfile)

    wizard.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    main()
