import sys
import tkinter as tk
import model
import view

class Controller(object):
  def __init__(self):
    self.model = model.Model()
    self.columnNames = []
    self.gradeSheet = []
    self.filename = None
    if len(sys.argv) == 2:
      self.columnNames, self.gradeSheet = self.loadGrades(sys.argv[1])
    self.view = view.View(self, self.columnNames, self.gradeSheet)
    tk.mainloop()
    
  def addStudent(self, first, last): self.model.addStudent(first, last)
  def getCount(self): return self.model.getCount()
  def dummy(self): print("dummy button")
  ############################copied###################################3
  def saveGrades(self, cols, gs):
    self.columnNames, self.gradeSheet = cols, gs
    self.model.setGradeSheet(self.columnNames, self.gradeSheet)
    self.model.saveGrades(self.filename)

  def saveGradesAs(self, cols, gs, filename):
    self.columnNames, self.gradeSheet = cols, gs
    self.filename = filename
    self.model.setGradeSheet(self.columnNames, self.gradeSheet)
    self.model.saveGrades(self.filename)

  def loadGrades(self, filename):
    self.filename = filename
    if (self.model.loadGrades(self.filename) != "Success"):
      self.view.openFileError()
      return ("Error", "Error")
    self.columnNames, self.gradeSheet = self.model.getGradeSheet()
    return self.columnNames, self.gradeSheet
    
  def getFilename(self):
    return self.filename

  
  #####################################################################

if __name__ == "__main__":
  controller = Controller()
  tk.mainloop()

