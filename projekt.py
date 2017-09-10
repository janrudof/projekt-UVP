import tkinter as tk
import random


def nakljucno_izberi_besedo(datoteka_besed='besede.txt'):
    '''Iz datoteke se naključno izbere beseda za vislice.'''
    seznam_besed = []
    with open(datoteka_besed) as besede:
        for vrstica in besede:
            seznam_besed.append(
                vrstica.strip())  # besede iz datoteke damo v seznam, iz katerega bomo naključno izbrali besedo za igro
    stevilo_besed = len(seznam_besed)
    nakljucna_beseda = seznam_besed[random.randint(0, stevilo_besed - 1)]
    return nakljucna_beseda


class UgibanjeBesede:
    def __init__(self):
        self.beseda = nakljucno_izberi_besedo()
        self.seznam_besede = []
        self.seznam_iskane_besede = []
        self.stevilo_napacnih_poskusov = 0
        for znak in self.beseda:
            self.seznam_besede.append(znak)
            self.seznam_iskane_besede.append('-')

    def izbrana_beseda(self):
        return self.beseda

    def dolzina_besede(self):
        return len(self.beseda)

    def ugibanje(self, izbrana_crka):
        '''Ko izberemo črko, nadomestimo - z črko, če le ta je v besedi.'''

        if izbrana_crka in self.beseda:
            for i in range(0, len(self.seznam_besede)):
                if self.seznam_besede[i] == izbrana_crka:
                    self.seznam_iskane_besede[i] = izbrana_crka
                    if self.seznam_iskane_besede == self.seznam_besede:
                        return 'Zmagal si!'
            return ''.join(self.seznam_iskane_besede)
        else:
            if self.stevilo_napacnih_poskusov == 11:
                return 'Konec igre.'
            else:
                self.stevilo_napacnih_poskusov += 1
                print(self.stevilo_napacnih_poskusov)
                return ' '.join(self.seznam_iskane_besede)

    def stevilo_napak(self):
        '''Hočemo, da nam vrne število napak, da lahko rišemo.'''
        print(self.stevilo_napacnih_poskusov)
        return self.stevilo_napacnih_poskusov

okno = tk.Tk()

class Vislice:
    def __init__(self, okno):
        self.ugibana_beseda = UgibanjeBesede()
        self.okno = okno
        self.okno.bind('<Key>', self.ugibanje_prikaz)

        self.naslovna_vrstica = tk.Label(okno, text='VISLICE', font=('HELVETICA',30), bg= 'white', width=21)
        self.naslovna_vrstica.pack()

        self.podvrstica= tk.Label(okno, text = 'Začni z ugibanjem', font=('HELVETICA',14))
        self.podvrstica.pack()

        self.platno = tk.Canvas(okno, height=300, width=300, bg='white')
        self.platno.pack()

        self.iskana_beseda = tk.Label(okno, text= (self.ugibana_beseda.dolzina_besede() * ' - '), font =('Helvetica', 20))
        self.iskana_beseda.pack()

        self.gumb = tk.Button(okno, text='Nova igra', font=16)
        self.gumb.pack()


    def ugibanje_prikaz(self, event):
        '''Hočemo, da se prikaže črka, če je le ta v besedi, drugače naj ostane - .'''
        izbrana_crka = event.keysym
        if izbrana_crka in self.ugibana_beseda.izbrana_beseda():
            self.podvrstica.config(text= 'Pravilno!', fg= 'green')
        else:
            self.podvrstica.config(text= 'Narobe!', fg='red')
        posodobljena_beseda = self.ugibana_beseda.ugibanje(izbrana_crka)
        self.iskana_beseda.config(text=posodobljena_beseda)

    def risanje_visli(self):
        '''Če črke ni v besedi, se nariše ena poteza.'''
        if self.ugibana_beseda.stevilo_napacnih_poskusov() == 1:
            self.platno.create_line(10,10,50,50)








vislica = Vislice(okno)
okno.mainloop()
