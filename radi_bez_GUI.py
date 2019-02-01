import networkx as nx
import matplotlib.pyplot as plt
import random as random
import Tkinter as tk


def daj_tezinu_grane(grana):
    return grana[2]

class PrimovAlgoritam:

    def __init__(self):
        self.G = nx.Graph()
        self.prvo_crtanje = True
        self.color_map = []
        self.edge_map = []
        
        #za prima pomocne varijable
        self.all_pairs=[]
        self.not_added_pairs=[]
        self.added_pairs=[]
        self.curr_pairs=[]
        self.all_nodes=[]
        self.added_nodes=[]
        self.not_added_nodes=[]
        self.poc_cvor=None

        self.zabranjeni_indeksi=[]
        self.br_dodanih=1
        self.bestezinske_grane=[]

    def GUI(self):
        root = tk.Tk()
        theLabel = tk.Label(root, text="this is too izi")
        theLabel.pack()
        root.mainloop()

    def daj(self):
        return self.prvo_crtanje

    def dajg(self):
        return self.G

    def generisi_nasumicni_graf_slova(self):
        # nasumicni graf ima 10-26 cvorova, slova abecede
        br_cvor = random.randint(4, 7)
        for i in range(0, br_cvor, 1):
            self.G.add_node(i)
            self.all_nodes.append(i)
            self.not_added_nodes.append(i)

        # graf ce imati (3*br_cvorova) grana
        for i in range(2 * self.G.number_of_nodes()):
            cvor1 = random.randint(0, self.G.number_of_nodes() - 1)
            cvor2 = random.randint(0, self.G.number_of_nodes() - 1)
            while cvor1==cvor2:
                cvor2 = random.randint(0, self.G.number_of_nodes() - 1)
            tezina = max(cvor1,cvor2)
            if ((cvor1,cvor2) in self.bestezinske_grane) or ((cvor2,cvor1) in self.bestezinske_grane):
                continue
            self.bestezinske_grane.append((cvor1,cvor2))
            self.G.add_edge(cvor1, cvor2, color='black', weight=tezina)
            self.all_pairs.append((cvor1,cvor2,tezina))
            self.not_added_pairs.append((cvor1,cvor2,tezina))
        print('----------------- sve grane --------')
        print('all pairs', self.all_pairs)
        print('not_added_pairs', self.not_added_pairs)
        print('----------')

    def crtaj_cvor(self, tjt):
        # moze koncept biti iskoristen za drugu boju trenutne grane ili cvora
        # samo druga varijabla posto se self.edge_map koristi vec
        # self.edge_map = ['red' if e[0]==tjt else 'black' for e in self.G.edges]
        if self.prvo_crtanje:
            for node in self.G:
                self.color_map.append('blue')
            for i in range(len(self.G.edges)):
                self.edge_map.append('black')
            self.prvo_crtanje = False
        else:
            #plt.gcf().clear()
            for node in range(len(self.color_map)):
                if node == tjt:
                    self.color_map[node] = 'green'
            i = 0
            for e in self.G.edges:
                if e[0] == tjt or e[1] == tjt:
                    self.edge_map[i] = 'red'
                i += 1
        plt.pause(2)
        #pos = nx.get_node_attributes(self.G, 'pos')
        #labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx(self.G, pos=nx.circular_layout(self.G),
                         node_color=self.color_map, with_labels=True,
                         edge_color=self.edge_map)
        #kemo
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos=nx.circular_layout(self.G),
                                     edge_labels=labels)

    def crtaj_graf(self, tjt, grana):
        # moze koncept biti iskoristen za drugu boju trenutne grane ili cvora
        # samo druga varijabla posto se self.edge_map koristi vec
        # self.edge_map = ['red' if e[0]==tjt else 'black' for e in self.G.edges]
        if self.prvo_crtanje:
            for node in self.G:
                self.color_map.append('blue')
            for i in range(len(self.G.edges)):
                self.edge_map.append('black')
            self.prvo_crtanje = False
        else:
            #plt.gcf().clear()
            for node in range(len(self.color_map)):
                if node == tjt:
                    self.color_map[node] = 'green'
            
            i = 0
            for e in self.G.edges:
                if e[0] == tjt or e[1] == tjt:
                    if not (i in self.zabranjeni_indeksi):
                        self.edge_map[i] = 'red'
                i += 1
            i = 0
            for e in self.G.edges:
                if ( e[0] == grana[0] and e[1]==grana[1] ) or ( e[1] == grana[0] and e[0]==grana[1] ):
                    self.edge_map[i] = 'yellow'
                    self.zabranjeni_indeksi.append(i)
                i += 1
        plt.pause(2)
        #pos = nx.get_node_attributes(self.G, 'pos')
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx(self.G, pos=nx.circular_layout(self.G),
                         node_color=self.color_map, with_labels=True,
                         edge_color=self.edge_map)
        nx.draw_networkx_edge_labels(self.G, pos=nx.circular_layout(self.G),
                                     edge_labels=labels)

    #funkcija uklanja grane koje povezuju dva cvora koja vec imamo u sastavu kostura
    def ukloni_zabranjene(self, cvor):
        for x in self.curr_pairs:
            if ( x[0]==cvor and (x[1] in self.added_nodes) ):
                self.curr_pairs.remove(x)
            if ( x[1]==cvor and (x[0] in self.added_nodes) ):
                self.curr_pairs.remove(x)

    #funkcija dodaje sve grane novododanog cvora u listu (tako da se mogu razmatrati)
    def dodaj_nove_grane(self, cvor):
        #n=len(self.not_added_pairs)
        #for i in range(len(self.not_added_pairs)):
        #    if self.not_added_pairs[i][0]==cvor or self.not_added_pairs[i][1]==cvor:
        #        self.curr_pairs.append(self.not_added_pairs.pop(i))
        #        n=n-1
        #        i=i-1

        pomocni=[]
        for grana in self.not_added_pairs:
            print(grana)
            if grana[0]==cvor or grana[1]==cvor:
                self.curr_pairs.append(grana)
                pomocni.append(grana)
        for grana in pomocni:
            self.not_added_pairs.remove(grana)
                #self.not_added_pairs.remove(grana)
                
        #bugfix, ne smiju se ukloniti grane za zadnji cvor, ostane nepovezan
        #if self.br_dodanih<len(self.all_nodes):
        #self.ukloni_zabranjene(cvor)
    
    #azurira cvorove, odnosno novododani uklanja iz liste "nedodanih" i ubacuje u listu "dodanih"
    def azuriraj_cvorove(self, grana):
        if not(grana[0] in self.added_nodes):
            self.added_nodes.append(grana[0])
            self.not_added_nodes.remove(grana[0])
            return grana[0]

        if not(grana[1] in self.added_nodes):
            self.added_nodes.append(grana[1])
            self.not_added_nodes.remove(grana[1])
            return grana[1]


    def zapocni_pretragu(self):
        self.crtaj_cvor(1000)
        self.poc_cvor=3
        self.added_nodes.append(self.poc_cvor)
        self.not_added_nodes.remove(self.poc_cvor)
        self.dodaj_nove_grane(self.poc_cvor)
        self.crtaj_cvor(self.poc_cvor)
        self.curr_pairs.sort(key=daj_tezinu_grane)
        self.br_dodanih=1
        while True:
            print('Added nodes: ', self.added_nodes)
            print('Not added nodes: ', self.not_added_nodes)
            print('Current pairs: ', self.curr_pairs)
            print('Not_added pairs: ', self.not_added_pairs)
            print('----------------------------------------')
            self.br_dodanih+=1
            if (self.br_dodanih==len(self.all_nodes)):
                zadnji_cvor = self.not_added_nodes[0]
                self.curr_pairs.sort(key=daj_tezinu_grane)
                self.not_added_pairs.sort(key=daj_tezinu_grane)
                for x in self.curr_pairs:
                    if x[0]==zadnji_cvor or x[1]==zadnji_cvor:
                        grana=x
                grana = self.curr_pairs[0]
                #novo_dodani_cvor=self.azuriraj_cvorove(grana)
                x=(grana[0],grana[1])
                self.crtaj_graf(zadnji_cvor,x)
                break
            else:
                grana = self.curr_pairs[0]
                self.added_pairs.append(grana)
                self.curr_pairs.remove(grana)
                novo_dodani_cvor=self.azuriraj_cvorove(grana)
                x=(grana[0],grana[1])
                self.crtaj_graf(novo_dodani_cvor,x)
                self.dodaj_nove_grane(novo_dodani_cvor)
                self.ukloni_zabranjene(novo_dodani_cvor)
                self.curr_pairs.sort(key=daj_tezinu_grane)
        plt.pause(5)

objekat = PrimovAlgoritam()

objekat.generisi_nasumicni_graf_slova()
#objekat.GUI()

objekat.zapocni_pretragu()
#for i in range(0, 10):
#    objekat.crtaj_graf(i, (i+1, i+3)) #prvi parametar cvor, drugi parametar grana kao tuple
