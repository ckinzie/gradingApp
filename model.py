import sys
import tkinter as tk

class Model(object):
  def __init__(self):
    self.count = 0
  
  def addStudent(self, first, last):
    self.count += 1
    
  def getCount(self):
    return self.count

if __name__ == "__main__":
  model = Model()
