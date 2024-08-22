import wx
import wx.adv

import tools
import utils
import preset
import locale
import datetime
import bookmarks
import chrome2excel

from wx.lib.mixins import listctrl
from wx.lib.scrolledpanel import ScrolledPanel

locale.setlocale(locale.LC_ALL, preset.SYMBOL_EMPTY)


class ListCtrl(wx.ListCtrl, listctrl.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id_, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, id_, pos, size, style)
        listctrl.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(19)


class MainUrlPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.header = preset.Header()

        self.url_objects = []
        self.list_ctrl = ListCtrl(self, wx.ID_ANY, size=(100, -1), style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        self.save_file_name = None

        #######################################################################################
        # TODO: 01 AUTO SAVE COLUMNS WIDTH
        # TODO: 01 DELETE SELECTED ROW (OR EVEN MULTIPLE SELECTED ROWS)
        # TODO: 01 SELECT COLUMNS TO SHOW IN POPUP MENU https://wiki.wxpython.org/PopupMenuOnRightClick
        # TODO: 01 EDIT ROW ITEMS INPLACE https://www.blog.pythonlibrary.org/2011/01/04/wxpython-wx-listctrl-tips-and-tricks/
        # TODO: 01 SORT ROWS BY CLICKING HEADER https://www.blog.pythonlibrary.org/2011/01/04/wxpython-wx-listctrl-tips-and-tricks/
        #######################################################################################
        self.update_url_screen(False)

        edit_button = wx.Button(self, label=preset.MESSAGE[preset.EDIT])
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)

        html_button = wx.Button(self, label=preset.MESSAGE[preset.EXPORT_HTML])
        html_button.Bind(wx.EVT_BUTTON, self.on_html)

        xlsx_button = wx.Button(self, label=preset.MESSAGE[preset.EXPORT_XLSX])
        xlsx_button.Bind(wx.EVT_BUTTON, self.on_xlsx)

        reset_button = wx.Button(self, label=preset.MESSAGE[preset.RESET_BUTTON])
        reset_button.Bind(wx.EVT_BUTTON, self.on_reset)

        button_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_box_sizer.Add(edit_button, 1)
        button_box_sizer.Add(html_button, 1)
        button_box_sizer.Add(xlsx_button, 1)
        button_box_sizer.Add(reset_button, 1)

        list_control_box_sizer = wx.BoxSizer(wx.VERTICAL)
        list_control_box_sizer.Add(wx.StaticLine(self, wx.HORIZONTAL), 0, wx.EXPAND, 0)
        list_control_box_sizer.Add(self.list_ctrl, 2, wx.ALL | wx.EXPAND, 0)
        list_control_box_sizer.Add(wx.StaticLine(self, wx.HORIZONTAL), 0, wx.EXPAND, 0)
        list_control_box_sizer.Add(button_box_sizer, 0, wx.ALL | wx.EXPAND, 0)
        list_control_box_sizer.Add(wx.StaticLine(self, wx.HORIZONTAL), 0, wx.EXPAND, 0)

        self.SetSizer(list_control_box_sizer)

    def on_html(self, event):
        if self.url_objects:
            self.on_save_file(preset.HTML)
            if self.save_file_name:
                bookmarks_data = self.to_dict()
                start_progress_dialog(True)
                #######################################################################################
                # TODO: 02 CANCEL AND RETURN IF PROGRESS BAR CANCEL BUTTON IS PRESSED
                #######################################################################################

                paramz = {
                    preset.OUTPUT_NAME: (False, self.save_file_name),
                    preset.COMMAND_REFRESH_URL_TITLE: self.parent.application_settings.refresh_url_title,
                    preset.UNDUPE: self.parent.application_settings.remove_duplicated_urls,
                    preset.COMMAND_CLEAN_URL_FROM_TRACKING: self.parent.application_settings.remove_tracking_tokens_from_url,
                    preset.COMMAND_REFRESH_FOLDER_NAME: self.parent.application_settings.refresh_folder_name_with_hostname_title
                }

                chrome2excel.generate_web_page(bookmarks_data, paramz)
                start_progress_dialog(False)

    def on_xlsx(self, event):
        if self.url_objects:
            self.on_save_file(preset.XLSX)
            if self.save_file_name:
                bookmarks_data = self.to_dict()
                start_progress_dialog(True)
                #######################################################################################
                # TODO: 02 CANCEL AND RETURN IF PROGRESS BAR CANCEL BUTTON IS PRESSED
                #######################################################################################

                paramz = {
                    preset.OUTPUT_NAME: (True, self.save_file_name),
                    preset.COMMAND_REFRESH_URL_TITLE: self.parent.application_settings.refresh_url_title,
                    preset.UNDUPE: self.parent.application_settings.remove_duplicated_urls,
                    preset.COMMAND_CLEAN_URL_FROM_TRACKING: self.parent.application_settings.remove_tracking_tokens_from_url,
                    preset.COMMAND_REFRESH_FOLDER_NAME: self.parent.application_settings.refresh_folder_name_with_hostname_title
                }

                chrome2excel.generate_work_book(bookmarks_data, paramz)
                start_progress_dialog(False)

    def on_reset(self, event):
        self.header = None
        self.url_objects = []
        self.update_url_screen(True)
        set_total_items(self.parent)

    def to_dict(self):
        bookmarks_data = []
        for row in self.url_objects:
            bookmarks_data.append(row.to_dict())
        return bookmarks_data

    def on_edit(self, event):
        selected_item = self.list_ctrl.GetFocusedItem()
        if selected_item >= 0:
            edit_dialog = EditDialog(self.url_objects[selected_item])
            return_value = edit_dialog.ShowModal()
            if return_value == wx.ID_OK:
                self.list_ctrl.DeleteItem(selected_item)
                self.update_element(selected_item, edit_dialog.url.to_list())
                self.update_column_width()

    def update_url_screen(self, reset):
        if reset:
            self.list_ctrl.ClearAll()

        if self.list_ctrl.GetColumnCount() < 1:
            for label_index, label_element in enumerate(preset.label_dictionary):
                self.list_ctrl.InsertColumn(label_index, preset.label_dictionary[label_index], width=50)
                if label_index > 27:
                    break

    def update_url_listing(self, path_to_text_file):
        self.update_url_screen(False)
        url_list = chrome2excel.generate_from_txt(chrome2excel.import_text_file(path_to_text_file))
        self.update_list(url_list)

    def update_element(self, index, url):
        for label_index, label_element in enumerate(preset.label_dictionary):
            key = list(url.keys())[label_index]
            if label_index > 28:
                break
            if label_index == 0:
                self.list_ctrl.InsertItem(index, url[key])
            element = url[key]
            if isinstance(element, datetime.datetime):
                element = utils.date_to_string(element)
            self.list_ctrl.SetItem(index, label_index, str(element))

    def update_list(self, url_list):
        total_items = len(url_list)
        if total_items:
            start_progress_dialog(True)
            #######################################################################################
            # TODO: 02 CANCEL AND RETURN IF PROGRESS BAR CANCEL BUTTON IS PRESSED
            #######################################################################################
            utils.update_progress(preset.MESSAGE[preset.LOADING_BOOKMARKS], -1, total_items)
            for index, url in enumerate(url_list):
                self.update_element(index, url)
                url_object = preset.Header()
                url_object.set_data(url)
                self.url_objects.append(url_object)
                #######################################################################################
                # TODO: 03 LET USER CHANGE COLOR IN POPUP MENU https://wiki.wxpython.org/PopupMenuOnRightClick
                # TODO: 03 CHANGE COLOR IN POPUP MENU http://revxatlarge.blogspot.com/2011/06/wxpython-listbox-popupmenu.html
                # TODO: 03 CHANGE COLOR IN POPUP MENU https://www.daniweb.com/programming/software-development/threads/352474/wxpython-wx-listctrl-and-wx-menu
                #######################################################################################
                if index % 2:
                    self.list_ctrl.SetItemBackgroundColour(index, '#FFFFFF')
                else:
                    self.list_ctrl.SetItemBackgroundColour(index, '#EEEEEE')
                utils.update_progress(preset.MESSAGE[preset.LOADING_BOOKMARKS], index, total_items)
            self.update_column_width()
            start_progress_dialog(False)
        else:
            set_status_message(self.parent, preset.MESSAGE[preset.USER_HAS_NO_BOOKMARKS])

    def update_column_width(self):
        #######################################################################################
        # TODO: DATE COLUMNS MUST BE AUTO WIDTH (USE AUTO-DETECT INSTEAD OF CONSTANT NUMBERS)
        #######################################################################################
        self.list_ctrl.SetColumnWidth(4, -1)
        self.list_ctrl.SetColumnWidth(5, -1)
        self.list_ctrl.SetColumnWidth(6, -1)
        self.list_ctrl.SetColumnWidth(13, -1)
        self.list_ctrl.SetColumnWidth(14, -1)
        self.list_ctrl.SetColumnWidth(15, -1)

    def on_save_file(self, save_file_default):
        if save_file_default == preset.HTML:
            wildcard_export = preset.MESSAGE[preset.HTML_FILE_FILTER]
        else:
            wildcard_export = preset.MESSAGE[preset.XLSX_FILE_FILTER]

        save_file_dialog = wx.FileDialog(self,
                                         message=preset.MESSAGE[preset.SAVE_FILE],
                                         defaultDir=preset.SYMBOL_EMPTY,
                                         wildcard=wildcard_export,
                                         style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if save_file_dialog.ShowModal() == wx.ID_OK:
            self.save_file_name = save_file_dialog.GetPath()
        else:
            self.save_file_name = None


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,
                          parent=None,
                          title=preset.MESSAGE[preset.BOOKMARKS_EDITOR],
                          size=(1200, 600))
        self.Bind(wx.EVT_CLOSE, self.frame_button_close)

        application_icon = wx.Icon()
        application_icon.CopyFromBitmap(wx.Bitmap(preset.MAIN_ICON, wx.BITMAP_TYPE_ANY))
        self.SetIcon(application_icon)
        self.application_settings = bookmarks.Options()
        self.application_settings.load_settings()
        self.selected_account = -1

        self.status_bar = self.CreateStatusBar(3)
        self.set_status_bar()
        self.Bind(wx.EVT_SIZE, self.on_resize, self)

        self.status_bar.SetStatusText(preset.MESSAGE[preset.APPLICATION_TITLE])
        self.status_bar.SetStatusText(preset.SYMBOL_EMPTY, 1)
        self.status_bar.SetStatusText(f'{preset.MESSAGE[preset.TOTAL_ITEMS]}0', 2)

        self.main_url_panel = MainUrlPanel(self)
        self.create_menu()
        self.Show()

    def set_status_bar(self):
        width, height = self.GetSize()
        self.status_bar.SetStatusWidths([int(width*0.3), int(width*0.4), -1])

    def on_resize(self, event):
        self.set_status_bar()
        event.Skip()

    def create_menu(self):
        #######################################################################################
        # TODO: http://zetcode.com/wxpython/menustoolbars/
        #######################################################################################
        menu_bar = wx.MenuBar()
        options_menu = wx.Menu()

        open_account_menu_item = options_menu.Append(wx.ID_ADD, preset.MESSAGE[preset.IMPORT_ACCOUNT_MENU], preset.MESSAGE[preset.IMPORT_ACCOUNT_DESCRIPTION])
        open_folder_menu_item = options_menu.Append(wx.ID_OPEN, preset.MESSAGE[preset.OPEN_FILE_MENU], preset.MESSAGE[preset.OPEN_FILE_DESCRIPTION])
        open_settings_menu_item = options_menu.Append(wx.ID_PREFERENCES, preset.MESSAGE[preset.SETTINGS_MENU], preset.MESSAGE[preset.SETTINGS_DESCRIPTION])
        options_menu.AppendSeparator()
        open_exit_menu_item = options_menu.Append(wx.ID_EXIT, preset.MESSAGE[preset.EXIT_MENU], preset.MESSAGE[preset.EXIT_DESCRIPTION])

        menu_bar.Append(options_menu, preset.MESSAGE[preset.OPTIONS_MENU])

        self.Bind(event=wx.EVT_MENU, handler=self.on_open_account, source=open_account_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_folder_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_settings, source=open_settings_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_exit, source=open_exit_menu_item)

        about_menu = wx.Menu()
        open_about_menu_item = about_menu.Append(wx.ID_ABOUT, preset.MESSAGE[preset.ABOUT_MENU], preset.MESSAGE[preset.ABOUT_DESCRIPTION])
        menu_bar.Append(about_menu, preset.MESSAGE[preset.ABOUT_MENU])
        self.Bind(event=wx.EVT_MENU, handler=self.on_about, source=open_about_menu_item)

        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        open_folder_dialog = wx.FileDialog(self,
                                           message=preset.MESSAGE[preset.CHOOSE_FILE],
                                           defaultFile=preset.TEXT_FILENAME,
                                           wildcard=preset.MESSAGE[preset.TEXT_FILE_FILTER],
                                           style=wx.DD_DEFAULT_STYLE)
        if open_folder_dialog.ShowModal() == wx.ID_OK:
            self.main_url_panel.update_url_listing(open_folder_dialog.GetPath())
            set_total_items(self)

    def on_open_account(self, event):
        profile_chooser_dialog = ProfileChooser(self, -1)
        button_pressed = profile_chooser_dialog.ShowModal()
        if button_pressed == wx.ID_OK:
            tools.print_display(preset.MESSAGE[preset.LOADING_BOOKMARKS])
            data_table = bookmarks.generate_data(bookmarks.generate_bookmarks(self.selected_account))
            self.main_url_panel.update_list(data_table)
            self.main_url_panel.Update()
            set_total_items(self)
        else:
            self.selected_account = -1

    def on_open_settings(self, event):
        settings_dialog = SettingsDialog(self, 0)
        settings_dialog.ShowModal()

    def on_about(self, event):
        AboutDialog(self)

    def on_open_exit(self, event):
        if self.application_settings.exit_dialog_confirmation:
            exit_dialog = wx.RichMessageDialog(self,
                                               preset.MESSAGE[preset.EXIT_QUESTION],
                                               preset.MESSAGE[preset.EXIT_TITLE],
                                               wx.YES_NO | wx.ICON_QUESTION)
            exit_dialog.ShowCheckBox(preset.MESSAGE[preset.EXIT_CONFIRMATION])
            exit_value = exit_dialog.ShowModal()
            if exit_dialog.IsCheckBoxChecked():
                self.application_settings.exit_dialog_confirmation = False
                self.application_settings.save_settings()

            if exit_value == wx.ID_YES:
                self.Destroy()
        else:
            self.Close()

    def frame_button_close(self, event):
        self.Destroy()


