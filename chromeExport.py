import wx
import wx.adv
import tools
import bookMarks
import chromeProfile
import chrome2excel
from configparser import ConfigParser, DuplicateSectionError


date_added = "Date Added"
date_modified = "Date Modified"
date_visited = "Date Visited"
url_name = "URL Name"
url_clean = "URL Clean"
original_url = "URL Address"
url_hostname = "Hostname"


class urlPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}
        self.list_ctrl = wx.ListCtrl(self, size=(10, 500), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        # TODO: SAVE COLUMNS WIDTH
        # TODO: SELECT COLUMNS TO SHOW IN SETTINGS
        # TODO: MERGE TXT ROWS TO CHROME ROWS IF IMPORT TXT OPTION IS SELECTED
        self.list_ctrl.InsertColumn(0, date_added, width=200)
        self.list_ctrl.InsertColumn(1, date_modified, width=200)
        self.list_ctrl.InsertColumn(2, date_visited, width=200)
        self.list_ctrl.InsertColumn(3, url_name, width=200)
        self.list_ctrl.InsertColumn(4, url_clean, width=200)
        self.list_ctrl.InsertColumn(5, original_url, width=200)
        self.list_ctrl.InsertColumn(6, url_hostname, width=200)

        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.AddStretchSpacer()

        edit_button = wx.Button(self, label='Edit')
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        html_button = wx.Button(self, label='Export to HTML')
        html_button.Bind(wx.EVT_BUTTON, self.on_html)
        xlsx_button = wx.Button(self, label='Export to XLSX')
        xlsx_button.Bind(wx.EVT_BUTTON, self.on_xlsx)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(edit_button, 1, wx.EXPAND)
        box.Add(html_button, 1, wx.EXPAND)
        box.Add(xlsx_button, 1, wx.EXPAND)
        main_sizer.Add(box, 1, wx.EXPAND)

        self.SetSizer(main_sizer)

    def on_html(self, event):
        # TODO: https://wxpython.org/Phoenix/docs/html/wx.GenericProgressDialog.html
        print("_______________")
        print("HTML SETUP")
        print("reload:", self.parent.reload_title)
        print("undupe:", self.parent.remove_duplicates)
        print("clean:", self.parent.clean_url)
        print("txt:", self.parent.import_txt)
        # TODO: MUST CHECK IF WORKBOOK IS DONE FOR GENERATION
        # TODO: Generate HTML
        # chrome2excel.generate_html(refresh, undupe, clean, input)

    def on_xlsx(self, event):
        print("_______________")
        print("XLSX SETUP")
        print("reload:", self.parent.reload_title)
        print("undupe:", self.parent.remove_duplicates)
        print("clean:", self.parent.clean_url)
        # TODO: MUST CHECK IF WORKBOOK IS DONE FOR GENERATION
        # TODO: Generate XLSX
        # chrome2excel.generate_workbook(refresh, undupe, clean)

    def on_edit(self, event):
        selection = self.list_ctrl.GetFocusedItem()
        if selection >= 0:
            url = self.row_obj_dict[selection]
            dlg = EditDialog(url)
            dlg.ShowModal()
            self.update_url_listing(self.current_folder_path)
            dlg.Destroy()

    def update_url_listing(self, folder_path):
        self.current_folder_path = folder_path
        self.list_ctrl.ClearAll()
        self.list_ctrl.InsertColumn(0, date_added, width=115)
        self.list_ctrl.InsertColumn(1, date_modified, width=118)
        self.list_ctrl.InsertColumn(2, date_visited, width=120)
        self.list_ctrl.InsertColumn(3, url_name, width=150)
        self.list_ctrl.InsertColumn(4, url_clean, width=150)
        self.list_ctrl.InsertColumn(5, original_url, width=150)
        self.list_ctrl.InsertColumn(6, url_hostname, width=150)
        url_list = []
        url_list = chrome2excel.generate_from_txt(chrome2excel.import_txt(folder_path))
        self.update_list(url_list)

    def update_list(self, url_list):
        index = 0
        url_objects = []
        for url in url_list[1:]:
            self.list_ctrl.InsertItem(index, tools.stringDate(url[13]))  # 'URL Added',       #13
            self.list_ctrl.SetItem(index, 1, tools.stringDate(url[14]))  # 'URL Modified',    #14
            self.list_ctrl.SetItem(index, 2, tools.stringDate(url[15]))  # 'URL Visited',     #15
            self.list_ctrl.SetItem(index, 3, url[16])                    # 'URL Name',        #16
            self.list_ctrl.SetItem(index, 4, url[17])                    # 'URL Clean',       #17
            self.list_ctrl.SetItem(index, 5, url[18])                    # 'URL',             #18
            self.list_ctrl.SetItem(index, 6, url[21])                    # 'Hostname',        #21
            # TODO: Sync list_ctrl with url_object data
            url_object = bookMarks.nobj(tools.stringDate(url[13]),
                                        tools.stringDate(url[14]),
                                        tools.stringDate(url[15]),
                                        url[16],
                                        url[17],
                                        url[18],
                                        url[21])
            url_objects.append(url_object)
            self.row_obj_dict[index] = url_object
            index += 1


class urlFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None,
                          title='Bookmarks Editor',
                          size=(1200, 600))

        self.export_file_type = False
        self.reload_title = False
        self.remove_duplicates = False
        self.clean_url = False
        self.import_txt = False

        loadSettings(self)

        self.selected = -1

        self.panel = urlPanel(self)
        self.create_menu()
        self.Show()

    def create_menu(self):
        # TODO: http://zetcode.com/wxpython/menustoolbars/
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        open_account_menu_item = file_menu.Append(wx.ID_ANY, 'Import &Account', 'Import Account from Chrome')
        open_folder_menu_item = file_menu.Append(wx.ID_ANY, 'Open &File', 'Open a text file with URLs')
        open_settings_menu_item = file_menu.Append(wx.ID_ANY, '&Settings', 'Set options on/off')
        open_exit_menu_item = file_menu.Append(wx.ID_ANY, '&Exit', 'Set options on/off')

        menu_bar.Append(file_menu, '&Options')

        self.Bind(event=wx.EVT_MENU, handler=self.on_open_account, source=open_account_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_folder_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_settings, source=open_settings_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_exit, source=open_exit_menu_item)

        file_menu2 = wx.Menu()
        open_about_menu_item = file_menu2.Append(wx.ID_ANY, '&About', 'About software')
        menu_bar.Append(file_menu2, '&About')
        self.Bind(event=wx.EVT_MENU, handler=self.on_about, source=open_about_menu_item)

        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        wildcard = "Text file (*.txt)|*.txt"
        dlg = wx.FileDialog(self,
                            message="Choose a file:",
                            defaultFile="chrome.txt",
                            wildcard=wildcard,
                            style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_url_listing(dlg.GetPath())
        dlg.Destroy()

    def on_open_account(self, event):
        dlg = MyDialog(self, -1)
        retval = dlg.ShowModal()
        if retval == wx.ID_OK:
            # TODO: Load bookmars from Chrome profile
            print("Loading Bookmarks...")
            url_data = bookMarks.generate_data(bookMarks.generate_bookmarks(self.selected))
            self.panel.update_list(url_data)
            self.panel.Update()
        else:
            self.selected = -1
        dlg.Destroy()

    def on_open_settings(self, event):
        dlg = SettingsDialog(self, -1)
        dlg.ShowModal()
        dlg.Destroy()

    def on_about(self, event):
        AboutDialog()

    def on_open_exit(self, event):
        dlg = wx.MessageDialog(self,
                               "Want to exit?",
                               "Exit",
                               wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Destroy()
        dlg.Destroy()
        # self.Close(True)


class AboutDialog(wx.Dialog):
    def __init__(self):
        info = wx.adv.AboutDialogInfo()
        info.Name = "Chrome Exporter"
        info.Version = "1.0"
        info.Copyright = "OTDS H Co."
        info.Description = "This Python Application helps you to convert your Google Bookmarks to" \
                           " a Microsoft Excel Spreadsheet." \
                           "\n\nHow it works:\n\nThis software access your Google Chrome Bookmarks "\
                           "and dump database to Excel Spreadsheet format." \
                           "\nIt also has features regarding to clean URLs, stripping tracking tokens."
        info.WebSite = ("https://github.com/vliopard/chrome2excel",
                        "Chrome Bookmarks to Microsoft Excel")
        info.Developers = ["Vincent Liopard."]
        info.License = "This is an Open Source Project that uses other General Public License (GPL) " \
                       "sources from the web."

        wx.adv.AboutBox(info)


class EditDialog(wx.Dialog):
    def __init__(self, url):
        date_visited = f'Editing "{url.date_visited}"'
        super().__init__(parent=None, title=date_visited)
        self.url = url
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.date_added = wx.TextCtrl(self, value=self.url.date_added)
        self.add_widgets(date_added, self.date_added)
        self.date_modified = wx.TextCtrl(self, value=self.url.date_modified)
        self.add_widgets(date_modified, self.date_modified)
        self.date_visited = wx.TextCtrl(self, value=self.url.date_visited)
        self.add_widgets(date_visited, self.date_visited)
        btn_sizer = wx.BoxSizer()
        save_btn = wx.Button(self, label='Save')
        save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        btn_sizer.Add(save_btn, 0, wx.ALL, 5)
        btn_sizer.Add(wx.Button(self, id=wx.ID_CANCEL), 0, wx.ALL, 5)
        self.main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(self.main_sizer)

    def add_widgets(self, label_text, text_ctrl):
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label=label_text, size=(50, -1))
        row_sizer.Add(label, 0, wx.ALL, 5)
        row_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.main_sizer.Add(row_sizer, 0, wx.EXPAND)

    def on_save(self, event):
        self.url.date_added = self.date_added.GetValue()
        self.url.date_modified = self.date_modified.GetValue()
        self.url.date_visited = self.date_visited.GetValue()
        self.url.save()
        self.Close()


class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title="Profile Chooser", size=(600, 600)):
        wx.Dialog.__init__(self, parent, id, title)

        pnl = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        my_list = chromeProfile.profile_list()

        self.parent = parent
        self.parent.selected = 0
        position = 10
        if my_list:
            sizer.Add(wx.RadioButton(pnl, 0, label=my_list[0], pos=(10, 10), style=wx.RB_GROUP))
            for nro, x in enumerate(my_list[1:]):
                position = position + 20
                sizer.Add(wx.RadioButton(pnl, nro+1, label=x, pos=(10, position)))

            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)

            position = position + 20
            sizer.Add(wx.Button(pnl, wx.ID_OK, " OK ", pos=(10, position)))
        else:
            sizer.Add(wx.StaticText(pnl, wx.ID_ANY, label="No account installed on Chrome", pos=(10, position)))
            position = position + 30

        sizer.Add(wx.Button(pnl, wx.ID_CANCEL, " Cancel ", pos=(130, position)))

        self.Centre()
        self.Show(True)

    def OnRadiogroup(self, e):
        rb = e.GetEventObject()
        self.myval = rb.GetId()
        self.parent.selected = rb.GetId()


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, id, title="Settings", size=(200, 100)):
        wx.Dialog.__init__(self, parent, id, title)

        self.parent = parent

        label, value = setButtonToggle(self, 0, False)
        self.tb1 = wx.ToggleButton(self, id=0, label=label, pos=(10, 10))
        self.tb1.SetValue(value)

        label, value = setButtonToggle(self, 1, False)
        self.tb2 = wx.ToggleButton(self, id=1, label=label, pos=(10, 40))
        self.tb2.SetValue(value)

        label, value = setButtonToggle(self, 2, False)
        self.tb3 = wx.ToggleButton(self, id=2, label=label, pos=(10, 70))
        self.tb3.SetValue(value)

        label, value = setButtonToggle(self, 3, False)
        self.tb4 = wx.ToggleButton(self, id=3, label=label, pos=(10, 100))
        self.tb4.SetValue(value)

        label, value = setButtonToggle(self, 4, False)
        self.tb5 = wx.ToggleButton(self, id=4, label=label, pos=(10, 130))
        self.tb5.SetValue(value)

        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnRadiogroup)

        self.btn = wx.Button(self, wx.ID_OK, " OK ", pos=(10, 160))
        self.Centre()
        self.Show(True)

    def OnRadiogroup(self, e):
        rb = e.GetEventObject()
        label, value = setButtonToggle(self, rb.GetId(), True)
        rb.SetLabel(label)
        rb.SetValue(value)
        saveSettings(self.parent)


