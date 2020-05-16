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

#Declarations
headers = {
    'Content-Type':'application/json',
    'connection':'keep-alive',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept':'*/*'
          }
     
#Payload Values       
body = {}
user_id={'user_id':''} 
email_id={'email_id':''} 
chapterid={'chapterid':''} 

class MyTaskSequence(TaskSequence):

    @seq_task(1)
    def Signup(self):
        res = string_generator(4)
        
        signup_data = {
        	"first_name" :"LoadTest",
        	"user_name" :"loadtest"+res+"@gmail.com",
        	"password": "test1234"
        }

        response = self.client.post(url = "/signup",name="Signup",data=json.dumps(signup_data),auth=None, headers=headers)
        
        user_id['user_id'] = response.json().get("user_id","")
         
        email_id['email_id'] = response.json().get("email","")

    @seq_task(2)
    def login(self):
        
        login_data = {
            "user_name": email_id['email_id'],
            "password": "test1234"   
                    } 

        response = self.client.post(url = "/login",name="login",data=json.dumps(login_data),auth=None, headers=headers)

        headers ['embibe-token']= response.cookies['preprod-embibe-token']
        
    @seq_task(3)
    def getSearchResults(self):
    
        #query needs to be changed as per params
        response = self.client.get(url = f"/search/results?query=magnet&user_id={user_id['user_id']}&size=10&grade=10&goal=CBSE",name="getSearchResults",data=body, headers=headers)
        
    @seq_task(4)
    def getSearchSuggestions(self):
    
        response = self.client.get(url = f"/search/suggestions?query=magnet&user_id={user_id['user_id']}&size=10&grade=10&goal=CBSE",name="getSearchSuggestions",data=body, headers=headers)
        
    @seq_task(5)
    def conceptconnect(self):
        #query needs to be changed as per params-  concept id  and name must be parameterized
        response = self.client.get(url = "/concepts/connected/new_KG559?content_id=2759099",name="conceptconnect",data=body, headers=headers)
        
    @seq_task(6)
    def conceptmoreconnect(self):
        #query needs to be changed as per params-  concept id  and name must be parameterized
        response = self.client.get(url = "/concepts/more/new_KG5596?content_id=2759099",name="conceptmoreconnect",data=body, headers=headers)
        
    @seq_task(7)
    def getHomeData(self):
    
        home_data = {
            "child_id" : user_id['user_id'],
            "grade" :"10",
            "goal" : "CBSE"
        }
    
        response = self.client.post(url = "/home",name="getHomeData",data=json.dumps(home_data), headers=headers)
        
    @seq_task(8)
    def getfilteredHomeData(self):
    
        filteredhome_data = {
            "child_id" : user_id['user_id'],
            "grade" : "10",
            "goal" : "CBSE",
            "onlyPractise" : True
        }
    
        response = self.client.post(url = "/home/Physics",name="getfilteredHomeData",data=json.dumps(filteredhome_data), headers=headers)
        
    @seq_task(9)
    def getRelatedData(self):
    
        #query needs to be changed as per params-  concept id  and name must be parameterized
        response = self.client.get(url = "/cg/related_data/new_KG2663",name="getRelatedData",data=body, headers=headers)
        
    @seq_task(10)
    def updateStatus(self):
    
        contentstatus_data = {
            "content_id" : "3213355",
            "content_type" :"Video",
            "is_watched" : True,
            "content_status" :"COMPLETED",
            "watched_duration" : 7000,
            "child_id" : user_id['user_id']
        }
        
        response = self.client.post(url = "/content-status",name="updateStatus",data=json.dumps(contentstatus_data), headers=headers)
   
    @seq_task(11)
    def getStatus(self):
        #query needs to be changed as per params-  concept id  and name must be parameterized
        response = self.client.get(url = "/content-status/abc/Video?child_id=423423525",name="getStatus",headers=headers)
        
    @seq_task(12)
    def getChapterList(self):

        response = self.client.get(url = "/chapters",name="getChapterList",data=body, headers=headers)
     
        chapterid['chapterid'] = response.json().get("id","")
 
    @seq_task(13)
    def getChapterDetail(self):
    
        response = self.client.get(url = f"/chapters/chapterDetail/{chapterid['chapterid']}",name="getChapterDetail",data=body, headers=headers)
        
    @seq_task(14)
    def getChapterList_subject(self):

        response = self.client.get(url = "/chapters/Chemistry",name="getChapterList_subject",data=body, headers=headers)
        
    @seq_task(15)
    def concept_prerequisites(self):
         #query needs to be changed as per params-  concept id  and name must be parameterized
        response = self.client.get(url = "/concepts/prerequisites/new_KG1433?content_id=2759099",name="concept_prerequisites",data=body, headers=headers)
        
    @seq_task(16)
    def getContentDetails(self):
    
        contentdetails_data = {
            "child_id" : user_id['user_id'],
            "grade" : "10",
            "goal" : "CBSE"
        }
 
        response = self.client.get(url = "/contentDetails/coobo/2758887",name="getContentDetails",data=json.dumps(contentdetails_data), headers=headers)
        
    @seq_task(17)
    def getUserHome(self):
    
        home_data = {
            "board":"CBSE",
            "child_id":user_id['user_id'],
            "goal":"CBSE",
            "grade":"10"
         }
    
        response = self.client.post(url = "/userHome",name="getUserHome",data=json.dumps(home_data), headers=headers)
        
    @seq_task(18)
    def getConceptDetails(self):

         #query needs to be changed as per params-  concept id  and name must be parameterized      
        response = self.client.get(url = "/concept/content?conceptIds=new_KG2663,new_KG2081,new_KG2631",name="getConceptDetails",data=body, headers=headers)
        
    @seq_task(19)
    def getnextConceptDetails(self):
        
         #query needs to be changed as per params-  concept id  and name must be parameterized      
        response = self.client.get(url = "/concepts/next/new_KG2663",name="getnextConceptDetails",data=body, headers=headers)
        
    @seq_task(20)
    def postLike_Event(self):
    
        event_data = {
            "content_id":"3213355",
            "content_type":"Video",
            "activity_type":"Like",
            "content_category_type":"Practice",
            "status": False,
            "timestamp": 85,
            "child_id":user_id['user_id']
        }
    
        response = self.client.post(url = "/event",name="postLike_Event",data=json.dumps(event_data), headers=headers)
        
    @seq_task(21)
    def getLikes(self):
    
        like_data = {
            "content_id":"3213355",
            "content_type":"Video",
            "content_category_type":"Learn",
            "liked": True,
            "timestamp": 5,
            "child_id": user_id['user_id']
        }
    
        response = self.client.post(url = "/like",name="getLikes",data=json.dumps(like_data), headers=headers)
        
    @seq_task(22)
    def getBookmark(self):
    
        bm_data = {
            "content_id":"3213355",
            "content_type":"Video",
            "bookmarked": True,
            "timestamp": 5,
            "child_id": user_id['user_id']
        }
    
        response = self.client.post(url = "/bookmark",name="getBookmark",data=json.dumps(bm_data), headers=headers)
        
    @seq_task(23)
    def getBookmark_child(self):
 
        response = self.client.get(url = f"/bookmark?child_id={user_id['user_id']}",name="getBookmark_child",data=body, headers=headers)
        
    @seq_task(24)
    def like_child(self):
 
        response = self.client.get(url = f"/like?child_id={user_id['user_id']}",name="like_child",data=body, headers=headers)
        
    @seq_task(25)
    def connected_profiles(self):
 
        response = self.client.get(url = "/user/profile/connected_profiles",name="connected_profiles",data=body, headers=headers)
        
    @seq_task(26)
    def profiles_exists(self):
        #Checking userid here for profile id
        response = self.client.get(url = f"/user/profile/exists?id={user_id['user_id']}",name="profiles_exists",data=body, headers=headers)
        
    @seq_task(27)
    def forgotpwd(self):
    
        pwd_data = {
            "login":"9560486632"
        }
 
        response = self.client.post(url = "/user/forgot-password",name="forgotpwd",data=json.dumps(pwd_data), headers=headers)
        
    @seq_task(28)
    def resetpwd_otp(self):
    
        #mobile no needs to be added   
        reset_data = {
            "new_password":"12345678",
            "login":"9560486632"
        }
 
        response = self.client.put(url = "/user/reset-password-via-otp/1222",name="forgotpwd",data=json.dumps(reset_data), headers=headers)
        
    @seq_task(29)
    def validate_otp(self):
    
        otp_data = {
            "otp" : "1234",
            "login":"9770181024"
        }
 
        response = self.client.get(url = "/user/is-reset-password-otp-valid",name="validate_otp",data=json.dumps(otp_data), headers=headers)
        
    @seq_task(30)
    def add_user(self):

        user_data = {
            "parent_id": user_id['user_id'],
            "first_name": "LoadTest",
            "user_type" : "child",
            "email_id" : email_id['email_id'],
            "goal" : "g10",
            "grade" : "10", 
            "board" : "CBSE",
            "school" : "DPS",
            "state" : "Delhi",
            "city" : "Delhi",
            "avatar_image" : "S3 Url (String)"
        }
        response = self.client.post(url = "/addUser",name="add_user",data=json.dumps(user_data), headers=headers)
        
class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence

