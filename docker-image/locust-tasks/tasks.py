from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange
import json


#constants
cookies = {}
syllabus_data = {}
answer_data = {}
user_emails = []
headers = {
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json;charset=UTF-8',
}

#/locust-tasks/

#functions 
with open('user_emails.txt','r') as file:
    user_emails = file.read().split(",")


class MyTaskSequence(TaskSequence):

    @seq_task(1)
    def login_funtoot(self):
        
        user_email = user_emails[randrange(len(user_emails)-1)]
        
        login_data = {
            "UserName": user_email,
            "Password": 'funtoot'
        }
        
        response = self.client.post(url="/api/Account/Login", data=json.dumps(login_data), auth=None,headers=headers)
        cookies['.ASPXAUTH'] = response.cookies['.ASPXAUTH']
        cookies['LogId'] = response.cookies['LogId']
        
    @seq_task(2)
    def profile_funtoot(self):
        response = self.client.get(url="/api/Account/GetProfile", auth=None,headers=headers, cookies=cookies)

    @seq_task(3)
    def get_usage_funtoot(self):
        response = self.client.get(url="/api/Student/GetUsage", auth=None,headers=headers, cookies=cookies)

    @seq_task(4)
    def get_syllabus_funtoot(self):
        response = self.client.get(url="/api/Syllabus/Get", auth=None,headers=headers, cookies=cookies)
        syllabus_data['data'] = response.json()['Content'][0]['Children'][0]['Children'][0]

    @seq_task(5)
    def get_problem_funtoot(self):
        response = self.client.post(url="/api/Problem/Generate", data=json.dumps(syllabus_data['data']), auth=None,headers=headers, cookies=cookies)
        answer_data['data'] = response.json()

    @seq_task(6)
    def get_solution_funtoot(self):
        response = self.client.post(url="/api/Problem/Evaluate", data=json.dumps(answer_data['data']), auth=None,headers=headers, cookies=cookies)
        


class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
