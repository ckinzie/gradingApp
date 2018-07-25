import sys
import tkinter as tk
import xml.sax
import xmlCollector

class Model(object):
  def __init__(self):
    self.columnNames = ["Last Name", "First Name", "Grade", "Comments", "Partner"]
    self.gradeSheet = []

#############copied################333
  def saveGrades(self, filename):
    output = open(filename, 'w')
    output.write('<?xml version = "1.0"?>\n')
    output.write("<GradeSheet>\n")
    for x in self.columnNames:
      self.writeXmlElement(output, '  ', 'ColumnName', x)
    output.write('\n')
    for x in self.gradeSheet:
      self.writeXmlElement(output, '  ', 'Name', x[0])
      for g in range(1,len(x)):
        self.writeXmlElement(output, '    ', 'grade', x[g])
    output.write("</GradeSheet>\n")
    output.close()
    
  def writeXmlElement(self, output, spaces, elName, content):
    output.write(spaces+"<"+elName+">")
    output.write(content)
    output.write("</"+elName+">\n")
##################################################

  def addStudent(self, name):
    print("add student: " + name)

  def loadGrades(self, filename):
    try:
      parser = xml.sax.make_parser()
      collector = xmlCollector.XmlCollector()
      parser.setContentHandler( collector )
      parser.parse(filename)
      self.gradeSheet = collector.getGradeSheet()
      return ("Success")
    except (IOError):
      return ("Error reading file " + filename,)
    except (xml.sax.SAXParseException):
      return ("Error parsing " + filename)

  def generateDefaultSheet(self, numberRows, numberCols):
    for col in range(numberCols):
      self.columnNames.append('Column '+str(col))
    for row in range(numberRows):
      t = ['Name '+str(row)]
      for col in range(numberCols):
        t.append('('+str(row)+', '+str(col)+')')
      self.gradeSheet.append( list(t) )

  def getColumnNames(self):
    return self.columnNames

  def setGradeSheet(self, gs):
    self.gradeSheet = gs

  def getGradeSheet(self):
    return self.gradeSheet
  
  def newSheet(self):
    self.gradeSheet = []

if __name__ == "__main__":
  model = Model()