def setButtonToggle(self, btnId, toggle):
    label = None
    if btnId == 0:
        if toggle:
            self.parent.export_file_type = not self.parent.export_file_type
        if self.parent.export_file_type:
            label = "[html]  Output type"
            value = True
        else:
            label = "[xlsx] Output type"
            value = False
    if btnId == 1:
        if toggle:
            self.parent.reload_title = not self.parent.reload_title
        if self.parent.reload_title:
            label = "[on]  Refresh URL"
            value = True
        else:
            label = "[off] Refresh URL"
            value = False
    if btnId == 2:
        if toggle:
            self.parent.undupe_url = not self.parent.undupe_url
        if self.parent.undupe_url:
            label = "[on]  Undupe URLs"
            value = True
        else:
            label = "[off] Undupe URLs"
            value = False
    if btnId == 3:
        if toggle:
            self.parent.clean_url = not self.parent.clean_url
        if self.parent.clean_url:
            label = "[on]  Clean URL"
            value = True
        else:
            label = "[off] Clean URL"
            value = False
    if btnId == 4:
        if toggle:
            self.parent.text_import = not self.parent.text_import
        if self.parent.text_import:
            label = "[on]  Import TXT"
            value = True
        else:
            label = "[off] Import TXT"
            value = False
    return label, value


