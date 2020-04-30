import wx
import wx.adv

import bookMarks
import chrome2excel
import chromeProfile

import tools
from tools import add

date_added = "Date Added"
date_modified = "Date Modified"
date_visited = "Date Visited"
url_name = "URL Name"
url_clean = "URL Clean"
original_url = "URL Address"
url_hostname = "Hostname"
folder_name = "Folder"


class MainUrlPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        main_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}
        self.list_ctrl = wx.ListCtrl(self, size=(10, 500), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        #######################################################################################
        # TODO: SAVE COLUMNS WIDTH
        #######################################################################################
        # TODO: SELECT COLUMNS TO SHOW IN SETTINGS
        #######################################################################################
        # TODO: MERGE TXT ROWS TO CHROME ROWS IF IMPORT TXT OPTION IS SELECTED
        #######################################################################################
        index = [-1]

        self.list_ctrl.InsertColumn(add(index), date_added, width=200)
        self.list_ctrl.InsertColumn(add(index), date_modified, width=200)
        self.list_ctrl.InsertColumn(add(index), date_visited, width=200)
        self.list_ctrl.InsertColumn(add(index), folder_name, width=200)
        self.list_ctrl.InsertColumn(add(index), url_name, width=200)
        self.list_ctrl.InsertColumn(add(index), url_clean, width=200)
        self.list_ctrl.InsertColumn(add(index), original_url, width=200)
        self.list_ctrl.InsertColumn(add(index), url_hostname, width=200)

        main_box_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        main_box_sizer.AddStretchSpacer()

        edit_button = wx.Button(self, label='Edit')
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        html_button = wx.Button(self, label='Export to HTML')
        html_button.Bind(wx.EVT_BUTTON, self.on_html)
        xlsx_button = wx.Button(self, label='Export to XLSX')
        xlsx_button.Bind(wx.EVT_BUTTON, self.on_xlsx)

        #######################################################################################
        # TODO: KEEP BUTTON RATIO WHEN SCREEN IS MAXIMIZED
        #######################################################################################
        button_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_box_sizer.Add(edit_button, 1, wx.EXPAND)
        button_box_sizer.Add(html_button, 1, wx.EXPAND)
        button_box_sizer.Add(xlsx_button, 1, wx.EXPAND)
        main_box_sizer.Add(button_box_sizer, 1, wx.EXPAND)

        self.SetSizer(main_box_sizer)

    def on_html(self, event):
        #######################################################################################
        # TODO: https://wxpython.org/Phoenix/docs/html/wx.GenericProgressDialog.html
        #######################################################################################
        tools.display("_______________")
        tools.display("HTML SETUP")
        tools.display("reload:", self.parent.refresh_url_title)
        tools.display("undupe:", self.parent.remove_duplicates)
        tools.display("clean:", self.parent.remove_tracking_tokens_from_url)
        tools.display("txt:", self.parent.import_txt)
        #######################################################################################
        # TODO: MUST CHECK IF WORKBOOK IS DONE FOR GENERATION
        #######################################################################################
        # TODO: Generate HTML
        #######################################################################################
        # chrome2excel.generate_html(refresh, undupe, clean, input)

    def on_xlsx(self, event):
        tools.display("_______________")
        tools.display("XLSX SETUP")
        tools.display("reload:", self.parent.refresh_url_title)
        tools.display("undupe:", self.parent.remove_duplicates)
        tools.display("clean:", self.parent.remove_tracking_tokens_from_url)
        #######################################################################################
        # TODO: MUST CHECK IF WORKBOOK IS DONE FOR GENERATION
        #######################################################################################
        # TODO: Generate XLSX
        #######################################################################################
        # chrome2excel.generate_workbook(refresh, undupe, clean)

    def on_edit(self, event):
        selected_item = self.list_ctrl.GetFocusedItem()
        if selected_item >= 0:
            edit_dialog = EditDialog(self.row_obj_dict[selected_item])
            edit_dialog.ShowModal()
            self.update_url_listing(self.current_folder_path)
            edit_dialog.Destroy()

    def update_url_listing(self, folder_path):
        self.current_folder_path = folder_path
        self.list_ctrl.ClearAll()
        index = [-1]
        self.list_ctrl.InsertColumn(add(index), date_added, width=115)
        self.list_ctrl.InsertColumn(add(index), date_modified, width=118)
        self.list_ctrl.InsertColumn(add(index), date_visited, width=120)
        self.list_ctrl.InsertColumn(add(index), folder_name, width=150)
        self.list_ctrl.InsertColumn(add(index), url_name, width=150)
        self.list_ctrl.InsertColumn(add(index), url_clean, width=150)
        self.list_ctrl.InsertColumn(add(index), original_url, width=150)
        self.list_ctrl.InsertColumn(add(index), url_hostname, width=150)

        url_list = chrome2excel.generate_from_txt(chrome2excel.import_text_file(folder_path))
        self.update_list(url_list)

    def update_list(self, url_list):
        index = 0
        url_objects = []
        #######################################################################################
        # TODO: Using Class Header no need of strip url_list[header:]
        #######################################################################################
        for url in url_list[1:]:
            position = [0]
            #######################################################################################
            # TODO: May change from index to dict key
            #######################################################################################
            self.list_ctrl.InsertItem(index, tools.date_to_string(url[13]))  # 'URL Added',       #13
            self.list_ctrl.SetItem(index, add(position), tools.date_to_string(url[14]))  # 'URL Modified',    #14
            self.list_ctrl.SetItem(index, add(position), tools.date_to_string(url[15]))  # 'URL Visited',     #15
            self.list_ctrl.SetItem(index, add(position), url[7])  # 'Folder Name',     #07
            self.list_ctrl.SetItem(index, add(position), url[16])  # 'URL Name',        #16
            self.list_ctrl.SetItem(index, add(position), url[17])  # 'URL Clean',       #17
            self.list_ctrl.SetItem(index, add(position), url[18])  # 'URL',             #18
            self.list_ctrl.SetItem(index, add(position), url[21])  # 'Hostname',        #21
            #######################################################################################
            # TODO: Sync list_ctrl with url_object data
            #######################################################################################
            url_object = bookMarks.TemporaryObject([tools.date_to_string(url[13]),
                                                    tools.date_to_string(url[14]),
                                                    tools.date_to_string(url[15]),
                                                    url[7],
                                                    url[16],
                                                    url[17],
                                                    url[18],
                                                    url[21]])
            url_objects.append(url_object)
            self.row_obj_dict[index] = url_object
            index += 1


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,
                          parent=None,
                          title='Bookmarks Editor',
                          size=(1200, 600))
        self.settings = bookMarks.Options()
        self.settings.load_settings()
        self.selected = -1
        self.panel = MainUrlPanel(self)
        self.create_menu()
        self.Show()

    def create_menu(self):
        #######################################################################################
        # TODO: http://zetcode.com/wxpython/menustoolbars/
        #######################################################################################
        menu_bar = wx.MenuBar()
        options_menu = wx.Menu()

        open_account_menu_item = options_menu.Append(wx.ID_ANY, 'Import &Account', 'Import Account from Chrome')
        open_folder_menu_item = options_menu.Append(wx.ID_ANY, 'Open &File', 'Open a text file with URLs')
        open_settings_menu_item = options_menu.Append(wx.ID_ANY, '&Settings', 'Set options on/off')
        open_exit_menu_item = options_menu.Append(wx.ID_ANY, '&Exit', 'Set options on/off')

        menu_bar.Append(options_menu, '&Options')

        self.Bind(event=wx.EVT_MENU, handler=self.on_open_account, source=open_account_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_folder_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_settings, source=open_settings_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_exit, source=open_exit_menu_item)

        about_menu = wx.Menu()
        open_about_menu_item = about_menu.Append(wx.ID_ANY, '&About', 'About software')
        menu_bar.Append(about_menu, '&About')
        self.Bind(event=wx.EVT_MENU, handler=self.on_about, source=open_about_menu_item)

        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        wildcard = "Text file (*.txt)|*.txt"
        open_folder_dialog = wx.FileDialog(self,
                                           message="Choose a file:",
                                           defaultFile="chrome.txt",
                                           wildcard=wildcard,
                                           style=wx.DD_DEFAULT_STYLE)
        if open_folder_dialog.ShowModal() == wx.ID_OK:
            self.panel.update_url_listing(open_folder_dialog.GetPath())
        open_folder_dialog.Destroy()

    def on_open_account(self, event):
        profile_chooser_dialog = ProfileChooser(self, -1)
        button_pressed = profile_chooser_dialog.ShowModal()
        if button_pressed == wx.ID_OK:
            #######################################################################################
            # TODO: Load bookmars from Chrome profile
            #######################################################################################
            tools.display("Loading Bookmarks...")
            data_table = bookMarks.generate_data(bookMarks.generate_bookmarks(self.selected))
            self.panel.update_list(data_table)
            self.panel.Update()
        else:
            self.selected = -1
        profile_chooser_dialog.Destroy()

    def on_open_settings(self, event):
        settings_dialog = SettingsDialog(self, 0)
        settings_dialog.ShowModal()
        settings_dialog.Destroy()

    def on_about(self, event):
        AboutDialog(self)

    def on_open_exit(self, event):
        #######################################################################################
        # TODO: EXIT CONFIRMATION SHOW NEXT TICKER
        #######################################################################################
        exit_dialog = wx.MessageDialog(self,
                                       "Want to exit?",
                                       "Exit",
                                       wx.YES_NO | wx.ICON_QUESTION)
        if exit_dialog.ShowModal() == wx.ID_YES:
            self.Destroy()
        exit_dialog.Destroy()
        # self.Close(True)


class AboutDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        about_application = wx.adv.AboutDialogInfo()
        about_application.Name = "Chrome Exporter"
        about_application.Version = "1.0"
        about_application.Copyright = "OTDS H Co."
        about_application.Description = "This Python Application helps you to convert your Google Bookmarks to" \
                                        " a Microsoft Excel Spreadsheet." \
                                        "\n\nHow it works:\n\nThis software access your Google Chrome Bookmarks " \
                                        "and dump database to Excel Spreadsheet format." \
                                        "\nIt also has features regarding to clean URLs, stripping tracking tokens."
        about_application.WebSite = ("https://github.com/vliopard/chrome2excel",
                                     "Chrome Bookmarks to Microsoft Excel")
        about_application.Developers = ["Vincent Liopard."]
        about_application.License = "This is an Open Source Project that uses other General Public License (GPL) " \
                                    "sources from the web."
        about_application.SetTranslators = ["Vincent Liopard."]

        wx.adv.AboutBox(about_application)


class EditDialog(wx.Dialog):
    def __init__(self, edit_url):
        date_visited_title = f'Editing "{edit_url.date_visited}"'
        super().__init__(parent=None, title=date_visited_title)
        self.url = edit_url
        self.main_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.date_added = wx.TextCtrl(self, value=self.url.date_added)
        self.add_widgets(date_added, self.date_added)
        self.date_modified = wx.TextCtrl(self, value=self.url.date_modified)
        self.add_widgets(date_modified, self.date_modified)
        self.date_visited = wx.TextCtrl(self, value=self.url.date_visited)
        self.add_widgets(date_visited_title, self.date_visited)
        button_box_sizer = wx.BoxSizer()
        save_button = wx.Button(self, label='Save')
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        button_box_sizer.Add(save_button, 0, wx.ALL, 5)
        button_box_sizer.Add(wx.Button(self, id=wx.ID_CANCEL), 0, wx.ALL, 5)
        self.main_box_sizer.Add(button_box_sizer, 0, wx.CENTER)
        self.SetSizer(self.main_box_sizer)

    def add_widgets(self, text_label, text_ctrl):
        box_sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label=text_label, size=(50, -1))
        box_sizer_horizontal.Add(label, 0, wx.ALL, 5)
        box_sizer_horizontal.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.main_box_sizer.Add(box_sizer_horizontal, 0, wx.EXPAND)

    def on_save(self, event):
        self.url.date_added = self.date_added.GetValue()
        self.url.date_modified = self.date_modified.GetValue()
        self.url.date_visited = self.date_visited.GetValue()
        self.url.save()
        self.Close()


