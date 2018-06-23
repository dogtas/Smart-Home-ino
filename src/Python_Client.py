#!/usr/bin/env python3

##  @package Smart Home-ino
#   This is the dokumentation of the Source Code from the project Smart Home
#
#   @author Okan Dogtas <odogtas@uni-bremen.de>
#   @date 2018-06-20
#
#   @copyright GNU General Public License v3.0

import tkinter as tk
import tkinter.font as tkFont
from tkinter import colorchooser
import socket as so
import smtplib as smt

## Variables for the Designe colors. These variables are used to color the Tkinter GUI
#
# @param main_bg            contains the color for the main background
# @param btn_color          contains the color for a default button
# @param btn_color_pressed  contains the color for a butten, when pressed/clicked
# @param text_color         contains the color for the default texts
# @param highlight_color    contains the color for highlighted objects (e.g. buttons, labels)
main_bg='#C5C1C0'
btn_color='#0A1612'
btn_color_pressed='#8E3843'
text_color='#C5C1C0'
highlight_color='#cc0000'

##  a class for the Wifi connection
#
#   @brief This class handles the connection between the arduino and the python program and also contains the methods to send and receive messages through the wirelles connection
#
class WifiConnect(object):

    ##  the default constructor
    #
    # @brief This method handles the connection between the arduino and the python program as a client
    #
    # @param window         The parent (root) window
    # @param TCP_IP         Ip addres of the arduino
    # @param TCP_PORT       Port of the arduino
    # @param on_receive     function to run when receiving a message from the arduino
    # @param window         parent window safed as local variable in the class
    # @param on_receive     on_receive function safed as local variable in the class
    # @param socket         safe the socket library as socket
    def __init__(self, window, TCP_IP, TCP_PORT, on_receive):
        self.window= window
        self.on_receive= on_receive
        self.socket= so.socket(so.AF_INET, so.SOCK_STREAM)
        ## connect to the arduino
        self.socket.connect((TCP_IP, TCP_PORT))
        self.socket.setblocking(False)
        self.rd_buff= bytes()
        ## run periodic socket check
        self.periodic_socket_check()

    ## Sends message to the arduino
    #
    # This method sends a message to the ESP server (arduino)
    #
    # @param message        contains the message to be send in bytes
    def send_msg(self, message):
        self.socket.send(message)
        print('message send')

    ##close the connection
    #
    # This method closes the connection between the arduino and the python program
    def close(self):
        self.socket.close()
        self.window.after_cancel(self.after_event)

    ## checks for received message
    #
    # This method checks, if a message from the arduino has been send to the python programm in a periodic frequence
    # @param line       here the received message is saved
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
            ## if a message has been received, the message will be send to the on_receive method
            self.on_receive(line)

        self.after_event= self.window.after(
            100, self.periodic_socket_check
        )
        

## This class handles the frame switch buttons
#
# @brief The class FrameButtons creates and handles the frame switch buttons
#
class FrameButtons(object):

    ## The default constructor
    #
    # @brief here the informations for the buttons will be saved in the Class Object
    #
    # @param frame      contains the parent frame / window of the button
    # @param name       contains the text/name of the button
    # @param nr         contains the number/id of the button (for the frame_switch method)
    def __init__(self, frame, name, nr):
        self.frame= frame
        self.name= name
        self.nr= nr
        ## here the button can now be created
        self.create_button()


    ## creates the button
    #
    # @brief this method creates the button witch the according colors and command and places them with the .grid method from tkinter
    #
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

    ## switches frames acording to the pressed button
    #
    # @brief this method is executed, when a frame switch button is pressed, so that the frames switch accordingly
    #
    def frame_switch(self):
        window.forget_frames()
        self.button.config(bg= highlight_color, fg= btn_color)
        if self.nr == 0:
            window.frame_rgb.pack(fill=tk.Y, anchor=tk.W, side=tk.LEFT)
        elif self.nr == 1:
            window.frame_alarm.pack(fill=tk.Y, anchor=tk.W, side=tk.LEFT)
        elif self.nr == 2:
            window.frame_welcome.pack(fill=tk.Y, anchor=tk.W, side=tk.LEFT)

