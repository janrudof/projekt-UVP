import tkinter as tk
import random

def nakljucno_izberi_besedo(datoteka_besed='besede.txt'):
    '''Iz datoteke se naključno izbere beseda za vislice.'''
    seznam_besed = []
    with open(datoteka_besed) as besede:
        for vrstica in besede:
            seznam_besed.append(vrstica.strip())  # besede iz datoteke damo v seznam, iz katerega bomo naključno izbrali besedo za igro
    stevilo_besed = len(seznam_besed)
    nakljucna_beseda = seznam_besed[random.randint(0, stevilo_besed - 1)]
    return nakljucna_beseda

class UgibanjeBesede:
    def __init__(self):
        self.beseda = nakljucno_izberi_besedo()
        self.seznam_besede = [] #crke iskane besede v seznamu
        self.seznam_iskane_besede = []#crke, ki smo ze ugotovili v seznamu
        self.stevilo_napacnih_poskusov = 0
        for znak in self.beseda:
            self.seznam_besede.append(znak)
            self.seznam_iskane_besede.append('-')

    def __str__(self):
        return 'Iskanje besede {}.'.format(self.beseda)

    def izbrana_beseda(self):
        return self.beseda

    def dolzina_besede(self):
        return len(self.beseda)

    def razlicne_crke_besede(self):
        razlicne_crke = set()
        for crka in self.beseda:
            razlicne_crke.add(crka)
        return len(razlicne_crke)

    def ugibanje(self, izbrana_crka):
        '''Ko izberemo črko, nadomestimo - z črko, če le ta je v besedi.'''

        if izbrana_crka in self.beseda:
            for i in range(0, len(self.seznam_besede)):
                if self.seznam_besede[i] == izbrana_crka:
                    self.seznam_iskane_besede[i] = izbrana_crka
                    if self.seznam_iskane_besede == self.seznam_besede:
                        return 'Zmagal si! Pravilna beseda je {}.'.format(self.beseda)
            return ''.join(self.seznam_iskane_besede)
        else:
            if self.stevilo_napacnih_poskusov == 10:
                return 'Konec igre. Pravilna beseda je {}.'.format(self.beseda)
            else:
                self.stevilo_napacnih_poskusov += 1
                return ' '.join(self.seznam_iskane_besede)

    def stevilo_napak(self):
        '''Hočemo, da nam vrne število napak, da lahko rišemo.'''
        return self.stevilo_napacnih_poskusov


okno = tk.Tk()

class Vislice:
    def __init__(self, okno):
        self.ugibana_beseda = UgibanjeBesede()
        self.okno = okno
        self.okno.bind('<Key>', self.ugibanje_prikaz)

        self.naslovna_vrstica = tk.Label(okno, text='VISLICE', relief= 'ridge', font=('HELVETICA',30), bg= 'white', width=21)
        self.naslovna_vrstica.pack()

        self.podvrstica= tk.Label(okno, text = 'Začni z ugibanjem', font=('HELVETICA',14))
        self.podvrstica.pack()

        self.platno = tk.Canvas(okno, height=300, width=300, bg='white')
        self.platno.pack()

        self.iskana_beseda = tk.Label(okno, text= (self.ugibana_beseda.dolzina_besede() * ' - '), font =('Helvetica', 18), fg='blue', bg='white')
        self.iskana_beseda.pack()

        self.gumb = tk.Button(okno, text='Nova igra', font=16, command = self.nova_igra)
        self.gumb.pack()

        self.stevilo_napacnih_crk = 0
        self.stevilo_pravilnih_crk = set()

    def __str__(self):
        return 'Igranje igre VISLICE, kjer iščemo besedo {}.'.format(self.ugibana_beseda.izbrana_beseda())

    def ugibanje_prikaz(self, event):
        '''Hočemo, da se prikaže črka, če je le ta v besedi, drugače naj ostane - . Prav tako, če zmagaš ali izgubiš, se začne nova igra.'''

        if self.stevilo_napacnih_crk == 11 or len(self.stevilo_pravilnih_crk)  == self.ugibana_beseda.razlicne_crke_besede():
            self.nova_igra()
        else:
            izbrana_crka = event.keysym #pritisneš tipko
            if izbrana_crka in self.ugibana_beseda.izbrana_beseda():
                self.stevilo_pravilnih_crk.add(izbrana_crka)
                self.podvrstica.config(text= 'Pravilno!', fg= 'green')
            else:
                self.stevilo_napacnih_crk += 1
                self.risanje_visli()
                self.podvrstica.config(text= 'Narobe! {}. nepravilen poskus.'.format(self.stevilo_napacnih_crk), fg='red')

            posodobljena_beseda = self.ugibana_beseda.ugibanje(izbrana_crka)
            self.iskana_beseda.config(text=posodobljena_beseda)

    def risanje_visli(self):
        '''Če črke ni v besedi, se nariše ena poteza.'''
        if self.ugibana_beseda.stevilo_napak() == 0:
            self.platno.create_line(50,300,150,300, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 1:
            self.platno.create_line(100,300,100,100, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 2:
            self.platno.create_line(100,100,200,100, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 3:
            self.platno.create_line(100,150,130,100, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 4:
            self.platno.create_line(200,100,200,120, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 5:
            self.platno.create_oval(180,120,220,160, width=2, fill='black', activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 6:
            self.platno.create_line(200,160,200,220, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 7:
            self.platno.create_line(200,160,180,190, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 8:
            self.platno.create_line(200,160,220,190, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 9:
            self.platno.create_line(200,220,180,250, width=2, activefill='red')
        elif self.ugibana_beseda.stevilo_napak() == 10:
            self.platno.create_line(200,220,220,250, width=2, activefill='red')

    def nova_igra(self):
        '''Ko pritisneš gumb, se začne nova igra.'''
        self.platno.delete('all')
        self.ugibana_beseda = UgibanjeBesede()
        self.iskana_beseda.config(text= ' - ' * self.ugibana_beseda.dolzina_besede())
        self.podvrstica.config(text= 'Začni z ugibanjem', fg= 'black')
        self.stevilo_napacnih_crk = 0
        self.stevilo_pravilnih_crk = set()


vislica = Vislice(okno)
okno.mainloop()
