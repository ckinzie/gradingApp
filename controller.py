import sys
import tkinter as tk
import model
import view

class Controller(object):
  def __init__(self):
    self.model = model.Model()
    self.gradeSheet = []
    self.filename = None
    if len(sys.argv) == 2:
      self.gradeSheet = self.loadGrades(sys.argv[1])
    self.view = view.View(self, self.gradeSheet)
    tk.mainloop()
    
  def addStudent(self, first, last): self.model.addStudent(first, last)
  def getCount(self): return self.model.getCount()
  def dummy(self): print("dummy button")

  def saveGrades(self, gs):
    self.gradeSheet = gs
    self.model.setGradeSheet(self.gradeSheet)
    self.model.saveGrades(self.filename)

  def saveGradesAs(self, gs, filename):
    self.gradeSheet = gs
    self.filename = filename
    self.model.setGradeSheet(self.gradeSheet)
    self.model.saveGrades(self.filename)

  def loadGrades(self, filename):
    self.filename = filename
    if (self.model.loadGrades(self.filename) != "Success"):
      self.view.openFileError()
      return ("Error", "Error")
    self.gradeSheet = self.model.getGradeSheet()
    return self.gradeSheet
    
  def getFilename(self):
    return self.filename

  def getStudents(self):
    students = []
    for s in self.gradeSheet:
      students.append(s[0] + " " + s[1])
    return students

if __name__ == "__main__":
  controller = Controller()
  tk.mainloop()

