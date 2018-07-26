import sys
import tkinter as tk
import xml.sax
import xmlCollector

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

  def generateDefaultSheet(self, numberRows, numberCols):
    for col in range(numberCols):
      self.columnNames.append('Column '+str(col))
    for row in range(numberRows):
      t = ['Name '+str(row)]
      for col in range(numberCols):
        t.append('('+str(row)+', '+str(col)+')')
      self.gradeSheet.append( list(t) )

  def setGradeSheet(self, gs):
    self.gradeSheet = gs

  def getGradeSheet(self):
    return self.gradeSheet
  
  def setComments(self, c):
    self.comments = c
  
  def getComments(self):
    return self.comments
    
  def addComment(self, value, note):
    t = [note, value]
    self.comments.append(list(t))
  
  def newSheet(self):
    self.gradeSheet = []

if __name__ == "__main__":
  model = Model()
