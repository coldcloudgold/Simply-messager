import socket
import threading
from tkinter import *
from tkinter import messagebox


class Cleint:
    def connect_with_server(self):
        self.cleint_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.cleint_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.cleint_socket.connect((self.ip, self.port))
        receive = threading.Thread(
            target=self.receive_message_from_server, daemon=True)
        receive.start()

    def receive_message_from_server(self):
        while True:
            self.receive_message = self.cleint_socket.recv(1024)
            self.receive_message = str(self.receive_message.decode('utf-8'))
            self.update_message_from_server()

    def update_message_from_server(self):
        self.text_uotput_message.configure(state=NORMAL)
        self.text_uotput_message.insert(index=END, chars=self.receive_message)
        self.text_uotput_message.configure(state=DISABLED)

    def send_message_to_server(self):
        self.data = str(self.text_input_message.get(index1=1.0, index2=END))
        self.text_input_message.delete(index1=1.0, index2=END)
        self.send_message = f'{self.nickname}: {self.data}'
        self.send_message = self.send_message.encode('utf-8')
        self.cleint_socket.send(self.send_message)


class Validation(Cleint):
    def get_data(self):
        self.message_nickname = self.verification_nickname()
        self.messagentry_ip = self.verification_ip()
        self.messagentry_port = self.verification_port()
        self.message_all = self.message_nickname + \
            self.messagentry_ip + self.messagentry_port
        if len(self.message_all) > 0:
            self.switcher = False
            messagebox.showerror(title='Ошибка', message=self.message_all)
        else:
            self.switcher = True
            self.message_all = 'Данные введены корректо. Производится поключение к серверу.'
            messagebox.showinfo(title='Подключение', message=self.message_all)
            self.connect_with_server()
            self.connecting_window.destroy()

    def verification_nickname(self):
        try:
            message = ''
            self.nickname = str(self.entry_client_nickname.get())
            if (len(self.nickname) < 5 or len(self.nickname) > 15):
                self.entry_client_nickname.delete(first=0, last=END)
                message = '\nПоле "Ваш ник" содержит ошибку:\n\
    Ник должен иметь не менее 5 и не более 15 символов.'
        except:
            message = '\nПоле "Ваш ник" содержит ошибку:\n\
    Ник должен иметь не менее 5 и не более 15 символов.'
        return message

    def verification_ip(self):
        try:
            message = ''
            self.ip = str(self.entry_client_ip.get())
            if (len(self.ip) < 7 or len(self.ip) > 30):
                self.entry_client_ip.delete(first=0, last=END)
                message = '\nПоле "Ip" содержит ошибку:\n\
    Ip должен содержать конктретные значения (пример: 0.0.0.0).'
        except:
            message = '\nПоле "Ip" содержит ошибку:\n\
    Ip должен содержать конктретные значения (пример: 0.0.0.0).'
        return message

    def verification_port(self):
        try:
            message = ''
            self.port = int(self.entry_client_port.get())
            if not(-1 < self.port < 65536):
                self.entry_client_port.delete(first=0, last=END)
                message = '\nПоле "Port" содержит ошибку:\n\
    Port должен быть целым числом, входящим в промежуток от 0 до 65535 (пример: 8443).'
        except:
            message = '\nПоле "Port" содержит ошибку:\n\
    Port должен быть целым числом, входящим в промежуток от 0 до 65535 (пример: 8443).'
        return message


class Interface(Validation):
    def __init__(self, master):
        self.label_output_message = Label(master, text='Чат:')
        self.text_uotput_message = Text(
            master, height=20, width=60, wrap=WORD, state=DISABLED)
        self.text_input_message = Text(master, height=2, width=60, wrap=WORD)
        self.button_send_message = Button(
            master=master, text="Отправить", width=57, command=self.send_message_to_server)
        self.button_settings = Button(
            master=master, text="Подключиться", width=57, command=self.show_connecting_window)
        self.label_output_message.grid(row=0, column=0)
        self.text_uotput_message.grid(row=1, column=0)
        self.text_input_message.grid(row=2, column=0)
        self.button_send_message.grid(row=3, column=0)
        self.button_settings.grid(row=4, column=0)

    def show_connecting_window(self):
        self.connecting_window = Toplevel()
        self.connecting_window.resizable(width=False, height=False)
        self.connecting_window.title("Подключение")
        self.label_client_nickname = Label(
            self.connecting_window, text='Ваш ник:')
        self.label_client_ip = Label(self.connecting_window, text='Ip:')
        self.label_client_port = Label(self.connecting_window, text='Port:')
        self.entry_client_nickname = Entry(self.connecting_window, width=30)
        self.entry_client_ip = Entry(self.connecting_window, width=30)
        self.entry_client_port = Entry(self.connecting_window, width=30)
        self.button_client_back = Button(
            self.connecting_window, text="Назад", command=self.connecting_window.destroy)
        self.button_client_connect = Button(
            self.connecting_window, text="Подключиться", width=27, command=self.get_data)
        self.label_client_nickname.grid(row=0, column=0)
        self.label_client_ip.grid(row=1, column=0)
        self.label_client_port.grid(row=2, column=0)
        self.entry_client_nickname.grid(row=0, column=1)
        self.entry_client_ip.grid(row=1, column=1)
        self.entry_client_port.grid(row=2, column=1)
        self.button_client_back.grid(row=3, column=0)
        self.button_client_connect.grid(row=3, column=1)


root = Tk()
root.title("Чат v:0.0.1")
root.resizable(False, False)
client = Interface(root)
root.mainloop()
