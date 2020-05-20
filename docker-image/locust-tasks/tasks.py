from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange
import json
import csv

#constants
global_searches = []
fiber_searches = []

#functions
#with open('/locust-tasks/globalsearch_queries.csv','r') as file:
    #global_searches = file.read().split(",")
    
with open('/locust-tasks/fibersearch_queries.csv','r') as file:
    fiber_searches = file.read().split(",")

#Declarations
headers = {}
     
#Payload Values       
body = {}

class MyTaskSequence(TaskSequence):
      
    # @seq_task(1)
    # def GlobalSearch(self):
        # global_search = global_searches[randrange(len(global_searches)-1)]

        # response = self.client.get(url =f"/dsl/gs_ms/search?consumer=tech&query={global_search}",name="GlobalSearch", data=body, headers=headers)
        # logging.info('Response for API 1 is %s',response.json())
        
    @seq_task(1)
    def QuickLink_Search(self):
        fiber_search = fiber_searches[randrange(len(fiber_searches)-1)]

        response = self.client.get(url = f"/fs_ms/quicklink?query={fiber_search}&user_id=1&start=0&size=10&grade=10",name="QuickLink_Search", data=body, headers=headers)
        
    @seq_task(2)
    def FiberSearch(self): 
        fiber_search = fiber_searches[randrange(len(fiber_searches)-1)]
        
        response = self.client.get(url = f"/fs_ms/search?query={fiber_search}&user_id=1&start=0&size=10&grade=10",name="FiberSearch", data=body, headers=headers)
       
class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
