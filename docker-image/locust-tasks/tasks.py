from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange
import json
import csv

#constants
user_Ids = []

#functions
with open('/locust-tasks/user_Ids.txt','r') as file:
    user_Ids = file.read().split(",")

#Declarations
headers = {
    'Accept':'application/json'
          }
     
#Payload Values       
body = {}

class MyTaskSequence(TaskSequence):
      
    @seq_task(1)
    def DefaultSearch(self):
        user_Id = user_Ids[randrange(len(user_Ids)-1)]
        response = self.client.get(url = "/fs_ms/search?user_id={user_Id}&query=%2A&size=10",name="DefaultSearch", data=body, headers=headers)
        
    @seq_task(2)
    def QuickLink_Search(self): 
        user_Id = user_Ids[randrange(len(user_Ids)-1)]
        response = self.client.get(url = "/fs_ms/quicklink?user_id={user_Id}&query=%2A&size=10",name="QuickLink_Search", data=body, headers=headers)
            
        
class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
