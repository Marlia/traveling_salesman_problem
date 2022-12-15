#DatabaseSubsystem.py
import sqlite3
import hashlib
from PyQt4 import QtCore, QtGui
import os.path

DB_FILENAME = 'Users.db'
Q_INIT = 'CREATE TABLE IF NOT EXISTS `Users`(`Mark` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `Login` varchar(255) NOT NULL, `Password` char(64) NOT NULL);'
Q_AUTH = 'SELECT Password FROM Users WHERE Login = ?;'
Q_REG = 'INSERT INTO `Users`(`Login`, `Password`) VALUES(?, ?);'

class TDatabaseSubsystem:
	__fConnected = False
	def __init__(self):
		print("Создан объект TDatabaseSystem...")
		
	def Connect(self, AQParent):
		try:
			if (os.path.isfile(DB_FILENAME) == False):
				QtGui.QMessageBox.information(AQParent, "Первый запуск приложения", "Обнаружен первый запуск приложения, осуществляется создание чистой базы данных...")
			self.connMain = sqlite3.connect(DB_FILENAME)
			self.crWork = self.connMain.cursor()
			self.__fConnected = True
			self.Initializate()
		except sqlite3.Error as ESQLite3Exception:
			QtGui.QMessageBox.critical(AQParent, "Произошла ошибка", "Произошла ошибка при соединении с базой данных: {}. Приложение должно быть закрыто.".format(ESQLite3Exception))
			self.Disconnect()
			return
		print("Соединение установлено.")
			
	def Disconnect(self):
		self.crWork.close()
		if (self.connMain):
			self.connMain.close()
		print("Соединение разорвано.")

	def AuthorizeUser(self, Login, Password):
		if (self.__fConnected == True):
			AuthData = (Login, )
			self.crWork.execute(Q_AUTH, AuthData)
			StoredPassword = self.crWork.fetchone()
			if (StoredPassword != None):
				if (StoredPassword[0] == hashlib.sha512(Password.encode()).hexdigest()):
					return 0
				else:
					return 1
			else:
				return 2

	def RegisterUser(self, Login, Password):
		if (self.__fConnected == True):
			if (self.AuthorizeUser(Login, Password) == 2):
				AuthData = (Login, hashlib.sha512(Password.encode()).hexdigest())
				self.crWork.execute(Q_REG, AuthData)
				self.connMain.commit()
				print("Авторизация провалена, регистрация...")
				return 0
			else:
				return 1
			
	def Initializate(self):
		if (self.__fConnected == True):
			self.crWork.execute(Q_INIT)
			self.connMain.commit()
			print("Инициализация завершена.")