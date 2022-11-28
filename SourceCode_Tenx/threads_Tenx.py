# -*- coding: utf-8 -*-
#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import (QTextCursor,QColor,QPalette)
from PyQt5.QtCore import (QThread,pyqtSignal)
from random import randint
import os,time,webbrowser,re
from urllib import parse
from ui_Tenx import ui_Tenx

class WorkThread_Tenx(QThread):
	# 使用信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
	finishSignal = pyqtSignal()
	signal_1 = pyqtSignal()
	signal_2 = pyqtSignal()
	def __init__(self, entry_1, port, parent=None):
		super().__init__(parent)
		self.entry_1 = entry_1
		self.port = port

	def run(self):
		if re.match(r"^https?:/{2}\w.+$", self.entry_1): 	# 正则表达式判定是否为合法连接
			ip = parse.quote_plus(self.entry_1)  			# 视频连接加密
			webbrowser.open(self.port + ip)  					# 用浏览器打开网址
			self.signal_1.emit()
		else:
			self.signal_2.emit()
		self.finishSignal.emit()  		# 发射程序结束输出
		return


# entry_1 = "D:/Dev/Object/Python/test/111.xls"
# entry_2 = "111"
# entry_3 = "D:/Dev/Object/Python/test1"
# entry_4 = "txt"
# WorkThread(entry_1=entry_1, entry_2=entry_2, entry_3=entry_3, entry_4=entry_4).run()