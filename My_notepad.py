import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.colorchooser import *
from tkinter import ttk
import tkinter.font as tkFont


class MyNotepad:
    __root = Tk()
    __textArea = Text(__root)

    # Menu Design
    __MenuBar = Menu(__root)
    __FileMenu = Menu(__MenuBar, tearoff=0)
    __EditMenu = Menu(__MenuBar, tearoff=0)
    __FormatMenu = Menu(__MenuBar, tearoff=0)
    __FontStyle = Menu(__FormatMenu, tearoff=0)
    __FontColor = Menu(__FormatMenu, tearoff=0)

    __ViewMenu = Menu(__MenuBar, tearoff=0)
    __ZoomMenu = Menu(__ViewMenu, tearoff=0)

    __HelpMenu = Menu(__MenuBar, tearoff=0)
    popup_menu = Menu(__root, tearoff=0)
    # Scrolling
    __ScrollBar = Scrollbar(__textArea)

    __file = None
    __edited = 0
    __currentSave = 0
    __size = 10
    __defaultStyle = ""
    __find = None
    __replace = None
    __k = 1
    __top = None
    __r = None
    __font_family = "times new roman"
    __font_size = 8
    __font_weight = "normal"
    __font = ["Times New Roman", "Wide Latin""Rockwell Extra Bold", "Segoe UI Semibold", "MV Boli",
              "Matura MT Script Capitals", "Microsoft Sans Serif""Gill Sans Ultra Bold", "Cooper Black", "Algerian",
              "Goudy Stout", "Corbel", "Arial black", "Calibri", "Berlin Sans FB Demi"]
    __sizeF = [8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
    __weight = ["bold", "italic", "normal"]

    def __init__(self, **kwargs):

        # self.__root = master
        # self.__root.geometry("700x400")
        # icon
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass
        self.__callingBinding()
        # Set window size as mentioned above (the default is 300x300)
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Center the window
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        # For left-allin
        left = (screen_width / 2) - (self.__thisWidth / 2)
        # For right-allin
        up = (screen_height / 2) - (self.__thisHeight / 2)
        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, up))
        # To make the text area auto resizable
        self.__root.title("*untiled - Notepad")
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__textArea.grid(sticky=N + E + W + S)
        self.binding_functions_config()
        self.__ScrollBar.configure(cursor="plus")
        self.popUp()

        # Starting File Menu
        self.new_image = PhotoImage(file="img/new.png").subsample(24, 24)
        self.new_window = PhotoImage(file="img/nwindow.png").subsample(24, 24)
        self.open_image = PhotoImage(file="img/open.png").subsample(24, 24)
        self.save_image = PhotoImage(file="img/save.png").subsample(24, 24)
        self.save_as = PhotoImage(file="img/saveas.png").subsample(24, 24)
        self.print_image = PhotoImage(file="img/print.png").subsample(24, 24)
        self.exit_image = PhotoImage(file="img/exit.png").subsample(24, 24)

        self.__FileMenu.add_command(label="New", image=self.new_image, compound=LEFT, accelerator='Ctrl+N',
                                    command=self.__newFile)

        self.__FileMenu.add_command(label="New Window", image=self.new_window, compound=LEFT, accelerator='Ctrl+W',
                                    command=self.__createNew)
        self.__FileMenu.add_command(label="Open...", image=self.open_image, compound=LEFT, accelerator='Ctrl+O',
                                    command=self.__openFile)

        self.__FileMenu.add_command(label="Save", image=self.save_image, compound=LEFT, accelerator='Ctrl+S',
                                    command=self.__saveFile)

        self.__FileMenu.add_command(label="Save As", image=self.save_as, compound=LEFT, command=self.__saveASFile)
        self.__FileMenu.add_separator()
        self.__FileMenu.add_command(label="Print...", image=self.print_image, compound=LEFT, accelerator='Ctrl+P')
        self.__FileMenu.add_separator()
        self.__FileMenu.add_command(label="Exit", image=self.exit_image, compound=LEFT, accelerator='Ctrl+Q')
        self.__MenuBar.add_cascade(label="File", menu=self.__FileMenu)

        # Starting Edit Menu
        self.undo_image = PhotoImage(file="img/undo.png").subsample(24, 24)
        self.redo_image = PhotoImage(file="img/redo.png").subsample(24, 24)
        self.cut_image = PhotoImage(file="img/cut.png").subsample(24, 24)
        self.copy_image = PhotoImage(file="img/copy.png").subsample(24, 24)
        self.paste_image = PhotoImage(file="img/paste.png").subsample(24, 24)
        self.delete_image = PhotoImage(file="img/delete.png").subsample(24, 24)
        self.find_image = PhotoImage(file="img/find.png").subsample(24, 24)
        self.replace_image = PhotoImage(file="img/replace.png").subsample(24, 24)
        self.select_all_image = PhotoImage(file="img/sall.png").subsample(24, 24)

        self.__EditMenu = Menu(self.__MenuBar, tearoff=0)
        self.__EditMenu.add_command(label="Undo", image=self.undo_image, compound=LEFT, command=lambda: self.__undoText())
        self.__EditMenu.add_command(label="Redo", image=self.redo_image, compound=LEFT, command=self.__redoText)
        self.__EditMenu.add_separator()
        self.__EditMenu.add_command(label="Cut", image=self.cut_image, compound=LEFT, accelerator='Ctrl+X',
                                    command=self.__cut)

        self.__EditMenu.add_command(label="Copy", image=self.copy_image, compound=LEFT, accelerator='Ctrl+C',
                                    command=self.__copy)

        self.__EditMenu.add_command(label="Paste", image=self.paste_image, compound=LEFT, accelerator='Ctrl+V',
                                    command=self.__paste)

        self.__EditMenu.add_command(label="Delete", image=self.delete_image, compound=LEFT, accelerator='Ctrl+D')
        self.__EditMenu.add_separator()
        self.__EditMenu.add_command(label="Find ", image=self.find_image, compound=LEFT, accelerator='Ctrl+F',command=lambda: self.find_replace(1))
        self.__EditMenu.add_command(label="Replace", image=self.replace_image, compound=LEFT,command=lambda: self.find_replace(2))
        self.__EditMenu.add_separator()
        self.__EditMenu.add_command(label="Select All", image=self.select_all_image, compound=LEFT,
                                    accelerator='Ctrl+A', command=self.__selectAll)
        self.__MenuBar.add_cascade(label="Edit", menu=self.__EditMenu)

        # Starting format Menu
        self.font_style_image = PhotoImage(file="img/fontstyle.png").subsample(24, 24)
        self.font_color_image = PhotoImage(file="img/fontcolor.png").subsample(24, 24)

        self._FormatMenu = Menu(self.__MenuBar, tearoff=0)
        self.__FormatMenu.add_checkbutton(label="Word Wrap", onvalue=1, offvalue=0)
        self.__FormatMenu.add_command(label="Font Style", image=self.font_style_image, compound=LEFT, command=self.__fontStyle)
        self.__FormatMenu.add_command(label="Font Color",image=self.font_color_image, compound=LEFT, command=self.__textColor)
        self.__MenuBar.add_cascade(label="Format", menu=self.__FormatMenu)


        # Starting View Menu
        self.zoom_in_image = PhotoImage(file="img/zoomin.png").subsample(24, 24)
        self.zoom_out_image = PhotoImage(file="img/zoomout.png").subsample(24, 24)
        self.default_image = PhotoImage(file="img/default.png").subsample(24, 24)

        self.__ViewMenu = Menu(self.__MenuBar, tearoff=0)
        self.__MenuBar.add_cascade(label="View", menu=self.__ViewMenu)
        self.__ZoomMenu.add_command(label="Zoom In", image=self.zoom_in_image, compound=LEFT, command=self.__zoomIn)
        self.__ZoomMenu.add_command(label="Zoom Out", image=self.zoom_out_image, compound=LEFT, command=self.__zoomOut)
        self.__ZoomMenu.add_command(label="Restore Default Zoom", image=self.default_image, compound=LEFT,
                                    command=self.__zoomDefault)

        self.__ViewMenu.add_cascade(label="Zoom", image=self.default_image, compound=LEFT, menu=self.__ZoomMenu)

        # Starting Help Menu
        self.help_image = PhotoImage(file="img/help.png").subsample(24, 24)
        self.feed_image = PhotoImage(file="img/feedback.png").subsample(24, 24)
        self.about_image = PhotoImage(file="img/about.png").subsample(24, 24)

        self.__HelpMenu = Menu(self.__MenuBar, tearoff=0)
        self.__HelpMenu.add_command(label="View Help", image=self.help_image, compound=LEFT, command=self.__helpSection)
        self.__HelpMenu.add_command(label="Send Feedback", image=self.feed_image, compound=LEFT, command=self.__feedBack)
        self.__HelpMenu.add_separator()
        self.__HelpMenu.add_command(label="About notepad", image=self.about_image, compound=LEFT,
                                    command=self.__aboutSection)

        self.__MenuBar.add_cascade(label="Help", menu=self.__HelpMenu)

        # Some Important
        self.__root.config(menu=self.__MenuBar)
        self.__ScrollBar.pack(side=RIGHT, fill=Y)
        self.__ScrollBar.config(command=self.__textArea.yview)
        self.__textArea.config(yscrollcommand=self.__ScrollBar.set)

