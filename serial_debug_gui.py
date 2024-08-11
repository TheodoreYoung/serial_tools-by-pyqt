# serial_debug_gui_full_gbk.py

import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QLineEdit, QLabel, QHBoxLayout)
from PyQt5.QtCore import QTimer

class SerialDebugApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_port = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)

    def initUI(self):
        self.setWindowTitle('串口调试助手')
        self.setGeometry(100, 100, 800, 600)

        # Create widgets
        self.port_label = QLabel('串口:', self)
        self.port_combobox = QComboBox(self)
        self.refresh_ports_button = QPushButton('刷新串口', self)
        self.refresh_ports_button.clicked.connect(self.refresh_ports)

        self.baudrate_label = QLabel('波特率:', self)
        self.baudrate_combobox = QComboBox(self)
        self.baudrate_combobox.addItems(['9600', '19200', '38400', '57600', '115200'])

        self.open_button = QPushButton('打开串口', self)
        self.open_button.clicked.connect(self.open_serial)

        self.close_button = QPushButton('关闭串口', self)
        self.close_button.clicked.connect(self.close_serial)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText('接收到的串口数据...')
        self.send_line_edit = QLineEdit(self)
        self.send_button = QPushButton('发送', self)
        self.send_button.clicked.connect(self.send_data)

        # Create layout
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_combobox)
        port_layout.addWidget(self.refresh_ports_button)

        baudrate_layout = QHBoxLayout()
        baudrate_layout.addWidget(self.baudrate_label)
        baudrate_layout.addWidget(self.baudrate_combobox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.send_line_edit)
        button_layout.addWidget(self.send_button)

        layout = QVBoxLayout()
        layout.addLayout(port_layout)
        layout.addLayout(baudrate_layout)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize serial ports
        self.refresh_ports()

    def refresh_ports(self):
        self.port_combobox.clear()
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combobox.addItems(ports)

    def send_data(self):
        if self.serial_port and self.serial_port.is_open:
            data = self.send_line_edit.text()
            try:
                # Encode data to GBK before sending
                self.serial_port.write(data.encode('gbk'))
                self.text_edit.append(f"Sent: {data}")
            except Exception as e:
                self.text_edit.append(f"Error: {str(e)}")
        else:
            self.text_edit.append("Error: Serial port is not open")

    def read_serial(self):
        if self.serial_port and self.serial_port.is_open:
            while self.serial_port.in_waiting:
                try:
                    # Read and decode data using GBK
                    data = self.serial_port.read(self.serial_port.in_waiting)
                    decoded_data = data.decode('gbk')
                    self.text_edit.append(f"Received: {decoded_data}")
                except Exception as e:
                    self.text_edit.append(f"Error: {str(e)}")

    def open_serial(self):
        port = self.port_combobox.currentText()
        baudrate = int(self.baudrate_combobox.currentText())
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            self.timer.start(100)  # Check for incoming data every 100ms
            self.text_edit.append(f"Serial port {port} opened with baudrate {baudrate}")
        except Exception as e:
            self.text_edit.append(f"Error: {str(e)}")

    def close_serial(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.timer.stop()
            self.text_edit.append("Serial port closed")
        else:
            self.text_edit.append("Error: Serial port is not open")

    def closeEvent(self, event):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialDebugApp()
    ex.show()
    sys.exit(app.exec_())
