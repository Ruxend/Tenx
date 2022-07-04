# -*- coding: utf-8 -*-
#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import (QApplication,QMainWindow,QDockWidget,QWidget,QFrame,QLabel,
						QLineEdit,QTextEdit,QPushButton,QDialog,QSlider,QMessageBox,
						QInputDialog,QFileDialog,QFontDialog,QColorDialog,QToolBar,
						QMenuBar,QStatusBar,QGroupBox,QGridLayout,QHBoxLayout,QVBoxLayout,
						QFormLayout,QListWidget,QScrollBar,QDesktopWidget,QProgressBar,
						QShortcut)
from PyQt5.QtGui import (QFont,QIcon,QPixmap,QColor,QTextCursor,QPalette,QKeySequence)
from PyQt5.QtCore import (Qt,QFile,QTimer,QDateTime,QThread,pyqtSignal,QBasicTimer,QObject)
# from PyQt5.QtMultimedia import QAudioInput,QAudioOutput,QAudioDeviceInfo
import os,sys,time
from res import res
from random import randint
# from eth import eth
# from xlwt_style import style
from ui_Tenx import ui_Tenx
from threads_Tenx import WorkThread_Tenx

class myWidget_Tenx(QMainWindow, ui_Tenx):
	signal_child_3 = pyqtSignal()
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.btn_confirm.clicked.connect(self.Tenx_confirm) 		# 连接槽
		QShortcut(QKeySequence("Return"), self, self.Tenx_confirm)
		self.btn_quit.clicked.connect(self.close)					# 连接槽
		QShortcut(QKeySequence("Escape"), self, self.close)
	
	def Tenx_confirm(self):
		self.entry_1_value = self.entry_1.text()
		if self.entry_1_value=="": 
			self.text.append("----------Oops！Please Input All Necessary Parameters！----------\n")
			self.refresh_color()
			self.statusbar.showMessage("请输入必要参数!", 1000)
		else:
			try:
				self.work_start()
			except Exception as e:
				self.text.append("{}\n".format(e))  # 打印输出内容
				self.refresh_color()

	# def Makedirs_quit(self):
	# 	quit = QMessageBox.question(self, "Quit", "Do you want to quit ?", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
	# 	if quit == QMessageBox.Ok:
	# 		self.close()
	
	def work_start(self):
		self.btn_confirm.setDisabled(True)  	# 设置按钮不可用
		self.btn_confirm.setText("Waiting...")
		self.text.append("------------The program is running!------------\n")
		self.statusbar.showMessage("请稍等,正在处理...", 3600000)
		self.thread = WorkThread_Tenx(entry_1=self.entry_1_value)
		# 将线程th的信号finishSignal和UI主线程中的槽函数button_finish进行连接
		self.thread.finishSignal.connect(self.work_finish)
		self.thread.signal_1.connect(self.signal_1_call)
		self.thread.signal_2.connect(self.signal_2_call)
		self.thread.start()  				# 启动线程

	def signal_1_call(self):
		self.text.update()
		self.text.append("视频链接地址正常,解析成功!")  # 打印输出内容
		self.refresh_color()

	def signal_2_call(self):
		self.text.update()
		self.text.append("视频链接地址无效,请重新输入!")  # 打印输出内容
		self.refresh_color()

	def work_finish(self):
		self.btn_confirm.setDisabled(False) 		# 设置按钮可用
		self.btn_confirm.setText("Confirm(&C)")
		self.text.update()
		self.text.append("\n----------Done! Data Output Successfully!----------\n")
		self.refresh_color()
		self.statusbar.showMessage(f"处理完成!", 15000)
		
	def refresh_color(self):
		self.text.moveCursor(QTextCursor.End)	   # 使滚动条位置一直处于最后
		self.text.setTextColor(QColor(randint(0,255),randint(0,255),randint(0,255),255)) # 改变text字体颜色
		self.text.update()
	
	# 每一个QObject对象或其子对象都有一个QObject.timerEvent方法
	# 为了响应定时器的超时事件，需要重写进度条的timerEvent方法
	def closeEvent(self, event):
		"""重写该方法使用sys.exit(0) 时就会只要关闭了主窗口，所有关联的子窗口也会全部关闭"""
		reply = QMessageBox.question(self, "Quit", "Do you want to quit ?", QMessageBox.Yes, QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
			self.signal_child_3.emit()
		else:
			event.ignore()
	
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = myWidget_Tenx()
	window.show()
	sys.exit(app.exec())
	