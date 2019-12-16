from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter import filedialog
from tkinter.messagebox import askokcancel
import os

class Notepad(Frame):
    def __init__(self, parent=None, file=None):
        Frame.__init__(self, parent)
        self.layoutkolom = Frame(root)
        self.frm = Frame(parent)
        self.frm.pack(fill=X)
        self.layoutkolom = Frame(root)
        self.buatJudul()
        self.parent =parent
        self.parent.title('Notepad - Maulana ID')
        self.buatTombol()
        self.kolomTeksUtama()
        self.settext(text='',file=file)
        self.kolomTeks.config(font=('Consolas',10,"normal"))
        self.path = ''
        self.indeks = 1.0
        self.buatCari()
        self.buatMenuBar()
        self.buatPopUp()

    def buatTombol(self):
        Button(self.frm, text='Open', relief='flat', command=self.bukaFile).pack(side=LEFT)
        Button(self.frm, text='Simpan', relief='flat', command=self.perintahSimpan).pack(side=LEFT)
        Button(self.frm, text='Copy', relief='flat', command=self.perintahCopy).pack(side=LEFT)
        Button(self.frm, text='Cut', relief='flat', command=self.perintahCut).pack(side=LEFT)
        Button(self.frm, text='Paste', relief='flat', command=self.perintahPaste).pack(side=LEFT)
        Button(self.frm, text='Undo', relief='flat', command=self.perintahUndo).pack(side=LEFT)
        Button(self.frm, text='Redo', relief='flat', command=self.perintahRedo).pack(side=LEFT)
        Button(self.frm, text='Keluar', relief='flat', command=self.perintahKeluar).pack(side=LEFT)

    def kolomTeksUtama(self):
        scroll = Scrollbar(self)
        kolomTeks = Text(self, relief='sunken')
        scroll.config(command=kolomTeks.yview)
        kolomTeks.config(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        kolomTeks.pack(side=LEFT, expand=YES, fil=BOTH)
        self.kolomTeks = kolomTeks
        self.pack(expand=YES, fill=BOTH)

    def buatMenuBar(self):
        self.menubar = Menu(self.parent,bd=0)
        self.fileMenu = Menu(self.parent,tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.bukaFile)
        self.fileMenu.add_command(label="Save", command=self.perintahSimpan)
        self.fileMenu.add_command(label="Exit", command=self.perintahKeluar)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        self.menuEdit = Menu(self.parent, tearoff=0)
        self.menuEdit.add_command(label="Undo", command=self.perintahUndo)
        self.menuEdit.add_command(label="Redo", command=self.perintahRedo)
        self.menuEdit.add_separator()
        self.menuEdit.add_command(label="Copy", command=self.perintahCopy)
        self.menuEdit.add_command(label="Cut", command=self.perintahCut)
        self.menuEdit.add_command(label="Paste", command=self.perintahPaste)
        self.menubar.add_cascade(label="Edit", menu=self.menuEdit)

        self.menuAbout = Menu(self.parent, tearoff=0)
        self.menuAbout.add_command(label="Tentang Aplikasi", command=self.about)
        self.menubar.add_cascade(label="About", menu=self.menuAbout)

        self.parent.config(menu=self.menubar)
        self.pack()

    def buatPopUp(self):
        self.menu = Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Undo", command=self.perintahUndo)
        self.menu.add_command(label="Pilih Semua", command=self.perintahPilihSemua)
        self.menu.add_command(label="Redo", command=self.perintahRedo)
        self.menu.add_separator()
        self.menu.add_command(label="Copy", command=self.perintahCopy)
        self.menu.add_command(label="Cut", command=self.perintahCut)
        self.menu.add_command(label="Paste", command=self.perintahRedo)
        self.menu.add_separator()
        self.parent.bind("<Button-3>",self.tampilkanMenu)
        self.pack()

    def tampilkanMenu(self, e):
        self.menu.post(e.x_root,e.y_root)

    def perintahSimpan(self):
        print(self.path)
        if self.path:
            alltext = self.gettext()
            open(self.path, 'w').write(alltext)
            messagebox.showinfo('File Telah Tersimpan!')
        else:
            tipeFile = [('Text file','*.txt'), ('Python file', '*asdf.py'), ('All files','.*')]
            filename = asksaveasfilename(filetypes=(tipeFile), initialfile=self.kolomJudul.get())
            if filename:
                alltext = self.gettext()
                open(filename, 'w').write(alltext)
                self.path = filename

    def perintahCopy(self):
        try:
            text = self.kolomTeks.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
            self.kolomTeks.selection_clear()
        except:
            pass

    def perintahCut(self):
        try:
            text = self.kolomTeks.get(SEL_FIRST, SEL_LAST)
            self.kolomTeks.delete(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
        except:
            pass

    def perintahPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.kolomTeks.insert(INSERT, text)
        except TclError:
            pass

    def perintahFind(self):
        target = self.kolomCari.get()
        if target:
            self.indeks = self.kolomTeks.search(target, str(float(self.indeks) + 0.1), stopindex=END)
            if self.indeks:
                pastit = self.indeks + ('+%dc' % len(target))
                self.kolomTeks.tag_remove(SEL, '1.0', END)
                self.kolomTeks.tag_add(SEL, self.indeks, pastit)
                self.kolomTeks.mark_set(INSERT, pastit)
                self.kolomTeks.see(INSERT)
                self.kolomTeks.focus()
            else:
                self.indeks = '0.9'

    def perintahKeluar(self):
        ans = askokcancel('Keluar', "Anda yakin ingin keluar")
        if ans:
            Frame.quit(self)

    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
            self.kolomTeks.delete('1.0', END)
            self.kolomTeks.insert('10', text)
            self.kolomTeks.mark_set(INSERT, '1.0')
            self.kolomTeks.focus()

    def gettext(self):
        return self.kolomTeks.get('1.0',END+'-1c')

    def buatJudul(self):
        top = Frame(root)
        top.pack(fill=BOTH, expand=1, padx=17, pady=5)
        judul = Label(top, text="Judul : ")
        judul.pack(side="left")
        self.kolomJudul = Entry(top)
        self.kolomJudul.pack(side="left")

    def buatCari(self):
        Button(self.frm, text='Cari', command=self.perintahFind).pack(side="right")
        self.kolomCari = Entry(self.frm)
        self.kolomCari.pack(side="right")

    def bukaFile(self):
        extensiFile = [('All files', '*'), ('Text files', '*.txt'), ('Python files', '*.py')]
        buka = filedialog.askopenfilename(filetypes = extensiFile)
        if buka !='':
            text = self.readFile(buka)
            if text:
                self.path = buka
                nama = os.path.basename(buka)
                self.kolomJudul.delete(0, END)
                self.kolomJudul.insert(END, nama)
                self.kolomTeks.delete('1.0', END)
                self.kolomTeks.insert(END, text)

    def readFile(self, filename):
        try:
            x = open(filename, "r")
            text = x.read()
            return text
        except:
            messagebox.showerror("Error!!! file tidak bisa di buka")
            return None

    def about(self):
        messagebox.showinfo("Tentang Aplikasi", "Aplikasi Notepad/Teks Editor Sederhana\n"
                            "Yang Terbuat Dari Bahasa Python\n"
                            "Mohon Maaf Sekiranya Ada Yang Salah\n"
                            "Dan Mungkin Ada Sedikit Bug\n"
                            "\n"
                            "Created By Maulana ID")

    def perintahUndo(self):
        try:
            self.kolomTeks.edit_undo()
        except:
            pass

    def perintahRedo(self):
        try:
            self.kolomTeks.edit_redo()
        except:
            pass
    def perintahPilihSemua(self):
        self.kolomTeks.tag_add(SEL, '1.0', END)
        self.kolomTeks.mark_set(INSERT, END)
        self.kolomTeks.see(INSERT)
        self.kolomTeks.focus()

root = Tk()
Notepad(root)
mainloop()