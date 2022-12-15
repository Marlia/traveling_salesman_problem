#GUISubsystem.py
import DatabaseSubsystem as DS
import GraphSubsystem as GS
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
import numpy as NP
from numpy import sqrt
from matplotlib import rc
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as PLT

class TfrmRegistration(QDialog):
	def __init__(self, ADS):
		super(TfrmRegistration, self).__init__()
		self._oDS = ADS
		self.setWindowTitle("Регистрация")
		self._lblLogin = QLabel('Имя пользователя:')
		self._lblPassword = QLabel('Пароль:')
		self._lblPassword2 = QLabel('Пароль (ещё раз):')
		self._edtLogin = QLineEdit()
		self._edtPassword = QLineEdit()
		self._edtPassword2 = QLineEdit()
		self._btnRegister = QPushButton('Регистрация...')
		self._loHLogin = QHBoxLayout()
		self._loHPassword = QHBoxLayout()
		self._loHPassword2 = QHBoxLayout()
		self._loVPrime = QVBoxLayout()
		self._edtInit()
		self._btnInit()
		self._loInit()
	def _loInit(self):
		self._loHLogin.addWidget(self._lblLogin)
		self._loHLogin.addWidget(self._edtLogin)
		self._loHPassword.addWidget(self._lblPassword)
		self._loHPassword.addWidget(self._edtPassword)
		self._loHPassword2.addWidget(self._lblPassword2)
		self._loHPassword2.addWidget(self._edtPassword2)
		self._loVPrime.addLayout(self._loHLogin)
		self._loVPrime.addLayout(self._loHPassword)
		self._loVPrime.addLayout(self._loHPassword2)
		self._loVPrime.addWidget(self._btnRegister)
		self.setLayout(self._loVPrime)
	def _edtInit(self):
		self._edtPassword.setEchoMode(QLineEdit.Password)
		self._edtPassword2.setEchoMode(QLineEdit.Password)
		self._edtLogin.textChanged.connect(self._OnEditChange)
		self._edtPassword.textChanged.connect(self._OnEditChange)
		self._edtPassword2.textChanged.connect(self._OnEditChange)
	def _btnInit(self):
		self._btnRegister.setEnabled(False)
		self._btnRegister.clicked.connect(self._On_btnRegisterClick)
	def _OnEditChange(self):
		if self._edtLogin.text() and self._edtPassword.text() and self._edtPassword2.text():
			self._btnRegister.setEnabled(True)
		else:
			self._btnRegister.setEnabled(False)
	def _On_btnRegisterClick(self):
		if self._edtPassword.text() == self._edtPassword2.text():
			decRegisterCode = self._oDS.RegisterUser(self._edtLogin.text(), self._edtPassword.text())
			if (decRegisterCode == 0):
				QMessageBox.information(self, 'Информация.', 'Регистрация прошла успешно. Используйте ваше имя и пароль для авторизации.')
				self.close()
			elif (decRegisterCode == 1):
				QMessageBox.critical(self, 'Внимание!', 'Такое имя пользователя уже присутствует. Выберите другое имя пользователя.')
				self._edtLogin.clear()
		else:
			QMessageBox.critical(self, 'Внимание!', 'Пароль и его подтверждение не совпадают.')
			self._edtPassword.clear()
			self._edtPassword2.clear()