class ProfileChooser(wx.Dialog):
    def __init__(self, parent, id_, title="Profile Chooser", size=(600, 600)):
        wx.Dialog.__init__(self, parent, id_, title)

        profile_chooser_panel = wx.Panel(self)
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)
        chrome_profile_list = chromeProfile.profile_list()

        self.parent = parent
        self.parent.selected = 0

        position = 10
        if chrome_profile_list:
            vertical_box_sizer.Add(wx.RadioButton(profile_chooser_panel, 0, label=chrome_profile_list[0][1], pos=(10, 10), style=wx.RB_GROUP))
            for profile in chrome_profile_list[1:]:
                position = position + 20
                vertical_box_sizer.Add(wx.RadioButton(profile_chooser_panel, profile[0], label=profile[1], pos=(10, position)))

            self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_group)

            position = position + 30
            vertical_box_sizer.Add(wx.Button(profile_chooser_panel, wx.ID_OK, " OK ", pos=(10, position)))
        else:
            vertical_box_sizer.Add(wx.StaticText(profile_chooser_panel, wx.ID_ANY, label="No account installed on Chrome", pos=(10, position)))
            position = position + 30

        vertical_box_sizer.Add(wx.Button(profile_chooser_panel, wx.ID_CANCEL, " Cancel ", pos=(130, position)))

        self.Centre()
        self.Show(True)

    def on_radio_group(self, event):
        event_object = event.GetEventObject()
        self.parent.selected = event_object.GetId()


class SettingsDialog(wx.Dialog):
    def __init__(self, parent, id_, title="Settings"):
        wx.Dialog.__init__(self, parent, id_, title)

        self.parent = parent

        self.SetSize((320, 190))
        button_size = (135, 25)

        settings_button_label, settings_button_value = set_button_toggle(self, 0, False)
        self.toggle_button01 = wx.ToggleButton(self, id=0, label=settings_button_label, size=button_size, pos=(10, 10), style=wx.BU_LEFT)
        self.toggle_button01.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 1, False)
        self.toggle_button02 = wx.ToggleButton(self, id=1, label=settings_button_label, size=button_size, pos=(10, 40), style=wx.BU_LEFT)
        self.toggle_button02.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 2, False)
        self.toggle_button03 = wx.ToggleButton(self, id=2, label=settings_button_label, size=button_size, pos=(10, 70), style=wx.BU_LEFT)
        self.toggle_button03.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 3, False)
        self.toggle_button04 = wx.ToggleButton(self, id=3, label=settings_button_label, size=button_size, pos=(150, 10), style=wx.BU_LEFT)
        self.toggle_button04.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 4, False)
        self.toggle_button05 = wx.ToggleButton(self, id=4, label=settings_button_label, size=button_size, pos=(150, 40), style=wx.BU_LEFT)
        self.toggle_button05.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 5, False)
        self.toggle_button06 = wx.ToggleButton(self, id=5, label=settings_button_label, size=button_size, pos=(150, 70), style=wx.BU_LEFT)
        self.toggle_button06.SetValue(settings_button_value)

        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_radio_group)

        self.ok_button = wx.Button(self, wx.ID_OK, " OK ", size=button_size, pos=(70, 120))
        self.Centre()
        self.Show(True)

    def on_radio_group(self, event):
        event_object = event.GetEventObject()
        label, value = set_button_toggle(self, event_object.GetId(), True)
        event_object.SetLabel(label)
        event_object.SetValue(value)
        self.parent.settings.save_settings()


def set_button_toggle(self, button_id, toggle_button):
    settings_button_label = None
    settings_button_value = None
    if button_id == 0:
        if toggle_button:
            self.parent.settings.export_file_type = not self.parent.settings.export_file_type
        if self.parent.settings.export_file_type:
            settings_button_label = " [html]  Output type"
            settings_button_value = True
        else:
            settings_button_label = " [xlsx] Output type"
            settings_button_value = False
    if button_id == 1:
        if toggle_button:
            self.parent.settings.refresh_url_title = not self.parent.settings.refresh_url_title
        if self.parent.settings.refresh_url_title:
            settings_button_label = " [ON]  Refresh URL"
            settings_button_value = True
        else:
            settings_button_label = " [off] Refresh URL"
            settings_button_value = False
    if button_id == 2:
        if toggle_button:
            self.parent.settings.remove_duplicated_urls = not self.parent.settings.remove_duplicated_urls
        if self.parent.settings.remove_duplicated_urls:
            settings_button_label = " [ON]  Undupe URLs"
            settings_button_value = True
        else:
            settings_button_label = " [off] Undupe URLs"
            settings_button_value = False
    if button_id == 3:
        if toggle_button:
            self.parent.settings.remove_tracking_tokens_from_url = not self.parent.settings.remove_tracking_tokens_from_url
        if self.parent.settings.remove_tracking_tokens_from_url:
            settings_button_label = " [ON]  Clean URL"
            settings_button_value = True
        else:
            settings_button_label = " [off] Clean URL"
            settings_button_value = False
    if button_id == 4:
        if toggle_button:
            self.parent.settings.import_urls_from_text_file = not self.parent.settings.import_urls_from_text_file
        if self.parent.settings.import_urls_from_text_file:
            settings_button_label = " [ON]  Import TXT"
            settings_button_value = True
        else:
            settings_button_label = " [off] Import TXT"
            settings_button_value = False
    if button_id == 5:
        if toggle_button:
            self.parent.settings.refresh_folder_name_with_hostname_title = not self.parent.settings.refresh_folder_name_with_hostname_title
        if self.parent.settings.refresh_folder_name_with_hostname_title:
            settings_button_label = " [ON]  Check hostname"
            settings_button_value = True
        else:
            settings_button_label = " [off] Check hostname"
            settings_button_value = False
    return settings_button_label, settings_button_value


if __name__ == '__main__':
    application = wx.App(False)
    application_frame = MainFrame()
    application.MainLoop()