def set_total_items(self):
    self.status_bar.SetStatusText(preset.MESSAGE[preset.TOTAL_ITEMS] + '{:n}'.format(self.main_url_panel.list_ctrl.GetItemCount()), 2)


def set_status_message(self, message):
    self.status_bar.SetStatusText(message, 1)


class AboutDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        about_application = wx.adv.AboutDialogInfo()
        about_application.Name = preset.CHROME_EXPORTER
        about_application.Version = preset.TEXT_VERSION
        about_application.Copyright = preset.TEXT_OTDS_H_CO
        about_application.Description = preset.MESSAGE[preset.APPLICATION_DESCRIPTION]
        about_application.WebSite = (preset.GITHUB, preset.MESSAGE[preset.APPLICATION_WEBSITE])
        vincent_liopard = preset.TEXT_VINCENT_LIOPARD
        about_application.Developers = [vincent_liopard]
        about_application.License = preset.MESSAGE[preset.APPLICATION_LICENCE]
        about_application.SetTranslators = [vincent_liopard]
        about_application.DocWriters = [vincent_liopard]
        about_application.SetArtists = [vincent_liopard]

        wx.adv.AboutBox(about_application)


class EditDialog(wx.Dialog):
    def __init__(self, edit_url):
        super().__init__(parent=None, title=f'{preset.MESSAGE[preset.EDIT_TITLE]}[{edit_url.url_info_name}]', size=(700, 590), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.url = edit_url

        self.scrolled_panel = ScrolledPanel(self)
        self.scrolled_panel.SetupScrolling()

        self.left_box_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_box_sizer = wx.BoxSizer(wx.VERTICAL)

        max_length = 0
        for item in preset.label_dictionary:
            label_length = len(item)
            if label_length > max_length:
                max_length = label_length

        self.attribute_list = []
        for index, item in enumerate(edit_url.to_list()):
            element_value = edit_url.get_item(item)
            if isinstance(element_value, datetime.datetime):
                item_value = utils.date_to_string(element_value)
            else:
                item_value = str(element_value)
            self.attribute_list.append(wx.TextCtrl(self.scrolled_panel, value=item_value))
            dialog_place = preset.LEFT
            if index > 21:
                dialog_place = preset.RIGHT
            if index < 29:
                self.add_widgets(edit_url.get_label(index), self.attribute_list[index], dialog_place, max_length)

        cancel_button = wx.Button(self, id=wx.ID_CANCEL, label=preset.MESSAGE[preset.CANCEL_BUTTON])

        save_button = wx.Button(self, id=wx.ID_OK, label=preset.MESSAGE[preset.EDIT_SAVE])
        save_button.Bind(wx.EVT_BUTTON, self.on_save)

        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_box_sizer.Add(self.left_box_sizer, 1, wx.EXPAND, 1)
        horizontal_box_sizer.Add(self.right_box_sizer, 1, wx.EXPAND, 1)

        self.scrolled_panel.SetSizer(horizontal_box_sizer)
        self.scrolled_panel.SetAutoLayout(1)

        button_box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_box_sizer.Add(save_button, 1)
        button_box_sizer.Add(cancel_button, 1)

        main_box_sizer = wx.BoxSizer(wx.VERTICAL)
        main_box_sizer.Add(self.scrolled_panel, 1, wx.EXPAND, 1)
        main_box_sizer.Add(button_box_sizer, 0, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(main_box_sizer)

    def add_widgets(self, text_label, text_ctrl, dialog_place, max_length):
        spaces_gap = max_length - len(text_label)
        text_label = text_label + preset.SYMBOL_SPACE * spaces_gap + preset.SYMBOL_COLON
        static_text = wx.StaticText(self.scrolled_panel, label=text_label, size=(max_length*8, -1))
        # noinspection PyUnresolvedReferences
        static_text.SetFont(wx.Font(8, wx.TELETYPE, wx.NORMAL, wx.BOLD, underline=True))

        static_bullet = wx.StaticText(self.scrolled_panel, label=preset.SYMBOL_GRADE, size=(14, -1))
        static_bullet.SetFont(wx.Font(8, wx.TELETYPE, wx.NORMAL, wx.BOLD))

        box_sizer_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        box_sizer_horizontal.Add(static_bullet, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        box_sizer_horizontal.Add(static_text, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        box_sizer_horizontal.Add(text_ctrl, 1, wx.ALL, 0)

        if dialog_place == preset.LEFT:
            self.left_box_sizer.Add(box_sizer_horizontal, 1, wx.EXPAND, 1)
        else:
            self.right_box_sizer.Add(box_sizer_horizontal, 1, wx.EXPAND, 1)

    def on_save(self, event):
        save_list = []
        for element in self.attribute_list:
            save_list.append(element.GetValue())
        self.url.set_data(save_list)
        self.EndModal(event.EventObject.Id)


class ProfileChooser(wx.Dialog):
    def __init__(self, parent, id_, title=preset.MESSAGE[preset.PROFILE_CHOOSER]):
        chrome_profile_list = tools.get_profile_list()
        maximum_length = 0
        for profile in chrome_profile_list:
            if len(profile[1]) > maximum_length:
                maximum_length = len(profile[1])
        chooser_width = maximum_length * 7
        chooser_height = len(chrome_profile_list) * 45 + 60
        wx.Dialog.__init__(self, parent, id_, title, size=(chooser_width, chooser_height))
        profile_chooser_panel = wx.Panel(self, size=(chooser_width, chooser_height))
        self.parent = parent
        self.parent.selected_account = 0
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)
        horizontal_box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        if chrome_profile_list:
            vertical_box_sizer.Add(wx.RadioButton(profile_chooser_panel, 0, label=chrome_profile_list[0][1], style=wx.RB_GROUP))
            for profile in chrome_profile_list[1:]:
                vertical_box_sizer.Add(wx.RadioButton(profile_chooser_panel, profile[0], label=profile[1]))
            self.Bind(wx.EVT_RADIOBUTTON, self.on_radio_group)
            horizontal_box_sizer.Add(wx.Button(profile_chooser_panel, wx.ID_OK, preset.MESSAGE[preset.OK_BUTTON]), 1)
        else:
            vertical_box_sizer.Add(wx.StaticText(profile_chooser_panel, wx.ID_ANY, label=preset.MESSAGE[preset.NO_ACCOUNT]))

        horizontal_box_sizer.Add(wx.Button(profile_chooser_panel, wx.ID_CANCEL, preset.MESSAGE[preset.CANCEL_BUTTON]), 1)
        combined_sizer = wx.BoxSizer(wx.VERTICAL)
        combined_sizer.Add(vertical_box_sizer, 1, wx.EXPAND)
        combined_sizer.Add(horizontal_box_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 10)
        profile_chooser_panel.SetSizer(combined_sizer)
        main_box_sizer = wx.BoxSizer(wx.VERTICAL)
        main_box_sizer.Add(wx.StaticLine(self, wx.HORIZONTAL), 0, wx.EXPAND, 0)
        main_box_sizer.Add(profile_chooser_panel, 2, wx.ALL | wx.EXPAND, 8)
        main_box_sizer.Add(wx.StaticLine(self, wx.HORIZONTAL), 0, wx.EXPAND, 0)
        self.SetSizerAndFit(main_box_sizer)

    def on_radio_group(self, event):
        event_object = event.GetEventObject()
        self.parent.selected_account = event_object.GetId()


class SettingsDialog(wx.Dialog):
    def __init__(self, parent, id_, title=preset.MESSAGE[preset.SETTINGS_TITLE]):
        wx.Dialog.__init__(self, parent, id_, title)

        self.parent = parent

        self.SetSize((320, 220))
        button_size = (135, 25)

        static_box = wx.StaticBox(wx.Panel(self, size=(145, 50)), id=wx.ID_ANY, label=preset.MESSAGE[preset.WORKS_ONLY_ON_CLI], pos=(10, 3), size=(135, 47))

        settings_button_label, settings_button_value = set_button_toggle(self, 0, False)

        if tools.get_system() == preset.SYSTEM_WINDOWS:
            self.toggle_button01 = wx.CheckBox(static_box, id=0, label=settings_button_label, size=(130, 25), style=wx.BU_LEFT, pos=(4, 17))
        else:
            self.toggle_button01 = wx.CheckBox(static_box, id=0, label=settings_button_label, size=button_size, style=wx.BU_LEFT)

        self.toggle_button01.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 1, False)
        self.toggle_button02 = wx.ToggleButton(self, id=1, label=settings_button_label, size=button_size, pos=(10, 55), style=wx.BU_LEFT)
        self.toggle_button02.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 2, False)
        self.toggle_button03 = wx.ToggleButton(self, id=2, label=settings_button_label, size=button_size, pos=(10, 85), style=wx.BU_LEFT)
        self.toggle_button03.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 3, False)
        self.toggle_button04 = wx.CheckBox(self, id=3, label=settings_button_label, size=button_size, pos=(152, 20), style=wx.BU_LEFT)
        self.toggle_button04.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 4, False)
        self.toggle_button05 = wx.ToggleButton(self, id=4, label=settings_button_label, size=button_size, pos=(150, 55), style=wx.BU_LEFT)
        self.toggle_button05.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 5, False)
        self.toggle_button06 = wx.ToggleButton(self, id=5, label=settings_button_label, size=button_size, pos=(150, 85), style=wx.BU_LEFT)
        self.toggle_button06.SetValue(settings_button_value)

        settings_button_label, settings_button_value = set_button_toggle(self, 6, False)
        self.toggle_button07 = wx.CheckBox(self, id=6, label=settings_button_label, size=(100, 25), pos=(152, 145))
        self.toggle_button07.SetValue(settings_button_value)

        self.language_combo_box = wx.ComboBox(self, id=7, value=parent.application_settings.system_language, pos=(10, 115), size=(135, 25), choices=preset.get_languages(), style=0)

        wx.StaticText(self, id=wx.ID_ANY, label=preset.MESSAGE[preset.TIMEOUT_LABEL], pos=(150, 120), size=(50, 25), style=0)
        self.time_out = wx.SpinCtrl(self, id=8, value=str(preset.TIMEOUT), pos=(205, 115), size=(80, 25), style=wx.SP_ARROW_KEYS, min=10, max=9000, initial=120)

        self.Bind(wx.EVT_CHECKBOX, self.on_radio_group)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_radio_group)
        self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.on_combo_box)
        self.Bind(wx.EVT_SPINCTRL, self.on_spin_control)

        self.ok_button = wx.Button(self, wx.ID_OK, preset.MESSAGE[preset.OK_BUTTON], size=button_size, pos=(10, 145))

        self.Centre()
        self.Show(True)

    def on_radio_group(self, event):
        event_object = event.GetEventObject()
        label, value = set_button_toggle(self, event_object.GetId(), True)
        event_object.SetLabel(label)
        event_object.SetValue(value)
        self.parent.application_settings.save_settings()

    def on_combo_box(self, event):
        event_object = event.GetEventObject()
        self.parent.application_settings.system_language = event_object.GetValue()
        self.parent.application_settings.save_settings()

    def on_spin_control(self, event):
        event_object = event.GetEventObject()
        preset.TIMEOUT = event_object.GetValue()
        self.parent.application_settings.save_settings()


