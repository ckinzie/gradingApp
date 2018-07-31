import sys, os
import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
import gradesheet
import ast

GEOMETRY = '1060x640+200+10'
WIDTH=120
HEIGHT=19

class NotAController:
  def dummy(self): print("dummy button")

class View:
  def __init__(self, controller, sheet):
    self.controller = controller
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
    filemenu.add_command(label="New", command=self.newSheet)
    filemenu.add_command(label="Open", command=self.loadGrades)
    filemenu.add_separator()
    filemenu.add_command(label="Save", command=self.saveGrades)
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
    helpmenu.add_command(label="About", command=self.about)
    menubar.add_cascade(label="Help", menu=helpmenu)
          
    root.config(menu=menubar)
    
    #Building the table
    self.gradesheet = gradesheet.GradeSheet(root, self, self.gradeSheet, width=144, height=30, wrap="none") 
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
    
    #Manage Students button
    button = tk.Button(buttonFrame, text="Manage Students", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.manageStudentsPopup)
    button.pack(side=tk.LEFT)
    #Manage Comments button
    button = tk.Button(buttonFrame, text="Manage Comments", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.manageCommentsPopup)
    button.pack(side=tk.LEFT)
    #Add Tab button
    button = tk.Button(buttonFrame, text="Add Tab", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.controller.dummy)
    button.pack(side=tk.LEFT)
    #Export button
    button = tk.Button(buttonFrame, text="Export as .txt", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#ff0000", command=self.controller.exportAsTxt)
    button.pack(side=tk.LEFT)
    
    self.namelabel = tk.Label(buttonFrame, text=self.filename, width=15, relief=tk.SUNKEN) 
    self.namelabel.config(padx=2, pady=2, bd=2, bg="#ffffff")
    self.namelabel.pack(side=tk.RIGHT)
  #Window for adding/removing comments from the table
  def manageCommentsPopup(self):
    t = tk.Toplevel()
    t.title("Manage Comments")
    
    scrollbar = tk.Scrollbar(t)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.commentslistbox = tk.Listbox(t, selectmode=tk.SINGLE)
    self.commentslistbox.pack(side="top", fill="both", expand=True)
    
    comments = self.controller.getComments()
    for c in comments:
      self.commentslistbox.insert(tk.END, ("(-" + c[1] + ") " + c[0]))
       
    buttonFrame = tk.Frame(t)
    buttonFrame.config(height=HEIGHT, padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#000000')
    buttonFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
    button = tk.Button(buttonFrame, text="Add Comment", width=12) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.addCommentPopup)
    button.pack(side=tk.LEFT)
    
    button = tk.Button(buttonFrame, text="Delete Comment", width=12, command=lambda: self.confirmDelete(self.deleteComment, self.commentslistbox.get(self.commentslistbox.curselection())))
    button.config(padx=5, pady=5, bd=5, bg="#ff0000")
    button.pack(side=tk.LEFT)
    
    button = tk.Button(buttonFrame, text="Exit", width=10) 
    button.config(padx=5, pady=5, bd=5, bg="#ff0000", command=t.destroy)
    button.pack(side=tk.RIGHT)
    
    self.commentslistbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=self.commentslistbox.yview)
    
  def addCommentPopup(self):
    t = tk.Toplevel()
    t.title("Add Student")
    
    ventry = tk.StringVar()
    nentry = tk.StringVar()
    
    value = tk.Label(t, text = "Value:")
    value.pack(side=tk.LEFT, fill="both", expand=True)
    
    valueentry = tk.Entry(t, textvariable = ventry, width=3)
    valueentry.focus_set()
    valueentry.pack(side=tk.LEFT, fill="both", expand=True)
    
    note = tk.Label(t, text = "Comment:")
    note.pack(side=tk.LEFT, fill="both", expand=True)
    
    noteentry = tk.Entry(t, textvariable = nentry)
    noteentry.pack(side=tk.LEFT, fill="both", expand=True)
    
    button = tk.Button(t, text="Enter", width=10) 
    button.config(padx=5, pady=5, bd=5, bg="#ff0000", command=lambda: addComment(ventry.get(), nentry.get()))
    button.pack(side=tk.BOTTOM)
    
    def addComment(value, note):
      comment = "(-" + value + ") " + note
      self.controller.addComment(value, note)
      self.gradeSheet = self.gradesheet.getGradeSheet()
      self.commentslistbox.insert(tk.END, comment)
      t.destroy()
   
  def deleteComment(self):
    comment = self.commentslistbox.curselection()[0]
    self.commentslistbox.delete(self.commentslistbox.curselection())
    self.controller.deleteComment(comment)
    self.t.destroy()
    
  #Window for applying comments to a specific grade
  def applyCommentsPopup(self, index):
    t = tk.Toplevel()
    t.title("Apply Comments")
    appliedComments = ast.literal_eval(str(self.gradeSheet[index][2]))
    
    chkboxFrame = tk.Frame(t)
    chkboxFrame.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#000000')
    comments = self.controller.getComments()
    variables = []
    
    count = 0
    for c in comments:
      self.var = tk.IntVar(value=0)
      chkbutton = tk.Checkbutton(chkboxFrame, text="(-" + c[1] + ") " + c[0], variable=self.var)
      if appliedComments != None and count in appliedComments:
        self.var = tk.IntVar(value=1)
        chkbutton.config(variable = self.var)
      chkbutton.pack(side=tk.TOP, fill = tk.BOTH)
      variables.append(self.var)
      count+=1
    
    chkboxFrame.pack(side=tk.TOP, fill=tk.BOTH)
       
    buttonFrame = tk.Frame(t)
    buttonFrame.config(height=HEIGHT, padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#000000')
    buttonFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
    def updateComments():
      count = 0
      c = []
      for var in variables:
        if (var.get() == 1):
          c.append(count)
        count+=1
      self.gradeSheet[index][2] = c
      self.updateGrade(index)
      self.newView(self.gradeSheet)
      t.destroy()
    
    button = tk.Button(buttonFrame, text="Apply", width=10) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=updateComments)
    button.pack(side=tk.LEFT)
    
    button = tk.Button(buttonFrame, text="Exit", width=10) 
    button.config(padx=5, pady=5, bd=5, bg="#ff0000", command=t.destroy)
    button.pack(side=tk.RIGHT)
    
  def updateGrade(self, index):
    appliedComments = ast.literal_eval(str(self.gradeSheet[index][2]))
    comments = self.controller.getComments()
    
    count = 0
    grade = 100
    for c in comments:
      if count in appliedComments:
        grade -= int(c[1])
      count+=1
    self.gradeSheet[index][1] = grade
    
      
  #Window for adding/removing students from the table
  def manageStudentsPopup(self):
    t = tk.Toplevel()
    t.title("Manage Students")
    
    scrollbar = tk.Scrollbar(t)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.studentlistbox = tk.Listbox(t, selectmode=tk.SINGLE)
    self.studentlistbox.pack(side="top", fill="both", expand=True)
    
    students = self.controller.getStudents()
    for s in students:
      self.studentlistbox.insert(tk.END, s)
       
    buttonFrame = tk.Frame(t)
    buttonFrame.config(height=HEIGHT, padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#000000')
    buttonFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
    button = tk.Button(buttonFrame, text="Add Student", width=12) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.addStudentPopup)
    button.pack(side=tk.LEFT)
    
    button = tk.Button(buttonFrame, text="Delete Student", width=12, command=lambda: self.confirmDelete(self.deleteStudent, self.studentlistbox.get(self.studentlistbox.curselection())))
    button.config(padx=5, pady=5, bd=5, bg="#ff0000")
    button.pack(side=tk.LEFT)
    
    button = tk.Button(buttonFrame, text="Exit", width=10) 
    button.config(padx=5, pady=5, bd=5, bg="#ff0000", command=t.destroy)
    button.pack(side=tk.RIGHT)
    
    self.studentlistbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=self.studentlistbox.yview)
  
  def addStudentPopup(self):
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
      name = last + ", " + first
      self.gradesheet.addStudent(name)
      self.gradeSheet = self.gradesheet.getGradeSheet()
      self.controller.updateRoster(self.gradeSheet)
      self.studentlistbox.insert(tk.END, name)
      t.destroy()
   
  def deleteStudent(self):
    name = self.studentlistbox.get(self.studentlistbox.curselection())
    self.studentlistbox.delete(self.studentlistbox.curselection())
    self.gradesheet.deleteName(name)
    self.t.destroy()
  
  def newView(self, grades):
    self.gradeSheet = grades
    self.gradesheet.eraseSheet()
    self.gradesheet.makeNewSheet(self.gradeSheet)
    
  def loadGrades(self):
    self.filename = filedialog.askopenfilename(initialdir=os.getcwd()+"/coursesDir", filetypes=(("XML File", "*.xml"),("All Files","*.*")), title= "Choose a file")
    if not self.filename:
      return
    gs = self.controller.loadGrades(self.filename)
    if(gs != "Error"):
      self.gradeSheet = gs 
      self.newView(self.gradeSheet)
      self.namelabel.config(text=self.filename.rsplit('/')[-1])
  
  def newSheet(self):
    self.controller.newSheet()
    self.gradeSheet = []
    self.controller.clearFilename()
    self.newView(self.gradeSheet)
    self.namelabel.config(text="New Sheet")
    
  def saveAs(self):
    filename = filedialog.asksaveasfilename(initialdir=os.getcwd()+"/coursesDir", filetypes=(("XML File", "*.xml"),("All Files","*.*")), title= "Choose location to save")
    if not filename:
      return
    self.gradeSheet = self.gradesheet.getGradeSheet()
    self.comments = self.controller.getComments()
    filename = filename.rsplit('.')[0] + ".xml"
    self.controller.saveGradesAs(self.gradeSheet, self.comments, filename)
    self.saveCompleted(filename)
      
  def saveGrades(self):
    if (self.controller.getFilename() == None):
      self.saveAs()
      return
    self.gradeSheet = self.gradesheet.getGradeSheet()
    self.comments = self.controller.getComments()
    self.controller.saveGrades(self.gradeSheet, self.comments)
    filename = self.controller.getFilename()
    self.saveCompleted(filename)
    
  def openFileError(self):
    messagebox.showwarning('ERROR', 'Could not open selected file')
  
  def saveCompleted(self, filename):
    self.filename = filename
    filename = filename.split('/')[-1]
    msg = "Grades saved to: " + filename
    messagebox.showinfo('Success',msg)
    self.namelabel.config(text=self.filename.rsplit('/')[-1])
    
  def exportCompleted(self, filename):
    self.filename = filename
    filename = filename.split('/')[-1]
    msg = "Grades exported to: " + filename
    messagebox.showinfo('Success',msg)
    self.namelabel.config(text=self.filename.rsplit('/')[-1])
    
  def confirmDelete(self, c, item):
    self.t = tk.Toplevel()
    self.t.title("Confirm Deletion")
    label = tk.Label(self.t, text='Are you sure you wish to delete "' + str(item)+'"', width=50, height=5)
    label.pack(side=tk.TOP)
    
    buttonFrame = tk.Frame(self.t)
    buttonFrame.config(height=HEIGHT, padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#000000')
    buttonFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
    confirm = tk.Button(buttonFrame, text="Confirm", width=12)
    confirm.config(padx=5, pady=5, bd=5, bg="#00ff00", command=c)
    confirm.pack(side=tk.LEFT)
    
    deny = tk.Button(buttonFrame, text="Deny", width=12) 
    deny.config(padx=5, pady=5, bd=5, bg="#ff0000", command=self.t.destroy)
    deny.pack(side=tk.RIGHT)
      
  def about(self):
    messagebox.showinfo("About", "This app was created by Connor Kinzie for CPSC 8700 at Clemson University taught by Dr. Brian Malloy on August 3rd, 2018. For questions, contact ckinzie@clemson.edu\n\n" + "This app calculates and stores grades for students. You can add students to a new page through the 'Manage Students' button. To create a list of comments, use the 'Manage Comments' button. Each comment must have an number value and an accompanying note. The program will calculate each students' grade by deducting applied comments from their max score. To assign comments to a student, click on the 'Comments' cell for that specific student and check the comments you wish to apply. Their grade will automatically be updated. You can also export a .txt file with students, grades, and applied comments with the 'Export as .txt' button.")

if __name__ == "__main__":
  view = View(NotAController())
  view.root.mainloop()
