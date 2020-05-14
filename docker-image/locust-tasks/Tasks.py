from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange
import json
import csv
import random
import string


#constants
def string_generator(size):
    chars = string.ascii_uppercase + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))
    
res = []
email_password = []
chars = string.ascii_letters
size = 3

#functions
with open('/locust-tasks/email_password.csv', 'r') as csvfile:
        email_password = list (csv.reader(csvfile, delimiter=','))

#Declarations
headers = {
    'Content-Type':'application/json',
    'connection':'keep-alive',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept':'*/*'
          }
     
#Payload Values       
body = {}

class MyTaskSequence(TaskSequence):

    @seq_task(1)
    def Signup(self):
        res = string_generator(4)
        
        Signin_data = "{\n                \"first_name\" :\"Test\",\n                \"user_name\" :\"test"+res+"@gmail.com\",\n                \"password\": \"test1234\"\n}"
 
        response = self.client.post(url = "/signup",name="Signup",data=Signin_data,auth=None, headers=headers)
        global user_id 
        user_id = response.json().get("user_id","")
        global email_id 
        email_id = response.json().get("email","")

    @seq_task(2)
    def login(self):
    
        rnum = randrange(len(email_password)-1)
        
        login_data = {
            "user_name": email_password[rnum][0],
            "password": email_password[rnum][1]   
                    } 

        response = self.client.post(url = "/login",name="login",data=json.dumps(login_data),auth=None, headers=headers)
        headers ['embibe-token']= response.cookies['preprod-embibe-token']
        
    @seq_task(3)
    def getSearchResults(self):
    
        response = self.client.get(url = "/search/results?query=magnet&user_id=12&size=10&grade=10&goal=CBSE",name="getSearchResults",data=body, headers=headers)
        
    @seq_task(4)
    def getSearchSuggestions(self):
    
        response = self.client.get(url = "/search/suggestions?query=magnet&user_id=12&size=10&grade=10&goal=CBSE",name="getSearchSuggestions",data=body, headers=headers)
        
    @seq_task(5)
    def conceptconnect(self):
    
        response = self.client.get(url = "/concepts/connected/new_KG559?content_id=2759099",name="conceptconnect",data=body, headers=headers)
        
    @seq_task(6)
    def conceptmoreconnect(self):
    
        response = self.client.get(url = "/concepts/more/new_KG5596?content_id=2759099",name="conceptmoreconnect",data=body, headers=headers)
    
    @seq_task(7)
    def getfilteredHomeData(self):
    
        filteredhome_data = {
                    "child_id" : 1117071647,
                    "grade" : "10",
                    "goal" : "CBSE",
                    "onlyPractise" : true
                            }
    
        response = self.client.post(url = "/home/Physics",name="getfilteredHomeData",data=json.dumps(filteredhome_data), headers=headers)
        
    @seq_task(8)
    def getRelatedData(self):
    
        response = self.client.get(url = "/cg/related_data/new_KG2663",name="getRelatedData",data=body, headers=headers)
        
    @seq_task(9)
    def updateStatus(self):
    
        contentstatus_data = "{\n\n\t\"content_id\" : \"abc\",\n\n\t\"content_type\" : \"Video\",\n\n\t\"is_watched\" : true,\n\n\t\"content_status\" : \"COMPLETED\",\n\n\t\"watched_duration\" : 7000,\n\n\t\"child_id\" : 423423525\n\n}"
        
        response = self.client.post(url = "/content-status",name="updateStatus",data=contentstatus_data, headers=headers)
   
    @seq_task(10)
    def getStatus(self):
 
        response = self.client.get(url = "/content-status/abc/Video?child_id=423423525",name="getStatus",data=body, headers=headers)
        
    @seq_task(11)
    def getChapterList(self):

        response = self.client.get(url = "/chapters",name="getChapterList",data=body, headers=headers)
        global chapterid 
        chapterid = response.json().get("id","")
 
    @seq_task(12)
    def getChapterDetail(self):
    
        response = self.client.get(url = f"/chapters/chapterDetail/{chapterid}",name="getChapterDetail",data=body, headers=headers)
        
    @seq_task(13)
    def getChapterList_subject(self):

        response = self.client.get(url = "/chapters/Chemistry",name="getChapterList_subject",data=body, headers=headers)
        
    @seq_task(14)
    def concept_prerequisites(self):
    
        response = self.client.get(url = "/concepts/prerequisites/new_KG1433?content_id=2759099",name="concept_prerequisites",data=body, headers=headers)
  
    @seq_task(15)
    def getConceptDetails(self):
              
        response = self.client.get(url = "/concept/content?conceptIds=new_KG2663,new_KG2081,new_KG2631",name="getConceptDetails",data=body, headers=headers)
        
    @seq_task(16)
    def getnextConceptDetails(self):
              
        response = self.client.get(url = "/concepts/next/new_KG2663",name="getnextConceptDetails",data=body, headers=headers)
    
    @seq_task(17)
    def getBookmark_child(self):
 
        response = self.client.get(url = "/bookmark?child_id=1117055025",name="getBookmark_child",data=body, headers=headers)
        
    @seq_task(18)
    def like_child(self):
 
        response = self.client.get(url = "/like?child_id=1117100193",name="like_child",data=body, headers=headers)
        
    @seq_task(19)
    def connected_profiles(self):
 
        response = self.client.get(url = "/user/profile/connected_profiles",name="connected_profiles",data=body, headers=headers)
        
    @seq_task(20)
    def profiles_exists(self):
 
        response = self.client.get(url = "/user/profile/exists?id=9770181024",name="profiles_exists",data=body, headers=headers)
        
    @seq_task(21)
    def forgotpwd(self):
    
        pwd_data = "{\"login\":\"9560486632\"}"
 
        response = self.client.post(url = "/user/forgot-password",name="forgotpwd",data=pwd_data, headers=headers)
        
    @seq_task(22)
    def resetpwd_otp(self):
    
        reset_data = "{\n\"new_password\":\"12345678\",\n\"login\":\"9560486632\"\n}"
 
        response = self.client.put(url = "/user/reset-password-via-otp/1222",name="forgotpwd",data=reset_data, headers=headers)
        
    @seq_task(23)
    def validate_otp(self):
    
        otp_data = "{\n\"otp\" : \"1234\",\n\"login\":\"9770181024\"\n}"
 
        response = self.client.get(url = "/user/is-reset-password-otp-valid",name="validate_otp",data=otp_data, headers=headers)
        
    @seq_task(24)
    def add_user(self):
    
        user_data = {
                "parent_id": {user_id},
                "first_name": "Test",
                "user_type" : "child",
                "email_id" : {email_id},
                "goal" : "gl9",
                "grade" : "String", 
                "board" : "String",
                "school" : "String",
                "state" : "String",
                "city" : "String",
                "avatar_image" : "S3 Url (String)"
                    }
                    
        response = self.client.post(url = "/addUser",name="add_user",data=json.dumps(user_data), headers=headers)
     
        
class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
    

        

               
              
        

