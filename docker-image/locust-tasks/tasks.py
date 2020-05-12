from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange
import json
import csv

#constants
email_password = []
mocktest_bundle_path= "/mock-test/jee-main/full-test/predicted-jee-main-2019-april"


#functions
with open('/locust-tasks/email_password_embibe.csv', 'r') as csvfile:
        email_password = list (csv.reader(csvfile, delimiter=','))

#Declarations
headers = {
    'Connection':'keep-alive',
    'Accept':'application/json, text/plain, */*',
    'Content-Type':'application/json;charset=UTF-8',
          }
     
#Payload Values       
body = {}

class MyTaskSequence(TaskSequence):

    @seq_task(1)
    def login(self):
        rnum = randrange(len(email_password)-1)
       
        login_data={
                    "login":email_password[rnum][0],
                    "password":email_password[rnum][1],
                    "password_confirmation":email_password[rnum][1]
                   }
        response = self.client.post(url = "/user_ms/auth/sign_in",name="Login",data=json.dumps(login_data), headers=headers)
        headers ['embibe-token']= response.headers['embibe-token']
        
    @seq_task(2)
    def Search_Request(self):   

        response = self.client.get(url = "/ask/v1/search?query=&size=10&start=0",name="Search_Request", data=body, headers=headers)
        
    @seq_task(3)
    def Search_AutoComplete(self):   

        response = self.client.get(url = "/ask/v1/autocomplete?query_prefix=as",name="Search_AutoComplete", data=body, headers=headers)
        
    @seq_task(4)
    def Create_Question(self):
       
        question_data= "{\"text\":\"Creating Question\",\"title\":\"Questionu0021\",\"tag\":{},\"ocrUrls\":[]}"

        response = self.client.post(url = "/ask/v1/question",name="Create_Question", data=question_data, headers=headers)
        global question_id 
        question_id = response.json().get("questionId","")
        
    @seq_task(5)
    def Edit_Question(self):
    
        editquestion_data= "{\"text\":\"Editing Question\",\"title\":\"Questionu0021\"}"

        response = self.client.put(url = f"/ask/v1/question/{question_id}",name="Edit_Question", data=editquestion_data, headers=headers)
        
    @seq_task(6)
    def My_Question(self):   

        response = self.client.get(url = "/ask/v1/questions/my-questions?limit=10&offset=0",name="My_Question", data=body, headers=headers)
        
    @seq_task(7)
    def Get_Question(self):   

        response = self.client.get(url = f"/ask/v1/questions?ids={question_id}",name="Get_Question", data=body, headers=headers)
        
    @seq_task(8)
    def View_Question(self):   

        response = self.client.post(url = f"/ask/v1/question/{question_id}/view",name="View_Question", data=body, headers=headers)
        
    @seq_task(9)
    def Like_Question(self):   

        response = self.client.post(url = f"/ask/v1/question/{question_id}/like",name="Like_Question", data=body, headers=headers)
        
    @seq_task(10)
    def UnLike_Question(self):   

        response = self.client.post(url = f"/ask/v1/question/{question_id}/unlike",name="UnLike_Question", data=body, headers=headers)
        
    @seq_task(11)
    def Bookmark_Question(self):   

        response = self.client.post(url = f"/ask/v1/question/{question_id}/bookmark",name="Bookmark_Question", data=body, headers=headers)
        
    @seq_task(12)
    def Delete_Question(self):   

        response = self.client.delete(url = f"/ask/v1/question/{question_id}",name="Delete_Question", data=body, headers=headers)
        
    @seq_task(13)
    def Create_Answer(self):
    
        createanswer_data="{\"questionId\":\"5eb4fbf177f78f27bbc13405\",\"text\":\"Answer2\"}"

        response = self.client.post(url = "/ask/v1/answer",name="Create_Answer", data=createanswer_data, headers=headers)
        global answer_id 
        answer_id = response.json().get("answerId","")
        
    @seq_task(14)
    def Get_Answer(self):   

        response = self.client.get(url = "/ask/v1/answer?limit=10&offset=0&questionId=5eb4fbf177f78f27bbc13405",name="Get_Answer", data=body, headers=headers)
        
    @seq_task(15)
    def Edit_Answer(self):
    
        editanswer_data = "{\"text\":\"Answer2Edit\",\"questionId\":\"5eb4fbf177f78f27bbc13405\"}"

        response = self.client.put(url = f"/ask/v1/answer/{answer_id}",name="Edit_Answer", data=editanswer_data, headers=headers)
        
    @seq_task(16)
    def Like_Answer(self):

        response = self.client.post(url = f"/ask/v1/answer/{answer_id}/like",name="Like_Answer", data=body, headers=headers)
        
    @seq_task(17)
    def UnLike_Answer(self):

        response = self.client.post(url = f"/ask/v1/answer/{answer_id}/unlike",name="UnLike_Answer", data=body, headers=headers)
        
    @seq_task(18)
    def Helpful_Answer(self):

        response = self.client.post(url = f"/ask/v1/answer/{answer_id}/helpful",name="Helpful_Answer", data=body, headers=headers)
        
    @seq_task(19)
    def Mine_Answer(self):   

        response = self.client.get(url = "/ask/v1/answers/my-answers?limit=10&offset=0",name="Mine_Answer", data=body, headers=headers)
        
    @seq_task(20)
    def Delete_Answer(self):   

        response = self.client.delete(url = f"/ask/v1/answer/{answer_id}",name="Delete_Answer", data=body, headers=headers)
        
    @seq_task(21)
    def Spam_Detect(self):
    
        spam_data="{\"text\":\"Questionu0021Creating Question\"}"
    
        response = self.client.post(url = "/ask/v1/spam",name="Spam_Detect", data=spam_data, headers=headers)
        
    @seq_task(22)
    def Smart_Tagging(self):
    
        smarttag_data="{\"goal\":\"engineering\",\"text\":\"Creating Question\"}"
    
        response = self.client.post(url = "/ask/v1/spam",name="Smart_Tagging", data=smarttag_data, headers=headers)
      
     
class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
