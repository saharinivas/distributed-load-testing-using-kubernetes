from locust import HttpUser,SequentialTaskSet,task, between
from random import randrange
from random import randint
import json
import csv
import string
import random
#import sys, logging

#constants
def string_generator(size=7):
        chars = string.ascii_uppercase + string.ascii_lowercase
        return ''.join(random.choice(chars) for _ in range(size))
host = "https://preprodms.embibe.com"
res = []
Params = []
email_password = []

#functions
with open('/locust-tasks/email_password_embibe.csv', 'r') as csvfile:
        email_password = list (csv.reader(csvfile, delimiter=','))
        
with open('/locust-tasks/JIO_Params.csv', 'r') as csvfile:
        Params = list (csv.reader(csvfile, delimiter=','))
        


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

class UserBehaviour(SequentialTaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.headers = {
            'Content-Type':'application/json',
            'connection':'keep-alive',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept':'*/*'
}
        self.value=None
         
    @task
    def login(self):
        
        rnum = randrange(len(email_password)-1)
       
        login_data={
                    "login":email_password[rnum][0],
                    "password":email_password[rnum][1]
                   }
        response = self.client.post('/user_auth/auth/sign_in', data=json.dumps(login_data), name="login",headers=self.headers)
        
        json_dict = json.loads(response.content)
        
        user_id['user_id'] = json_dict["resource"]["id"]
                      
        if (response.status_code != 200):
            print(response.request.headers)
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
                              
        #logging.info('Response for login API is %s',response.content)
        self.headers ['embibe-token']= response.headers['embibe-token']
        
        
    @task
    def getSearchResults(self):
        
        # generate some integers for size value
        
        for _ in range(1000):
            self.value = randint(1, 1000)

        response = self.client.get(url = f"/fiber_ms/search/results?query=magnet&user_id={user_id['user_id']}&size={self.value}&grade=10&goal=CBSE",name="getSearchResults",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getSearchResults -{host}/fiber_ms/search/results?query=magnet&user_id={user_id['user_id']}&size={self.value}&grade=10&goal=CBSE")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
    @task
    def getSearchSuggestions(self):
    
        response = self.client.get(url = f"/fiber_ms/search/suggestions?query=magnet&user_id={user_id['user_id']}&size={self.value}&grade=10&goal=CBSE",name="getSearchSuggestions",data=body, headers=self.headers)

        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getSearchSuggestions -{host}/fiber_ms/search/suggestions?query=magnet&user_id={user_id['user_id']}&size={self.value}&grade=10&goal=CBSE")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def conceptconnect(self):
    
        rnum = randrange(len(Params)-1)
       
        # response = self.client.get(url = f"/concepts/connected/{Params[rnum][0]}?content_id={Params[rnum][1]}",name="conceptconnect",data=body, headers=self.headers)
        response = self.client.get(url = f"/fiber_ms/concepts/connected/new_KG4607?content_id={Params[rnum][1]}",name="conceptconnect",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"conceptconnect -{host}/fiber_ms/concepts/connected/new_KG4607?content_id={Params[rnum][1]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
    
    @task
    def conceptmoreconnect(self):
    
        rnum = randrange(len(Params)-1)
        
        #print (Params[rnum][0],Params[rnum][1])
       
        # response = self.client.get(url = f"/concepts/more/{Params[rnum][0]}?content_id={Params[rnum][1]}",name="conceptmoreconnect",data=body,headers=self.headers)
        
        response = self.client.get(url = f"/fiber_ms/concepts/more/new_KG4607?content_id={Params[rnum][1]}",name="conceptmoreconnect",data=body,headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"conceptmoreconnect -{host}/fiber_ms/concepts/more/new_KG4607?content_id={Params[rnum][1]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getHomeData(self):
    
        home_data = {
            "child_id" : user_id['user_id'],
            "grade" :"10",
            "goal" : "CBSE"
        }
    
        response = self.client.post(url = "/fiber_ms/home",name="getHomeData",data=json.dumps(home_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getHomeData -{host}/fiber_ms/home")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getfilteredHomeData(self):
    
        filteredhome_data = {
            "child_id" : user_id['user_id'],
            "grade" : "10",
            "goal" : "CBSE",
            "onlyPractise" : True
        }
    
        response = self.client.post(url = "/fiber_ms/home/Physics",name="getfilteredHomeData",data=json.dumps(filteredhome_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getfilteredHomeData -{host}/fiber_ms/home/Physics")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getRelatedData(self):
        
        rnum = randrange(len(Params)-1)
                
        response = self.client.get(url = f"/fiber_ms/cg/related_data/{Params[rnum][0]}",name="getRelatedData",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getRelatedData -{host}/fiber_ms/cg/related_data/{Params[rnum][0]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def updateStatus(self):
    
        rnum = randrange(len(Params)-1)
    
        contentstatus_data = {
            "content_id" : Params[rnum][1],
            "content_type" :Params[rnum][2],
            "is_watched" : True,
            "content_status" :"COMPLETED",
            "watched_duration" : 7000,
            "child_id" : user_id['user_id']
        }
        
        response = self.client.post(url = "/fiber_ms/content-status",name="updateStatus",data=json.dumps(contentstatus_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"updateStatus -{host}/fiber_ms/content-status")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
   
    @task
    def getStatus(self):
    
        rnum = randrange(len(Params)-1)

        #print (Params[rnum][1],Params[rnum][2],user_id['user_id'])
        # response = self.client.get(url = f"/content-status/{Params[rnum][1]}/{Params[rnum][2]}?child_id={user_id['user_id']}",name="getStatus",headers=self.headers)
        response = self.client.get(url ="/fiber_ms/content-status/abc/Video?child_id=423423525",name="getStatus",headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getStatus -{host}/fiber_ms/content-status/abc/Video?child_id=423423525")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
        
    # @task
    # def getChapterList(self):

        # response = self.client.get(url = "/chapters",name="getChapterList",data=body, headers=self.headers)
        # logging.info('Headers for getChapterList API is %s',response.content)
        
        chapterid['chapterid'] = response.json().get("id","5e79df54810bc73565cb2696")
 
    @task
    def getChapterDetail(self):
    
        response = self.client.get(url = f"/fiber_ms/chapters/chapterDetail/{chapterid['chapterid']}",name="getChapterDetail",data=body, headers=self.headers)
       
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getChapterDetail -{host}/fiber_ms/chapters/chapterDetail/{chapterid['chapterid']}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getChapterList_subject(self):

        response = self.client.get(url = "/fiber_ms/chapters/Chemistry",name="getChapterList_subject",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getChapterList_subject -{host}/fiber_ms/chapters/Chemistry")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def concept_prerequisites(self):
    
        rnum = randrange(len(Params)-1)
         
        response = self.client.get(url = f"/fiber_ms/concepts/prerequisites/new_KG4607?content_id={Params[rnum][1]}",name="concept_prerequisites",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"concept_prerequisites -{host}/fiber_ms/concepts/prerequisites/new_KG4607?content_id={Params[rnum][1]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getContentDetails(self):
    
        rnum = randrange(len(Params)-1)
    
        contentdetails_data = {
            "child_id" : user_id['user_id'],
            "grade" : "10",
            "goal" : "CBSE"
        }
 
        response = self.client.get(url = f"/fiber_ms/contentDetails/{Params[rnum][2]}/{Params[rnum][1]}",name="getContentDetails",data=json.dumps(contentdetails_data),
        headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getContentDetails -{host}/fiber_ms/contentDetails/{Params[rnum][2]}/{Params[rnum][1]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")

        
    @task
    def getUserHome(self):
    
        home_data = {
            "board":"CBSE",
            "child_id":user_id['user_id'],
            "goal":"CBSE",
            "grade":"10"
         }
    
        response = self.client.post(url = "/fiber_ms/userHome",name="getUserHome",data=json.dumps(home_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getUserHome -{host}/fiber_ms/userHome")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getConceptDetails(self):

        rnum = randrange(len(Params)-1)
        rnum1 = randrange(len(Params)-1)
        rnum2 = randrange(len(Params)-1)
        
        response = self.client.get(url = f"/fiber_ms/concept/content?conceptIds={Params[rnum][0]},{Params[rnum1][0]},{Params[rnum2][0]}",name="getConceptDetails",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getConceptDetails -{host}/fiber_ms/concept/content?conceptIds={Params[rnum][0]},{Params[rnum1][0]},{Params[rnum2][0]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getnextConceptDetails(self):
        
        rnum = randrange(len(Params)-1)    
        
        #response = self.client.get(url = f"/concepts/next/{Params[rnum][0]}",name="getnextConceptDetails",data=body, headers=self.headers)
        response = self.client.get(url = f"/fiber_ms/concepts/next/new_KG4607",name="getnextConceptDetails",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getnextConceptDetails -{host}/fiber_ms/concepts/next/new_KG4607")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
        
    @task
    def postLike_Event(self):
    
        rnum = randrange(len(Params)-1)
    
        event_data = {
            "content_id":Params[rnum][1],
            "content_type":Params[rnum][2],
            "activity_type":"Like",
            "content_category_type":"Practice",
            "status": False,
            "timestamp": 85,
            "child_id":user_id['user_id']
        }
    
        response = self.client.post(url = "/fiber_ms/event",name="postLike_Event",data=json.dumps(event_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"postLike_Event -{host}/fiber_ms/event")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getLikes(self):
    
        rnum = randrange(len(Params)-1)
    
        like_data = {
            "content_id":Params[rnum][1],
            "content_type":Params[rnum][2],
            "content_category_type":"Learn",
            "liked": True,
            "timestamp": 5,
            "child_id": user_id['user_id']
        }
    
        response = self.client.post(url = "/fiber_ms/like",name="getLikes",data=json.dumps(like_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getLikes -{host}/fiber_ms/like")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getBookmark(self):
    
        rnum = randrange(len(Params)-1)
    
        bm_data = {
            "content_id":Params[rnum][1],
            "content_type":Params[rnum][2],
            "bookmarked": True,
            "timestamp": 5,
            "child_id": user_id['user_id']
        }
    
        response = self.client.post(url = "/fiber_ms/bookmark",name="getBookmark",data=json.dumps(bm_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getBookmark -{host}/fiber_ms/bookmark")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getBookmark_child(self):
 
        response = self.client.get(url = f"/fiber_ms/bookmark?child_id={user_id['user_id']}",name="getBookmark_child",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getBookmark_child -{host}/fiber_ms/bookmark?child_id={user_id['user_id']}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
    @task
    def like_child(self):
 
        response = self.client.get(url = f"/fiber_ms/like?child_id={user_id['user_id']}",name="like_child",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"like_child -{host}/fiber_ms/like?child_id={user_id['user_id']}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def connected_profiles(self):
 
        response = self.client.get(url = "/fiber_ms/user/profile/connected_profiles",name="connected_profiles",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"connected_profiles -{host}/fiber_ms/user/profile/connected_profiles")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def profiles_exists(self):
        #Checking userid here for profile id
        response = self.client.get(url = f"/fiber_ms/user/profile/exists?id={user_id['user_id']}",name="profiles_exists",data=body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"profiles_exists -{host}/fiber_ms/user/profile/exists?id={user_id['user_id']}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    # @task
    # def forgotpwd(self):
    
        # pwd_data = {
            # "login":"9560486632"
        # }
 
        # response = self.client.post(url = "/user/forgot-password",name="forgotpwd",data=json.dumps(pwd_data), headers=self.headers)
        
    # @task
    # def resetpwd_otp(self):
    
        # #mobile no needs to be added   
        # reset_data = {
            # "new_password":"12345678",
            # "login":"9560486632"
        # }
 
        # response = self.client.put(url = "/user/reset-password-via-otp/1222",name="forgotpwd",data=json.dumps(reset_data), headers=self.headers)
        
    # @task
    # def validate_otp(self):
    
        # otp_data = {
            # "otp" : "1234",
            # "login":"9770181024"
        # }
 
        # response = self.client.get(url = "/user/is-reset-password-otp-valid",name="validate_otp",data=json.dumps(otp_data), headers=self.headers)
        
    @task
    def add_user(self):
    
        res = string_generator(8)

        user_data = {
            "parent_id": user_id['user_id'],
            "first_name": "Test",
            "user_type" : "child",
            "email_id" : "test"+res+"@gmail.com",
            "goal" : "g10",
            "grade" : "10", 
            "board" : "CBSE",
            "school" : "DPS",
            "state" : "Delhi",
            "city" : "Delhi",
            "avatar_image" : "S3 Url (String)"
        }
 
        response = self.client.post(url = "/fiber_ms/addUser",name="add_user",data=json.dumps(user_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"add_user -{host}/fiber_ms/addUser")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
       
class WebsiteTest(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(2, 5)
    host = "https://preprodms.embibe.com"
