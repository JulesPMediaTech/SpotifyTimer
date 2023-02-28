from tkinter import *
from tkinter import font
from tkmacosx import Button
import os


global path


class Splash:
    def __init__ (self, master):
        path = (os.path.dirname(__file__))
        self.hfont = ('Arona Bold',48)
        self.descfont = ((font.nametofont('TkDefaultFont').actual('family')),14) 
        self.popup = Toplevel(master,pady=10)
        self.popup.title("welcome to my bits and pieces")
        self.popup.grab_set()
        self.text_frame = Frame(self.popup,padx=20,pady=20)
        self.logo_canvas = Canvas(self.popup,width=450,height=250)
        self.desctext = '''
Software written by Jules Pyke
LDAP: @julesp
info@golively.tv
© Jules Pyke 2023 
under MIT licence

Always up for more coding projects,
so just HOLLER!
        '''
        self.heading = Label(self.popup,text="Spotify Timer", font=self.hfont,justify='center')
        self.desc = Label(self.text_frame,text=self.desctext,font=self.descfont,justify='left')
        self.cool_b = Button(self.popup,text="Cool.. 😎",font=self.descfont,pady=10,
                              state='active',command=self.popup.destroy)
        self.popup.bind('<Return>', (lambda e, b=self.cool_b: b.invoke()))

        self.logo_canvas.grid(row=1,column=0)
        
        self.text_frame.grid(row=1,column=1)
        self.heading.grid(row=0,column=0,columnspan=2)
        self.desc.grid(row=0,column=1)
        # self.img = PhotoImage(file=f'{path}/images/logo.png')
        self.img = PhotoImage(file='logo.png')
        # self.img = PhotoImage(file='SpotifyTimer/images/logo.png')
        self.logo_canvas.create_image(20,20,image=self.img,anchor='nw')
        self.cool_b.grid(row=2,column=0,columnspan=2)
# SpotifyTimer/images/logo.png
