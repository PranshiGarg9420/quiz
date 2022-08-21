import socket
from threading import Thread
from tkinter import *

# nickname= input('Choose your nickname: ')

client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address= '127.0.0.1'
port=8000

client.connect((ip_address, port))
print('You are now connected to the server..')

class GUI:
    def __init__(self):
        self.Window= Tk()
        self.Window.withdraw()

        self.login= Toplevel()
        self.login.title('Login Window')
        self.login.resizable(height=False, width=False)
        self.login.configure(width=400, height=300)

        self.pls= Label(self.login, text='Please Login to Continue', justify= CENTER, font='Helvetica 14 bold')
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.labelName= Label(self.login, text='Name', justify= CENTER, font='Helvetica 14')
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryName= Entry(self.login, font='Helvetica 14')
        self.entryName.place(relwidth= 0.4,relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()

        self.go= Button(self.login, text='LOGIN', font='Helvetica 14', command= lambda:self.trigger(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.Window.mainloop()
    
    def trigger(self,name):
        self.login.destroy()
        self.layout(name)
        rcv= Thread(target=self.receive)
        rcv.start()
    

    
    def layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title('Harry Potter Quiz')
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg='#17202A')

        self.labelHead= Label(self.Window, bg='#17202A',fg='#EAECEE', font='Helvetica 14 bold', text=self.name,pady=5)
        self.labelHead.place(relwidth=1)

        self.line= Label(self.Window, width=450, bg='#ABB2B9')
        self.line.place(relheight=0.012, relwidth=1, rely=0.07)

        self.textCons= Text(self.Window, width=20, height=2, bg='#17202A', fg='#EAECEE',font='Helvetica 14 bold', padx=5, pady=5)
        self.textCons.place(relwidth=1, rely=0.08, relheight=0.745)
        self.textCons.config(cursor='arrow')

        self.labelBottomm= Label(self.Window, height=80, bg='#ABB2B9')
        self.labelBottomm.place(relwidth=1, rely=0.825)

        self.entryMsg= Entry(self.labelBottomm, bg='#2C3E50', font='Helvetica 13', fg='#EAECEE')
        self.entryMsg.place(relheight=0.06, rely=0.008, relwidth=0.74, relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg= Button(self.labelBottomm, text='SEND', font='Helvetica 14', width=20, bg='#ABB2B9',command=lambda:self.sendBtn(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.scrollbar= Scrollbar(self.textCons)
        self.scrollbar.place(relheight=1, relx=0.974)
        self.scrollbar.config(command=self.textCons.yview)
    
    def sendBtn(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg= msg
        self.entryMsg.delete(0,END)
        snd= Thread(target=self.write)
        snd.start()

    def show_message(self, message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            message= (f"{self.name}:{self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break

    def receive(self):
        while True:
            try:
                message= client.recv(2048).decode('utf-8')
                if message== 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_message(message)
            except:
                print('An error occured')
                client.close()
                break

g=GUI()




# receive_thread= Thread(target=receive)
# receive_thread.start()
# write_thread= Thread(target=write)
# write_thread.start()