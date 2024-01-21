import os

from selection_windows import CodeSelection
import wx
import wx.adv


########################################################################

class TitledPage(wx.adv.WizardPageSimple):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, title):
        """Constructor"""
        wx.adv.WizardPageSimple.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.SetSizer(sizer)

        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND | wx.ALL, 5)


########################################################################
class UseAltBitmapPage(wx.adv.WizardPage):
#--------------------------------------------------
    def __init__(self, parent, title):
        wx.adv.WizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label=title)
        title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.sizer.Add(title)

        self.sizer.Add(wx.StaticText(self, -1, "This page uses a different bitmap"),
                       0, wx.ALL, 5)
        self.sizer.Layout()

    # ----------------------------------------------------------------------
    def SetNext(self, next):
        self.next = next

    # ----------------------------------------------------------------------
    def SetPrev(self, prev):
        self.prev = prev

    # ----------------------------------------------------------------------
    def GetNext(self):
        return self.next

    # ----------------------------------------------------------------------
    def GetPrev(self):
        return self.prev

    # ----------------------------------------------------------------------
    def GetBitmap(self):
        # You usually wouldn't need to override this method
        # since you can set a non-default bitmap in the
        # wxWizardPageSimple constructor, but if you need to
        # dynamically change the bitmap based on the
        # contents of the wizard, or need to also change the
        # next/prev order then it can be done by overriding
        # GetBitmap.
        return
        #return images.WizTest2.GetBitmap()
########################################################################



def main():
    app = wx.App()

    data = [('TFT', 'TFT дисплеи'), ('LCD', 'ЖКИ'),
            ('DOT', 'Точечные индикаторы'), ('GPI', 'Имитатор протоколов СУЛ'),
            ('MODB', 'Modbus to CAN конвертер')]

    #CodeSelection(None, "ОБОЗНАЧЕНИЕ", data)
    wizard = wx.adv.Wizard(None, -1, "Dynamic Wizard")
    page1 = TitledPage(wizard, "Page 1")
    page2 = TitledPage(wizard, "Page 2")
    page3 = TitledPage(wizard, "Page 3")
    page4 = UseAltBitmapPage(wizard, "Page 4")
    page5 = TitledPage(wizard, "Page 5")

    wizard.FitToPage(page1)
    page5.sizer.Add(wx.StaticText(page5, -1, "\nThis is the last page."))

    # Set the initial order of the pages
    page1.SetNext(page2)
    page2.SetPrev(page1)
    page2.SetNext(page3)
    page3.SetPrev(page2)
    page3.SetNext(page4)
    page4.SetPrev(page3)
    page4.SetNext(page5)
    page5.SetPrev(page4)

    wizard.GetPageAreaSizer().Add(page1)
    wizard.RunWizard(page1)
    wizard.Destroy()
    app.MainLoop()


if __name__ == '__main__':
    main()
