from locust import HttpUser,task,between
from random import randrange
import json
import random
import csv

#constants
query_params = []

#functions
with open('/locust-tasks/Mobile_User.csv', 'r') as csvfile:
        query_params = list (csv.reader(csvfile, delimiter=','))
        
#Declarations
headers = {
    'Content-Type': 'multipart/form-data',
          }
     
#Payload Values       

class UserBehaviour(HttpUser):
    wait_time = between(1, 3)
    host = "https://preprodms.embibe.com"

    @task
    def Login(self):
    
        rnum = randrange(len(query_params)-1)
    
        payload = {'pack_type': 'PACK-NTA',
                   'user[login]': query_params[rnum][0],
                   'user[password]': query_params[rnum][1],
                   'app_id': 'NTA--SandwichApp'
                  }
                  
        files = [

                ]
    
         
        response = self.client.post(url = "/user_auth/mobile/sandwich_app/login",name="Login",data=payload, headers=headers,files=files)
         if (response.status_code!=200):
                print(response.content)