# Exit Window
    def __exitNotepad(self, *event):
        self.__root.destroy()

# Zoom Section
    def __zoomIn(self, *event):
        self.__size = self.__size + 5 if self.__size < 50 else self.__size
        self.__textArea.config(font=(self.__defaultStyle, self.__size))

    def __zoomOut(self, *event):
        self.__size = self.__size - 5 if self.__size < 50 else self.__size
        self.__textArea.config(font=(self.__defaultStyle, self.__size))

    def __zoomDefault(self, *event):
        self.__textArea.config(font=(self.__defaultStyle, 10))

# Format Section
    def __textColor(self):
        (a, b) = askcolor()
        self.__textArea.config(fg=b)

    def __fontStyle(self,*event):
        window = Toplevel()
        window.minsize(height=400, width=410)
        window.maxsize(height=400, width=410)

        Label(window).grid(row=0, column=0)
        Label(window, text="Font :").grid(row=0, column=1, sticky="W")
        Label(window).grid(row=0, column=2)
        Label(window, text="Font Style :").grid(row=0, column=3, sticky="W")
        Label(window).grid(row=0, column=4)
        Label(window, text="Size :").grid(row=0, column=5, sticky="W")
        t1 = Entry(window, width=30)
        t1.grid(row=1, column=1)
        t1.insert(0, self.__font_family)

        t2 = Entry(window)
        t2.grid(row=1, column=3)
        t2.insert(0, self.__font_weight)

        t3 = Entry(window, width=10)
        t3.grid(row=1, column=5)
        t3.insert(0, self.__font_size)

        def CurSelet_lbox(evt):
            try:
                self.__font_family = lbox.get(lbox.curselection())
                t1.delete(0, END)
                t1.insert(0, self.__font_family)
                myFont.configure(family=self.__font_family)
            except TclError:
                return

        def CurSelet_lbox2(evt):
            try:
                self.__font_weight = lbox2.get(lbox2.curselection())
                t2.delete(0, END)
                t2.insert(0, self.__font_weight)
                myFont.configure(weight=self.__font_weight)

            except TclError:
                return

        def CurSelet_lbox3(evt):
            try:
                self.__font_size = int(lbox3.get(lbox3.curselection()))
                t3.delete(0, END)
                t3.insert(0, self.__font_size)
                myFont.configure(size=self.__font_size)
            except TclError:
                return

        def click_OK():
            self.__textArea.config(font=myFont)
            window.destroy()

        myFont = tkFont.Font(family=self.__font_family, size=self.__font_size, weight=self.__font_weight)
        lbox = Listbox(window, width=30, height=8)
        lbox.grid(row=2, column=1)
        lbox.bind('<<ListboxSelect>>', CurSelet_lbox)

        lbox2 = Listbox(window, height=8)
        lbox2.grid(row=2, column=3)
        lbox2.bind('<<ListboxSelect>>', CurSelet_lbox2)
        lbox3 = Listbox(window, width=10, height=8)
        lbox3.grid(row=2, column=5)
        lbox3.bind('<<ListboxSelect>>', CurSelet_lbox3)
        label_frame = LabelFrame(window, text="Sample", width=50, height=30)
        label_frame.grid(row=3, column=2, columnspan=4, sticky="E",
                         padx=5, pady=10, ipadx=70, ipady=30)
        sample = Label(label_frame, text="AaBbYyZz", font=myFont)
        sample.place(x=60, y=25)
        # sample["text"] = myFont

        b1 = ttk.Button(window, text="OK", width=12, command=click_OK)
        b1.grid(row=4, column=3, pady=80)
        b2 = ttk.Button(window, text="Cancel", width=12, command=lambda: window.destroy())
        b2.grid(row=4, column=4, columnspan=3, pady=80)
        for font in self.__font:
            lbox.insert(END, font)
        for weight in self.__weight:
            lbox2.insert(END, weight)
        for size in self.__sizeF:
            lbox3.insert(END, size)
        window.update()



