from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from tkinter import filedialog
import os

class Notepad(Frame):
    def __init__(self, parent=None, file=None):
        Frame.__init__(self, parent)
        self.frm = Frame(parent)
        self.frm.pack(fill=X)
        self.buatJudul()
        parent.title('Notepad - Maulana ID')
        self.buatTombol()
        self.kolomTeksUtama()
        self.settext(text='',file=file)
        self.kolomTeks.config(font=('Consolas',10,"normal"))
        self.path = ''

    def buatTombol(self):
        Button(self.frm, text='Open', relief='flat', command=self.bukaFile).pack(side=LEFT)
        Button(self.frm, text='Simpan', relief='flat', command=self.perintahSimpan).pack(side=LEFT)

    def kolomTeksUtama(self):
        scroll = Scrollbar(self)
        kolomTeks = Text(self, relief='sunken')
        scroll.config(command=kolomTeks.yview)
        kolomTeks.config(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        kolomTeks.pack(side=LEFT, expand=YES, fil=BOTH)
        self.kolomTeks = kolomTeks
        self.pack(expand=YES, fill=BOTH)

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

    def settext(self, text='',file=None):
        if file:
            text = open(file, 'r').read()
            self.kolomTeks.delete('1.0', END)
            self.kolomTeks.insert('10', text)
            self.kolomTeks.mark_set(INSERT, '1.0')
            self.kolomTeks.focus()

    def gettext(self):
        return self.kolomTeks.get('1.0',END+'-1')

    def buatJudul(self):
        top = Frame(root)
        top.pack(fill=BOTH, expand=1, padx=17, pady=5)
        judul = Label(top, text="Judul : ")
        judul.pack(side="left")
        self.kolomJudul = Entry(top)
        self.kolomJudul.pack(side="left")

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

root = Tk()
Notepad(root)
mainloop()