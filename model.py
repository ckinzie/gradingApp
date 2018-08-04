import sys
import tkinter as tk
import xml.sax
import xmlCollector
import ast

class Model(object):
  def __init__(self):
    self.columnNames = ["Name", "Grade", "Comments", "Partner"]
    self.gradeSheet = []
    self.comments = []

  def saveGrades(self, filename):
    output = open(filename, 'w')
    output.write('<?xml version = "1.0"?>\n')
    output.write("<GradeSheet>\n")
    for x in self.gradeSheet:
      self.writeXmlElement(output, '  ', 'Name', x[0])
      self.writeXmlElement(output, '    ', 'Grade', x[1])
      self.writeXmlElement(output, '    ', 'Comments', x[2])
      self.writeXmlElement(output, '    ', 'Partner', x[3])
    output.write("\n")
    for c in self.comments:
      self.writeXmlElement(output, '  ', 'Note', c[0])
      self.writeXmlElement(output, '    ', 'Value', c[1])
    output.write("</GradeSheet>\n")
    output.close()
    
  def writeXmlElement(self, output, spaces, elName, content):
    output.write(spaces+"<"+elName+">")
    output.write(content)
    output.write("</"+elName+">\n")

  def loadGrades(self, filename):
    try:
      parser = xml.sax.make_parser()
      collector = xmlCollector.XmlCollector()
      parser.setContentHandler( collector )
      parser.parse(filename)
      self.gradeSheet = collector.getGradeSheet()
      self.comments = collector.getComments()
      return ("Success")
    except (IOError):
      return ("Error reading file " + filename,)
    except (xml.sax.SAXParseException):
      return ("Error parsing " + filename)
  '''
  def generateDefaultSheet(self, numberRows, numberCols):
    for col in range(numberCols):
      self.columnNames.append('Column '+str(col))
    for row in range(numberRows):
      t = ['Name '+str(row)]
      for col in range(numberCols):
        t.append('('+str(row)+', '+str(col)+')')
      self.gradeSheet.append( list(t) )
  '''
  
  def exportAsTxt(self, filename):
    output = open(filename, 'w')
    studentCount=0
    for x in self.gradeSheet:
      output.write(x[0] + " (" + str(x[1]) + "):\n")
      commentCount = 0
      appliedComments = ast.literal_eval(str(self.gradeSheet[studentCount][2]))
      for c in self.comments:
        if appliedComments != None and commentCount in appliedComments:
          output.write("(-" + c[1] + ") " + c[0])
          output.write("\n")
        commentCount+=1
      studentCount+=1
      output.write("\n")
    output.close()

  def setGradeSheet(self, gs):
    self.gradeSheet = gs

  def getGradeSheet(self):
    return self.gradeSheet
  
  def setComments(self, c):
    self.comments = c
  
  def getComments(self):
    return self.comments
    
  def addComment(self, note, value):
    t = [note, value]
    self.comments.append(list(t))
  
  def deleteComment(self, index):
    del self.comments[index]

  def newSheet(self):
    self.gradeSheet = []

if __name__ == "__main__":
  model = Model()