# Help Section
    def __helpSection(self):
        showinfo("Information","Developed By Adarsh Raj")

    def __aboutSection(self):
        showinfo("Information","Developed By Adarsh Raj")

    def __feedBack(self):
        showinfo("Information","Developed By Adarsh Raj")

# Edit Section

    def __cut(self, *args):
        self.__textArea.event_generate("<<Cut>>")

    def __copy(self, *args):
        self.__textArea.event_generate("<<Copy>>")

    def __paste(self, *args):
        self.__textArea.event_generate("<<Paste>>")

    # undo-redo Section
    def binding_functions_config(self):
        self.__textArea.tag_configure("sel", background="red")
        self.__textArea.configure(undo=True, autoseparators=True, maxundo=-1)
        return

    def __undoText(self, *event):
        self.__textArea.event_generate("<<Undo>>")

    def __redoText(self, *event):
        self.__textArea.event_generate("<<Redo>>")

    def __selectAll(self, *event):
        pass


# Find And Replace Section
    def __findText(self,*event):

        self.__textArea.tag_remove('found', '1.0', END)
        alltext = str(self.__textArea.get(1.0, END))
        if len(alltext) > 1:
            s = self.__find.get()
            if s:
                idx = '1.0'
                while 1:
                    idx = self.__textArea.search(s, idx, nocase=1, stopindex=END)
                    if not idx:
                        break
                    lastidx = '%s+%dc' % (idx, len(s))
                    self.__textArea.tag_add('found', idx, lastidx)
                    idx = lastidx
                self.__textArea.tag_config('found', foreground="red")
            self.__find.focus_set()
        else:
            showwarning("Warning", "Notepad is Empty")

    def __replaceText(self,*event):

        find1 = self.__find.get()
        replace1 = str(self.__replace.get())

        alltext = str(self.__textArea.get(1.0, END))
        if find1 and replace1:
            alltext1 = alltext.replace(find1, replace1)
            self.__textArea.delete(1.0, END)
            self.__textArea.insert('1.0', alltext1)
        else:
            showwarning("Warning")

    # Here the Display copy of popup box
    def find_replace(self,s):

        if self.__k != 0:
            if s == 1:
                self.__k = 0

                self.__top = Toplevel()
                self.__top.title("Find")
                self.height(300, 75, self.__top)
                # top.minsize(width=300, height=75)
                # top.maxsize(width=300, height=75)
                frame = Frame(self.__top)
                Label(frame).grid(row=0, column=0)
                Label(frame, text="Find What").grid(row=1, column=0)
                self.__find = ttk.Entry(frame)
                self.__find.grid(row=1, column=1)
                f = ttk.Button(frame, text="Find", command=self.__findText)
                f.grid(row=1, column=2)
                frame.grid(row=0, column=1)

                self.__top.bind("<Destroy>", self.__resetFlag)
                # top.mainloop()
            else:
                self.__k = 0
                # top.destroy()
                self.__top = Toplevel()
                self.__top.title("Find & Replace")
                self.height(300, 150, self.__top)
                frame = Frame(self.__top)
                Label(frame).grid(row=0, column=0)
                Label(frame, text="Find What").grid(row=1, column=0)
                self.__find = ttk.Entry(frame)
                self.__find.grid(row=1, column=1)
                f = ttk.Button(frame, text="Find", command=self.__findText)
                f.grid(row=1, column=2)
                Label(frame).grid(row=2, column=0)
                Label(frame, text="Replace With").grid(row=3, column=0)
                self.__replace = ttk.Entry(frame)
                self.__replace.grid(row=3, column=1)
                self.__r = ttk.Button(frame, text="Replace", command=self.__replaceText)
                self.__r.grid(row=3, column=2)
                frame.grid(row=0, column=1)

                self.__top.bind("<Destroy>", self.__resetFlag)

    def height(self,w, h, __top):
        __top.minsize(width=w, height=h)
        __top.maxsize(width=w, height=h)