def set_button_toggle(self, button_id, toggle_button):
    settings_button_label = None
    settings_button_value = None
    if button_id == 0:
        if toggle_button:
            self.parent.application_settings.export_file_type = not self.parent.application_settings.export_file_type
        if self.parent.application_settings.export_file_type:
            settings_button_label = preset.MESSAGE[preset.OUTPUT_OFF] + preset.MESSAGE[preset.OUTPUT_TYPE]
            settings_button_value = True
        else:
            settings_button_label = preset.MESSAGE[preset.OUTPUT_ON] + preset.MESSAGE[preset.OUTPUT_TYPE]
            settings_button_value = False
    if button_id == 1:
        if toggle_button:
            self.parent.application_settings.refresh_url_title = not self.parent.application_settings.refresh_url_title
        if self.parent.application_settings.refresh_url_title:
            settings_button_label = preset.MESSAGE[preset.ON_LABEL] + preset.MESSAGE[preset.REFRESH_URL_TITLE]
            settings_button_value = True
        else:
            settings_button_label = preset.MESSAGE[preset.OFF_LABEL] + preset.MESSAGE[preset.REFRESH_URL_TITLE]
            settings_button_value = False
    if button_id == 2:
        if toggle_button:
            self.parent.application_settings.remove_duplicated_urls = not self.parent.application_settings.remove_duplicated_urls
        if self.parent.application_settings.remove_duplicated_urls:
            settings_button_label = preset.MESSAGE[preset.ON_LABEL] + preset.MESSAGE[preset.UNDUPE_URLS]
            settings_button_value = True
        else:
            settings_button_label = preset.MESSAGE[preset.OFF_LABEL] + preset.MESSAGE[preset.UNDUPE_URLS]
            settings_button_value = False
    if button_id == 5:
        if toggle_button:
            self.parent.application_settings.remove_tracking_tokens_from_url = not self.parent.application_settings.remove_tracking_tokens_from_url
        if self.parent.application_settings.remove_tracking_tokens_from_url:
            settings_button_label = preset.MESSAGE[preset.ON_LABEL] + preset.MESSAGE[preset.CLEAN_URL_STRING]
            settings_button_value = True
        else:
            settings_button_label = preset.MESSAGE[preset.OFF_LABEL] + preset.MESSAGE[preset.CLEAN_URL_STRING]
            settings_button_value = False
    if button_id == 3:
        if toggle_button:
            self.parent.application_settings.display_exit_dialog = not self.parent.application_settings.display_exit_dialog
        if self.parent.application_settings.display_exit_dialog:
            settings_button_label = preset.MESSAGE[preset.ON_LABEL] + preset.MESSAGE[preset.DISPLAY_EXIT_DIALOG]
            settings_button_value = True
        else:
            settings_button_label = preset.MESSAGE[preset.OFF_LABEL] + preset.MESSAGE[preset.DISPLAY_EXIT_DIALOG]
            settings_button_value = False
    if button_id == 4:
        if toggle_button:
            self.parent.application_settings.refresh_folder_name_with_hostname_title = not self.parent.application_settings.refresh_folder_name_with_hostname_title
        if self.parent.application_settings.refresh_folder_name_with_hostname_title:
            settings_button_label = preset.MESSAGE[preset.ON_LABEL] + preset.MESSAGE[preset.CHECK_HOSTNAME]
            settings_button_value = True
        else:
            settings_button_label = preset.MESSAGE[preset.OFF_LABEL] + preset.MESSAGE[preset.CHECK_HOSTNAME]
            settings_button_value = False
    if button_id == 6:
        if toggle_button:
            preset.DEBUG_MODE = not preset.DEBUG_MODE
        if preset.DEBUG_MODE:
            settings_button_label = preset.MESSAGE[preset.DEBUG_SYSTEM] + preset.MESSAGE[preset.ON_LABEL]
            settings_button_value = True
        else:
            settings_button_label = preset.MESSAGE[preset.DEBUG_SYSTEM] + preset.MESSAGE[preset.OFF_LABEL]
            settings_button_value = False
    return settings_button_label, settings_button_value


def start_progress_dialog(start):
    if start:
        preset.GUI_PROGRESS_DIALOG = wx.GenericProgressDialog(preset.SYMBOL_EMPTY, preset.SYMBOL_EMPTY, style=wx.PD_AUTO_HIDE | wx.PD_APP_MODAL | wx.PD_CAN_ABORT)
    else:
        preset.GUI_PROGRESS_DIALOG = None


def main():
    preset.RUN_GUI = True
    application = wx.App(False)
    MainFrame()
    application.MainLoop()
