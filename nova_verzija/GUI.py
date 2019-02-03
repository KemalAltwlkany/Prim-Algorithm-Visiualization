import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2
from primalg import*
import copy



a=False
global pairs
pairs=list([])
global objekat 
objekat = PrimovAlgoritam()
global nazad
nazad=True
global br_cvorova
br_cvorova=5


def dek():
    global objekat
    global nazad
    print('nazad klinuto')
    nazad=False
    objekat = PrimovAlgoritam()


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.font = tkfont.Font(family='Helvetica', size=15)

        container = tk.Frame(self,  width=800, height=600)
        container.pack(side="top", fill="both", expand=True)
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, Korak, Unos,  Animacija,):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Vizualizacija Primovog algoritma", font=controller.title_font)
        label.pack(side="top", fill="x", pady=100, padx=100)
        

        button1 = tk.Button(self, text="Slucajno generisati graf")
        button1.bind('<Button 1>', self.generisi_graf)

        button2 = tk.Button(self, text="Rucni unos grafa", command=lambda: controller.show_frame("Unos"))

        button1.pack()
        button2.pack()
        self.entry_1 = tk.Entry(self)
        self.entry_1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        button3 = tk.Button(self, text="OK",  command=lambda: self.broj())
        button3.pack()


        #label_1 = tk.Label(self, text="Broj cvorova")
        #label_1.place(relx=0.4, rely=0.5, anchor=tk.CENTER) 

    def broj(self):
        global br_cvorova
        global objekat
        br_cvorova=int(self.entry_1.get())
        self.entry_1.delete(0, tk.END)
        objekat.setuj_broj_cv(br_cvorova)

    def generisi_graf(self, event):
        global objekat
        objekat.generisi_nasumicni_graf_slova()
        self.controller.show_frame("PageOne")

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Graf je unesen!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        label_2=tk.Label(self, text="U narednom dijelu omogucena su 2 tipa vizualizacije", font=controller.font)
        label_3=tk.Label(self, text=" i to korak po korak, te animacioni prikaz.", font=controller.font)
        #label_2.pack(side="top", fill="x", pady=5)
        #label_3.pack(side="top", fill="x", pady=5)
        label_2.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        label_3.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

        button = tk.Button(self, text="Nazad",
                           command=lambda: (dek(), controller.show_frame("StartPage")))
        

        button_1 = tk.Button(self, text="Animacija", command=self.aktivacija)
                           #command=lambda:  self.aktivacija)
        #button_1.bind('<Button 1>', self.aktivacija)                   
        

        button_2 = tk.Button(self, text="Korak po korak",
                           command=lambda:  controller.show_frame("Korak"))

        button.place(relx=0.335, rely=0.7, anchor=tk.CENTER)                   
        button_1.place(relx=0.47, rely=0.7, anchor=tk.CENTER)
        button_2.place(relx=0.65, rely=0.7, anchor=tk.CENTER)


    def aktivacija(self):
        self.controller.show_frame("Animacija")
        objekat.zapocni_pretragu()
        global nazad
        while (objekat.animacija_u_toku and nazad):
            pass
        nazad=True
        dek()
        self.controller.show_frame("StartPage")
              

class Animacija(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller   
        label = tk.Label(self, text="Animacija u toku", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Nazad na pocetnu stranicu",
                           command=lambda:(dek(), controller.show_frame("StartPage")))
        
        
        img = tk.PhotoImage(file='satsat.png')
        self.lbl=tk.Label(self, image=img)
        self.lbl.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        button.place(relx=0.5, rely=0.87, anchor=tk.CENTER)


class Unos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #label = tk.Label(self, text="Unos grafa", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)

        label_1 = tk.Label(self, text="Cvor 1") 
        label_2 = tk.Label(self, text="Cvor 2") 
        label_3 = tk.Label(self, text="Tezina") 

        button3 = tk.Button(self, text="Dalje", fg="blue")
        button4 = tk.Button(self, text="Ponovni unos", fg="blue")
        button5 = tk.Button(self, text="Zavrsen unos", fg="blue", command=lambda: self.zavrsen_unos() )

        button3.bind('<Button 1>', self.dalje)
        button4.bind('<Button 1>', self.ponovni_unos)

        button3.place(relx=0.31, rely=0.7, anchor=tk.CENTER)
        button4.place(relx=0.46, rely=0.7, anchor=tk.CENTER)
        button5.place(relx=0.65, rely=0.7, anchor=tk.CENTER)

        label_1.place(relx=0.3, rely=0.2, anchor=tk.CENTER)
        label_2.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
        label_3.place(relx=0.3, rely=0.4, anchor=tk.CENTER) 
        self.entry_1 = tk.Entry(self) 
        self.entry_2 = tk.Entry(self) 
        self.entry_3 = tk.Entry(self)
        self.entry_1.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.entry_2.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        self.entry_3.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        button = tk.Button(self, text="    Nazad   ",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def zavrsen_unos(self):
        global pairs
        global objekat
        objekat.rucni_unos_grafa(pairs)
        self.controller.show_frame("PageOne")

    def dalje(self,event):
        global pairs
        pairs.append([int(self.entry_1.get()),int(self.entry_2.get()),int(self.entry_3.get())])
        self.entry_1.delete(0, tk.END)
        self.entry_2.delete(0, tk.END)
        self.entry_3.delete(0, tk.END)
        print(pairs)
    def ponovni_unos(self,event):
        global pairs
        pairs =list()
        self.entry_1.delete(0, tk.END)
        self.entry_2.delete(0, tk.END)
        self.entry_3.delete(0, tk.END)

class Korak(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda:(dek(), controller.show_frame("StartPage")))
        button.pack()
        button_1 = tk.Button(self, text="Sljedeci korak",
                           command=lambda: self.dalje())
        button_1.pack()

    def dalje(self):
        global objekat
        if(not(objekat.zadnja_iter)):
            objekat.step_by_step_iter()
        else:
            dek()
            self.controller.show_frame("StartPage")


if __name__ == "__main__":

    #objekat.generisi_nasumicni_graf_slova()
    app = SampleApp()   
    app.mainloop()