## This class creates labels
#
class CreateLabel(object):

    ## The default constructor
    #
    # @brief in the instructor the label will be created with the given informations
    #
    # @param parent     the parent frame / window of the label
    # @param content    the content text, which will be written in the label
    # @param size       the font size of the label text
    # @param color      the color of the label text
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

## class to send emails
#
# @brief in this class an email can be send to an defined adress
#
class sendMail(object):

    ## The  default constructor
    #
    # @brief the Smtp server will be initialized in this constructor
    #
    # @param server     the SMTP server connection (here gmail)
    def __init__(self):
        self.server = smt.SMTP('smtp.gmail.com', 587)

    ## method to send an E-Mail
    #
    # @brief here the the e-mail will be send wit a given message and receiver
    #
    # @param receiver   e-mail adress to which the e-mail will be send
    # @param msg        the content of the e-mail
    def sendmail(self, receiver, msg):
        self.server.starttls()
        self.server.login("arduino.smarthome1@gmail.com", "uni-bremen")

        self.receiver= receiver
        self.msg = msg
        self.server.sendmail("arduino.smarthome1@gmail.de", self.receiver, self.msg)

    ## method to close the SMTP server connection
    #
    def close(self):
        self.server.quit()

## This class creates default buttons
#
class CreateButton(object):

    ## The default constructor
    #
    # @brief in the instructor the button will be created with the given informations
    #
    # @param parent     the parent frame / window of the button
    # @param content    the text, which will be written in the button
    # @param size       the font size of the button text
    # @param command    the executed command by pressing the button
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

