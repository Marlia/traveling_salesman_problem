#GraphSubsystem.py
import matplotlib.pyplot as PLT
from matplotlib import rc
import numpy as NP
from numpy import sqrt

class TGraphSubsystem:
	def __init__(self, ATownCount, ATownStart, AFigure):
		self._fTownCount = ATownCount
		self._fTownStart = ATownStart
		self._fFigure = AFigure
		axisPlot = self._fFigure.add_subplot(111)
		axisPlot.clear()
		self._fWeights = NP.zeros([ATownCount, ATownCount])
	def NormalizeWeights(self):
		for decCounterA in NP.arange(0, self._fTownCount, 1):
			for decCounterB in NP.arange(0, self._fTownCount, 1):
				if decCounterA != decCounterB:
					self._fWeights[decCounterA, decCounterB] = sqrt((self._fX[decCounterA] - self._fX[decCounterB])**2 + (self._fY[decCounterA] - self._fY[decCounterB])**2)
				else:
					self._fWeights[decCounterA, decCounterB] = float('inf')
	def RandomGenerate(self):
		self._fX = NP.random.uniform(0, 100, self._fTownCount)
		self._fY = NP.random.uniform(0, 100, self._fTownCount)
	def Solve(self):
		self.fRoute = []
		self.fRoute.append(self._fTownStart)
		for decCounterA in NP.arange(1, self._fTownCount, 1):
			self._Tmp = []
			for decCounterB in NP.arange(0, self._fTownCount, 1):
				self._Tmp.append(self._fWeights[self.fRoute[decCounterA - 1], decCounterB])
			self.fRoute.append(self._Tmp.index(min(self._Tmp))) #Индекс ближайшего города.
			for decCounterB in NP.arange(0, decCounterA, 1):
				self._fWeights[self.fRoute[decCounterA], self.fRoute[decCounterB]] = float('inf')
				self._fWeights[self.fRoute[decCounterA], self.fRoute[decCounterB]] = float('inf')
		fltAmount = sum([sqrt((self._fX[self.fRoute[decCounterA]] - self._fX[self.fRoute[decCounterA + 1]])**2 + (self._fY[self.fRoute[decCounterA]] - self._fY[self.fRoute[decCounterA + 1]])**2) for decCounterA in NP.arange(0, self._fTownCount - 1, 1)]) + sqrt((self._fX[self.fRoute[self._fTownCount - 1]] - self._fX[self.fRoute[0]])**2 + (self._fY[self.fRoute[self._fTownCount - 1]] - self._fY[self.fRoute[0]])**2)
		return [fltAmount, self.fRoute]
	def Visualize(self):
		self.axisPlot = self._fFigure.add_subplot(111)
		self.axisPlot.clear()
		descFont = {'family': 'times new roman', 'weight': 'normal', 'size': 14}
		rc('font', **descFont)
		self._fX1=[self._fX[self.fRoute[decCounter]] for decCounter in NP.arange(0, self._fTownCount, 1)]
		self._fY1=[self._fY[self.fRoute[decCounter]] for decCounter in NP.arange(0, self._fTownCount, 1)]
		self.axisPlot.plot(self._fX1, self._fY1, color='r', linestyle=' ', marker='o')
		self.axisPlot.plot(self._fX1, self._fY1, color='b', linewidth = 1)   
		self._fX2=[self._fX[self.fRoute[self._fTownCount - 1]], self._fX[self.fRoute[0]]]
		self._fY2=[self._fY[self.fRoute[self._fTownCount - 1]], self._fY[self.fRoute[0]]]
		self.axisPlot.plot(self._fX2, self._fY2, color = 'g', linewidth = 2,  linestyle='-', label='Путь от последнего \n к начальному городу')
		for decCounter in range(self._fTownCount):
			self.axisPlot.text(self._fX[decCounter] + 0.2, self._fY[decCounter] + 0.2, str(decCounter))
		self.axisPlot.legend(loc='best')
		self.axisPlot.grid(True)
		return self.axisPlot