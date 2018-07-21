import sys
import tkinter as tk
from tkinter import Menu

GEOMETRY = '1060x640+200+10'
WIDTH=120
HEIGHT=19

class NotAController:
  def addStudent(self): self.model.addStudent("John", "Doe")
  def getCount(self): return self.model.getCount
  def dummy(self): print("dummy button")

class View:
  def __init__(self, controller):
    self.controller = controller
    root = tk.Tk()
    root.title('Grader')
    root.geometry(GEOMETRY)
    
    self.count = 0
    self.boxFont = ('symbol', 14)
    
    #Creating top menu bar
    menubar = Menu(root)
    #File menu
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=self.controller.dummy)
    filemenu.add_command(label="Open", command=self.controller.dummy)
    filemenu.add_separator()
    filemenu.add_command(label="Save", command=self.controller.dummy)
    filemenu.add_command(label="Save As", command=self.controller.dummy)
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
    self.tableframe = tk.Frame(root)
    self.tableframe.pack(side=tk.TOP, fill=tk.X)
    
    last=tk.Label(self.tableframe, text='LAST', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    last.grid(row=0,column=0)
    first=tk.Label(self.tableframe, text='FIRST', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    first.grid(row=0,column=1)
    grade=tk.Label(self.tableframe, text='GRADE', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    grade.grid(row=0,column=2)
    comments=tk.Label(self.tableframe, text='COMMENTS', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    comments.grid(row=0,column=3)
    partner=tk.Label(self.tableframe, text='PARTNER', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    partner.grid(row=0,column=4)

    val = self.controller.getCount()
    if(val > 0):
      for x in range(1,val):
        for y in range(0,5):
          cell=tk.Label(self.tableframe, text='BLANK', fg='black', bg='white', width=10, bd=2, relief=tk.SUNKEN)
          cell.grid(row=x,column=y)

    #Frame to hold the bottom buttons
    buttonFrame = tk.Frame(root)
    buttonFrame.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#000000')
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
    button.config(padx=5, pady=5, bd=5, bg="#ff0000", command=lambda: self.addStudent(fentry.get(), lentry.get()))
    button.pack(side=tk.BOTTOM)
    
  def addStudent(self, first, last):  
    self.controller.addStudent(first, last)
    print(first, last)
    print(self.controller.getCount())
    val = self.controller.getCount()
    if(val > 0):
      for x in range(0,val):
        for y in range(0,5):
          if(y==0):
            txt = first
          elif(y==1):
            txt = last
          elif(y==2):
            txt = "Blank"
          elif(y==3):
            txt = "Blank"
          elif(y==4):
            txt = "Blank"
          cell=tk.Label(self.tableframe, text=txt, fg='black', bg='white', width=10, bd=2, relief=tk.SUNKEN)
          cell.grid(row=x+1,column=y)

if __name__ == "__main__":
  view = View(NotAController())
  view.root.mainloop()
