from selection_windows import CodeSelection
from wx import App

def main():
    app = App()

    data = [('TFT', 'TFT дисплеи'), ('LCD', 'ЖКИ'),
            ('DOT', 'Точечные индикаторы'), ('GPI', 'Имитатор протоколов СУЛ'),
            ('MODB', 'Modbus to CAN конвертер')]

    CodeSelection(None, "ОБОЗНАЧЕНИЕ", data)
    app.MainLoop()


if __name__ == '__main__':
    main()
