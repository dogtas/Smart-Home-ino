#!/usr/bin/env python3

import tkinter as tk
import tkinter.font as tkFont
from tkinter import colorchooser
import socket as so
import smtplib as smt

#Designe
main_bg='#C5C1C0'
btn_color='#0A1612'
btn_color_pressed='#8E3843'
text_color='#C5C1C0'
highlight_color='#cc0000'

#class to setup the Arduino connection
class WifiConnect(object):
    def __init__(self, window, TCP_IP, TCP_PORT, on_receive):
        self.window= window
        self.on_receive= on_receive
        self.socket= so.socket(so.AF_INET, so.SOCK_STREAM)
        self.socket.connect((TCP_IP, TCP_PORT))
        self.socket.setblocking(False)
        self.rd_buff= bytes()
        self.periodic_socket_check()

    def send_msg(self, message):
        self.socket.send(message)
        print('message send')

    #close the connection
    def close(self):
        self.socket.close()
        self.window.after_cancel(self.after_event)

    #checks if message was send to the socket
    def periodic_socket_check(self):
        try:
            msg= self.socket.recv(1024)

            if not msg:
                raise(IOError('Connection closed'))

            self.rd_buff+= msg

        except so.error:
            pass

        while b'\n' in self.rd_buff:
            line, self.rd_buff= self.rd_buff.split(b'\n')

            line= line.decode('utf-8').strip()
            self.on_receive(line)

        self.after_event= self.window.after(
            100, self.periodic_socket_check
        )
        

#class to create buttons
class FrameButtons(object):
    def __init__(self, frame, name, nr):
        self.frame= frame
        self.name= name
        self.nr= nr
        self.create_button()


    #creates the button
    def create_button(self):
        self.button= tk.Button(
            self.frame,
            text= self.name,
            fg= text_color,
            bg= btn_color,
            font=tkFont.Font(family="Helvetica", size=10, weight=tkFont.BOLD),
            activebackground=btn_color_pressed,
            command= self.frame_switch
        )
        self.button.grid(row=0, column=self.nr, sticky=tk.W+tk.E)

    #switches frames acording to pressed button
    def frame_switch(self):
        window.forget_frames()
        self.button.config(bg= highlight_color, fg= btn_color)
        if self.nr == 0:
            window.frame_rgb.pack(fill=tk.Y, anchor=tk.W, side=tk.LEFT)
        elif self.nr == 1:
            window.frame_alarm.pack(fill=tk.Y, anchor=tk.W, side=tk.LEFT)
        elif self.nr == 2:
            window.frame_welcome.pack(fill=tk.Y, anchor=tk.W, side=tk.LEFT)

#class to create labels
class CreateLabel(object):
    def __init__(self, parent, content, size, color):
        self.label= tk.Label(
            parent,
            text=content,
            justify= tk.LEFT,
            anchor= "w",
            fg=color,
            bg=main_bg,
            font=tkFont.Font(family="Helvetica", size=size, weight=tkFont.BOLD)
        )

class sendMail(object):
    def __init__(self):
        self.server = smt.SMTP('smtp.gmail.com', 587)

    def sendmail(self, receiver, msg):
        self.server.starttls()
        self.server.login("arduino.smarthome1@gmail.com", "uni-bremen")

        self.receiver= receiver
        self.msg = msg
        self.server.sendmail("arduino.smarthome1@gmail.de", self.receiver, self.msg)
    def close(self):
        self.server.quit()

#class to create labels
class CreateButton(object):
    def __init__(self, parent, content, size, command):
        self.button= tk.Button(
            parent,
            text=content,
            fg=text_color,
            bg=btn_color,
            font=tkFont.Font(family="Helvetica", size=10),
            activebackground=btn_color_pressed,
            command= command
        )

