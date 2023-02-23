from tkinter import *
from tkinter import font
from tkmacosx import Button
from time import sleep
from sys import stdout
import threading
import kill_Spotify
from splash import Splash


class MainWindow(Tk):
    def __init__ (self):
        super().__init__()
        self.title('Spotify Timer')
        # print(self.cget('bg'))
        
        self.isrunning = False
        
        self.configure(padx=10,pady=10)
        self.field_frame = Frame(self,padx=10,pady=10,bg='blue')
        spacer_frame = Frame(self,height=20)     
        self.hour_field = TimeField(self.field_frame,'hours')
        self.colon1 = TimerColon(self.field_frame)
        self.min_field = TimeField(self.field_frame,'minutes','01') # Default mins on execution
        self.colon2 = TimerColon(self.field_frame)
        self.sec_field = TimeField(self.field_frame,'seconds')
        self.startButton = Buttons(self,'Start',self.start_timer,'green','light green')
        self.stopButton = Buttons(self,'Stop', self.stop_timer,'red')
        self.aboutButton = Button(self,text="About",command=self.splash)
        self.bind ('<Return>',self.hit_return)
        self.aboutButton.grid(row=0,column=0,pady=10)
        self.field_frame.grid(row=1,column=0,columnspan=3)
        # GUI elements of self.field_frame (ie hour/min/sec fields and separating colons)
        self.hour_field.field.grid(row=0,column=0)
        self.colon1.lab.grid(row=0,column=1)
        self.min_field.field.grid(row=0,column=2)
        self.colon2.lab.grid(row=0,column=3)
        self.sec_field.field.grid(row=0,column=4)
        
        spacer_frame.grid(row=2,column=0,columnspan=3)
        self.startButton.b.grid(row=3,column=0)
        self.stopButton.b.grid(row=3,column=1)
        self.field_list = [self.hour_field,self.min_field,self.sec_field]
        # print(f"{self.hour_field.text} : {self.min_field.text} : {self.sec_field.text}")
        
        
    def splash(self):
        self.sp = Splash(self) # instance needs to be created using self to avoid 'garbage collection' and the image being removed
        
        
    def start_timer(self):
        zero_count = 0
        for fl in self.field_list: 
            fl.correct_digit_format()
            if fl.field.get() == '00':
                zero_count += 1
        if zero_count == 3:
            # print("TIMER IS AT ZERO")
            self.isrunning = False
        elif not (kill_Spotify.is_spotify_running()):
            # print("Spotify NOT running")
            self.no_spotify_warning = Popup(self,"Spotify is not running!")
            self.no_spotify_warning.popup.geometry('300x150')
            self.no_spotify_warning.button2 = Button(self.no_spotify_warning.popup,
                                                text='Open Spotify',
                                                command=self.open_app)
            self.no_spotify_warning.button2.pack()
        else:
            # print("Timer Started")
            self.startButton.b.configure(state='disabled')
            self.isrunning = True
        
            # lock the entry fields
            for fl in self.field_list:
                fl.field.config(state='readonly')
            for cl in (self.colon1,self.colon2): cl.set_bg('readonly') 
            
            t1 = threading.Thread(target=self.run_countdown)
            t1.start()
 
            
    def stop_timer(self):
        # print("Timer stopped")
        for fl in self.field_list: fl.correct_digit_format()
        self.startButton.b.configure(bg='green',state='normal')
        self.isrunning = False

        # unlock the entry fields
        for fl in self.field_list:
            fl.field.config(state='normal')
        for cl in (self.colon1,self.colon2): cl.set_bg('normal')
        
        
    def hit_return(self,event):  # When return
        if not self.isrunning:
            for fl in self.field_list: fl.correct_digit_format()
 
    
    def open_app(self):
        # self.no_spotify_warning.button.configure(state='normal')
        # self.no_spotify_warning.button2.configure(state='active')
        kill_Spotify.open_spotify()
        sleep(1)
        self.no_spotify_warning.popup.destroy()
 
            
    def run_countdown(self):
        hours, minutes, seconds = (int(i.field.get()) for i in self.field_list )
        # print (f"running time from {hours} : {minutes} : {seconds} ")
        total_seconds = (hours * 3600) + (minutes * 60) + seconds
        print(f"seconds remaining: {total_seconds}")
        for secs_remaining in range (total_seconds,-1,-1):
            if not self.isrunning:
                break
            hours = secs_remaining // 60 // 60
            minutes = (secs_remaining // 60) % 60
            seconds = secs_remaining % 60
            # countdown_display = (f"{hours:02} : {minutes:02} : {seconds:02}")
            # print(countdown_display)
            self.hour_field.textvar.set(f"{hours:02}")
            self.min_field.textvar.set(f"{minutes:02}")
            self.sec_field.textvar.set(f"{seconds:02}")
            
            self.update()
            sleep(1)
        
        if not secs_remaining == 0:
            print("Paused")
        else:
            print("Time's up")
            kill_Spotify.fade_down_Spotify()
            self.stop_timer()

        
class Buttons:
    def __init__ (self,master,name,comm,bg='systemWindowBackgroundColor',disbg='grey90'):
        # super().__init__()
        self.name = name
        self.comm = comm
        self.bg = bg
        self.disbg = disbg
        self.padx = 30
        self.pady = 10    
        self.font = ((font.nametofont('TkDefaultFont').actual('family')),24)  # uses the default font but with an increased size ',24'
        self.b = Button(master,text=self.name, bg=self.bg, font=self.font,
                        padx=self.padx, pady=self.pady,
                        disabledbackground=self.disbg,
                        command=self.comm
                        )
        

class DisplayVars:
    # common parameters for the 'display' ie text fields and colon labels
    def __init__ (self,robg='pink'):
        self.width = 4
        self.font = ("Helvetica", 64, "bold")
        # self.font_size = 64
        self.thick = 0
        self.bg = 'white'
        self.robg = robg


class TimeField(DisplayVars):
    # used for displaying the hours, minutes & seconds number fields
    def __init__ (self,master,unit,text='00'):
        super().__init__()
        self.unit = unit
        self.text = text
        self.textvar = StringVar()
        vcmd = master.register(self.callback) # validates user entry into the text fields
        # ivcmd = (MainWindow.register(self.on_invalid),)
        self.field = Entry(master, width=self.width,font=self.font, readonlybackground=self.robg,
                           justify='center',bg=self.bg,highlightthickness=self.thick,border=self.thick,
                           textvariable=self.textvar
                           )
        # self.field.insert(0, self.text)
        self.textvar.set(text)
        self.field.config(validate='key',validatecommand=(vcmd, '%P')) # validates when a key is pressed. %P is substitution for parsing correct user entry
        
        
    def correct_digit_format(self):
        num = self.field.get()
        while len(num) < 2:
            num = f"0{num}"
        # print(f"now the value is: {num}")
        self.textvar.set(num)

        
    def callback(self,value):
        # print(value)
        if len(value) > 2:
            # print ("too many digits")
            return False               
        if value.isdigit() and int(value) <60:
            # print("Is a number")
            # if int(value) <60:
                # print("less than 60")
            return True
            # else:
            #     return False
        elif value == "":
            return True          
        # else:
        #     print("NOT a number")
        return False           
            
        
class TimerColon(DisplayVars):
    def __init__ (self,master):
        super().__init__()
        self.text = ' : '
        self.lab = Label(master,text=self.text,font=self.font,
                         justify='center',bg=self.bg,border=self.thick
                         )
        
    def set_bg (self,state):
        if state == 'readonly':
            self.lab.configure(bg=self.robg)
        else:
            self.lab.configure(bg=self.bg)
            
            
class Popup:
    def __init__  (self,master,msg,okbut='Ok'):
        self.msg = msg
        self.popup = (Toplevel(master))
        self.popup.grab_set()
        self.popup.geometry('300x100')
        self.popup.title('WARNING!')
        self.warnlab = Label(self.popup,text=msg).pack(padx=20,pady=20)
        self.button = Button(self.popup,text=okbut,state='active',command=self.popup.destroy)
        self.popup.bind('<Return>', (lambda e, b=self.button: b.invoke()))
        # self.popup.bind_all('<Key>', self.beep)
        self.button.pack(padx=20,pady=5)
        
        
    # def beep(self,event):
    #     print('Key pressed')
    #     stdout.write('\a')
    #     stdout.flush()


if __name__ == "__main__":     
    root = MainWindow()
    root.mainloop()