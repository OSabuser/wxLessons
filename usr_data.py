import os
import configparser


class ParametersDataBase:
    def __init__(self, ini_filename):
        self.__user_data = {}
        self.__software_code = []
        self.__config_file_path = ini_filename
        self.__is_something_changed = False
        self.__parse_ini_data(self.__config_file_path)

    def __parse_ini_data(self, filename):
        if os.path.isfile(filename):
            config = configparser.ConfigParser()
            config.read(filename, encoding="utf-8")
            # Считывание данных посекционно в объект - базу-данных tester
            for section in config.sections():
                self.__add_user_data(section, [(key.upper(), config[section][key]) for key in config[section]])
        else:
            raise SystemExit(f"Не удалось найти файл конфигурации {filename}")

    def save_changes(self):
        if self.__is_something_changed:
            # Запись изменений в файл
            config = configparser.ConfigParser()

            # Создание нового файла
            for key in self.get_all_keys():
                config[key] = {}
                for data in self.get_user_data(key):
                    config[key][data[0]] = data[1]

            with open(self.__config_file_path, 'w', encoding="utf-8") as configfile:
                config.write(configfile)
        else:
            print(f"В файл {self.__config_file_path} не было внесено изменений!")


    def __add_user_data(self, key, data):
        if key not in self.__user_data.keys():
            self.__user_data[key] = data
        else:
            print(f"Данные с ключом {key} уже существуют!")

    def get_software_code(self):
        return self.__software_code

    def show_all_keys(self):
        print(list(self.__user_data.keys()))

    def get_all_keys(self):
        return self.__user_data.keys()

    def add_part_to_software_code(self, idx, part):
        temp = len(self.__software_code)
        if idx < temp:
            self.__software_code[idx] = part
        else:
            self.__software_code.append(part)

    def del_part_from_software_code(self, idx):
        temp = len(self.__software_code)
        if idx < temp:
            del self.__software_code[idx]

    def show_all_user_data(self):
        print(**self.__user_data)

    def show_user_data(self, key):
        if key in self.__user_data.keys():
            print(f"{key}: {self.__user_data[key]}")
        else:
            print(f"Данных с ключом {key} не существует!")

    def get_user_data(self, key):
        if key in self.__user_data.keys():
            return self.__user_data[key]
        else:
            print(f"Данных с ключом {key} не существует!")

    def set_user_data(self, key, idx, val, append=True):
        if key in self.__user_data.keys():
            if append:
                self.__is_something_changed = True
                self.__user_data[key].append(val)
            else:
                if idx < len(self.__user_data[key]):
                    self.__is_something_changed = True
                    self.__user_data[key][idx] = val
                else:
                    print(f"{idx} out of range! Длина списка-value: {len(self.__user_data[key])}")
        else:
            print(f"Данных с ключом {key} не существует!")

    def delete_user_data(self, key, idx):
        if key in self.__user_data.keys():
            if idx < len(self.__user_data[key]):
                self.__is_something_changed = True
                del self.__user_data[key][idx]
            else:
                print(f"{idx} out of range! Длина списка-value: {len(self.__user_data[key])}")
        else:
            print(f"Данных с ключом {key} не существует!")