def saveSettings(settings):
    category = 'main'
    config_file = 'config.ini'
    config = ConfigParser()
    config.read(config_file)
    try:
        config.add_section(category)
    except DuplicateSectionError:
        pass

    config.set(category, 'export_file_type', str(settings.export_file_type))
    config.set(category, 'reload_title', str(settings.reload_title))
    config.set(category, 'remove_duplicates', str(settings.undupe_url))
    config.set(category, 'clean_url', str(settings.clean_url))
    config.set(category, 'import_txt', str(settings.text_import))
    with open(config_file, 'w') as f:
        config.write(f)


def loadSettings(settings):
    category = 'main'
    config_file = 'config.ini'
    config = ConfigParser()
    try:
        config.read(config_file)
        settings.export_file_type = config.getboolean(category, 'export_file_type')
        settings.reload_title = config.getboolean(category, 'reload_title')
        settings.undupe_url = config.getboolean(category, 'remove_duplicates')
        settings.clean_url = config.getboolean(category, 'clean_url')
        settings.text_import = config.getboolean(category, 'import_txt')
    except:
        settings.export_file_type = False
        settings.reload_title = False
        settings.undupe_url = False
        settings.clean_url = False
        settings.text_import = False
    return settings


if __name__ == '__main__':
    app = wx.App(False)
    frame = urlFrame()
    app.MainLoop()
