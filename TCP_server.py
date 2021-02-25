import socket
import threading
from tkinter import *
from tkinter import messagebox


class Server:
    def start_server(self):
        self.list_conection = []
        self.server_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()

    def accept_connetction(self):
        while True:
            self.connection, self.address = self.server_socket.accept()
            if self.connection not in self.list_conection:
                self.list_conection.append(self.connection)
                self.new_connection = threading.Thread(
                    target=self.message, args=(self.connection,), daemon=True)
                self.new_connection.start()

    def message(self, connection):
        while True:
            self.data = connection.recv(1024)
            if self.data.decode('utf-8') == '':
                self.list_conection.remove(connection)
                connection.close()
                break
            else:
                for self.connect in self.list_conection:
                    self.connect.send(self.data)

    def bloking_enty(self):
        self.entry_ip.configure(state=DISABLED)
        self.entry_port.configure(state=DISABLED)

    def start(self):
        self.start_server()
        self.accept_connetction()


class Validation(Server):
    def get_data(self):
        self.messagentry_ip = self.verification_ip()
        self.messagentry_port = self.verification_port()
        self.message_all = self.messagentry_ip + self.messagentry_port
        if len(self.message_all) > 0:
            self.switcher = False
            messagebox.showerror(title='Ошибка', message=self.message_all)
        else:
            self.switcher = True
            self.message_all = 'Данные введены корректо. Производится запуск сервера.'
            messagebox.showinfo(title='Запуск', message=self.message_all)
            self.thread_server = threading.Thread(
                target=self.start, daemon=True)
            self.thread_server.start()
            self.bloking_enty()

    def verification_ip(self):
        try:
            message = ''
            self.ip = str(self.entry_ip.get())
            if (len(self.ip) < 7 or len(self.ip) > 30):
                self.entry_ip.delete(first=0, last=END)
                message = '\nПоле "Ip" содержит ошибку:\n\
    Ip должен содержать конктретные значения (пример: 0.0.0.0).'
        except:
            message = '\nПоле "Ip" содержит ошибку:\n\
    Ip должен содержать конктретные значения (пример: 0.0.0.0).'
        return message

    def verification_port(self):
        try:
            message = ''
            self.port = int(self.entry_port.get())
            if not(-1 < self.port < 65536):
                self.entry_port.delete(first=0, last=END)
                message = '\nПоле "Port" содержит ошибку:\n\
    Port должен быть целым числом, входящим в промежуток от 0 до 65535 (пример: 8443).'
        except:
            message = '\nПоле "Port" содержит ошибку:\n\
    Port должен быть целым числом, входящим в промежуток от 0 до 65535 (пример: 8443).'
        return message


class Interface(Validation):
    def __init__(self, master):
        self.label_ip = Label(master, text='Ip:')
        self.label_port = Label(master, text='Port:')
        self.entry_ip = Entry(master, width=30)
        self.entry_port = Entry(master, width=30)
        self.button_start = Button(
            master, text='Запустить сервер', width=30, command=self.get_data)
        self.label_ip.grid(row=0, column=0)
        self.entry_ip.grid(row=0, column=1)
        self.label_port.grid(row=1, column=0)
        self.entry_port.grid(row=1, column=1)
        self.button_start.grid(row=2, column=0, columnspan=2)


root = Tk()
root.title("Сервер v:0.0.1")
root.resizable(False, False)
server = Interface(root)
root.mainloop()
