from gen_main_window import wx, MainFrame


def main():
    app = wx.App()

    program_name = "Software S/N handler"
    base_file_path = "code_database.ini"
    main_icon_path = "app_logo.png"
    version_number = "v. A0.1 (2024-23-01)"

    frame = MainFrame(None, title=program_name, path_to_icon=main_icon_path,
                      path_to_database=base_file_path, version=version_number)

    # frame = DecodeFrame(None, program_name, path_to_icon=main_icon_path,
    #                     serial_number="MODB.32.NN.NN.U.NN.NN.06.06.080.NN.NN",
    #                     path_to_database=base_file_path)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
