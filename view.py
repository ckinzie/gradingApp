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
    tableframe = tk.Frame(root)
    tableframe.pack(side=tk.TOP, fill=tk.X)
    
    last=tk.Label(tableframe, text='LAST', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    last.grid(row=0,column=0)
    first=tk.Label(tableframe, text='FIRST', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    first.grid(row=0,column=1)
    grade=tk.Label(tableframe, text='GRADE', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    grade.grid(row=0,column=2)
    comments=tk.Label(tableframe, text='COMMENTS', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    comments.grid(row=0,column=3)
    partner=tk.Label(tableframe, text='PARTNER', fg='black', bg='#66a0ff', width=10, bd=2, relief=tk.SUNKEN)
    partner.grid(row=0,column=4)

    val = self.controller.getCount()
    if(val > 0):
      for x in range(1,val):
        for y in range(0,5):
          cell=tk.Label(tableframe, text='BLANK', fg='black', bg='white', width=10, bd=2, relief=tk.SUNKEN)
          cell.grid(row=x,column=y)

    #Frame to hold the bottom buttons
    buttonFrame = tk.Frame(root)
    buttonFrame.config(padx=5, pady=5, bd=5, relief=tk.RAISED, bg='#000000')
    buttonFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
    #Update Students button
    button = tk.Button(buttonFrame, text="Update Students", width=15) 
    button.config(padx=5, pady=5, bd=5, bg="#00ff00", command=self.controller.addStudent)
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

if __name__ == "__main__":
  view = View(NotAController())
  view.root.mainloop()
