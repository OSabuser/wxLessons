class DataTest:
    def __init__(self):
        self.__user_data = {}

    def add_user_data(self, key, data):
        if key not in self.__user_data.keys():
            self.__user_data[key] = data
        else:
            print(f"Данные с ключом {key} уже существуют!")

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