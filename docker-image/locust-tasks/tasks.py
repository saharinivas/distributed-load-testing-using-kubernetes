from locust import HttpLocust, TaskSet, TaskSequence, seq_task, between
import csv
import time
from random import randrange


headers = {
'Content-Type': 'application/json',
'Cookie': 'PHPSESSID=gpsi2or2l71vfo4v6qmu8gqet0; PHPSESSID=gpsi2or2l71vfo4v6qmu8gqet0; AWSALB=KbJK/T8knVZNFpTcX25QRdRnfxq+l9pYzy0TiVql1sDAg9FKnSOhE4NwHjqbAmyUD05Czlzf4OJBZnYrsUsx2P+AekuTVrrhBxvYlG0BycIDzpiZ8sMM3isblodU; AWSALBCORS=KbJK/T8knVZNFpTcX25QRdRnfxq+l9pYzy0TiVql1sDAg9FKnSOhE4NwHjqbAmyUD05Czlzf4OJBZnYrsUsx2P+AekuTVrrhBxvYlG0BycIDzpiZ8sMM3isblodU'
}

user_emails= []


with open('bulk_users.txt','r') as file:
	user_emails = file.read().split(",")


class MyTaskSequence(TaskSequence):
    @seq_task(1)
    def student_login(self):
    	data = {"partner_id": "educationgoa", "email": user_emails[randrange(50000)]} 
    	response = self.client.post(url="/apis/student_login.php",data=data,auth=None,headers=headers)


class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
    wait_time = between(1, 5)