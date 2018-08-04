import sys
import model
import unittest
import gradesheet

class TestModel(unittest.TestCase):

  def setUp(self):
    self.model = model.Model()

  def testSetGradeSheet(self):
    self.model.setGradeSheet([[0,1,2],[3,4,5],[6,7,8]])
    self.assertEqual([[0,1,2],[3,4,5],[6,7,8]], self.model.getGradeSheet())

  def testNewSheet(self):
    self.model.setGradeSheet([[0,0,0],[1,1,1],[2,2,2]])
    self.assertEqual([[0,0,0],[1,1,1],[2,2,2]], self.model.getGradeSheet())
    self.model.newSheet()
    self.assertEqual([], self.model.getGradeSheet())

  def testAddComment(self):
    self.model.addComment("comment 1", 5)
    comm = self.model.getComments()
    self.assertEqual(comm[0][0], "comment 1")
    self.assertEqual(comm[0][1], 5)
    
    
  def testDeleteComment(self):
    self.model.addComment("comment 1", 5)
    self.model.addComment("comment 2", 10)
    self.model.addComment("comment 3", 1)
    comm = self.model.getComments()
    self.assertEqual(comm, [["comment 1", 5], ["comment 2", 10], ["comment 3", 1]])
    self.model.deleteComment(1)
    comm = self.model.getComments()
    self.assertEqual(comm, [["comment 1", 5], ["comment 3", 1]])
  
  def testSetComments(self):
    comms = [["comment 1", 5], ["comment 2", 10], ["comment 3", 1]]
    self.model.setComments(comms)
    self.assertEqual(self.model.getComments(), [["comment 1", 5], ["comment 2", 10], ["comment 3", 1]])
    
if __name__=="__main__":
  unittest.main()
