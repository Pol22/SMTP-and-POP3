from tkinter import *
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText


class SMTP_class(object):
    def __init__(self, master):
        self.server = Label(master, text="SMTP Server:", font=16)
        self.server.place(x=5, y=5, height=30, width=100)
        self.server_txt = Entry(master, font=16)
        self.server_txt.place(x=110, y=10, height=22, width=300)
        self.server_txt.insert(END, 'smtp.yandex.ru:587')

        self.login = Label(master, text="Login:", font=16)
        self.login.place(x=5, y=30, height=30, width=45)
        self.login_txt = Entry(master, font=16)
        self.login_txt.place(x=110, y=35, height=22, width=300)
        self.login_txt.insert(END, 'ilyutchenko22@yandex.ru')

        self.password = Label(master, text="Password:", font=16)
        self.password.place(x=5, y=55, height=30, width=75)
        self.password_txt = Entry(master, show='*', font=16)
        self.password_txt.place(x=110, y=60, height=22, width=300)

        self.content = Label(master, text="Content:", font=16)
        self.content.place(x=5, y=105, height=30, width=60)
        self.content_txt = Text(master, font=16)
        self.content_txt.place(x=5, y=130, height=315, width=790)

        self.to_user = Label(master, text="To:", font=16)
        self.to_user.place(x=5, y=80, height=30, width=22)
        self.to_user_txt = Entry(master, font=16)
        self.to_user_txt.place(x=110, y=85, height=22, width=300)

        self.button = Button(master, text="Send", font=16, command=self.send)
        self.button.place(x=415, y=5, height=100, width=380)


    def send(self):
        try:
            msg_content = self.content_txt.get(1.0, END).replace('\n', '')
            message = MIMEText(msg_content, 'html')

            message['From'] = self.login_txt.get()
            message['To'] = self.to_user_txt.get()
            message['Subject'] = 'Any subject'

            msg_full = message.as_string()

            server = smtplib.SMTP(self.server_txt.get())
            server.starttls()
            server.login(self.login_txt.get(), self.password_txt.get())
            server.sendmail(self.login_txt.get(), self.to_user_txt.get(), msg_full)
            server.quit()
        except:
            messagebox.showerror("Error", "Something going wrong!!!")
        else:
            messagebox.showinfo("Done", "Done!")


if __name__ == '__main__':
    root = Tk()
    smtp_class = SMTP_class(root)
    root.minsize(width=800, height=450)
    root.wm_title("SMTP")
    root.mainloop()
