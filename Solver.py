import numpy as np
import math
from scipy.linalg import lu_factor, lu_solve
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


import threading
from threading import Timer


class HW1Problem1:
    #"This is the class for hw1"  
    def InputData(self,fileName, plotInteractive = 0):
        self.isInteractive = plotInteractive
        try:
            f = open(fileName)
        except OSError as reason:
            print("open File error, plz check fileName...")
            return;
        
        line = f.readline()
        count = 0
        while line:
            count = count + 1
            line = f.readline()
        f.close()
        print("data length is %d"%(count))
        self.ROW = count
        self.COL = count 
        self.data = np.zeros([2,count])
        f = open(fileName)
        line = f.readline()
        count = 0
        while line:
            print(float(line.split(',')[0]))
            print(float(line.split(',')[1]))
            self.data[0,count] = float(line.split(',')[0])
            self.data[1,count] = float(line.split(',')[1])
            count = count + 1
            line = f.readline()
        f.close()
        #print("data matrix is:\n",self.data)
        self.XMin = min(self.data[0,:])
        self.XMax = max(self.data[0,:])
        
        print("(XMin,XMax: %f,%f)\n"%(self.XMin,self.XMax))
        
    #"This is area of Problem 1:"
    def Calculation(self):
        print("Problem is gonna run...")
        self.FormMatA_MatB()
        self.Solve()
       
    def FormMatA_MatB(self):
        print("In MatA Filling...")
        self.MatA = np.zeros([self.ROW,self.COL])
        self.MatB = np.zeros([self.ROW,1])
        for i in range(self.ROW):
            for j in range(self.COL):
                if j == 0:
                    self.MatA[i,j] = 1
                else:
                    self.MatA[i,j] = pow(self.data[0,i],j)
            self.MatB[i,0] = self.data[1,i]
            
        # Lu Solver Precomputing:
        self.lu, self.piv = lu_factor(self.MatA)
        
    def Solve(self):
        self.x = lu_solve((self.lu, self.piv), self.MatB)
        print("Solution: \n",self.x)
    def GetFittedValue(self, x):
        temp = 0
        for i in range(self.ROW):
            if i == 0:
                temp = temp + self.x[i,0]
            else:
                temp = temp + pow(x,i) * self.x[i,0]
            
        return temp
    
    def PlotData(self):
        #Create Figure to show plot
        #raw data
        plt.plot(self.data[0,:],self.data[1,:],'ro',label='Sample')
        
        
        #fitted curve
        fittedNumber = 100
        self.fittedCurve= np.zeros([2,fittedNumber])
        
        self.XRange = self.XMax - self.XMin
        # self.XMin = self.XMin - self.XRange/10
        # self.XMax = self.XMax + self.XRange/10
        
        for i in range(fittedNumber):
            self.fittedCurve[0,i]= i/(fittedNumber-1)*(self.XMax-self.XMin)+self.XMin
            self.fittedCurve[1,i]= self.GetFittedValue(self.fittedCurve[0,i])
        plt.plot(self.fittedCurve[0,:],self.fittedCurve[1,:],'b',label='Curve Problem 1')
        plt.legend()
        plt.title("HW1 Problem")
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        
        if  self.isInteractive == 1:
            plt.ion()                         #Enable interactive plot mode
        plt.show()
        
        
        # self.ax.scatter()
        
        
