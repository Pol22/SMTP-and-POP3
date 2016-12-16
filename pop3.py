import poplib
import email
import threading
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

header = ["Number", "From", "To", "Subject", "Date"]


class Pop3:
    def __init__(self, master):

        self.messages = dict()
       
        self.server_label = Label(master, text="Server", font=16)
        self.server_label.place(x=5, y=5, height=30, width=50)
        self.server = Entry(master, font=16)
        self.server.place(x=60, y=10, height=22, width=200)
        self.server.insert(END, 'pop.gmail.com')

        self.checker = Radiobutton(master, text="", variable=1, fg="red")
        self.checker.place(x=270, y=10)

        self.login_label = Label(master, text="Login", font=16)
        self.login_label.place(x=5, y=35, height=30, width=40)
        self.login = Entry(master, font=16)
        self.login.place(x=50, y=40, height=22, width=200)
        self.login.insert(END, 'recent:ilyutchenko22@gmail.com')

        self.delete_button = Button(master, text="Delete", font=16,
                                    command=self.delete_func)
        self.delete_button.place(x=645, y=35, height=30, width=100)

        self.password_label = Label(master, text="Password", font=16)
        self.password_label.place(x=255, y=35, height=30, width=70)
        self.password = Entry(master, font=16, show='*')
        self.password.place(x=330, y=40, height=22, width=200)
        
        self.login_button = Button(master, text="Login", font=16,
                                   command=self.login_func)
        self.login_button.place(x=535, y=35, height=30, width=100)

        self.quit_button = Button(master, text="X", font=16,
                                   command=self.quit_func)
        self.quit_button.place(x=755, y=35, height=30, width=20)

        container = ttk.Frame()
        container.place(x=0, y=80, height=250, width=800)

        self.tree = ttk.Treeview(columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky="ns", in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        for col in header:
            self.tree.heading(col, text=col.title().upper())
            self.tree.column(col, width=font.Font().measure(col.title()))

        self.tree.bind("<Double-1>", self.OnDoubleClick)

        self.listbox = Text()
        self.listbox.configure(state='normal')
        self.listbox.place(x=0, y=330, height=370, width=800)
        scrollbar = Scrollbar(self.listbox, orient="vertical",
                              command=self.listbox.yview)
        scrollbar.grid(row=0, column=1)
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=RIGHT, fill=Y)

        self.progress = ttk.Progressbar(master, orient='horizontal',
                                        length=490, mode='determinate')
        self.progress.place(x=300, y=10, height=22)
        self.progress["value"] = 0

    def OnDoubleClick(self, event):
        self.listbox.delete(1.0, END)
        index = self.tree.item(self.tree.selection())['values'][0]
        self.listbox.insert(END, self.messages[str(index)])

    def login_func(self):
        try:
            self.mail_box = poplib.POP3_SSL(self.server.get())
            #self.mail_box.set_debuglevel(2)
            self.mail_box.user(self.login.get())
            self.mail_box.pass_(self.password.get())
        except:
            self.checker['fg'] = 'red'
            messagebox.showerror("ERROR", "Something wrong!")
        else:
            newthread = threading.Thread(target=self.get_messagess)
            newthread.daemon = True
            newthread.start()

            self.checker['fg'] = 'green'
            messagebox.showinfo("Login successful", "Login successful")
         
    def get_messagess(self):
        self.tree.delete(*self.tree.get_children())
        list_messages = self.mail_box.list()[1]
        self.progress['maximum'] = len(list_messages)
        self.progress['value'] = 0
        for msg_info in list_messages:
            self.progress['value'] += 1
            num = msg_info.decode().split(' ')[0]
            msg = self.mail_box.retr(num)[1]
            message = email.message_from_bytes(b'\n'.join(msg))
            self.messages[num] = message
            line = (num, message.get('from'), message.get('to'),
                    message.get('subject'), message.get('date'))
            self.tree.insert('', 'end', values=line)

    def delete_func(self):
        if self.checker['fg'] == 'green':
            index = self.tree.item(self.tree.selection())['values'][0]
            self.mail_box.dele(index)

    def quit_func(self):
        if self.checker['fg'] == 'green':
            self.mail_box.quit()
            self.checker['fg'] = 'red'
            
    def close(self):
        root.destroy()
        self.mail_box.quit()
        root.quit()


if __name__ == '__main__':
    root = Tk()
    pop = Pop3(root)
    root.minsize(width=800, height=700)
    root.wm_title("POP3")
    root.protocol('WM_DELETE_WINDOW', pop.close)
    root.mainloop()