## The class to setup the main tkinter window
#
# @brief in this class the main window will created and the contend setup is executed
#
class WindowFunction(object):

    ## The default constructor
    #
    # @brief The arduino and Email server connection will be initialized and all window setup methods will be executed
    #
    # @param rgb_red        red value for the rgb light
    # @param rgb_green      green value for the rgb light
    # @param rgb_blue       blue value for the rgb light
    # @param arduino        the WifiConnection object
    # @param mailer         the sendMail object
    # @param host           the IP address for the wifi connection
    # @param port           the port for the wifi connection
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

    

    ## handels the received commands from the Arduino
    #
    # @brief receives the the message from the arduino
    #
    # when the message is "alarm" the rgb light will turn red, the button will be adjusted and the alarm status will turn to 2
    #
    # @param alarm_status   status of the alarm (0 = alarm off ; 1 = alarm active ; 2 = alarm triggered)
    def on_receive(self, line):
        if line == 'alarm':
            self.alarm_btn.button.config(text= 'turn off', bg= highlight_color)
            self.alarm_status= 2
            self.arduino.send_msg(b'rgb' +b'\n' +b'255' +b'\n' +b'0' +b'\n' +b'0')

            #'sends alarm E-mail...
            self.mailer.sendmail('okan-09@hotmail.de', 'Alert something happened')
            

    ## this method creates the window
    #
    # @brief this method creates the window with the a given title, geometry and an window delete protocol (method window_close)
    #
    def setup_window(self):
        self.window= tk.Tk()
        self.window.title('Smart Home')
        self.window.geometry('400x300')
        self.window.protocol("WM_DELETE_WINDOW", self.window_close)

    ## handler for Window close
    #
    # @brief by closing the window first the arduino and SMTP connection will be closed
    #
    def window_close(self):
        self.arduino.close()
        self.mailer.close()
        self.window.destroy()

    ## runs the tkinter module to show the window
    #
    def run(self):
        self.window.mainloop()

    ## sets the frame buttons on window top
    #
    # @brief the frame-switch-button frame will created and right after the frame-switch-buttons
    #
    # @param frame      the parent frame for the window switch buttons
    # @param btn1       first frame-switch-button "LIGHT"
    # @param btn2       second frame-switch-button "ALARM"
    # @param btn3       third frame-switch-button "WELCOME"
    def setup_framebtn(self):
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.X, side=tk.TOP)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.btn1= FrameButtons(self.frame, 'LIGHT', 0)
        self.btn2= FrameButtons(self.frame, 'ALARM', 1)
        self.btn3= FrameButtons(self.frame, 'WELCOME', 2)

    ## this method sets the frames for the main functions of the project
    #
    # @brief the main frames will be created and the on program start opened frame will be packed, so it is visible
    #
    # @param frame_rgb 
    # @param frame_alarm
    # @param frame_welcome
    def setup_frames(self):
        self.frame_rgb= tk.Frame(self.window, width=400, background=main_bg)
        self.frame_alarm= tk.Frame(self.window, width=400, background=main_bg)
        self.frame_welcome= tk.Frame(self.window, width=400, background=main_bg)
        self.frame_welcome.pack(fill=tk.Y, anchor=tk.W, side=tk.LEFT)

    ## let all frames dissapear (pack_forget)
    #
    # @brief here all main frames will be unpacked, so they are not visible and the frame-switch-buttons color will be set to default
    #
    # this method will be used in the FrameButtons class for the frame_switch method
    #
    def forget_frames(self):
        self.btn1.button.config(bg= btn_color, fg=text_color)
        self.btn2.button.config(bg= btn_color, fg=text_color)
        self.btn3.button.config(bg= btn_color, fg=text_color)
        self.frame_rgb.pack_forget()
        self.frame_alarm.pack_forget()
        self.frame_welcome.pack_forget()

    ## setup the rgb-frame widgets
    #
    # @brief in this method the contend of the rgb_frame will be created and placed
    #
    # @param rgb_title          the label object for the title of the frame  
    # @param color_btn          the button for the color selection
    # @param rgb_text           the description text
    # @param rgb_description    the description label object with the description text as content
    # @param rgb_off_btn        button to set the rgb values to zero (turn rgb led off)
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
        

    ## setup the alarm-frame widgets
    #
    # @brief in this method the contend of the alarm_frame will be created and placed
    #
    # @param alarm_title            the label object for the title of the frame 
    # @param alarm_text             the description text
    # @param alarm_description      the description label object with the description text as content
    # @param alarm_btn              the button for the alarm control
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

    ## setup the welcome-frame widgets
    #
    # @brief in this method the contend of the welcome_frame will be created and placed
    #
    # @param welcome_title          the label object for the title of the frame 
    # @param welcome_text           the description text
    # @param welcome_description    the description label object with the description text as content
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

    ## method for the alarm button
    #
    # @brief this method will be executed, when the alarm button is pressed
    #
    # the method will send messages to the arduino acordingly to the alarmstatus and also change the alarm button configuration. at the start of the message to the arduino there is alarm written, so that the arduino will know for what the message will be
    #
    # @param alarm_status       status of the alarm (0 = alarm off ; 1 = alarm active ; 2 = alarm triggered)
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

    ## method for the color choose button
    #
    # @brief this method will be executed, when the color_btn is pressed
    #
    # this method asks for a color and saves it in the rgb variables, sends them to the arduino and changes the color of the button to the choosen color. at the start of the message there is rgb written, so that the arduino will know for what the message will be
    #
    # @param rgb
    def choose_color(self):
        ## the colorchooser.askcolor gives the rgb values as an two dimensional array e.g. [(255, 255, 255),(#FFFFFF)]
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

    ## method for the lights off button
    #
    # @breif this method will be executed, when the rgb_off_btn is pressed
    #
    # this method sets the rgb variables to zero and sends these values to the arduino like in choose_color() method
    #
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
