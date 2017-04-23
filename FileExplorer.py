import gtk
import os
import shutil
import errno


#for running any linux command
import subprocess
from subprocess import call
#ends here

new_name="New Folder" #global variable for new folder function
file_to_be_renamed="/" #global variable for renaming a file

#dialog box for about

class about(gtk.Dialog):

    def __init__(self, parent):
        gtk.Dialog.__init__(self, "About ProjectX", parent, 0)

        self.set_default_size(150, 100)

        label1=gtk.Label()
        label1.set_markup("ProjectX lets you organize files and folders on your computer :)")
        label1.set_line_wrap(True)

        label = gtk.Label()
        label.set_markup("  Developed by Avneet Singh Saluja, Ayudh Kumar Gupta, Ayur Jain, Ayush Garg, Ayush Rohatgi  ")
        
        label2=gtk.Label()
        label2.set_markup("V 1.0")
        label2.set_line_wrap(True)

        box = self.get_content_area()
        box.add(label1)
        box.add(label2) 
        box.add(label) 

        self.ok_button=gtk.Button("OK")
        box.add(self.ok_button)
        self.ok_button.connect("clicked",self.closer)

        self.show_all()

    def closer(self,widget):
        self.destroy()

#ends here


#Properties Popup

selected_path_for_prop="/"


class prop(gtk.Dialog):

    def __init__(self, parent):
        gtk.Dialog.__init__(self, "Properties", parent, 0)

        self.set_default_size(150, 100)

        a=os.path.getsize(selected_path_for_prop)
        a=str(a/1024000.00)
        
        b=os.path.basename(selected_path_for_prop)
        
        label1=gtk.Label()
        label1.set_markup("  Name: "+b+"  ")
        label1.set_line_wrap(True)

        label2=gtk.Label()
        label2.set_markup("  Size: "+a+"MB  ")
        label2.set_line_wrap(True)

        label3=gtk.Label()
        label3.set_markup("  Directory: "+selected_path_for_prop+"  ")
        label3.set_line_wrap(True)

        box = self.get_content_area()
        box.add(label1)
        box.add(label2)
        box.add(label3)
        
        self.ok_button=gtk.Button("OK")
        box.add(self.ok_button)
        self.ok_button.connect("clicked",self.closer)
        
        self.show_all()
    def closer(self,widget):
        self.destroy()


#ends here

#Enter Name popup
class name(gtk.Dialog):

    def __init__(self, parent):
        gtk.Dialog.__init__(self, "Rename", parent, 0)

        self.set_default_size(150, 100)
        label1=gtk.Label()
        label1.set_markup("Enter New Name")
        
        self.newname=gtk.Entry()
        box = self.get_content_area()
        box.add(label1)
        box.add(self.newname)
        
        self.ok_button=gtk.Button("OK")
        box.add(self.ok_button)
        self.ok_button.connect("clicked",self.on_rename_ok_clicked)
        self.show_all()
                        

    def on_rename_ok_clicked(self,widget):
        temp=self.newname.get_text()
        os.renames(selected_path_for_prop,file_to_be_renamed+"/"+temp)
        self.destroy()


#ends here

#new folder name popup

class newfoldername(gtk.Dialog):

    def __init__(self, parent):
        gtk.Dialog.__init__(self, "New Folder", parent, 0)
        self.set_default_size(150, 100)
        label1=gtk.Label()
        label1.set_markup("Enter New Folder's Name")
        
        self.newname=gtk.Entry()
        box = self.get_content_area()
        box.add(label1)
        box.add(self.newname)
        
        self.ok_button=gtk.Button("OK")
        box.add(self.ok_button)
        self.ok_button.connect("clicked",self.on_newfolder_ok_clicked)
        self.show_all()               

    def on_newfolder_ok_clicked(self,widget):
        temp=self.newname.get_text()
        global new_name
        new_name=temp
        self.destroy()

#ends here


COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2
back_stack = []
forward_stack = []
selected_path = []
selected_isDir = []
selected_items = []
path2 = [('a',0)]

