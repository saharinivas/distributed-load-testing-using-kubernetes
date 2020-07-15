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
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))


host = "https://preprodms.embibe.com"
res = []
Params = []
email_password = []

#functions
# with open('email_password_embibe.csv', 'r') as csvfile:
        # email_password = list (csv.reader(csvfile, delimiter=','))
        
with open('/locust-tasks/JIO_Params.csv', 'r') as csvfile:
        Params = list (csv.reader(csvfile, delimiter=','))
        

#Declarations
     
#Payload Values       
# body = {}
# user_id={'user_id':''} 
# parent_id = {'parent_id':''}
# child_id={'child_id':''} 
# email_id={'email_id':''} 
# chapterid={'chapterid':''} 

class UserBehaviour(SequentialTaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.headers = {
            'Content-Type':'application/json',
            'connection':'keep-alive',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept':'*/*'
        }
        self.body = {}
        self.parent_id = None
        self.email_id = None
        self.child_id = None
        self.child_email_id = None
        self.chapter_id = '5e79df54810bc73565cb2696'
        self.value = 1      
        self.grade = randint(9,10)   
    
    @task
    def Signup(self):
        res = string_generator(7)
        
         
        signup_data = {"login":"loadtest"+res+"@gmail.com","password":"embibe1234", "flag":"sp"}
 

        response = self.client.post(url = "/user_auth_lt/auth/sign_in",name="Signup",data=json.dumps(signup_data),auth=None, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"Signup -{host}/user_auth_lt/auth/sign_in")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
        #print(response.json())
        
        self.headers['embibe-token'] = response.headers['embibe-token']
        
        json_dict = json.loads(response.content)
        self.parent_id = json_dict["resource"]["id"]
        self.email_id = json_dict["resource"]["email"]

        #user_id['user_id'] = response.json()['user_id']         
        #email_id['email_id'] = response.json()['email']
                
        
    @task
    def add_user(self):
    
        res = string_generator(6)

        user_data = {
            "parent_id": self.parent_id,
            "first_name": "Test",
            "user_type" : "child",
            "email_id" : "loadtestchild"+res+"@gmail.com",
            "goal" : "g10",
            "grade" : self.grade,
            "board" : "CBSE",
            "school" : "DPS",
            "state" : "Delhi",
            "city" : "Delhi",
            "avatar_image" : "S3 Url (String)"
        }
 
        response = self.client.post(url = "/fiber_ms_lt/addUser",name="add_user",data=json.dumps(user_data), headers=self.headers)
        
        json_dict = json.loads(response.content)        
        self.child_id = json_dict["linked_profiles"][0]["user_id"]
        self.child_email_id = json_dict["linked_profiles"][0]["email"]
        
        # print(self.child_id)
        
        #print(response.json())
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"add_user -{host}/fiber_ms_lt/addUser")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
    
       
    
    @task
    def login(self):
        
        # rnum = randrange(len(email_password)-1)
       
        login_data={
                    "login": self.email_id,
                    "password":"embibe1234"
                   }
        response = self.client.post('/user_auth_lt/auth/sign_in', data=json.dumps(login_data), name="login",headers=self.headers)
        
        #json_dict = json.loads(response.content)
        
        #user_id['user_id'] = json_dict["resource"]["id"]
                      
        if (response.status_code != 200):
            print(response.request.headers)
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
                                          
        #logging.info('Response for login API is %s',response.content)
        #self.headers ['embibe-token']= response.headers['embibe-token']
        
        
    @task
    def getSearchResults(self):
        
        # generate some integers for size value
        
        for _ in range(1000):
            self.value = randint(1, 1000)

        response = self.client.get(url = f"/fiber_ms_lt/search/results?query=magnet&user_id={self.parent_id}&size={self.value}&grade=10&goal=CBSE",name="getSearchResults",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getSearchResults -{host}/fiber_ms_lt/search/results?query=magnet&user_id={self.parent_id}&size={self.value}&grade=10&goal=CBSE")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
    @task
    def getSearchSuggestions(self):
    
        response = self.client.get(url = f"/fiber_ms_lt/search/suggestions?query=magnet&user_id={self.parent_id}&size={self.value}&grade=10&goal=CBSE",name="getSearchSuggestions",data=self.body, headers=self.headers)

        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getSearchSuggestions -{host}/fiber_ms_lt/search/suggestions?query=magnet&user_id={self.parent_id}&size={self.value}&grade=10&goal=CBSE")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def conceptconnect(self):
    
        rnum = randrange(len(Params)-1)
       
        # response = self.client.get(url = f"/concepts/connected/{Params[rnum][0]}?content_id={Params[rnum][1]}",name="conceptconnect",data=body, headers=self.headers)
        response = self.client.get(url = f"/fiber_ms_lt/concepts/connected/new_KG4607?content_id={Params[rnum][1]}",name="conceptconnect",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"conceptconnect -{host}/fiber_ms_lt/concepts/connected/new_KG4607?content_id={Params[rnum][1]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
    
    @task
    def conceptmoreconnect(self):
    
        rnum = randrange(len(Params)-1)
        
        #print (Params[rnum][0],Params[rnum][1])
       
        # response = self.client.get(url = f"/concepts/more/{Params[rnum][0]}?content_id={Params[rnum][1]}",name="conceptmoreconnect",data=body,headers=self.headers)
        
        response = self.client.get(url = f"/fiber_ms_lt/concepts/more/new_KG4607?content_id={Params[rnum][1]}",name="conceptmoreconnect",data=self.body,headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"conceptmoreconnect -{host}/fiber_ms_lt/concepts/more/new_KG4607?content_id={Params[rnum][1]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getHomeData(self):
    
        home_data = {
            "child_id" : self.parent_id,
            "grade" :"10",
            "goal" : "CBSE"
        }
    
        response = self.client.post(url = "/fiber_ms_lt/home",name="getHomeData",data=json.dumps(home_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getHomeData -{host}/fiber_ms_lt/home")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getHomeData(self):
    
        home_data = {
            "child_id" : self.parent_id,
            "grade" :self.grade,
            "goal" : "CBSE"
        }
    
        response = self.client.post(url = "/fiber_ms_lt/v1/home",name="getHomeData",data=json.dumps(home_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getHomeData -{host}/fiber_ms_lt/v1/home")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getfilteredHomeData(self):
    
        filteredhome_data = {
            "child_id" : self.parent_id,
            "grade" : "10",
            "goal" : "CBSE",
            "onlyPractise" : True
        }
    
        response = self.client.post(url = "/fiber_ms_lt/home/Physics",name="getfilteredHomeData",data=json.dumps(filteredhome_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getfilteredHomeData -{host}/fiber_ms_lt/home/Physics")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def homeSections(self):
    
        rnum = randrange(len(Params)-1)
    
        homeSections_data = {
            "child_id": self.parent_id,
            "grade": self.grade,
            "goal": "CBSE",
            "content_section_type": "BestLearningVideosFromInternet",
            "offset": 2,
            "size": 20
        }
        
        response = self.client.post(url = "/fiber_ms_lt/v1/home/sections",name="homeSections",data=json.dumps(homeSections_data), headers=self.headers)
        
        print(f"child id is {self.parent_id}")
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"homeSections -{host}/fiber_ms_lt/v1/home/sections")
            print(response.content)
            print(response.headers)
            print(f"child id is {self.parent_id}")
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def homepractise(self):
    
        homepractise_data = {
            "child_id" : self.parent_id,
            "grade" :self.grade,
            "goal" : "CBSE"
        }
    
        response = self.client.post(url = "/fiber_ms_lt/v1/home/practise",name="homepractise",data=json.dumps(homepractise_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"homepractise -{host}/fiber_ms_lt/v1/home/practise")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def homepractisesections(self):
    
        rnum = randrange(len(Params)-1)
    
        homepractisesections_data = {
                            "child_id": self.parent_id,
                            "grade": self.grade,
                            "goal": "CBSE",
                            "content_section_type": "PractiseMathematicsChapters",
                            "offset": 0,
                            "size": 20
}
        
        response = self.client.post(url = "/fiber_ms_lt/v1/home/practise/sections",name="homepractisesections",data=json.dumps(homepractisesections_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"homepractisesections -{host}/fiber_ms_lt/v1/home/practise/sections")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def userHome(self):
    
        userHome_data = {
            "child_id" : self.parent_id,
            "grade" :self.grade,
            "goal" : "CBSE"
        }
    
        response = self.client.post(url = "/fiber_ms_lt/v1/userHome",name="userHome",data=json.dumps(userHome_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"userHome -{host}/fiber_ms_lt/v1/userHome")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def Physics(self):
   
        home_data = {
            "child_id" : self.parent_id,
            "grade" :self.grade,
            "goal" : "CBSE",
            "fetch_all_content" : "true"
        }
   
        response = self.client.post(url = "/fiber_ms_lt/v1/home/Physics",name="Physics",data=json.dumps(home_data), headers=self.headers)
       
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"Physics -{host}/fiber_ms_lt/v1/home/Physics")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")

    @task
    def homePhysicsSection(self):
   
        home_data = {
            "child_id" : self.parent_id,
            "grade" :self.grade,
            "goal" : "CBSE",
            "content_section_type": "LearnPracticePhysicsBooks",
            "offset": 0,
            "size": 15
        }
   
        response = self.client.post(url = "/fiber_ms_lt/v1/home/Physics/sections",name="homePhysicsSection",data=json.dumps(home_data), headers=self.headers)
       
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"homePhysicsSection -{host}/fiber_ms_lt/v1/home/Physics/sections")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")

    @task
    def Chemistry(self):
   
        home_data = {
            "child_id" : self.parent_id,
            "grade" : self.grade,
            "goal" : "CBSE",
            "fetch_all_content" : "true"
        }
   
        response = self.client.post(url = "/fiber_ms_lt/v1/home/Chemistry",name="Chemistry",data=json.dumps(home_data), headers=self.headers)
       
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"Chemistry -{host}/fiber_ms_lt/v1/home/Chemistry")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")

    @task
    def homeChemistrySection(self):
   
        home_data = {
            "child_id" : self.parent_id,
            "grade" :self.grade,
            "goal" : "CBSE",
            "content_section_type": "RealLifeExamplesVideosSyllabus",
            "offset": 0,
            "size": 20
        }
   
        response = self.client.post(url = "/fiber_ms_lt/v1/home/Chemistry/sections",name="homeChemistrySection",data=json.dumps(home_data), headers=self.headers)
       
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"homeChemistrySection -{host}/fiber_ms_lt/v1/home/Chemistry/sections")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")

    @task
    def Biology(self):
   
        home_data = {
            "child_id" : self.parent_id,
            "grade" : self.grade,
            "goal" : "CBSE",
            "fetch_all_content" : "true"
        }
   
        response = self.client.post(url = "/fiber_ms_lt/v1/home/Biology",name="Biology",data=json.dumps(home_data), headers=self.headers)
       
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"Biology -{host}/fiber_ms_lt/v1/home/Biology")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")

    @task
    def homeBiologySection(self):
   
        home_data = {
            "child_id" : self.parent_id,
            "grade" : self.grade,
            "goal" : "CBSE",
            "content_section_type": "LearnPracticeBiologyBooks",
            "offset": 0,
            "size": 20
        }
   
        response = self.client.post(url = "/fiber_ms_lt/v1/home/Biology/sections",name="homeBiologySection",data=json.dumps(home_data), headers=self.headers)
       
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"homeBiologySection -{host}/fiber_ms_lt/v1/home/Biology/sections")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def Mathematics(self):
    
        rnum = randrange(len(Params)-1)
    
        Mathematics_data = {
                            "child_id": self.parent_id,
                            "grade": self.grade,
                            "goal": "CBSE",
                            "content_section_type": "PractiseMathematicsChapters",
                            "fetch_all_content" : "true"
}
        
        response = self.client.post(url = "/fiber_ms_lt/v1/home/Mathematics",name="Mathematics",data=json.dumps(Mathematics_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"Mathematics -{host}/fiber_ms_lt/v1/home/Mathematics")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def homeMathematicssections(self):
    
        rnum = randrange(len(Params)-1)
    
        homeMathematicssections_data = {
                            "child_id": self.parent_id,
                            "grade": self.grade,
                            "goal": "CBSE",
                            "content_section_type": "RealLifeExamplesVideosSyllabus",
                            "offset": 0,
                            "size": 20
}
        
        response = self.client.post(url = "/fiber_ms_lt/v1/home/Mathematics/sections",name="homeMathematicssections",data=json.dumps(homeMathematicssections_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"homeMathematicssections -{host}/fiber_ms_lt/v1/home/Mathematics/sections")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getRelatedData(self):
        
        rnum = randrange(len(Params)-1)
                
        response = self.client.get(url = f"/fiber_ms_lt/cg/related_data/{Params[rnum][0]}",name="getRelatedData",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getRelatedData -{host}/fiber_ms_lt/cg/related_data/{Params[rnum][0]}")
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
            "child_id" : self.child_id
        }
        
        response = self.client.post(url = "/fiber_ms_lt/content-status",name="updateStatus",data=json.dumps(contentstatus_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"updateStatus -{host}/fiber_ms_lt/content-status")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
   
    @task
    def getStatus(self):
    
        rnum = randrange(len(Params)-1)

        #print (Params[rnum][1],Params[rnum][2],user_id['user_id'])
        # response = self.client.get(url = f"/content-status/{Params[rnum][1]}/{Params[rnum][2]}?child_id={user_id['user_id']}",name="getStatus",headers=self.headers)
        response = self.client.get(url ="/fiber_ms_lt/content-status/abc/Video?child_id=423423525",name="getStatus",headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getStatus -{host}/fiber_ms_lt/content-status/abc/Video?child_id=423423525")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
        
    # @task
    # def getChapterList(self):

        # response = self.client.get(url = "/chapters",name="getChapterList",data=body, headers=self.headers)
        # logging.info('Headers for getChapterList API is %s',response.content)
        
        # chapterid['chapterid'] = response.json().get("id","5e79df54810bc73565cb2696")
 
    @task
    def getChapterDetail(self):
    
        response = self.client.get(url = f"/fiber_ms_lt/chapters/chapterDetail/{self.chapter_id}",name="getChapterDetail",data=self.body, headers=self.headers)
       
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getChapterDetail -{host}/fiber_ms_lt/chapters/chapterDetail/{self.chapter_id}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getChapterList_subject(self):

        #response = self.client.get(url = "/fiber_ms_lt/chapters/Chemistry",name="getChapterList_subject",data=body, headers=self.headers)
        response = self.client.get(url = "/fiber_ms_lt/chapters/Chemistry?grade=10",name="getChapterList_subject",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getChapterList_subject -{host}/fiber_ms_lt/chapters/Chemistry")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def concept_prerequisites(self):
    
        rnum = randrange(len(Params)-1)
         
        response = self.client.get(url = f"/fiber_ms_lt/concepts/prerequisites/new_KG4607?content_id={Params[rnum][1]}",name="concept_prerequisites",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"concept_prerequisites -{host}/fiber_ms_lt/concepts/prerequisites/new_KG4607?content_id={Params[rnum][1]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getContentDetails(self):
    
        rnum = randrange(len(Params)-1)
    
        contentdetails_data = {
            "child_id" : self.parent_id,
            "grade" : self.grade,
            "goal" : "CBSE"
        }
 
        response = self.client.get(url = f"/fiber_ms_lt/contentDetails/{Params[rnum][2]}/{Params[rnum][1]}",name="getContentDetails",data=json.dumps(contentdetails_data),
        headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getContentDetails -{host}/fiber_ms_lt/contentDetails/{Params[rnum][2]}/{Params[rnum][1]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")

        
    @task
    def getUserHome(self):
    
        home_data = {
            "board": "CBSE",
            "child_id": self.parent_id,
            "goal":"CBSE",
            "grade": self.grade
         }
    
        response = self.client.post(url = "/fiber_ms_lt/userHome",name="getUserHome",data=json.dumps(home_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getUserHome -{host}/fiber_ms_lt/userHome")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getConceptDetails(self):

        rnum = randrange(len(Params)-1)
        rnum1 = randrange(len(Params)-1)
        rnum2 = randrange(len(Params)-1)
        
        response = self.client.get(url = f"/fiber_ms_lt/concept/content?conceptIds={Params[rnum][0]},{Params[rnum1][0]},{Params[rnum2][0]}",name="getConceptDetails",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getConceptDetails -{host}/fiber_ms_lt/concept/content?conceptIds={Params[rnum][0]},{Params[rnum1][0]},{Params[rnum2][0]}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
            
    @task
    def getnextConceptDetails(self):
        
        rnum = randrange(len(Params)-1)    
        
        #response = self.client.get(url = f"/concepts/next/{Params[rnum][0]}",name="getnextConceptDetails",data=body, headers=self.headers)
        response = self.client.get(url = f"/fiber_ms_lt/concepts/next/new_KG4607",name="getnextConceptDetails",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getnextConceptDetails -{host}/fiber_ms_lt/concepts/next/new_KG4607")
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
            "child_id": self.child_id
        }
    
        response = self.client.post(url = "/fiber_ms_lt/event",name="postLike_Event",data=json.dumps(event_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"postLike_Event -{host}/fiber_ms_lt/event")
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
            "child_id": self.child_id
        }
    
        response = self.client.post(url = "/fiber_ms_lt/like",name="getLikes",data=json.dumps(like_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getLikes -{host}/fiber_ms_lt/like")
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
            "child_id": self.child_id
        }
    
        response = self.client.post(url = "/fiber_ms_lt/bookmark",name="getBookmark",data=json.dumps(bm_data), headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getBookmark -{host}/fiber_ms_lt/bookmark")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def getBookmark_child(self):
 
        response = self.client.get(url = f"/fiber_ms_lt/bookmark?child_id={self.child_id}",name="getBookmark_child",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"getBookmark_child -{host}/fiber_ms_lt/bookmark?child_id={self.child_id}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
    @task
    def like_child(self):
 
        response = self.client.get(url = f"/fiber_ms_lt/like?child_id={self.child_id}",name="like_child",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"like_child -{host}/fiber_ms_lt/like?child_id={self.child_id}")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def connected_profiles(self):
 
        response = self.client.get(url = "/fiber_ms_lt/user/profile/connected_profiles",name="connected_profiles",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"connected_profiles -{host}/fiber_ms_lt/user/profile/connected_profiles")
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
        
    @task
    def profiles_exists(self):
        #Checking userid here for profile id
        response = self.client.get(url = f"/fiber_ms_lt/user/profile/exists?id={self.parent_id}",name="profiles_exists",data=self.body, headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(f"profiles_exists -{host}/fiber_ms_lt/user/profile/exists?id={self.parent_id}")
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
        
    
       
class WebsiteTest(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(1, 2)
    host = "https://preprodms.embibe.com"