# <.............close section of Find And Replace .........>



# Open File
    def __openFile2(self):
        try:
            self.__file = askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"),
                                                                              ("All Files", "*.*")])
            if self.__file == "":
                # no file to open
                self.__file = None
            else:
                # Try to open the file
                # set the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
                self.__textArea.delete(0.0, END)
                file = open(self.__file, "r")
                self.__textArea.insert(0.0, file.read())
                file.close()
        except TypeError:
            return
        except AttributeError:
            return

    def __openFile(self, *event):
        if len(self.__textArea.get(1.0, END)) != 1:
            ask = askyesnocancel("My Notepad", "Do You Want to Save Changes in this file")
            if ask == YES:
                self.__saveFile()
                self.__openFile2()
            elif ask == NO:
                self.__textArea.delete(0.0, END)
                self.__root.title("*untitled-Notepad")
                self.__openFile2()

            else:
                pass

        else:
            self.__openFile2()

# New File
    def __newFile(self, *event):
        try:
            if self.__edited == 0:
                if self.__currentSave == 0:
                    self.__file = None
                    self.__textArea.delete(0.0, END)
                    self.__root.title("* new untitled-Notepad")
                    self.__currentSave = 1

            else:
                ask = askyesnocancel("My Notepad", "Do You Want to Save Changes in this file")
                if ask == YES:
                    self.__saveFile()
                    self.__file = None
                    self.__textArea.delete(0.0, END)
                    self.__root.title("untitled-Notepad")
                    self.__currentSave = 0
                elif ask == NO:
                    self.__textArea.delete(0.0, END)
                    self.__root.title("untitled-Notepad")
                    self.__edited = 0
                    self.__currentSave = 1
                else:
                    pass

        except TypeError:
            return