class PyApp(gtk.Window):
    def __init__(self):
        super(PyApp, self).__init__()

        #self.set_icon_from_file("icon.png")  #taskbar icon added
        self.set_size_request(650, 400)
        self.set_position(gtk.WIN_POS_CENTER)

        self.connect("destroy", gtk.main_quit)
        self.set_title("ProjectX")
        self.current_directory = '/'
        
        self.copy_dir = ["/home/ayush/Music"]
        self.paste_dir = "/home"
        vbox = gtk.VBox(False, 0);       
        

        #MenuBar declarations
        
        main_menu_bar=gtk.MenuBar()
       
        file_menu=gtk.Menu()
        file_menu_dropdown=gtk.MenuItem("File")
        file_new=gtk.MenuItem("New Folder")
        file_open=gtk.MenuItem("Open")
        file_exit=gtk.MenuItem("Exit")
        file_menu_dropdown.set_submenu(file_menu)
        file_menu.append(file_new)
        file_menu.append(file_open)
        file_menu.append(file_exit)
        main_menu_bar.append(file_menu_dropdown)
        vbox.pack_start(main_menu_bar,False,False,0 )

        file_exit.connect("activate",gtk.main_quit)
        file_open.connect("activate",self.on_open_clicked,"Open")
        file_new.connect("activate",self.on_newfolder_clicked)

        edit_menu=gtk.Menu()
        edit_menu_dropdown=gtk.MenuItem("Edit")
        edit_cut=gtk.MenuItem("Cut")
        edit_copy=gtk.MenuItem("Copy")
        edit_paste=gtk.MenuItem("Paste")
        edit_rename=gtk.MenuItem("Rename")
        edit_delete=gtk.MenuItem("Delete")

        edit_menu_dropdown.set_submenu(edit_menu)
        edit_menu.append(edit_cut)
        edit_menu.append(edit_copy)
        edit_menu.append(edit_paste)
        edit_menu.append(edit_rename)
        edit_menu.append(edit_delete)
        main_menu_bar.append(edit_menu_dropdown)
                
        edit_cut.connect("activate",self.on_cut,"Cut")
        edit_copy.connect("activate",self.on_copy,"Copy")
        edit_paste.connect("activate",self.on_paste,"Paste")
        edit_rename.connect("activate",self.on_rename_clicked,"Rename")
        edit_delete.connect("activate",self.on_delete,"Delete")


        terminal_menu=gtk.Menu()
        terminal_menu_dropdown=gtk.MenuItem("Terminal")
        terminal_launchterminal=gtk.MenuItem("Launch Terminal")
        terminal_launchterminal_pwd=gtk.MenuItem("Launch Terminal in Current Directory")
        terminal_menu_dropdown.set_submenu(terminal_menu)
        terminal_menu.append(terminal_launchterminal)
        terminal_menu.append(terminal_launchterminal_pwd)
        main_menu_bar.append(terminal_menu_dropdown)

        terminal_launchterminal.connect("activate",self.on_launch_terminal_clicked)
        terminal_launchterminal_pwd.connect("activate",self.on_launch_terminal_pwd_clicked)

        help_menu=gtk.Menu()
        help_menu_dropdown=gtk.MenuItem("Help")
        help_about=gtk.MenuItem("About")
        help_menu_dropdown.set_submenu(help_menu)
        help_menu.append(help_about)
        main_menu_bar.append(help_menu_dropdown)

        help_about.connect("activate",self.on_about_clicked)
        
    
        #ends here

        #Toolbars for bifurcation
       
        title_toolbar=gtk.Toolbar()
        vbox.pack_start(title_toolbar, False, False, 0)

        bookmarks_toolbar=gtk.Toolbar()
        vbox.pack_start(bookmarks_toolbar, False, False, 0)
         
        infobar_toolbar=gtk.Toolbar()
        vbox.pack_end(infobar_toolbar,False,False,0)
         

        #ends here

        #current directory bar
 
        self.pwd=gtk.Label()
        self.pwd.set_markup(self.current_directory)

        item3 = gtk.ToolItem()
        item3.add(self.pwd)
        infobar_toolbar.insert(item3, -1)

        #ends here


        #bookmarks bar
     
        bookmarks_label = gtk.Label("Go To :")
        item1 = gtk.ToolItem()
        item1.add(bookmarks_label)
        bookmarks_toolbar.insert(item1, -1)

        sep1 = gtk.SeparatorToolItem()  #seperator
        bookmarks_toolbar.insert(sep1, 1)


        self.desktop_Button = gtk.ToolButton(label="Desktop")
        self.desktop_Button.set_is_important(True)
        bookmarks_toolbar.insert(self.desktop_Button, -1)

        self.documents_Button = gtk.ToolButton(label="Documents")
        self.documents_Button.set_is_important(True)
        bookmarks_toolbar.insert(self.documents_Button, -1)

        self.downloads_Button = gtk.ToolButton(label="Downloads")
        self.downloads_Button.set_is_important(True)
        bookmarks_toolbar.insert(self.downloads_Button, -1)

        self.music_Button = gtk.ToolButton(label="Music")
        self.music_Button.set_is_important(True)
        bookmarks_toolbar.insert(self.music_Button, -1)

        self.pictures_Button = gtk.ToolButton(label="Pictures")
        self.pictures_Button.set_is_important(True)
        bookmarks_toolbar.insert(self.pictures_Button, -1)

        self.videos_Button = gtk.ToolButton(label="Videos")
        self.videos_Button.set_is_important(True)
        bookmarks_toolbar.insert(self.videos_Button, -1)
        
        #ends here

        #up home forward back search toolbar declaration
        
        toolbar = gtk.Toolbar()

        vbox.pack_start(toolbar, False, False, 0)

       
        #ends here

        #home and up buttons

        self.upButton = gtk.ToolButton(gtk.STOCK_GO_UP);
        self.upButton.set_is_important(True)
        self.upButton.set_sensitive(False)
        toolbar.insert(self.upButton, -1)

        homeButton = gtk.ToolButton(gtk.STOCK_HOME)
        homeButton.set_is_important(True)
        toolbar.insert(homeButton, -1)

        #ends here

        # Back and Forward buttons
       
        self.backButton = gtk.ToolButton(gtk.STOCK_GO_BACK)
        self.backButton.set_is_important(True)
        self.backButton.set_sensitive(False)
        toolbar.insert(self.backButton, -1)

        self.forwardButton = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
        self.forwardButton.set_is_important(True)
        self.forwardButton.set_sensitive(False)
        toolbar.insert(self.forwardButton, -1)

        #ends here

        #search bar
        sep = gtk.SeparatorToolItem() #seperator
        toolbar.insert(sep, 4)

        self.searchfile=gtk.Entry()
        self.searchfile.set_text("")
        item = gtk.ToolItem()
        item.add(self.searchfile)
        toolbar.insert(item, -1)
        
        self.searchButton = gtk.ToolButton(gtk.STOCK_FIND)
        self.searchButton.set_is_important(True)
        toolbar.insert(self.searchButton, -1)
        self.searchButton.connect("clicked",self.searchfunc)

        #ends here

        self.fileIcon = self.get_icon(gtk.STOCK_FILE)
        self.dirIcon = self.get_icon(gtk.STOCK_DIRECTORY)

        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)

        self.store = self.create_store()
        self.fill_store()

        #######
        eventbox = gtk.EventBox()

        iconView = gtk.IconView(self.store)
        iconView.set_selection_mode(gtk.SELECTION_MULTIPLE)


        #bookmarks toolbar signal connection
       
        self.desktop_Button.connect("clicked", self.on_desktop_clicked)
        self.documents_Button.connect("clicked", self.on_documents_clicked)
        self.downloads_Button.connect("clicked", self.on_downloads_clicked)
        self.music_Button.connect("clicked", self.on_music_clicked)
        self.pictures_Button.connect("clicked", self.on_pictures_clicked)
        self.videos_Button.connect("clicked", self.on_videos_clicked)
        
        #ends here

        #signal connection of up,home,forward and back buttons

        self.upButton.connect("clicked", self.on_up_clicked)
        homeButton.connect("clicked", self.on_home_clicked)
        self.backButton.connect("clicked", self.on_back_clicked)
        self.forwardButton.connect("clicked", self.on_forward_clicked)

        #ends

       

        iconView.set_text_column(COL_PATH)
        iconView.set_pixbuf_column(COL_PIXBUF)

        iconView.connect("item-activated", self.on_item_activated)  #extra

        iconView.connect("selection-changed", self.on_item_clicked)   #extra
        
        # extra 
        eventbox.add(iconView)

        # Right Click Popup menu

        rightClickMenu = gtk.Menu()

        item1 = gtk.MenuItem("Open")
        rightClickMenu.append(item1)
        item1.connect("activate",self.on_open_clicked,"Open")

        item2 = gtk.MenuItem("Copy")
        rightClickMenu.append(item2)    
        item2.connect("activate",self.on_copy,"Copy")
        
        item3 = gtk.MenuItem("Cut")
        rightClickMenu.append(item3)
        item3.connect("activate",self.on_cut,"Cut")

        item4 = gtk.MenuItem("Paste")
        rightClickMenu.append(item4)
        item4.connect("activate",self.on_paste,"Paste")

        item5 = gtk.MenuItem("Delete")
        rightClickMenu.append(item5)
        item5.connect("activate",self.on_delete,"Delete")

        # Terminal submenu
        terminalMenu = gtk.Menu()

        item6 = gtk.MenuItem("Launch Terminal")
        terminalMenu.append(item6)
        item6.connect("activate",self.on_launch_terminal_clicked)

        item7 = gtk.MenuItem("Launch Terminal in Current Directory")
        terminalMenu.append(item7)
        item7.connect("activate",self.on_launch_terminal_pwd_clicked)
        
        item8 = gtk.MenuItem("Terminal")
        rightClickMenu.append(item8)
        item8.set_submenu(terminalMenu)

        #Properties 
        item9 = gtk.MenuItem("Properties")
        rightClickMenu.append(item9)
        item9.connect("activate",self.on_properties_clicked)
        
        item10 = gtk.MenuItem("Rename")
        rightClickMenu.append(item10)
        item10.connect("activate",self.on_rename_clicked)

       

        item1.show()
        item2.show()
        item3.show()
        item4.show()
        item5.show()
        item6.show()
        item7.show()
        item8.show()
        item9.show()
        item10.show()

        terminalMenu.show()
        rightClickMenu.show()
        
        eventbox.connect_object("button-press-event", self.on_button_press_event,rightClickMenu)
        #iconView.connect("button-press-event", self.on_button_press_event_iconView)
        
        
        # RIght Click ends

        sw.add_with_viewport(eventbox)

        # extra ends
        iconView.grab_focus()

        self.add(vbox)
        self.show_all()

    def get_icon(self, name):
        theme = gtk.icon_theme_get_default()
        return theme.load_icon(name, 48, 0)


    def create_store(self):
        store = gtk.ListStore(str, gtk.gdk.Pixbuf, bool)
        store.set_sort_column_id(COL_PATH, gtk.SORT_ASCENDING)
        return store


    def fill_store(self):
        self.store.clear()

        if self.current_directory == None:
            return
        
        self.pwd.set_markup(self.current_directory)
        

        for fl in os.listdir(self.current_directory):

            if not fl[0] == '.':
                if os.path.isdir(os.path.join(self.current_directory, fl)):
                    self.store.append([fl, self.dirIcon, True])
                else:
                    self.store.append([fl, self.fileIcon, False])
                         

    #home button function

    def on_home_clicked(self, widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~'))
        self.fill_store()
        self.upButton.set_sensitive(True)

    #ends here

    # back and fwd functions 

    def on_back_clicked(self, widget):
        
        forward_stack.append(self.current_directory)
        self.current_directory = back_stack.pop()
        if not back_stack:
            self.backButton.set_sensitive(False) 
        self.forwardButton.set_sensitive(True)
        self.fill_store()
        self.upButton.set_sensitive(True)  

    def on_forward_clicked(self, widget):
        
        back_stack.append(self.current_directory)
        self.current_directory = forward_stack.pop()
        if not forward_stack:
            self.forwardButton.set_sensitive(False) 
        self.backButton.set_sensitive(True)
        self.fill_store()
        self.upButton.set_sensitive(True)         
        
        #end here
    

    def on_item_clicked(self, widget):

        mm = widget.get_cursor()
        if not mm:
            return
        
        selected_items = widget.get_selected_items()

        global model1

        del selected_path[:]
        del selected_isDir[:]
        for item in selected_items:
            model1 = widget.get_model()
            selected_path.append(model1[item][COL_PATH])
            selected_isDir.append(model1[item][COL_IS_DIRECTORY])        

    def on_open_clicked(self,widget,item):
        if not selected_isDir[0]:
            subprocess.call(["xdg-open",self.current_directory +"/"+selected_path[0]])  
            return

        back_stack.append(self.current_directory)
        forward_stack[:]= []
        self.forwardButton.set_sensitive(False)
        self.backButton.set_sensitive(True)
        self.current_directory = self.current_directory + os.path.sep + selected_path[0]
        self.fill_store()
        self.upButton.set_sensitive(True)


    def on_item_activated(self, widget, item):
        model = widget.get_model()
        #print model
        path = model[item][COL_PATH]
        #print path
        isDir = model[item][COL_IS_DIRECTORY] 
        #print isDir

        # opens a file withs its default preferred application(Ayudh)
        if not isDir:
            subprocess.call(["xdg-open",self.current_directory +"/"+path])
            return
        #ends here   
 
        # back and forward implementation
        back_stack.append(self.current_directory)
        forward_stack[:]= []
        self.forwardButton.set_sensitive(False)
        self.backButton.set_sensitive(True)
        self.current_directory = self.current_directory + os.path.sep + path
        self.fill_store()
        self.upButton.set_sensitive(True)

        #ends
    
    #up button function

    def on_up_clicked(self, widget):
        self.current_directory = os.path.dirname(self.current_directory)
        self.fill_store()
        sensitive = True
        if self.current_directory == "/": sensitive = False
        self.upButton.set_sensitive(sensitive)

    #ends here

    # Right Click Event

    def on_button_press_event(self, widget, event):
            # Check if right mouse button was preseed
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                # iconView.connect("",self.on_item_clicked)   #extra
                widget.popup(None, None, None, event.button, event.time)
                widget.grab_focus()
                return True # event has been handled
            #ends


    def copy(self, src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, dest)
            else:
                print('Directory not copied. Error: %s' % e)

    def on_copy(self,widget,event):
        del path2[:]
        del self.copy_dir[:]
        for path1 in selected_path:
            self.copy_dir.append(self.current_directory + os.path.sep + path1)
            path2.append((path1,0))
        print path2

    def on_cut(self,widget,event):
        del path2[:]
        del self.copy_dir[:]
        for path1 in selected_path:
            self.copy_dir.append(self.current_directory + os.path.sep + path1)
            path2.append((path1,1))
        print path2


    def on_paste(self,widget,event):
        for i in range(len(path2)):
            self.paste_dir = self.current_directory + os.path.sep + path2[i][0]
            if path2[i][1] == 0:
                self.copy(self.copy_dir[i],self.paste_dir)
                print "copied"
            else:
                shutil.move(self.copy_dir[i],self.paste_dir)        
                print "pasted"
        self.fill_store()

    def delete(self, path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                os.remove(path)
            else:
                print('Directory not copied. Error: %s' % e)

    def on_delete(self, widget, event):
        for x in selected_path:
            self.delpath = self.current_directory + os.path.sep + x
            self.delete(self.delpath)
            print self.delpath, "- deleted"
        
        self.fill_store()

    #Bookmarks bar functions

    def on_desktop_clicked(self,widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~/Desktop'))
        self.fill_store()
        self.upButton.set_sensitive(True)

    def on_documents_clicked(self,widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~/Documents'))
        self.fill_store()
        self.upButton.set_sensitive(True)  
        
    def on_downloads_clicked(self,widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~/Downloads'))
        self.fill_store()
        self.upButton.set_sensitive(True)  
        
    def on_music_clicked(self,widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~/Music'))
        self.fill_store()
        self.upButton.set_sensitive(True)  


    def on_pictures_clicked(self,widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~/Pictures'))
        self.fill_store()
        self.upButton.set_sensitive(True)  
        
    def on_videos_clicked(self,widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~/Videos'))
        self.fill_store()
        self.upButton.set_sensitive(True)         

    #ends here


    #search function
    
    def searchfunc(self,widget):
        fileName = self.searchfile.get_text()
        paths = "\n"
        for root, dirs, files in os.walk('/home', topdown=False):
            for name in files:
                if name == fileName:
                    paths += "  " + str(os.path.join(root, name))  + "  \n\n"
            for name in dirs:
                if name == fileName:
                    paths += "  " + str(os.path.join(root, name)) + "  \n\n"
        paths = paths[:-1]
        if len(paths) > 0 :
            self.popup = gtk.Window()
            self.popup.set_title( "Paths" )
            vbox = gtk.VBox(False,0)
            hbox = gtk.HBox(False)
            label = gtk.Label(paths)
            label.set_line_wrap( True )
            label.connect( "size-allocate",self.size_allocate)
            vbox.pack_start(gtk.Label(paths),True,False,0)
            closeButton = gtk.Button(" Close ")
            closeButton.set_sensitive(True)
            closeButton.connect("clicked",self.on_destroy)
            hbox.pack_start(closeButton,True,False,0)
            vbox.pack_start(hbox,True,False,10)
            self.popup.add(vbox)
            self.popup.set_type_hint( gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
            self.popup.show_all()

    def size_allocate(self,label,allocation):
        label.set_size_request(allocation.width - 2,-1)

    def on_destroy(self,popup):
        if not self.popup.emit("delete-event", gtk.gdk.Event(gtk.gdk.DELETE)):
            self.popup.destroy()
            self.searchfile.set_text("")
            
    #ends here

    #terminal menu commands
    
    def on_launch_terminal_clicked(self,widget):
      temp2="--working-directory="
      temp3="/~"
      subprocess.call(["gnome-terminal",temp2+temp3])

    def on_launch_terminal_pwd_clicked(self,widget):
      temp1="--working-directory="
      subprocess.call(["gnome-terminal",temp1+self.current_directory])    

    #ends here

    #about dialog box func

    def on_about_clicked(self, widget):
        dialog = about(self)
     
    #ends here

    def on_newfolder_clicked(self,widget):
        dialog = newfoldername(self) 
        gtk.Dialog.run(dialog)
        new_folder_path = self.current_directory + os.path.sep + new_name
        print new_folder_path
        os.mkdir(new_folder_path,0755)
        self.fill_store()
        

    def on_properties_clicked(self,widget):   
        #subprocess.call(["stat",self.current_directory +"/"+path1])
        global selected_path_for_prop
        selected_path_for_prop=self.current_directory +"/"+ selected_path[0]
        dialog = prop(self)

        
    def on_rename_clicked(self, widget):
        global file_to_be_renamed
        file_to_be_renamed=self.current_directory 
        global selected_path_for_prop
        selected_path_for_prop=self.current_directory +"/"+ selected_path[0]
        dialog = name(self)  
        gtk.Dialog.run(dialog)
        self.fill_store() 
        
             


PyApp()
gtk.main()
