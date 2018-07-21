import sys
import tkinter as tk
import model
import view

class Controller(object):
  def __init__(self):
    self.model = model.Model()
    self.view = view.View(self)
    tk.mainloop()
    
  def addStudent(self, first, last): self.model.addStudent(first, last)
  def getCount(self): return self.model.getCount()
  def dummy(self): print("dummy button")

if __name__ == "__main__":
  controller = Controller()
  tk.mainloop()