class TfrmAuthorization(QWidget):
	def __init__(self, ADS):
		super(TfrmAuthorization, self).__init__()
		self._oDS = ADS
		self._oDS.Connect(self)
		self.resize(300, 100)
		self.setWindowTitle("Авторизация")	
		self._lblLogin = QLabel('Имя пользователя:', self)
		self._lblPassword = QLabel('Пароль:', self)
		self._edtLogin = QLineEdit(self)
		self._edtPassword = QLineEdit(self)
		self._btnLogin = QPushButton('Войти', self)
		self._btnRegister = QPushButton('Регистрация...', self)		
		self._loGAuthData = QGridLayout()
		self._loHButtons = QHBoxLayout()
		self._loVPrime = QVBoxLayout()		
		self._edtInit()
		self._btnInit()
		self._loInit()
	def _loInit(self):
		self._loGAuthData.addWidget(self._lblLogin, 0, 0, 1, 1)
		self._loGAuthData.addWidget(self._edtLogin, 0, 1, 1, 1)
		self._loGAuthData.addWidget(self._lblPassword, 1, 0, 1, 1)
		self._loGAuthData.addWidget(self._edtPassword, 1, 1, 1, 1)
		self._loHButtons.addWidget(self._btnLogin)
		self._loHButtons.addWidget(self._btnRegister)
		self._loVPrime.addLayout(self._loGAuthData)
		self._loVPrime.addLayout(self._loHButtons)
		self.setLayout(self._loVPrime)
	def _edtInit(self):
		self._edtLogin.setPlaceholderText('Введите своё имя.')
		self._edtPassword.setPlaceholderText('Введите свой пароль.')
		self._edtPassword.setEchoMode(QLineEdit.Password)
		self._edtLogin.textChanged.connect(self._OnEditChange)
		self._edtPassword.textChanged.connect(self._OnEditChange)
	def _btnInit(self):
		self._btnLogin.setEnabled(False)
		self._btnLogin.clicked.connect(self._OnBtnLoginClick)
		self._btnRegister.clicked.connect(self._OnBtnRegisterClick)
	def _OnEditChange(self):
		if (self._edtLogin.text()) and (self._edtPassword.text()):
			self._btnLogin.setEnabled(True)
		else:
			self._btnLogin.setEnabled(False)
	def _OnBtnLoginClick(self):
		decAuthCode = self._oDS.AuthorizeUser(self._edtLogin.text(), self._edtPassword.text())
		if (decAuthCode == 0):
			QMessageBox.information(self, "Информация.", "Добро пожаловать, {}".format(self._edtLogin.text()))
			self._frmMain = TfrmMain(self._edtLogin.text(), self)
			self.close()
		elif (decAuthCode == 1):
			QMessageBox.critical(self, "Внимание!", "Имя пользователя и/или пароль неверны.")
			self._edtLogin.clear()
			self._edtPassword.clear()
			return
		elif (decAuthCode == 2):
			QMessageBox.critical(self, "Внимание!", "Такого имени пользователя нет в базе данных.")
			self._edtLogin.clear()
			self._edtPassword.clear()
			return
	def _OnBtnRegisterClick(self):
		self._frmRegistration = TfrmRegistration()
		self._frmRegistration.exec_()
	def showBis(self):
		self._edtLogin.clear()
		self._edtPassword.clear()
		self.show()
		del self._frmMain

