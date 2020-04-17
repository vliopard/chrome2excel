import wx
import glob

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
        self.list_ctrl.InsertColumn(0, 'Hostname', width=140)
        self.list_ctrl.InsertColumn(1, 'Title', width=140)
        self.list_ctrl.InsertColumn(2, 'URL', width=200)
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
        urls = glob.glob(folder_path + '/*.txt')
        url_objects = []
        index = 0

        url_list = []
        with open("chrome.txt",encoding='utf-8') as bm:
            for line in bm:
                url_list.append(line)

        for url in url_list:
            url_parts = htmlSupport.parseURL(line)
            self.list_ctrl.InsertItem(index, url_parts[2])
            self.list_ctrl.SetItem(index, 1, htmlSupport.clean_url(url)
            self.list_ctrl.SetItem(index, 2, url)

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
        open_folder_menu_item = file_menu.Append(wx.ID_ANY, 'Open Folder', 'Open a folder with TXTs')
        menu_bar.Append(file_menu, '&File')
        self.Bind(event=wx.EVT_MENU, handler=self.on_open_folder, source=open_folder_menu_item)
        self.SetMenuBar(menu_bar)

    def on_open_folder(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.update_url_listing(dlg.GetPath())
        dlg.Destroy()


class EditDialog(wx.Dialog):    
    def __init__(self, url):
        date_visited = f'Editing "{url.tag.date_visited}"'
        super().__init__(parent=None, title=date_visited)        
        self.url = url        
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.date_added = wx.TextCtrl(self, value=self.url.tag.date_added)
        self.add_widgets(date_added, self.date_added)
        self.date_modified = wx.TextCtrl(self, value=self.url.tag.date_modified)
        self.add_widgets(date_modified, self.date_modified)
        self.date_visited = wx.TextCtrl(self, value=self.url.tag.date_visited)
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
        self.url.tag.date_added = self.date_added.GetValue()
        self.url.tag.date_modified = self.date_modified.GetValue()
        self.url.tag.date_visited = self.date_visited.GetValue()
        self.url.tag.save()
        self.Close()


if __name__ == '__main__':
    app = wx.App(False)
    frame = urlFrame()
    app.MainLoop()


'''
import tkinter as tk

window = tk.Tk()

label = tk.Label(
    text="Hello, Tkinter",
    fg="white",
    bg="black",
    width=10,
    height=10
)

button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)

entry = tk.Entry(fg="yellow", bg="blue", width=50)

label.pack()
button.pack()
entry.pack()

window.mainloop()

import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Hello World')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        my_btn = wx.Button(panel, label='Press Me')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(my_sizer)
        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
'''