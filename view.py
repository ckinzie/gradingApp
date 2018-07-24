import sys, os
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
import gradesheet

GEOMETRY = '1060x640+200+10'
WIDTH=120
HEIGHT=19

class NotAController:
  def addStudent(self): self.model.addStudent("John", "Doe")
  def getCount(self): return self.model.getCount
  def dummy(self): print("dummy button")

class View:
  def __init__(self, controller, colNames, sheet):
    self.controller = controller
    self.columnNames = colNames
    self.gradeSheet = sheet
    root = tk.Tk()
    root.title('Grader')
    root.geometry(GEOMETRY)
    
    self.filename='New Sheet'
    self.boxFont = ('symbol', 14)
    
    #Creating top menu bar
    menubar = Menu(root)
    #File menu
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=self.controller.dummy)
    filemenu.add_command(label="Open", command=self.loadGrades)#self.openFile
    filemenu.add_separator()
    filemenu.add_command(label="Save", command=self.controller.dummy)
    filemenu.add_command(label="Save As", command=self.saveAs)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    #Edit menu
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Preferences", command=self.controller.dummy)
    editmenu.add_command(label="Add Tab", command=self.controller.dummy)
    editmenu.add_command(label="Delete Tab", command=self.controller.dummy)
    menubar.add_cascade(label="Edit", menu=editmenu)
    #View menu
    viewmenu = Menu(menubar, tearoff=0)
    viewmenu.add_command(label="Color Scheme", command=self.controller.dummy)
    menubar.add_cascade(label="View", menu=viewmenu)
    #Help menu
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=self.controller.dummy)
    menubar.add_cascade(label="Help", menu=helpmenu)
          
    root.config(menu=menubar)
    
    #Building the table
    self.gradesheet = gradesheet.GradeSheet(root, self, self.columnNames, self.gradeSheet, width=100, height=20, wrap="none") 
    if len(self.gradeSheet) == 0:
      self.gradesheet.eraseSheet()
    else:
      dirPath = sys.argv[1]
      tempName = dirPath.split(os.sep)
      tempName = tempName[-1]
      tempName = tempName.split('.')
      self.gradeLabel.config(text = tempName[-2], fg='#0000ff', font=self.myFont)

    #Frame to hold the bottom buttons
    buttonFrame = tk.Frame(root)
    buttonFrame.config(height=HEIGHT, padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#000000')
    buttonFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
    #Update Students button
    button = tk.Button(buttonFrame, text="Update Students", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.updateStudentsPopup)
    button.pack(side=tk.LEFT)
    #Update Comments button
    button = tk.Button(buttonFrame, text="Update Comments", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.controller.dummy)
    button.pack(side=tk.LEFT)
    #Add Tab button
    button = tk.Button(buttonFrame, text="Add Tab", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.controller.dummy)
    button.pack(side=tk.LEFT)
    #Export button
    button = tk.Button(buttonFrame, text="Export as .txt", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#ff0000", command=self.controller.dummy)
    button.pack(side=tk.LEFT)
    
    self.namelabel = tk.Label(buttonFrame, text=self.filename, width=15, relief=tk.SUNKEN) 
    self.namelabel.config(padx=2, pady=2, bd=2, bg="#ffffff")
    self.namelabel.pack(side=tk.RIGHT)

#Window for adding/removing students from the table
  def updateStudentsPopup(self):
    t = tk.Toplevel()
    t.title("Add Student")
    
    fentry = tk.StringVar()
    lentry = tk.StringVar()
    
    first = tk.Label(t, text = "First name:")
    first.pack(side=tk.LEFT, fill="both", expand=True)
    
    firstentry = tk.Entry(t, textvariable = fentry)
    firstentry.focus_set()
    firstentry.pack(side=tk.LEFT, fill="both", expand=True)
    
    last = tk.Label(t, text = "Last name:")
    last.pack(side=tk.LEFT, fill="both", expand=True)
    
    lastentry = tk.Entry(t, textvariable = lentry)
    lastentry.pack(side=tk.LEFT, fill="both", expand=True)
    
    button = tk.Button(t, text="Enter", width=10) 
    button.config(padx=5, pady=5, bd=5, bg="#ff0000", command=lambda: addStudent(fentry.get(), lentry.get()))
    button.pack(side=tk.BOTTOM)
    
    def addStudent(first, last):  
      self.controller.addStudent(first, last)
      val = self.controller.getCount()
      if(val > 0):
        for y in range(0,5):
          if(y==0):
            txt = first
          elif(y==1):
            txt = last
          elif(y==2):
            txt = 100
          elif(y==3):
            txt = "Blank"
          elif(y==4):
            txt = "Blank"
          cell=tk.Label(self.tableframe, text=txt, fg='black', bg='white', width=10, bd=2, relief=tk.SUNKEN)
          cell.grid(row=val+1,column=y)
      t.destroy() 
  
  def newView(self, columns, grades):
    self.columnNames = columns
    self.gradeSheet = grades
    self.gradesheet.eraseSheet()
    self.gradesheet.makeNewSheet(self.columnNames, self.gradeSheet)
    
  def loadGrades(self):
    self.filename = filedialog.askopenfilename(initialdir=os.getcwd()+"/coursesDir", filetypes=(("XML File", "*.xml"),("All Files","*.*")), title= "Choose a file")
    if not self.filename:
      return
    colNames, gs = self.controller.loadGrades(self.filename)
    if(colNames != "Error"):
      self.columnNames = colNames
      self.gradeSheet = gs 
      self.newView(self.columnNames, self.gradeSheet)
      self.namelabel.config(text=self.filename.rsplit('/')[-1])
    
  def saveAs(self):
    if len(self.gradeSheet) == 0:
      messagebox.showinfo('Oops!', 'Nothing to save.')
      return
    filename = filedialog.asksaveasfilename(initialdir=os.getcwd()+"/coursesDir", filetypes=(("XML File", "*.xml"),("All Files","*.*")), title= "Choose location to save")
    if not filename:
      return
    self.columnNames, self.gradeSheet = self.gradesheet.getGradeSheet()
    filename = filename.rsplit('.')[0] + ".xml"
    self.controller.saveGradesAs(self.columnNames, self.gradeSheet, filename)
    self.saveCompleted(filename)
      
##########################copied##############################
  def saveGrades(self):
    if len(self.gradeSheet) == 0:
      messagebox.showinfo('Oops!', 'Nothing to save.')
      return
    self.columnNames, self.gradeSheet = self.gradesheet.getGradeSheet() 
    self.controller.saveGrades(self.columnNames, self.gradeSheet)
    filename = self.controller.getFilename()
    self.saveCompleted(filename)
################################################################
    
  def openFileError(self):
    messagebox.showwarning('ERROR', 'Could not open selected file')
  
  def saveCompleted(self, filename):
    self.filename = filename
    filename = filename.split('/')[-1]
    msg = "Grades saved to: " + filename
    messagebox.showinfo('Success',msg)
    self.namelabel.config(text=self.filename.rsplit('/')[-1])

if __name__ == "__main__":
  view = View(NotAController())
  view.root.mainloop()
