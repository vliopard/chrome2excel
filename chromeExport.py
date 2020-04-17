import wx
import htmlSupport
import chromeProfile

hostname="Hostname"
url_title="Title"
url_addr="URL"
date_added="Date Added"
date_modified="Date Modified"
date_visited="Date Visited"
original_url="Original URL"

class urlPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.row_obj_dict = {}
        self.list_ctrl = wx.ListCtrl(self, size=(-1, 100), style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, hostname, width=140)
        self.list_ctrl.InsertColumn(1, url_title, width=140)
        self.list_ctrl.InsertColumn(2, url_addr, width=200)
        main_sizer.Add(self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        edit_button = wx.Button(self, label='Edit')
        edit_button.Bind(wx.EVT_BUTTON, self.on_edit)
        main_sizer.Add(edit_button, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(main_sizer)

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
        self.list_ctrl.InsertColumn(0, date_added, width=140)
        self.list_ctrl.InsertColumn(1, date_modified, width=140)
        self.list_ctrl.InsertColumn(2, date_visited, width=200)
        self.list_ctrl.InsertColumn(3, original_url, width=200)
        index = 0
        url_objects = []
        url_list = []
        with open(folder_path, encoding='utf-8') as bm:
            for line in bm:
                url_list.append(line)

        for url in url_list:            
            self.list_ctrl.InsertItem(index, "IndexA"+str(index))
            self.list_ctrl.SetItem(index, 1, "IndexB"+str(index))
            self.list_ctrl.SetItem(index, 2, "IndexC"+str(index))
            self.list_ctrl.SetItem(index, 3, url)
            url_object = { "Hostname":"HN"+str(index), "Title":"TT"+str(index), "URL":"UR"+str(index) }
            url_objects.append(url_object)
            self.row_obj_dict[index] = url_object
            index += 1


class urlFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Bookmarks Editor')

        # TODO: Recover settings from disk
        self.selected = ""
        self.file_type = False
        self.reload_title = False
        self.undupe_url = False
        self.clean_url = False
        self.text_import = False
        
        self.panel = urlPanel(self)
        self.create_menu()
        self.Show()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_account_menu_item = file_menu.Append(wx.ID_ANY, 'Import &Account', 'Import Account from Chrome')
        open_folder_menu_item = file_menu.Append(wx.ID_ANY, 'Open &File', 'Open a text file with URLs')
        open_settings_menu_item = file_menu.Append(wx.ID_ANY, '&Settings', 'Set options on/off')
        menu_bar.Append(file_menu, '&Options')
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_account, source=open_account_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_folder_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_settings, source=open_settings_menu_item)
        self.SetMenuBar(menu_bar)       

    def on_open_folder(self, event):
        wildcard = "Text file (*.txt)|*.txt"
        dlg = wx.FileDialog(self, message="Choose a file:", defaultFile="chrome.txt", wildcard=wildcard, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_url_listing(dlg.GetPath())
        dlg.Destroy()

    def on_open_account(self, event):
        dlg = MyDialog(self, -1)
        retval = dlg.ShowModal()
        if retval == wx.ID_OK:
            # TODO: Load bookmars from Chrome profile
            print("Loading Bookmarks...")
        else:
            self.selected = ""
        dlg.Destroy()

    def on_open_settings(self, event):
        dlg = SettingsDialog(self, -1)
        retval = dlg.ShowModal()
        dlg.Destroy()
    

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

    def __init__(self, parent, id, title = "Profile Chooser", size=(600, 600)):
        wx.Dialog.__init__(self, parent, id, title)

        pnl = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        my_list = chromeProfile.profile_list()
        
        self.parent = parent
        self.parent.selected = my_list[0]

        position = 10        
        sizer.Add(wx.RadioButton(pnl, 0, label = my_list[0], pos = (10, 10), style = wx.RB_GROUP))
        for nro, x in enumerate(my_list[1:]):            
            position = position + 20
            sizer.Add(wx.RadioButton(pnl, nro+1, label = x, pos = (10, position)))
            
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)

        position = position + 20
        sizer.Add(wx.Button(pnl, wx.ID_OK, " OK ", pos = (10, position)))
        position = position + 30        
        sizer.Add(wx.Button(pnl, wx.ID_CANCEL, " Cancel ", pos = (10, position)))

        self.Centre() 
        self.Show(True)

    def OnRadiogroup(self, e): 
       rb = e.GetEventObject() 
       self.myval = rb.GetId()
       self.parent.selected = rb.GetId()


class SettingsDialog(wx.Dialog):

    def __init__(self, parent, id, title = "Settings", size=(500, 200)):
        wx.Dialog.__init__(self, parent, id, title)
      
        self.parent = parent
        
        label, value = setButton(self,0)
        self.tb1=wx.ToggleButton(self, id=0, label=label, pos = (10, 10))
        self.tb1.SetValue(value)
        
        label, value = setButton(self,1)
        self.tb2=wx.ToggleButton(self, id=1, label=label, pos = (10, 40))
        self.tb2.SetValue(value)
        
        label, value = setButton(self,2)
        self.tb3=wx.ToggleButton(self, id=2, label=label, pos = (10, 70))
        self.tb3.SetValue(value)
        
        label, value = setButton(self,3)
        self.tb4=wx.ToggleButton(self, id=3, label=label, pos = (10, 100))
        self.tb4.SetValue(value)
        
        label, value = setButton(self,4)
        self.tb5=wx.ToggleButton(self, id=4, label=label, pos = (10, 130))
        self.tb5.SetValue(value)

        self.Bind(wx.EVT_TOGGLEBUTTON, self.OnRadiogroup)

        self.btn=wx.Button(self, wx.ID_OK, " OK ", pos = (10, 250))
        self.Centre() 
        self.Show(True)

    def OnRadiogroup(self, e): 
        rb = e.GetEventObject() 
        label, value = setButtonToggle(self, rb.GetId())
        rb.SetLabel(label)
        rb.SetValue(value)
        # TODO: Save settings to disk


def setButtonToggle(self, btnId):
    label = None
    if btnId == 0:
        self.parent.file_type = not self.parent.file_type
        if self.parent.file_type:
            label = "[html]  Output type"
            value = True
        else:
            label = "[xlsx] Output type"
            value = False
    if btnId == 1:
        self.parent.reload_title = not self.parent.reload_title
        if self.parent.reload_title:
            label = "[on]  Refresh URL"
            value = True
        else:
            label = "[off] Refresh URL"
            value = False
    if btnId == 2:
        self.parent.undupe_url = not self.parent.undupe_url
        if self.parent.undupe_url:
            label = "[on]  Undupe URLs"
            value = True
        else:
            label = "[off] Undupe URLs"
            value = False
    if btnId == 3:
        self.parent.clean_url = not self.parent.clean_url
        if self.parent.clean_url:
            label = "[on]  Clean URL"
            value = True
        else:
            label = "[off] Clean URL"
            value = False
    if btnId == 4:
        self.parent.text_import = not self.parent.text_import
        if self.parent.text_import:
            label = "[on]  Import TXT"
            value = True
        else:
            label = "[off] Import TXT"
            value = False
    return label, value


def setButton(self, btnId):
    label = None
    if btnId == 0:
        if self.parent.file_type:
            label = "[html]  Output type"
            value = True
        else:
            label = "[xlsx] Output type"
            value = False
    if btnId == 1:
        if self.parent.reload_title:
            label = "[on]  Refresh URL"
            value = True
        else:
            label = "[off] Refresh URL"
            value = False
    if btnId == 2:
        if self.parent.undupe_url:
            label = "[on]  Undupe URLs"
            value = True
        else:
            label = "[off] Undupe URLs"
            value = False
    if btnId == 3:
        if self.parent.clean_url:
            label = "[on]  Clean URL"
            value = True
        else:
            label = "[off] Clean URL"
            value = False
    if btnId == 4:
        if self.parent.text_import:
            label = "[on]  Import TXT"
            value = True
        else:
            label = "[off] Import TXT"
            value = False
    return label, value



if __name__ == '__main__':
    app = wx.App(False)
    frame = urlFrame()
    app.MainLoop()
