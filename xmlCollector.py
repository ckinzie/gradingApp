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
    self.names = []
    self.grades = []
    self.comments = []
    self.partners = []
    
    self.students = collections.OrderedDict()
    self.currentStudentName = None
    self.nameFound = False
    self.gradeFound = False
    self.commentsFound = False
    self.partnerFound = False

  def getGradeSheet(self):
    L = []
    t = []
    for x in self.students:
      t = [x]+self.students[x]
      L.append(t)
    return L

  def getStudents(self):
    return self.students

  def startElement( self, name, attributes ):
    if name == 'Last':
      self.nameFound = True
    elif name == 'Grade':
      self.gradeFound = True
    elif name == 'Comments':
      self.commentsFound = True
    elif name == 'Partner':
      self.partnerFound = True

  def endElement( self, name ) :
    self.nameFound = False
    self.gradeFound = False
    self.commentsFound = False
    self.partnerFound = False

  def characters( self, content ) :
    # strip only removes spaces!
    content = content.strip()
    content = str(content)  # convert unicode to ascii
    if content: 
      if self.nameFound:
        self.students[content] = []
        self.currentStudentName = content
      elif self.gradeFound:
        self.students[self.currentStudentName].append(content)
      elif self.commentsFound:
        self.students[self.currentStudentName].append(content)
      elif self.partnerFound:
        self.students[self.currentStudentName].append(content)

def main(filename):
  try:
    parser = xml.sax.make_parser()
    collector = XmlCollector()
    parser.setContentHandler( collector )
    parser.parse(filename)
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
