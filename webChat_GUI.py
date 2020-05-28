
import requests
from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from threading import Thread
import time

webChat_session = requests.Session()
url = 'http://165.22.14.77:8080/Naveen/28may/'

def changeSendButtonStatus(event):
	global btn_send
	btn_send.config(state = ('disabled' if message.get() == '' else 'normal'))

def changeLoginAndSignupButtonsStatus(event):
	btn_login.config(state = ('disabled' if userName.get() == '' or passWord.get() == '' else 'normal'))
	btn_signup.config(state = ('disabled' if userName.get() == '' or passWord.get() == '' else 'normal'))

def sendMessage(event = None):
	webChat_session.get(f'{url}send_message.jsp?sName={userName}&mSent={message.get()}')
	message.delete(0, last = END)
	messagebox.showinfo('Success', 'Successfully message sent.')

def register(userName, password, homeWindow):
	# response = webChat_session.get("http://165.22.14.77:8080/Naveen/28may/register.jsp?UserName="+userName+"&Password="+password)
	response = webChat_session.get(f'{url}/register.jsp?UserName={userName}&Password={password}')
	if(response.text.find("success")) > 0:
		messagebox.showinfo('Success', 'Registration successfull.')
	else:
		messagebox.showinfo('Error', 'Try with another username.')

def showActiveUsers():
	try:
		while True:
			response = webChat_session.get(f'{url}active_users.jsp?')
			activeUsers.config(state = 'normal')
			activeUsers.delete(1.0, END)
			activeUsers.insert(END, response.text.strip().replace("<br>", ""))
			activeUsers.config(state = DISABLED)
			time.sleep(2)
	except:
		print("", end = '')

def showMessages():
	try:
		while True:
			response = webChat_session.get(f'{url}show_messages.jsp?usrName={userName}')
			chatPanel.config(state = 'normal')
			if response.text.strip() != "":
				chatPanel.delete(1.0, END)
				# chatPanel.insert(END, f'{response.text.strip()}\n')
				chatPanel.insert(END, response.text.strip().replace("<br>", ""))
			chatPanel.config(state = DISABLED)
			time.sleep(1)
	except:
		print("", end = '')

def showChatWindow(name):
	global message
	global chatPanel
	global chatWindow
	global btn_send
	global userName
	global activeUsers 
	userName = name

	chatWindow = Tk()
	chatWindow.geometry('600x370')
	chatWindow.title('Chat window')
	chatWindow.resizable(0, 0)
	chatWindow.bind("<FocusIn>", changeSendButtonStatus)
	chatWindow.bind("<ButtonRelease>", changeSendButtonStatus)

	lbl_activeUsers = Label(chatWindow, text = 'Active users')
	lbl_activeUsers.place(x = 300, y = 10)

	activeUsers = scrolledtext.ScrolledText(width = 20, height = 7)
	activeUsers.place(x = 300, y = 30)
	activeUsers.config(state = DISABLED)

	lbl_message = Label(chatWindow, text = 'Enter message: ')
	lbl_message.place(x = 300, y = 200)

	message = Entry(chatWindow, width = 20)
	message.bind("<Return>", sendMessage)
	message.place(x = 415, y = 200)
	message.focus_set()

	btn_send = Button(chatWindow, text = 'Send message', command = sendMessage)
	btn_send.place(x = 350, y = 230)

	btn_signout = Button(chatWindow, text = 'Sign out', command = signout)
	btn_signout.place(x = 475, y = 230)

	chatPanel = scrolledtext.ScrolledText(width = 30, height = 18)
	chatPanel.place(x = 10, y = 10)
	chatPanel.config(state = DISABLED)

	Thread(target = showActiveUsers).start()
	Thread(target = showMessages).start()

	chatWindow.bind("<Key>", changeSendButtonStatus)
	mainloop()


def login(userName, password, homeWindow):
	response = webChat_session.get(f'{url}login.jsp?uName={userName}&pswd={password}')
	if(response.text.find("success")) > 0:
		messagebox.showinfo('Message', 'Successfully Logged in.')
		homeWindow.destroy()
		showChatWindow(userName)
	else:
		messagebox.showinfo('Error', 'Invalid credentials.')

def signout():
	try:
		response = webChat_session.get(f'{url}sign_out.jsp?uNam={userName}')
		messagebox.showinfo('Message', 'Successfully Logged out.')	
		chatWindow.destroy()
	except:
		print("", end = '')

def establish_Connection():
	response = webChat_session.get(f'{url}establish_connection.jsp?')

def showHomeWindow():
	establish_Connection()

	global userName
	global passWord
	global btn_login
	global btn_signup

	homeWindow = Tk()
	homeWindow.geometry('400x200')
	homeWindow.title('Registration and Login')
	homeWindow.resizable(0, 0)
	homeWindow.bind('<FocusIn>', changeLoginAndSignupButtonsStatus)

	lbl_userName = Label(homeWindow, text = 'Enter username: ')
	lbl_userName.place(x = 10, y = 10)

	userName = Entry(homeWindow, width = 20)
	userName.place(x = 160, y = 10)
	userName.focus_set()

	lbl_passWord = Label(homeWindow, text = 'Enter password: ')
	lbl_passWord.place(x = 10, y = 50)

	passWord = Entry(homeWindow, width = 20)
	passWord.place(x = 160, y = 50)

	btn_login = Button(homeWindow, text = 'Login', command = lambda: login(userName.get(), passWord.get(), homeWindow))
	btn_login.place(x = 160, y = 90)

	btn_signup = Button(homeWindow, text = 'SignUp', command = lambda: register(userName.get(), passWord.get(), homeWindow))
	btn_signup.place(x = 240, y = 90)

	homeWindow.bind("<Key>", changeLoginAndSignupButtonsStatus)
	mainloop()

showHomeWindow()