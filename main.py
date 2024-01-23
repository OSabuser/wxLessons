from gen_main_window import wx, MainFrame

def main():
    app = wx.App()

    program_name = "Software S/N handler"
    main_window_size = (480, 180)
    base_file_path = "code_database.ini"
    main_icon_path = "app_logo.png"
    version_number = "v. 0.1. (2024-23-01)"

    frame = MainFrame(None, title=program_name, size=main_window_size,
                      path_to_icon=main_icon_path, path_to_database=base_file_path, version=version_number)

    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
