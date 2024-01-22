class ParametersDataBase:
    def __init__(self):
        self.__user_data = {}
        self.__software_code = []

    def add_user_data(self, key, data):
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
                self.__user_data[key].append(val)
            else:
                if idx < len(self.__user_data[key]):
                    self.__user_data[key][idx] = val
                else:
                    print(f"{idx} out of range! Длина списка-value: {len(self.__user_data[key])}")
        else:
            print(f"Данных с ключом {key} не существует!")

    def delete_user_data(self, key, idx):
        if key in self.__user_data.keys():
            if idx < len(self.__user_data[key]):
                del self.__user_data[key][idx]
            else:
                print(f"{idx} out of range! Длина списка-value: {len(self.__user_data[key])}")
        else:
            print(f"Данных с ключом {key} не существует!")