class HW1Problem2:
    #"This is the class for hw1"  
    def InputData(self,fileName, sigma=1.0,plotInteractive = 0):
        self.isInteractive=plotInteractive
        self.sigma = sigma
        try:
            f = open(fileName)
        except OSError as reason:
            print("open File error, plz check fileName...")
            return;
        
        line = f.readline()
        count = 0
        while line:
            count = count + 1
            line = f.readline()
        f.close()
        print("data length is %d"%(count))
        self.ROW = count+1
        self.COL = count+1
        self.data = np.zeros([2,count])
        f = open(fileName)
        line = f.readline()
        count = 0
        while line:
            print(float(line.split(',')[0]))
            print(float(line.split(',')[1]))
            self.data[0,count] = float(line.split(',')[0])
            self.data[1,count] = float(line.split(',')[1])
            count = count + 1
            line = f.readline()
        f.close()
        #print("data matrix is:\n",self.data)
        self.XMin = min(self.data[0,:])
        self.XMax = max(self.data[0,:])
        
        print("(XMin,XMax: %f,%f)\n"%(self.XMin,self.XMax))
        
     #"This is area of Problem 1:"
    def Calculation(self):
        print("Problem is gonna run...")
        self.FormMatA_MatB()
        self.Solve()
        
    def GaussBasis(self, i, x):
        #index i from 1, stands for self.data[:,0]
        #x is the input x value
        xi = self.data[0,i-1]
        g=np.exp(-1*(x-xi)*(x-xi)/(2*self.sigma*self.sigma))
        return g
        
    def FormMatA_MatB(self):
        print("In MatA Filling...")
        self.MatA = np.zeros([self.ROW,self.COL])
        self.MatB = np.zeros([self.ROW,1])
        
        x_1 = self.data[0,0]
        x_value=[]
        for i in range(self.ROW):
            if i!= self.ROW -1:
                x_value = self.data[0,i]
            for j in range(self.COL):
                if ((j == 0) and (i == (self.ROW-1))):
                    self.MatA[i,j] = 0
                elif j==0:
                    self.MatA[i,j] = 1
                elif i!= (self.ROW-1):
                    self.MatA[i,j] = self.GaussBasis(j,x_value)
                else:
                    self.MatA[i,j] = -1*(x_1-self.data[0,j-1])/(self.sigma*self.sigma)*np.exp(-1*(x_1-self.data[0,j-1])*(x_1-self.data[0,j-1])/(2*self.sigma*self.sigma))
            if i!= (self.ROW-1):
                self.MatB[i,0] = self.data[1,i]
            else: 
                self.MatB[i,0] = (self.data[1,1]-self.data[1,0])/(self.data[0,1]-self.data[0,0])
            
            
        # Lu Solver Precomputing:
        self.lu, self.piv = lu_factor(self.MatA)
        
    def Solve(self):
        self.x = lu_solve((self.lu, self.piv), self.MatB)
        print("Solution: \n",self.x)
    def GetFittedValue(self, x):
        temp = 0
        for i in range(self.ROW):
            if i == 0:
                temp = temp + self.x[i,0]
            else:
                temp = temp + self.GaussBasis(i,x) * self.x[i,0]
            
        return temp
    
    def PlotData(self):
        #Create Figure to show plot
        #raw data
        # plt.plot(self.data[0,:],self.data[1,:],'go',label='Sample2')
        if self.isInteractive == 0:
            plt.plot(self.data[0,:],self.data[1,:],'ro',label='Sample')
        #fitted curve
        fittedNumber = 100
        self.fittedCurve= np.zeros([2,fittedNumber])
        
        self.XRange = self.XMax - self.XMin
        # self.XMin = self.XMin - self.XRange/10
        # self.XMax = self.XMax + self.XRange/10
        labelName= "Curve Problem 2 (Sigma: " + str(self.sigma)+")"
        for i in range(fittedNumber):
            self.fittedCurve[0,i]= i/(fittedNumber-1)*(self.XMax-self.XMin)+self.XMin
            self.fittedCurve[1,i]= self.GetFittedValue(self.fittedCurve[0,i])
        plt.plot(self.fittedCurve[0,:],self.fittedCurve[1,:],'g',label=labelName)
        plt.legend()
        if self.isInteractive == 0:
            plt.show()
        
class HW1Problem3:
    #"This is the class for hw1"  
    def InputData(self,fileName, fittedOrder = 3, plotInteractive = 0):
        self.isInteractive = plotInteractive
        try:
            f = open(fileName)
        except OSError as reason:
            print("open File error, plz check fileName...")
            return;
        
        line = f.readline()
        count = 0
        while line:
            count = count + 1
            line = f.readline()
        f.close()
        print("data length is %d"%(count))
        self.ROW = count
        self.COL = fittedOrder
        self.fittedOrder = fittedOrder
        self.data = np.zeros([2,count])
        f = open(fileName)
        line = f.readline()
        count = 0
        while line:
            print(float(line.split(',')[0]))
            print(float(line.split(',')[1]))
            self.data[0,count] = float(line.split(',')[0])
            self.data[1,count] = float(line.split(',')[1])
            count = count + 1
            line = f.readline()
        f.close()
        #print("data matrix is:\n",self.data)
        self.XMin = min(self.data[0,:])
        self.XMax = max(self.data[0,:])
        
        print("(XMin,XMax: %f,%f)\n"%(self.XMin,self.XMax))
        
     #"This is area of Problem 1:"
    def Calculation(self):
        print("Problem is gonna run...")
        self.FormMatA_MatB()
        self.Solve()
        
    def PolynomialBasis(self, i, x):
        #index i from 0
        #x is the input x value
        if i==0:
            return 1
        else:
            return pow(x,i)
        
        
        
    def FormMatA_MatB(self):
        print("In MatA Filling...")
        self.MatA = np.zeros([self.ROW,self.COL])
        self.MatB = np.zeros([self.ROW,1])
     
        for i in range(self.ROW):
            x_i = self.data[0,i]
            y_i = self.data[1,i]
            for j in range(self.COL):
                self.MatA[i,j]=self.PolynomialBasis(j,x_i)
            self.MatB[i,0]=y_i
            
        # Lu Solver Precomputing:
        self.lu, self.piv = lu_factor(np.matmul(self.MatA.transpose(),self.MatA))
        
    def Solve(self):
        self.x = lu_solve((self.lu, self.piv), np.matmul(self.MatA.transpose(),self.MatB))
        print("Solution: \n",self.x)
        
    def GetFittedValue(self, x):
        temp = 0
        for i in range(self.COL):
            temp = temp + self.PolynomialBasis(i,x) * self.x[i,0]
        return temp
    
    def PlotData(self):
        #Create Figure to show plot
        #fitted curve
        if self.isInteractive == 0:
            plt.plot(self.data[0,:],self.data[1,:],'ro',label='Sample')
        
        
        fittedNumber = 100
        self.fittedCurve= np.zeros([2,fittedNumber])
        
        self.XRange = self.XMax - self.XMin
        # self.XMin = self.XMin - self.XRange/10
        # self.XMax = self.XMax + self.XRange/10
        
        for i in range(fittedNumber):
            self.fittedCurve[0,i]= i/(fittedNumber-1)*(self.XMax-self.XMin)+self.XMin
            self.fittedCurve[1,i]= self.GetFittedValue(self.fittedCurve[0,i])
        labelName= "Curve Problem 3 (Order: " + str(self.fittedOrder)+")"
        plt.plot(self.fittedCurve[0,:],self.fittedCurve[1,:],'m',label=labelName)
        plt.legend()
        if self.isInteractive == 0:
            plt.show()
        
        
