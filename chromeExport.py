import wx
import glob
import htmlSupport

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
        self.panel = urlPanel(self)
        self.create_menu()
        self.Show()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        open_folder_menu_item = file_menu.Append(wx.ID_ANY, 'Open File', 'Open a text file with URLs')
        open_account_menu_item = file_menu.Append(wx.ID_ANY, 'Import Account', 'Import Account from Chrome')
        menu_bar.Append(file_menu, '&File')
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_folder_menu_item)
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_account_menu_item)
        self.SetMenuBar(menu_bar)       

    def on_open_folder(self, event):
        #dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        wildcard = "Text file (*.txt)|*.txt"
        dlg = wx.FileDialog(self, message="Choose a file:", defaultFile="chrome.txt", wildcard=wildcard, style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_url_listing(dlg.GetPath())
        dlg.Destroy()

    def on_open_account(self, event):
        pass

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

    def __init__(self, parent, id, title = "Test", size=(600,400)):
        wx.Dialog.__init__(self, parent, id, title)

        valueA = "Av"
        valueB = "Bv"
        valueC = "Cv"

        pnl = wx.Panel(self)
        self.myval = valueA
        self.rb1 = wx.RadioButton(pnl, 11, label = valueA, pos = (10,10), style = wx.RB_GROUP) 
        self.rb2 = wx.RadioButton(pnl, 22, label = valueB, pos = (10,30)) 
        self.rb3 = wx.RadioButton(pnl, 33, label = valueC, pos = (10,50)) 
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadiogroup)

        self.btn1 = wx.Button(pnl, wx.ID_OK, " OK ", pos = (10,80))
        self.btn2 = wx.Button(pnl, wx.ID_CANCEL, " Cancel ", pos = (10,110))

        self.Centre() 
        self.Show(True)
        
    def OnRadiogroup(self, e): 
       rb = e.GetEventObject() 
       self.myval = rb.GetLabel()

    def GetValue(self):
        return self.myval



if __name__ == '__main__':
    app = wx.App(False)
    frame = urlFrame()
    '''
    dlg = MyDialog(None, -1)
    retval = dlg.ShowModal()
    if retval == wx.ID_OK:
        print (dlg.GetValue())
    else:
        print ('None selected')
    dlg.Destroy()
    '''
    app.MainLoop()


