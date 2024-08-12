# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import serial
import serial.tools.list_ports
import socket
import threading
import sys

class ReceiverSignals(QtCore.QObject):
    data_received = QtCore.pyqtSignal(str)

class Ui_MainWindow(object):
    def __init__(self):
        self.receiver_signals = ReceiverSignals()
        self.receiver_signals.data_received.connect(self.append_to_receive_text_edit)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 创建布局
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # 添加串口选择框
        self.comboBox_port = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_port.setObjectName("comboBox_port")
        self.refresh_ports()  # 刷新可用串口列表

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.comboBox_baudrate = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_baudrate.setObjectName("comboBox_baudrate")
        self.comboBox_baudrate.addItems(["9600", "14400", "19200", "38400", "57600", "115200"])  # 添加常用波特率

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.pushButton_open = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_open.setFont(font)
        self.pushButton_open.setObjectName("pushButton_open")
        self.pushButton_open.clicked.connect(self.open_serial)  # 连接打开串口的按钮功能

        # 设置布局
        self.gridLayout.addWidget(self.label, 0, 0)
        self.gridLayout.addWidget(self.comboBox_port, 0, 1)
        self.gridLayout.addWidget(self.label_2, 0, 2)
        self.gridLayout.addWidget(self.comboBox_baudrate, 0, 3)
        self.gridLayout.addWidget(self.pushButton_open, 0, 4)

        # 添加发送和接收文本框及按钮
        self.textEdit_send = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_send.setObjectName("textEdit_send")
        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        font.setPointSize(20)
        self.pushButton_send.setFont(font)
        self.pushButton_send.setObjectName("pushButton_send")
        self.pushButton_send.clicked.connect(self.send_data)  # 连接发送数据按钮功能

        self.textEdit_receive = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_receive.setObjectName("textEdit_receive")

        self.gridLayout.addWidget(self.textEdit_receive, 1, 0, 1, 5)
        self.gridLayout.addWidget(self.textEdit_send, 2, 0, 1, 4)
        self.gridLayout.addWidget(self.pushButton_send, 2, 4)

        # 服务器配置
        self.label_server = QtWidgets.QLabel(self.centralwidget)
        self.label_server.setAlignment(QtCore.Qt.AlignCenter)
        self.label_server.setObjectName("label_server")

        self.lineEdit_server_port = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_server_port.setObjectName("lineEdit_server_port")

        self.pushButton_server_start = QtWidgets.QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.pushButton_server_start.setFont(font)
        self.pushButton_server_start.setObjectName("pushButton_server_start")
        self.pushButton_server_start.clicked.connect(self.start_server)  # 连接启动服务器按钮功能

        # 客户端配置
        self.label_client = QtWidgets.QLabel(self.centralwidget)
        self.label_client.setAlignment(QtCore.Qt.AlignCenter)
        self.label_client.setObjectName("label_client")

        self.lineEdit_client_ip = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_client_ip.setObjectName("lineEdit_client_ip")

        self.lineEdit_client_port = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_client_port.setObjectName("lineEdit_client_port")

        self.pushButton_client_start = QtWidgets.QPushButton(self.centralwidget)
        font.setPointSize(12)
        self.pushButton_client_start.setFont(font)
        self.pushButton_client_start.setObjectName("pushButton_client_start")
        self.pushButton_client_start.clicked.connect(self.start_client)  # 连接启动客户端按钮功能

        # 添加服务器和客户端配置到布局
        self.gridLayout.addWidget(self.label_server, 3, 0)
        self.gridLayout.addWidget(self.lineEdit_server_port, 3, 1)
        self.gridLayout.addWidget(self.pushButton_server_start, 3, 2)

        self.gridLayout.addWidget(self.label_client, 4, 0)
        self.gridLayout.addWidget(self.lineEdit_client_ip, 4, 1)
        self.gridLayout.addWidget(self.lineEdit_client_port, 4, 2)
        self.gridLayout.addWidget(self.pushButton_client_start, 4, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 初始化串口
        self.serial = None

        # 初始化服务器和客户端
        self.server_thread = None
        self.client_socket = None

        # 启动串口监听线程
        self.serial_thread = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "串口调试助手"))
        self.label.setText(_translate("MainWindow", "COM端口"))
        self.label_2.setText(_translate("MainWindow", "波特率"))
        self.pushButton_open.setText(_translate("MainWindow", "打开串口"))
        self.pushButton_send.setText(_translate("MainWindow", "发送"))
        self.label_server.setText(_translate("MainWindow", "服务器端口"))
        self.pushButton_server_start.setText(_translate("MainWindow", "启动服务器"))
        self.label_client.setText(_translate("MainWindow", "客户端配置"))
        self.pushButton_client_start.setText(_translate("MainWindow", "启动客户端"))

    def refresh_ports(self):
        """刷新可用串口列表"""
        self.comboBox_port.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.comboBox_port.addItem(port.device)

    def open_serial(self):
        """打开串口"""
        port = self.comboBox_port.currentText()
        baudrate = int(self.comboBox_baudrate.currentText())

        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
            self.pushButton_open.setText("关闭串口")
            self.pushButton_open.clicked.disconnect()
            self.pushButton_open.clicked.connect(self.close_serial)

            # 启动串口监听线程
            self.serial_thread = threading.Thread(target=self.read_serial_data)
            self.serial_thread.start()
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "错误", f"无法打开串口: {str(e)}")

    def close_serial(self):
        """关闭串口"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.serial = None
            self.pushButton_open.setText("打开串口")
            self.pushButton_open.clicked.disconnect()
            self.pushButton_open.clicked.connect(self.open_serial)

    def send_data(self):
        """发送数据"""
        if self.client_socket:
            data = self.textEdit_send.toPlainText()
            try:
                self.client_socket.sendall(data.encode('gbk'))
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "错误", f"发送数据失败: {str(e)}")
        elif self.serial and self.serial.is_open:
            data = self.textEdit_send.toPlainText()
            try:
                self.serial.write(data.encode('gbk'))
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "错误", f"发送数据失败: {str(e)}")
        else:
            QtWidgets.QMessageBox.warning(None, "警告", "请先打开串口或连接服务器")

    def read_serial_data(self):
        """读取串口数据"""
        while True:
            if self.serial and self.serial.is_open:
                data = self.serial.read(1024)
                if data:
                    self.receiver_signals.data_received.emit(f"接收到数据: {data.decode('gbk')}")
            else:
                break

    def start_server(self):
        """启动服务器"""
        port = int(self.lineEdit_server_port.text())
        self.server_thread = threading.Thread(target=self.server_function, args=(port,))
        self.server_thread.start()

    def server_function(self, port):
        """服务器功能"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(1)
        self.receiver_signals.data_received.emit("服务器已启动，等待连接...")

        while True:
            client_socket, addr = server_socket.accept()
            self.receiver_signals.data_received.emit(f"客户端 {addr} 已连接")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                self.receiver_signals.data_received.emit(f"接收到数据: {data.decode('gbk')}")
            client_socket.close()

    def start_client(self):
        """启动客户端"""
        ip = self.lineEdit_client_ip.text()
        port = int(self.lineEdit_client_port.text())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((ip, port))
            self.pushButton_client_start.setText("断开连接")
            self.pushButton_client_start.clicked.disconnect()
            self.pushButton_client_start.clicked.connect(self.stop_client)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "错误", f"连接失败: {str(e)}")

    def stop_client(self):
        """断开客户端连接"""
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
            self.pushButton_client_start.setText("启动客户端")
            self.pushButton_client_start.clicked.disconnect()
            self.pushButton_client_start.clicked.connect(self.start_client)

    def append_to_receive_text_edit(self, message):
        """在主线程中安全地更新接收文本框"""
        self.textEdit_receive.append(message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
