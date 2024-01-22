import wx


class InputValidator(wx.Validator):
    def __init__(self, value, key):
        wx.Validator.__init__(self)
        self.value = value
        self.key = key

    def Clone(self):
        return InputValidator(self.value, self.key)

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue()
        # TODO: английские символы + цифры!
        if len(text) == 0:
            wx.MessageBox("Поле не должно быть пустым!", "Ошибка")
            textCtrl.SetBackgroundColour("pink")
            textCtrl.SetFocus()
            textCtrl.Refresh()
            return False
        else:
            textCtrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
            textCtrl.Refresh()
            return True

    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        textCtrl.SetValue(self.value.get(self.key, ""))
        return True

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        self.value[self.key] = textCtrl.GetValue()
        return True


class ValueSetupDialog(wx.Dialog):
    def __init__(self, title, input_data):
        wx.Dialog.__init__(self, None, -1, title)
        name_l = wx.StaticText(self, -1, "Имя элемента:")
        comment_l = wx.StaticText(self, -1, "Комментарий:")

        name_t = wx.TextCtrl(self, validator=InputValidator(input_data, "Name"), size=(200, 25))  # , value=name)
        comment_t = wx.TextCtrl(self, validator=InputValidator(input_data, "Comment"),
                                size=(200, 25))  # , value=comment)

        ok = wx.Button(self, wx.ID_OK)
        ok.SetDefault()
        cancel = wx.Button(self, wx.ID_CANCEL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)

        fgs = wx.FlexGridSizer(2, 2, 5, 5)
        fgs.Add(name_l, 1, wx.ALIGN_RIGHT)
        fgs.Add(name_t, 1, wx.EXPAND, 25)
        fgs.Add(comment_l, 1, wx.ALIGN_RIGHT)
        fgs.Add(comment_t, 1, wx.EXPAND)
        sizer.Add(fgs, 1, wx.EXPAND | wx.ALL, 5)

        buttons = wx.StdDialogButtonSizer()
        buttons.AddButton(ok)
        buttons.AddButton(cancel)
        buttons.Realize()
        sizer.Add(buttons, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizerAndFit(sizer)
        self.Centre()
        self.ShowModal()
