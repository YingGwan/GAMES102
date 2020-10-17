#####################################################
##
##Author: YINGJUN TIAN From CUHK
##E-mail: tianyj1997@163.com
##
#####################################################
import os
import importlib 
import numpy as np
import Solver
import time
#Please provide the sample points in data.txt

importlib.reload(Solver)  # reload the Solver when necessary

p1 = Solver.HW1Problem1()
p1.InputData("data.txt")
p1.Calculation()
p1.PlotData()


sigma = float(input("In problem 2, Enter sigma value: "))
p2 = Solver.HW1Problem2()
p2.InputData("data.txt",sigma)
p2.Calculation()
p2.PlotData()


fitted_order_p3 = int(input("In problem 3, Enter Fitted Order value: "))
p3 = Solver.HW1Problem3()
p3.InputData("data.txt",fitted_order_p3)
p3.Calculation()
p3.PlotData()


fitted_order_p4 = int(input("In problem 4, Enter Fitted Order value: "))
regulation = float(input("In problem 4, Enter Regulation Coeff value: "))
p4 = Solver.HW1Problem4()
p4.InputData("data.txt",fitted_order_p4,regulation)
p4.Calculation()
p4.PlotData()

print("\n.................................................\nDraw in one plot")

p1 = Solver.HW1Problem1()
p1.InputData("data.txt",1)
p1.Calculation()
p1.PlotData()


p2 = Solver.HW1Problem2()
p2.InputData("data.txt",sigma,1)
p2.Calculation()
p2.PlotData()


p3 = Solver.HW1Problem3()
p3.InputData("data.txt",fitted_order_p3,1)
p3.Calculation()
p3.PlotData()


p4 = Solver.HW1Problem4()
p4.InputData("data.txt",fitted_order_p4,regulation,1)
p4.Calculation()
p4.PlotData()
