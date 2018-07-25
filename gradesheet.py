import sys, os
import tkinter as tk
from tkinter import messagebox
from tkinter import font

NAME_WIDTH = 17
HEADER_WIDTH = 15

class GradeSheet(object): 
  def __init__(self, parent, theView, gs, **keywords): 
    self.parent = parent
    self.myView = theView
    self.columnNames = ["Last Name", "First Name", "Grade", "Comments", "Partner"]
    self.gradeSheet = gs

    # self.gradesVarList is a list of the StringVar's in the Entry boxes
    # These StringVars will be updated for each change in the Entry box
    self.columnVarList = []
    self.gradesVarList = []
    self.namesVarList = []

    # Set some defaults 
    if "width" not in keywords: keywords["width"]=24 
    if "bg" not in keywords: keywords["bg"]="white" 
    if "relief" not in keywords: keywords["relief"]="sunken" 

    self.gradeSheetFrame = tk.Frame(self.parent, bd=5)
    self.gradeSheetFrame.pack(side=tk.TOP, padx=5, pady=5)

    self.headFrame = tk.Frame(self.gradeSheetFrame) 
    self.headFrame.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH) 

    # Adding column headers
    self.headText = tk.Text(self.headFrame, width=24, height=1)
    
    # If wrap isn't set to NONE, the scrollbar won't work
    # because there's nothing to scroll!
    self.headText.config(wrap=tk.NONE)
    dscrollbar = tk.Scrollbar(self.headFrame, orient=tk.VERTICAL) 
    dscrollbar.config(command=self.headText.yview) 
    dscrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
    self.headText.config(yscrollcommand=dscrollbar.set) 
    self.makeHeader()

    self.gradeFrame = tk.Frame(self.gradeSheetFrame) 
    self.gradeFrame.config(bg=keywords["bg"]) 
    self.gradeFrame.pack(side=tk.RIGHT, expand=tk.TRUE, fill=tk.BOTH) 

    # Create the two Scrollbars for the grades, and for the
    # horizontal column header, and the vertical name column
    vscrollbar = tk.Scrollbar(self.gradeFrame, orient=tk.VERTICAL) 
    hscrollbar = tk.Scrollbar(self.gradeFrame, orient=tk.HORIZONTAL) 
    self.headText.config( xscrollcommand=hscrollbar.set )

    # Create the Text widget that  will contain the grades 
    self.gradeText=tk.Text(self.gradeFrame, 
      yscrollcommand=vscrollbar.set, 
      xscrollcommand=hscrollbar.set, **keywords) 
    self.gradeText.config(wrap=tk.NONE)
    vscrollbar.config(command=self.gradeText.yview) 
    hscrollbar.config(command=self.gradeText.xview) 
    self.gradeText.bind_all("<Button-4>", self.onMousewheel)
    self.gradeText.bind_all("<Button-5>", self.onMousewheel)

    # First pack the scrollbars
    vscrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
    hscrollbar.pack(side=tk.BOTTOM, fill=tk.X) 
    # And then pack the Text boxes
    self.headText.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
    self.gradeText.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 

    self.makeSheet()

  def eraseView(self):
    self.gradeText.delete("1.0", tk.END)
    self.gradeText.config(state=tk.DISABLED)

  def makeSheetNormal(self):
    self.headText.config(state=tk.NORMAL)
    self.gradeText.config(state=tk.NORMAL)

  def makeSheetDisabled(self):
    self.headText.config(state=tk.DISABLED)
    self.gradeText.config(state=tk.DISABLED)

  def eraseSheet(self):
    self.makeSheetNormal()
    self.gradeSheet = []
    self.columnVarList = []
    self.gradesVarList = []
    self.namesVarList = []
    self.eraseView()
    self.makeSheetDisabled()
    
  def addStudent(self):
    self.makeSheetNormal()
    tempVars = []
    self.gradeSheet = self.getGradeSheet()
    L = list(self.gradeSheet[0])
    L[0] = 'name'
    sv = tk.StringVar()
    sv.set(L[0])
    tempVars.append(sv)
    count = 1
    while count < len(L):
      L[count] = '0'
      sv = tk.StringVar()
      sv.set(L[count])
      tempVars.append(sv)
      count += 1
    self.gradesVarList.insert(0, tempVars)
    self.gradeSheet.insert(0, L)
    self.eraseView()
    self.makeNewSheet(self.gradeSheet)
    self.makeSheetDisabled()

  def sortNames(self):
    self.makeSheetNormal()
    self.eraseView()
    # Not so fast: first: getGradeSheet, then sort, 
    # then use makeNewSheet to make a new gradeVars 
    # (old one is out of order)
    self.gradeSheet = self.getGradeSheet()
    self.gradeSheet.sort()
    self.makeNewSheet(self.gradeSheet)
    self.makeSheetDisabled()

  def makeNewSheet(self, sheet):
    self.makeSheetNormal()
    self.gradeSheet = sheet
    self.makeNames()
    self.makeSheet()
    self.makeSheetDisabled()

  def xview(self, *args):
    apply(self.gradeText.xview, args)
    apply(self.headText.xview, args)

  def yview(self, *args):
    apply(self.gradeText.yview, args)
    apply(self.headText.yview, args)

  def onMousewheel(self, event):
    direction = 0
    if event.num == 5: direction = 1
    if event.num == 4: direction = -1
    self.gradeText.yview_scroll(direction, "units")

  def makeHeader(self):
    self.columnVarList = []
    for col in self.columnNames: 
      sv = tk.StringVar()
      sv.set(col)
      self.columnVarList.append(sv)
      x=tk.Label(self.headText, textvariable=sv, width=HEADER_WIDTH, relief=tk.SUNKEN) 
      x.config(bg='#ccffcc')
      self.headText.window_create(tk.END, window=x) 

  def printEntry(self, event):
    #print "Value is:", event.widget.get()
    #self.printGradesVarList()
    # Move cursor to next widget:
    event.widget.tk_focusNext().focus()
    return("break")

  def sortColumn(self, event, withNames=False):
    columnName = event.widget.get()
    index = 0
    sum = 0
    for col in self.columnVarList: 
      if col.get() == event.widget.get():
        break
      index += 1
    L = []
    numNonZero = 0
    rowCount = 0
    for row in self.gradesVarList:
      for count in range(0, len(row)): 
        if count == index:
          value = float(row[count].get())
          if value > 0: numNonZero += 1 
          if withNames:
            L.append( (value, self.namesVarList[rowCount].get()) )
          else:
            L.append(value)
          sum += value
      rowCount += 1
    L.sort()
    L.reverse()
    avg = 0
    if numNonZero > 0: avg = sum/numNonZero
    self.printSortedColumn(columnName, L, avg, withNames)

  def printSortedColumn(self, columnName, grades, avg, withNames):
    dirName = self.myView.getGradeLabel()
    dirPath = 'coursesDir'+os.sep+dirName+os.sep+columnName+'.txt'
    outFile = open(dirPath, 'w')
    outFile.write(columnName)
    outFile.write('\n')
    count = 1
    for x in grades:
      if withNames:
        outFile.write('%5d. %-25s %5.2f' % (count,x[1],x[0]))
      else:
        outFile.write('%5d. %5.2f' % (count,x))
      outFile.write('\n')
      count += 1
    outFile.write('Average: '+str(avg))
    outFile.write('\n')
    outFile.close()
    tkMessageBox.showinfo(columnName+' Column Sorted',\
      'Sorted column saved to '+dirPath)

  def printAllNames(self, event):
    if len(self.namesVarList) == 0:
      self.mustLoadSheet()
      return
    columnName = event.widget.get()
    dirName = self.myView.getGradeLabel()
    dirPath = 'coursesDir'+os.sep+dirName+os.sep+'names.txt'
    outFile = open(dirPath, 'w')
    outFile.write('\t   Names\n')
    count = 1
    for name in self.namesVarList:
      outFile.write('%5d. %s' % (count,name.get()))
      outFile.write('\n')
      count += 1
    outFile.close()
    tkMessageBox.showinfo('Names','Names saved to '+dirPath)

  def printName(self, event):
    if len(self.namesVarList) == 0:
      self.mustLoadSheet()
      return
    searchName = event.widget.get()
    count = 1
    for name in self.namesVarList:
      if name.get() == searchName:
        # We fouond the target, now print it:
        print (self.gradeSheet[count-1])
        break
      count += 1
    self.notYet('print '+searchName)

  def deleteName(self, event):
    if len(self.namesVarList) == 0:
      self.mustLoadSheet()
      return
    searchName = event.widget.get()
    count = 1
    for name in self.namesVarList:
      if name.get() == searchName:
        break
      count += 1
    self.makeSheetNormal()
    del self.gradeSheet[count-1]
    self.eraseView()
    self.makeNewSheet(self.gradeSheet)
    self.makeSheetDisabled()
    self.successMessage(searchName, " deleted")

  def makeNames(self):
    self.namesVarList = []
    for row in self.gradeSheet: 
      sv = tk.StringVar()
      sv.set(row[0])
      self.namesVarList.append(sv)
      thisWidth = max(NAME_WIDTH, len(row[0])) 

  def makeSheet(self):
    L = []
    rowParity = True
    for row in self.gradeSheet: 
      rowParity ^= True
      t = []
      for count in range(1, len(row)): 
        sv = tk.StringVar()
        sv.set(row[count])
        t.append(sv)
        x=tk.Label(self.gradeText, textvariable=sv, width=HEADER_WIDTH, relief=tk.SUNKEN) 
        x.bind("<Return>", self.printEntry)
        if rowParity:
          x.config(bg='#ffffcc')
        self.gradeText.window_create(tk.END, window=x) 
      L.append(t)
      if row != self.gradeSheet[-1]:
        self.gradeText.insert(tk.END, "\n") 
    self.gradesVarList = L
    #self.debug()

  def getGradeSheet(self):
    L = []
    count = 0
    for x in self.gradesVarList:
      t = []
      t.append( self.namesVarList[count].get() )
      for y in x:
        t.append( y.get() )
      L.append(t)
      count += 1
    return L

  def mustLoadSheet(self):
    tkMessageBox.showinfo('Oops', 'Must load grades')

  def notYet(self, cmd):
    tkMessageBox.showinfo('Oops', cmd+'\nis not implemented Yet!')

  def successMessage(self, cmd, msg):
    tkMessageBox.showinfo('Success', cmd+'\n'+msg)

  def debug(self):
    print ("PRINTING gradeSheet")
    print (self.columnNames)
    print (self.gradeSheet)
    print ("gradesVarList:")
    self.printGradesVarList()
    print ("DONE")

if __name__ == "__main__":
  root = tk.Tk()
  root.bind('<Escape>', lambda event: root.quit())
  view = GradeSheet(root, [], [])
  root.mainloop()