class TfrmMain(QMainWindow):
	def __init__(self, ALogin, AParent):
		super(TfrmMain, self).__init__()
		self._fParent = AParent
		self.resize(800, 512)
		self.setWindowTitle("Метод ближайшего соседа")
		self._statusBar = QStatusBar()
		self._statusBar.showMessage("Вы вошли под именем: {}".format(ALogin), -1)
		self.setStatusBar(self._statusBar)
		self._actionsInit()
		self._menuInit()
		self._toolBarInit()
		self._wCentral = QWidget(self)
		self.setCentralWidget(self._wCentral)
		self._loHPrime = QHBoxLayout()
		self._loVLeft = QVBoxLayout()
		self._loVTop = QVBoxLayout()
		self._lblEnterVertices = QLabel("Введите количество вершин в графе:")
		self._edtVerticesCount = QLineEdit()
		self._lblEnterStart = QLabel("Введите номер стартового города:")
		self._edtStartNumber = QLineEdit()
		self._memoData = QTextEdit()
		self._GraphEnvironmentInit()
		self._loInit()
		self.show()
	def _actionsInit(self):
		self._actExit = QAction("Выход", self)
		self._actExit.setShortcut('Ctrl+Q')
		self._actExit.setStatusTip('Выход из системы.')
		self.connect(self._actExit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
		self._actSaveAs = QAction("Сохранить результат решения как...", self)
		self._actSaveAs.setShortcut('Ctrl+S')
		self._actSaveAs.setStatusTip('Сохранение графа с результатом решения задачи коммивояжёра в графический файл.')
		self._actSaveAs.triggered.connect(self._ActSaveAsExecute)
		self._actCallHelp = QAction("Справка...", self)
		self._actCallHelp.setShortcut('F1')
		self._actCallHelp.setStatusTip('Вызвать краткую справку.')
		self._actCallHelp.triggered.connect(self._ActCallHelpExecute)
		self._actRandomGen = QAction("Сгенерировать граф в случайном порядке", self)
		self._actRandomGen.setShortcut('Ctrl+R')
		self._actRandomGen.setStatusTip('Сгенерировать граф в случайном порядке.')
		self._actRandomGen.triggered.connect(self._ActRandomGenExecute)
		self._actSolve = QAction("Решить задачу коммивояжёра", self)
		self._actSolve.setShortcut('F3')
		self._actSolve.setStatusTip('Решить задачу коммивояжёра методом ближайшего соседа.')
		self._actSolve.triggered.connect(self._ActSolveExecute)
	def _menuInit(self):
		self._mmMain = self.menuBar()
		_miGraph = self._mmMain.addMenu("&Граф")
		_miGraph.addAction(self._actRandomGen)
		_miGraph.addAction(self._actSolve)
		_miGraph.addSeparator()
		_miGraph.addAction(self._actSaveAs)
		_miGraph.addSeparator()
		_miGraph.addAction(self._actExit)
	def _toolBarInit(self):
		self._tbMain = self.addToolBar('Основная панель')
		self._tbMain.addAction(self._actExit)
		self._tbMain.addSeparator()
		self._tbMain.addAction(self._actSolve)
		self._tbMain.addAction(self._actSaveAs)
		self._tbMain.addSeparator()
		self._tbMain.addAction(self._actCallHelp)
	def _GraphEnvironmentInit(self):
		self.fgFigure = Figure()
		self._cvCanvas = FigureCanvas(self.fgFigure)
		self._cvCanvas.draw()
	def _loInit(self):
		self._loVTop.addWidget(self._lblEnterVertices)
		self._loVTop.addWidget(self._edtVerticesCount)
		self._loVTop.addWidget(self._lblEnterStart)
		self._loVTop.addWidget(self._edtStartNumber)
		self._loVLeft.addLayout(self._loVTop)
		self._loVLeft.addWidget(self._memoData)
		self._loHPrime.addLayout(self._loVLeft)
		self._loHPrime.addWidget(self._cvCanvas)
		self._wCentral.setLayout(self._loHPrime)
	def _ActSaveAsExecute(self):
		strFileName = QFileDialog.getSaveFileName(self, "Выберите место сохранения графа.", "C:/", "PNG (*.png);; All Files (*)")
		if (strFileName != ""):
			self.fgFigure.savefig(strFileName)
	def _ActRandomGenExecute(self):
		self._cvCanvas.fgFigure.clear()
		self._oGS.RandomGenerate()
		self._oGS.NormalizeWeights()
		self._oGS.DrawGraph()
		self._cvCanvas.draw()
	def _ActSolveExecute(self):
		try:
			self._cvCanvas.figure.clear()
			self._memoData.clear()
			self._memoData.append("Внимание! Вершины ниже считаются с нуля.")
			self._memoData.append("Количество вершин в графе: {}".format(self._edtVerticesCount.text()))
			self._memoData.append("Стартовый город: {}".format(self._edtStartNumber.text()))
			if (int(self._edtVerticesCount.text()) <= int(self._edtStartNumber.text())):
				QMessageBox.critical(self, "Внимание!", "Номер стартового города должен быть меньше максимального номера города.")
				return
			if (int(self._edtStartNumber.text()) < 0):
				QMessageBox.critical(self, "Внимание!", "Номер стартового города должен быть больше нуля.")
				return
			if (int(self._edtVerticesCount.text()) <= 0):
				QMessageBox.critical(self, "Внимание!", "Количество вершин должно быть больше нуля.")
				return
			self._oGS = GS.TGraphSubsystem(int(self._edtVerticesCount.text()), int(self._edtStartNumber.text()), self.fgFigure)
			self._oGS.RandomGenerate()
			self._oGS.NormalizeWeights()
			Result = self._oGS.Solve()
			self._memoData.append("Длина пути: {}".format(Result[0]))
			self._oGS.Visualize()
			self._cvCanvas.draw()
			self._memoData.append("Маршрут: {}".format(Result[1]))
		except:
			self._cvCanvas.figure.clear()
			self._memoData.clear()
			self._edtVerticesCount.clear()
			self._edtStartNumber.clear()
			QMessageBox.critical(self, "Внимание!", "Обнаружена ошибка ввода. Попробуйте ещё раз.")
			return
	def _ActCallHelpExecute(self):
		self._frmHelp = TfrmHelp()
	def closeEvent(self, event):
		self._fParent.showBis()
		
class TfrmHelp(QDialog):
	def __init__(self):
		super(TfrmHelp, self).__init__()
		self.setWindowTitle("Краткая справка")
		self._memoHelp = QTextEdit("Краткая справка по работе с программой. \n После авторизации необходимо ввести количество вершин в графе для задания условий задачи коммивояжёра. После этого необходимо нажать на кнопку '''Решить задачу коммивояжёра'''. \n При необходимости результат решения можно сохранить в файл путём нажатия кнопки '''Сохранить результат решения'''.")
		self._loHPrime = QHBoxLayout()
		self._loHPrime.addWidget(self._memoHelp)
		self.setLayout(self._loHPrime)
		self.show()
			
class TGUISubsystem:
	def __init__(self):
		self.Startup()	
	def Startup(self):
		self._oDS = DS.TDatabaseSubsystem()	
		_oApplication = QtGui.QApplication(sys.argv)
		self._frmAuthorization = TfrmAuthorization(self._oDS)
		self._frmAuthorization.show()
		sys.exit(_oApplication.exec_())
		self.Shutdown()
	def __del__(self):
		self.Shutdown()
	def Shutdown(self):
		del self._oDS