# Save File
    def __saveFile(self, *event):
        try:
            if self.__file == None:
                # Save as new file
                self.__file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                                filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

                if self.__file == "":
                    self.__file = None
                else:
                    # Try to save the file
                    file = open(self.__file, "w")
                    file.write(self.__textArea.get(1.0, END))
                    file.close()
                    self.__currentSave = 1
                    self.__edited = 0

                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
            else:
                file = open(self.__file, "w")
                file.write(self.__textArea.get(1.0, END))
                file.close()
                self.__currentSave = 1
                self.__edited = 0
            self.__root.title(os.path.basename("untiled") + " - Notepad")

        except TypeError:
            return

# Save As File
    def __saveASFile(self, *event):
        try:
            files = [('Text Document', '*.txt')]
            loc = asksaveasfile(mode='w', initialfile='Untitled.txt', initialdir="/", title="Save File",
                                filetypes=files, defaultextension=files)
            fin = str(self.__textArea.get(0.0, END))
            loc.write(fin)
            loc.close()
        except TypeError:
            return
        except AttributeError:
            return

# For Value of edited
    def __resetFlag(self, *event):
        self.__edited = 1
        self.__k = 1
        try:
            self.__textArea.tag_config('found', foreground="black")
        except:
            return

# For Binding All the Shortcut Keys
    def __callingBinding(self):

        self.__root.bind("<Control-q>", self.__exitNotepad)
        self.__root.bind("<Control-i>", self.__zoomIn)
        self.__root.bind("<Control-d>", self.__zoomOut())
        self.__root.bind("<Control-l>", self.__zoomDefault())

        self.__root.bind("<Control-s>", self.__saveFile)
        self.__root.bind("<Control-o>", self.__openFile)
        self.__root.bind("<Control-n>", self.__newFile)
        self.__root.bind("<Control-w>", self.__createNew)

        self.__root.bind("<Control-x>", self.__cut)
        self.__root.bind("<Control-c>", self.__copy)
        self.__root.bind("<Control-v>", self.__paste)
        self.__root.bind("<Button-3>", self.showPopup)
        self.__textArea.bind("<Control-u>", self.__undoText)
        self.__textArea.bind("<Control-y>", self.__redoText)
        #self.__root.bind("<Control-t>", self.find_replace(1))
        #self.__root.bind("<Control-r>", self.find_replace(2))
        self.__root.bind("<Key>", self.__resetFlag)

# SHOW POPUP
    def showPopup(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def popUp(self):

        self.popup_menu.add_command(label="Undo", command=lambda: self.__undoText)
        self.popup_menu.add_command(label="Redo", command=lambda: self.__redoText)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Cut", accelerator='Ctrl+X', command=self.__cut)
        self.popup_menu.add_command(label="Copy", accelerator='Ctrl+C', command=self.__copy)
        self.popup_menu.add_command(label="Paste", accelerator='Ctrl+V', command=self.__paste)
        self.popup_menu.add_command(label="Delete", accelerator='Ctrl+D', command=lambda: print("!!hello"))
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Select All", command=lambda: print("select all"))

# Opening New Window
    def __createNew(self, *event):
        print("New Window")
        pass
        #newwindow = Toplevel()
        #c= MyNotepad(newwindow)
        #newwindow.configure(c=("new", MyNotepad()))
        #newwindow.mainloop()
        #self.runApplication()

    #  For Running The Notepad
    def runApplication(self):
        self.__root.mainloop()


if __name__ == '__main__':
    # top1 = Toplevel()
    notepad = MyNotepad(width=600, height=400)
    # top1.mainloop()
    notepad.runApplication()