class HW1Problem4:
    #"This is the class for hw1"  
    def InputData(self,fileName, fittedOrder = 3, regulationCoeff = 5, plotInteractive = 0):
        self.isInteractive = plotInteractive
        self.regulationCoeff = regulationCoeff
        try:
            f = open(fileName)
        except OSError as reason:
            print("open File error, plz check fileName...")
            return;
        
        line = f.readline()
        count = 0
        while line:
            count = count + 1
            line = f.readline()
        f.close()
        print("data length is %d"%(count))
        self.ROW = count
        self.COL = fittedOrder
        self.fittedOrder = fittedOrder
        self.data = np.zeros([2,count])
        f = open(fileName)
        line = f.readline()
        count = 0
        while line:
            print(float(line.split(',')[0]))
            print(float(line.split(',')[1]))
            self.data[0,count] = float(line.split(',')[0])
            self.data[1,count] = float(line.split(',')[1])
            count = count + 1
            line = f.readline()
        f.close()
        #print("data matrix is:\n",self.data)
        self.XMin = min(self.data[0,:])
        self.XMax = max(self.data[0,:])
        
        print("(XMin,XMax: %f,%f)\n"%(self.XMin,self.XMax))
        
     #"This is area of Problem 1:"
    def Calculation(self):
        print("Problem is gonna run...")
        self.FormMatA_MatB()
        self.Solve()
        
    def PolynomialBasis(self, i, x):
        #index i from 0
        #x is the input x value
        if i==0:
            return 1
        else:
            return pow(x,i)
        
        
        
    def FormMatA_MatB(self):
        print("In MatA Filling...")
        self.MatA = np.zeros([self.ROW,self.COL])
        self.MatB = np.zeros([self.ROW,1])
     
        for i in range(self.ROW):
            x_i = self.data[0,i]
            y_i = self.data[1,i]
            for j in range(self.COL):
                self.MatA[i,j]=self.PolynomialBasis(j,x_i)
            self.MatB[i,0]=y_i
            
        # Lu Solver Precomputing:
        
        self.lu, self.piv = lu_factor(np.matmul(self.MatA.transpose(),self.MatA)+self.regulationCoeff*np.identity(self.COL))
        
    def Solve(self):
        self.x = lu_solve((self.lu, self.piv), np.matmul(self.MatA.transpose(),self.MatB))
        print("Solution: \n",self.x)
        
    def GetFittedValue(self, x):
        temp = 0
        for i in range(self.COL):
            temp = temp + self.PolynomialBasis(i,x) * self.x[i,0]
        return temp
    
    def PlotData(self):
        #Create Figure to show plot
        #fitted curve
        if self.isInteractive == 0:
            plt.plot(self.data[0,:],self.data[1,:],'ro',label='Sample')
        
        
        fittedNumber = 100
        self.fittedCurve= np.zeros([2,fittedNumber])
        
        self.XRange = self.XMax - self.XMin
        # self.XMin = self.XMin - self.XRange/10
        # self.XMax = self.XMax + self.XRange/10
        
        for i in range(fittedNumber):
            self.fittedCurve[0,i]= i/(fittedNumber-1)*(self.XMax-self.XMin)+self.XMin
            self.fittedCurve[1,i]= self.GetFittedValue(self.fittedCurve[0,i])
        labelName= "Curve Problem 4 (Order: " + str(self.fittedOrder)+", Regulation Coeff: "+str(self.regulationCoeff)+")"
        plt.plot(self.fittedCurve[0,:],self.fittedCurve[1,:],'c',label=labelName)
        plt.legend()
        if self.isInteractive == 0:
            plt.show()