from locust import HttpLocust, TaskSet, TaskSequence, seq_task, between
from random import randrange
import json
import csv

#constants
email_password = []

#functions
with open('/locust-tasks/Dummy.csv', 'r') as csvfile:
        email_password = list (csv.reader(csvfile, delimiter=','))

#Declarations
headers = {
    'Connection':'keep-alive',
    'Accept':'application/json, text/plain,*/*',
    'Content-Type':'application/json;charset=UTF-8'
}
#Payload Values
body = {}
code={'code':''}
exam_code={'exam_code':''}

class MyTaskSequence(TaskSequence):

    @seq_task(1)
    def Login(self):
        rnum = randrange(len(email_password)-1)
        login_data={
                    "login":email_password[rnum][0],
                    "password":email_password[rnum][1],
                    "password_confirmation":email_password[rnum][1]
                   }
        response = self.client.post(url = "/user_ms/auth/sign_in",name="Login",data=json.dumps(login_data), headers=headers)
        headers['embibe-token']= response.headers['embibe-token']
        
    @seq_task(2)
    def Search(self):
        response = self.client.get(url = "/horizontal_ms/v1/embibe/en/global_search?query=Indefinite+Integration&start=0&size=10&goal_code=gl8",name="Search",data=body, headers=headers)
        code['code'] = response.json().get("code","ch264")
        
    @seq_task(3)
    def LearnCode(self):
        response = self.client.get(url = f"/content_ms/v1/embibe/en/learn?learn_path=indefinite-integration-chapter&entity_code={code['code']}",name="Learn_Code",data=body, headers=headers)
        exam_code['exam_code'] = response.json().get("exam_code","ex4")
        
    @seq_task(4)
    def BehaviorMeter(self):
        response = self.client.get(url = f"/horizontal_ms/v1/embibe/en/behavior-meter?content_code={code['code']}&content_type=chapter&exam_code={exam_code['exam_code']}",name="Behavior_Meter",data=body, headers=headers)

    @seq_task(5)
    def Test_Status(self):

        status_data = "{\"test_xpaths\":{\"/jee-main/chapterwise-test/mathematics/indefinite-integration\":\"engineering\"},\"practice_xpaths\":{}}"
        response = self.client.post(url = "/horizontal_ms/v1/embibe/en/test_and_practice_stats",name="Test_Status",data=status_data,headers=headers)

    @seq_task(6)
    def Social_Analytics(self):
        response = self.client.get(url = f"/horizontal_ms/v1/embibe/en/social-analytics?content_code={code['code']}&content_type=chapter&exam_code={exam_code['exam_code']}",name="Social_Analytics",data=body, headers=headers)

    @seq_task(7)
    def Find_Children(self):
        response = self.client.get(url = f"/content_ms/v1/embibe/en/learn/chapter/{code['code']}/children",name="Find_Children",data=body, headers=headers)

class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
