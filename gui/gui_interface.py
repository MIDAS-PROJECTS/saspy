import tkinter as tk
from tkinter import ttk
from serial.tools.list_ports import comports

from typing import Optional

from sasConnection import SasConnection

class MainFrame(tk.Frame):
    def __init__(self, root = None):
        super().__init__(master=root)
        self.pack(side="top", fill="both", expand="false", padx=10,pady=10)
        print("WEIIIIIII")
        self.__setup_gui()

        self.__sasConnection : Optional[SasConnection] = None
    
    def __setup_gui(self):
        self.__setup_label()
        self.__setup_port_selector()
        self.__setup_address_selector()
        self.__setup_buttons()
        self.__setup_message_areas()
        self.__setup_flush_buttons()
    
    def __setup_label(self):
        label = tk.Label(self, text = "Select SAS Connection configuration", anchor=tk.NW, font=("ARIAL",16))
        label.pack(side=tk.TOP, fill="both", expand=False)
    
    def __setup_port_selector(self):
        ports = [port.device for port in comports()]
        self.port_var = tk.StringVar(value=ports[0] if ports else "No ports")
        label = tk.Label(self, text = "Select Port", anchor=tk.NW)
        label.pack()
        self.port_menu = ttk.OptionMenu(self, self.port_var, self.port_var.get(), *ports)
        self.port_menu.pack(pady=5)
    
    def __setup_address_selector(self):
        self.addr_var = tk.IntVar(value = 1)
        label = tk.Label(self, text = "Select gaming machine Address (1 - 127):")
        label.pack()
        self.addr_spinbox = tk.Spinbox(self, from_=1, to=127, textvariable=self.addr_var, width=5)
        self.addr_spinbox.pack(pady=5)
    
    def __setup_buttons(self):
        frm = tk.Frame(master = self, relief=tk.RAISED)
        frm.pack(pady=5)

        self.start_btn = tk.Button(frm, text = "Start", command = self.__on_start)
        self.start_btn.pack(padx=10, side = tk.LEFT)

        self.stop_btn = tk.Button(frm, text = "Stop", command = self.__on_stop, state="disabled")
        self.stop_btn.pack(padx=10, side = tk.LEFT)
    
    def __setup_flush_buttons(self):
        frm = tk.Frame(master = self, relief = tk.RAISED)
        frm.pack(pady=5)

        flushException = tk.Button(frm, text = "flush exceptions", command = lambda : self.__flush_to_widget(self.exception_area))
        flushException.pack(padx=10, side = tk.LEFT)

        flushLongPolls = tk.Button(frm, text = "flush commands", command = lambda : self.__flush_to_widget(self.command_area))
        flushLongPolls.pack(padx=10, side = tk.LEFT)

        sendMeters = tk.Button(frm, text = "ask for meters", command = lambda : self.__sasConnection.send_meters_10_15())
        sendMeters.pack(padx = 10, side = tk.LEFT)
    
    def __on_start(self):
        selected_port = self.port_var.get()
        selected_addr = self.addr_var.get()
        self.__sasConnection = SasConnection(
            port = selected_port,
            address = selected_addr,
            exceptionLogFunc = lambda input: self.__log_to_widget(self.exception_area, input),
            commandLogFunc = lambda input: self.__log_to_widget(self.command_area, input),
        )
        self.__sasConnection.connect()

        self.start_btn.config(state="disabled")
        self.stop_btn.config(state = "normal")
        self.addr_spinbox.config(state = "disabled")
        self.port_menu.config(state = "disabled")
    
    def __on_stop(self):
        if self.__sasConnection:
            self.__sasConnection.stop()
            self.__sasConnection = None
        
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.addr_spinbox.config(state = "normal")
        self.port_menu.config(state = "normal")


    def __setup_message_areas(self):
        self.exception_area = tk.Text(self, height=8, width=60, state="disabled", wrap="word", bg="#FFFFFF")
        self.exception_area.pack(padx=10, pady=10)

        self.command_area = tk.Text(self, height=8, width=60, state="disabled", wrap="word", bg="#FFFFFF")
        self.command_area.pack(padx=10, pady=10)
    
    def __log_to_widget(self, widget, message):
        widget.config(state = "normal")
        widget.insert(tk.END, message + "\n")
        widget.see(tk.END)
        widget.config(state="disabled")
    
    def __flush_to_widget(self, widget):
        widget.config(state = "normal")
        widget.delete(1.0, tk.END)
        widget.config(state="disabled")
    


