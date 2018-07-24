#!/usr/bin/python
# This SAX parser will read a Malloy Grade sheet, storing the column
# names, student names, and grades in a corresponding data structure.

import sys
import xml.sax
import collections

class XmlCollector( xml.sax.ContentHandler ):
  """Custom xml.sax.ContentHandler"""

  def __init__(self):
    xml.sax.ContentHandler.__init__(self)
    self.columnNames = []
    # It's easier here to use an OrderedDict, which is a 
    # dictionary that maintains the original order.
    # I convert it to a list when getGradeSheet is called:
    self.students = collections.OrderedDict()
    self.currentStudentName = None
    self.columnNameFound = False
    self.nameFound = False
    self.gradeFound = False
    self.hashFound = False

  def getGradeSheet(self):
    ''' Looks like I'm turning the OrderedDict into a List: '''
    L = []
    t = []
    for x in self.students:
      t = [x]+self.students[x]
      L.append(t)
    return L

  def getStudents(self):
    return self.students

  def getColumnNames(self):
    return self.columnNames

  def startElement( self, name, attributes ):
    if name == 'ColumnName':
      self.columnNameFound = True
    elif name == 'Name':
      self.nameFound = True
    elif name == 'grade':
      self.gradeFound = True
    elif name == 'Hash':
      self.hashFound = True

  def endElement( self, name ) :
    self.columnNameFound = False
    self.nameFound = False
    self.gradeFound = False

  def characters( self, content ) :
    # strip only removes spaces!
    content = content.strip()
    content = str(content)  # convert unicode to ascii
    if content: 
      if self.columnNameFound:
        self.columnNames.append(content)
      elif self.nameFound:
        self.students[content] = []
        self.currentStudentName = content
      elif self.gradeFound:
        self.students[self.currentStudentName].append(content)
      elif self.hashFound:
        self.students[self.currentStudentName].append(content)

def main(filename):
  try:
    parser = xml.sax.make_parser()
    collector = XmlCollector()
    parser.setContentHandler( collector )
    parser.parse(filename)
    columnNames = collector.getColumnNames()
    print ('Column names:', columnNames)
    print (collector.getGradeSheet())
  except (IOError):
    print ("Error reading file")
  except (xml.sax.SAXParseException):
    print ("Error parsing file")

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print ("usage:", sys.argv[0], "<xml file>")
    sys.exit()
  main(sys.argv[1])
