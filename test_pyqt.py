from PyQt5.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)  # 创建 QApplication 实例
widget = QWidget()            # 创建 QWidget 实例
widget.show()                 # 显示 QWidget
sys.exit(app.exec_())         # 启动事件循环
