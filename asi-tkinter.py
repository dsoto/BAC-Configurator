import tkinter as tk
import pymodbus.client.sync      # Python Modbus library
# import serial


class row(tk.Frame):
    def __init__(self, parent, address):
        # self.address = 259
        # self.description = 'current'

        tk.Frame.__init__(self, parent)

        self.address_entry = tk.Entry(self, width=3)
        self.address_entry.insert(tk.END, address)
        self.address_entry.pack(side=tk.LEFT)

        self.description_label = tk.Label(self, text='default', width=30)
        self.description_label.pack(side = tk.LEFT)

        self.value_entry = tk.Entry(self, width=6)
        self.value_entry.insert(tk.END, 'default')
        self.value_entry.pack(side=tk.LEFT)

        self.read_button = tk.Button(self, text='Read', command=self.read)
        self.read_button.pack(side=tk.LEFT)

        self.write_button = tk.Button(self, text='Write', command=self.write)
        self.write_button.pack(side=tk.LEFT)

    def read(self):
        global asi_modbus
        print(asi_modbus.method)
        print(asi_modbus.port)
        print(asi_modbus.baudrate)
        address = int(self.address_entry.get())
        response = asi_modbus.read_holding_registers(address, 1, unit=0x01)
        print(response.registers[0])
        self.value_entry.delete(0, tk.END)
        # TODO: scale incoming value
        self.value_entry.insert(0, str(response.registers[0]))


    def write(self):
        global serial_port
        # TODO: scale outgoing value
        output = 'write {} {}\n'.format(self.address_entry.get(), self.value_entry.get())
        output = bytes(output, 'ascii')
        serial_port.write(output)
        response = serial_port.readline()
        print(response)

class Main_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # make drop down of serial ports
        serial_frame = tk.Frame(self)
        ports = ['one', 'two', 'three']
        import glob
        ports = glob.glob('/dev/tty.*')
        self.serial_port_choice = tk.StringVar()
        self.serial_port_choice.set(ports[-1])
        self.serial_menu = tk.OptionMenu(serial_frame, self.serial_port_choice, *ports)
        self.serial_menu.pack(side=tk.LEFT)
        serial_connect_button = tk.Button(serial_frame, text='Connect', command=self.connect)
        serial_connect_button.pack(side=tk.RIGHT)
        serial_frame.pack()

        # put in a button that inserts a new frame
        new_frame_button = tk.Button(self, text='New Row', command=self.new_frame)
        new_frame_button.pack()

        # loads up list of common addresses for GUI
        for address in default_addresses:
            frame = row(self, address)
            frame.pack()
            # fetch names for addresses

    def connect(self):

        global asi_modbus
        port = self.serial_port_choice.get()
        asi_modbus = pymodbus.client.sync.ModbusSerialClient(port = '/dev/tty.usbserial-DB00K1KY',
                                                            baudrate = 115200,
                                                            timeout = 2,
                                                            method = 'rtu')
        asi_modbus.connect()
        print('connected', asi_modbus.connect())
        print(asi_modbus)

    def new_frame(self):
        frame = row(self)
        frame.pack(side=tk.TOP)

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    global asi_modbus
    default_addresses = [259, 260, 261]

    app = Main_Window()
    app.title('ASI Configuratinator')
    app.geometry("600x300+300+300")
    app.mainloop()