#Class to setup the tkinter Window
class WindowFunction(object):
    def __init__(self):
        self.rgb_red= 0
        self.rgb_green= 0
        self.rgb_blue= 0
        self.setup_window()

        host= '192.168.43.133'
        port= '30303'
        self.arduino= WifiConnect(
            self.window,
            host, int(port),
            self.on_receive
        )
        self.mailer= sendMail()
        self.setup_framebtn()
        self.setup_frames()
        self.setup_rgbframe()
        self.setup_alarmframe()
        self.setup_welcomeframe()
        self.alarm_status= 0

    

    #handels the received commands from the Arduino
    def on_receive(self, line):
        if line == 'alarm':
            self.alarm_btn.button.config(text= 'turn off', bg= highlight_color)
            self.alarm_status= 2
            self.arduino.send_msg(b'rgb' +b'\n' +b'255' +b'\n' +b'0' +b'\n' +b'0')

            #send alarm E-mail...
            self.mailer.sendmail('okan-09@hotmail.de', 'Alert something happened')
            

    #creates the window
    def setup_window(self):
        self.window= tk.Tk()
        self.window.title('Smart Home')
        self.window.geometry('400x300')
        self.window.protocol("WM_DELETE_WINDOW", self.window_close)

    #handler for Window close
    def window_close(self):
        self.arduino.close()
        self.mailer.close()
        self.window.destroy()

    #runs the tkinter module to show the window
    def run(self):
        self.window.mainloop()

    #sets the frame buttons on window top
    def setup_framebtn(self):
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.X, side=tk.TOP)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.btn1= FrameButtons(self.frame, 'LIGHT', 0)
        self.btn2= FrameButtons(self.frame, 'ALARM', 1)
        self.btn3= FrameButtons(self.frame, 'WELCOME', 2)

    #sets the frames in which the main content will be
    def setup_frames(self):
        self.frame_rgb= tk.Frame(self.window, width=400, background=main_bg)
        self.frame_alarm= tk.Frame(self.window, width=400, background=main_bg)
        self.frame_welcome= tk.Frame(self.window, width=400, background=main_bg)
        self.frame_welcome.pack(fill=tk.Y, anchor=tk.W, side=tk.LEFT)

    #let all frames dissapear (pack_forget)
    def forget_frames(self):
        self.btn1.button.config(bg= btn_color, fg=text_color)
        self.btn2.button.config(bg= btn_color, fg=text_color)
        self.btn3.button.config(bg= btn_color, fg=text_color)
        self.frame_rgb.pack_forget()
        self.frame_alarm.pack_forget()
        self.frame_welcome.pack_forget()

    #setup the rgb-frame widgets
    def setup_rgbframe(self):
        self.rgb_title= CreateLabel(self.frame_rgb, 'Choose light color', 16, highlight_color)
        self.color_btn= CreateButton(self.frame_rgb, 'Color', 9, self.choose_color)
        self.rgb_text= '''Here you can choose the
color of the light by clicking
the button color and to turn
it of set the color to black'''
        self.rgb_description= CreateLabel(self.frame_rgb, self.rgb_text, 9, btn_color) 
        self.rgb_off_btn= CreateButton(self.frame_rgb, 'OFF', 9, self.lights_off)
        
        self.rgb_title.label.place(x=30, y=20)
        self.rgb_description.label.place(x=30, y=100, width=250)
        self.color_btn.button.place(x=30, y=60, width=120, height=25)
        self.rgb_off_btn.button.place(x=160, y=60, width=120, height=25)
        

    #setup the alarm-frame widgets
    def setup_alarmframe(self):
        self.alarm_title= CreateLabel(self.frame_alarm, 'Home Alarm System', 16, highlight_color)
        self.alarm_text= '''By pressing the button
you anable the alarm system,
so that any movement in your
house can be detected and trigger
the alarm.
in case of an alarm an email will be send.
you can disable it simply by pressing
the button again.'''
        self.alarm_description= CreateLabel(self.frame_alarm, self.alarm_text, 9, btn_color)
        self.alarm_btn= CreateButton(self.frame_alarm, 'Alarm ON', 9, self.alarm_handler)
        self.alarm_title.label.place(x=30, y=20)
        self.alarm_description.label.place(x=30, y=100, width=250)
        self.alarm_btn.button.place(x=30, y=60, width=120, height=25)

    #setup the welcome-frame widgets
    def setup_welcomeframe(self):
        self.welcome_title= CreateLabel(self.frame_welcome, 'SMART HOME-ino', 16, highlight_color)
        self.welcome_text= '''Welcome to the Smart home-ino
system. here you are able to manage
your house and keep it secure.

With the lightcontrolpanel under the panel
LIGHT you can control and change
the color of the lights in your house.
To manage the security you have to go to
panel ALARM, there you can find more
Instructions for the control.'''
        self.welcome_description= CreateLabel(self.frame_welcome, self.welcome_text, 9, btn_color)
        self.welcome_title.label.place(x=30, y=20)
        self.welcome_description.label.place(x=30, y=60, width=250)

    def alarm_handler(self):
        if self.alarm_status == 0:
            self.arduino.send_msg(b'alarm' + b'\n' + b'on')
            self.alarm_status = 1
            self.alarm_btn.button.config(text= 'Alarm OFF')
        elif self.alarm_status == 1:
            self.arduino.send_msg(b'alarm' + b'\n' + b'off')
            self.alarm_status = 0
            self.alarm_btn.button.config(text= 'Alarm ON')
        elif self.alarm_status == 2:
            self.alarm_status = 0
            self.alarm_btn.button.config(text= 'Alarm ON', bg= btn_color)
            self.arduino.send_msg(b'alarm' + b'\n' + b'off' + b'\n')
            self.arduino.send_msg(b'rgb' +
                                  b'\n' +
                                  str(self.rgb_red).encode('utf-8') +
                                  b'\n' +
                                  str(self.rgb_green).encode('utf-8') +
                                  b'\n' +
                                  str(self.rgb_blue).encode('utf-8')
                                  )

    def choose_color(self):
        self.rgb= colorchooser.askcolor()
        if self.rgb != (None, None) :
            self.rgb_red= int(self.rgb[0][0])
            self.rgb_green= int(self.rgb[0][1])
            self.rgb_blue= int(self.rgb[0][2])
            self.arduino.send_msg(b'rgb' +
                                  b'\n' +
                                  str(self.rgb_red).encode('utf-8') +
                                  b'\n' +
                                  str(self.rgb_green).encode('utf-8') +
                                  b'\n' +
                                  str(self.rgb_blue).encode('utf-8')
                                  )
            print(str(self.rgb_red) +'\n'+ str(self.rgb_green) +'\n'+ str(self.rgb_blue))
            self.color_btn.button.config(background= self.rgb[1])

    def lights_off(self):
        self.rgb_red= 0
        self.rgb_green= 0
        self.rgb_blue= 0
        self.arduino.send_msg(b'rgb' +
                                  b'\n' +
                                  str(self.rgb_red).encode('utf-8') +
                                  b'\n' +
                                  str(self.rgb_green).encode('utf-8') +
                                  b'\n' +
                                  str(self.rgb_blue).encode('utf-8')
                                  )
        self.color_btn.button.config(background= btn_color)

if __name__ == '__main__':
    window= WindowFunction()
    window.run()
