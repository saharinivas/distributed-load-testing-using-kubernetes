from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange
import json
import random

#constants

#functions

#Declarations
headers = {
    'Content-Type':'application/json',
    'connection':'keep-alive',
    'Accept':'*/*',
             }
     
#Payload Values       
body = {}

class MyTaskSequence(TaskSequence):

    @seq_task(1)
    def Healthcheck(self):
    
        response = self.client.get(url = "/healthcheck",name="Healthcheck",data=body, headers=headers)
       
    @seq_task(2)
    def GetPercentageConnections(self):
    
        grade = random.randint(1,12)
    
        response = self.client.get(url = f"/percentage-connections/?grade={grade}&goal=CBSE",name="GetPercentageConnections",data=body, headers=headers)
        
    @seq_task(3)
    def GetKeyRelations(self):
    
        fromgrade = random.randint(1,6)
        tograde = random.randint(7,12)
        
        response = self.client.get(url = f"/key-relations/?from_goal=CBSE&to_goal=CBSE&from_grade={fromgrade}&to_grade={tograde}&level=concept",name="GetKeyRelations",data=body, headers=headers)
   
        
class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
