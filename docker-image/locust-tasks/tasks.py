from locust import HttpLocust, TaskSet, TaskSequence, seq_task
from random import randrange
from random import randint
import json
import csv
import string
import random

#constants
def string_generator(size=7):
    chars = string.ascii_uppercase + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))
    
res = []
Params = []

#functions
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


class MyTaskSequence(TaskSequence):

    @seq_task(1)
    def Signup(self):
        res = string_generator(7)
        
        signup_data = {
        	"first_name" :"LoadTest",
        	"user_name" :"loadtest"+res+"@gmail.com",
        	"password": "test1234"
        }
      

        response = self.client.post(url = "/signup",name="Signup",data=json.dumps(signup_data),auth=None, headers=headers)
        
        user_id['user_id'] = response.json()['user_id']
         
        email_id['email_id'] = response.json()['email']

    @seq_task(2)
    def login(self):
        
        login_data = {
            "user_name": email_id['email_id'],
            "password": "test1234"   
                    } 

        response = self.client.post(url = "/login",name="login",data=json.dumps(login_data),auth=None, headers=headers)
   
        headers['embibe-token']= response.cookies['preprod-embibe-token']
        
        
    @seq_task(3)
    def getSearchResults(self):
        
        # generate some integers for size value
        global value
        for _ in range(1000):
            value = randint(1, 1000)

        response = self.client.get(url = f"/search/results?query=magnet&user_id={user_id['user_id']}&size={value}&grade=10&goal=CBSE",name="getSearchResults",data=body, headers=headers)
        
    @seq_task(4)
    def getSearchSuggestions(self):
    
        response = self.client.get(url = f"/search/suggestions?query=magnet&user_id={user_id['user_id']}&size={value}&grade=10&goal=CBSE",name="getSearchSuggestions",data=body, headers=headers)

        
    @seq_task(5)
    def conceptconnect(self):
    
        rnum = randrange(len(Params)-1)
       
        # response = self.client.get(url = f"/concepts/connected/{Params[rnum][0]}?content_id={Params[rnum][1]}",name="conceptconnect",data=body, headers=headers)
        response = self.client.get(url = f"/concepts/connected/new_KG4607?content_id={Params[rnum][1]}",name="conceptconnect",data=body, headers=headers)
        
    @seq_task(6)
    def conceptmoreconnect(self):
    
        rnum = randrange(len(Params)-1)
        
        print (Params[rnum][0],Params[rnum][1])
       
        # response = self.client.get(url = f"/concepts/more/{Params[rnum][0]}?content_id={Params[rnum][1]}",name="conceptmoreconnect",data=body,headers=headers)
        
        response = self.client.get(url = f"/concepts/more/new_KG4607?content_id={Params[rnum][1]}",name="conceptmoreconnect",data=body,headers=headers)
        
        
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
        
        rnum = randrange(len(Params)-1)
                
        response = self.client.get(url = f"/cg/related_data/{Params[rnum][0]}",name="getRelatedData",data=body, headers=headers)
        
    @seq_task(10)
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
        
        response = self.client.post(url = "/content-status",name="updateStatus",data=json.dumps(contentstatus_data), headers=headers)
   
    @seq_task(11)
    def getStatus(self):
    
        rnum = randrange(len(Params)-1)

        print (Params[rnum][1],Params[rnum][2],user_id['user_id'])
        # response = self.client.get(url = f"/content-status/{Params[rnum][1]}/{Params[rnum][2]}?child_id={user_id['user_id']}",name="getStatus",headers=headers)
        response = self.client.get(url ="/content-status/abc/Video?child_id=423423525",name="getStatus",headers=headers)
        
        
    # @seq_task(12)
    # def getChapterList(self):

        # response = self.client.get(url = "/chapters",name="getChapterList",data=body, headers=headers)
        # logging.info('Headers for getChapterList API is %s',response.content)
        
        chapterid['chapterid'] = response.json().get("id","5e79df54810bc73565cb2696")
 
    @seq_task(12)
    def getChapterDetail(self):
    
        response = self.client.get(url = f"/chapters/chapterDetail/{chapterid['chapterid']}",name="getChapterDetail",data=body, headers=headers)
       
    @seq_task(13)
    def getChapterList_subject(self):

        response = self.client.get(url = "/chapters/Chemistry",name="getChapterList_subject",data=body, headers=headers)
        
    @seq_task(14)
    def concept_prerequisites(self):
    
        rnum = randrange(len(Params)-1)
   
      
        response = self.client.get(url = f"/concepts/prerequisites/new_KG4607?content_id={Params[rnum][1]}",name="concept_prerequisites",data=body, headers=headers)
        
    @seq_task(15)
    def getContentDetails(self):
    
        rnum = randrange(len(Params)-1)
    
        contentdetails_data = {
            "child_id" : user_id['user_id'],
            "grade" : "10",
            "goal" : "CBSE"
        }
 
        response = self.client.get(url = f"/contentDetails/{Params[rnum][2]}/{Params[rnum][1]}",name="getContentDetails",data=json.dumps(contentdetails_data),
        headers=headers)

        
    @seq_task(16)
    def getUserHome(self):
    
        home_data = {
            "board":"CBSE",
            "child_id":user_id['user_id'],
            "goal":"CBSE",
            "grade":"10"
         }
    
        response = self.client.post(url = "/userHome",name="getUserHome",data=json.dumps(home_data), headers=headers)
        
    @seq_task(17)
    def getConceptDetails(self):

        rnum = randrange(len(Params)-1)
        rnum1 = randrange(len(Params)-1)
        rnum2 = randrange(len(Params)-1)
        
        response = self.client.get(url = f"/concept/content?conceptIds={Params[rnum][0]},{Params[rnum1][0]},{Params[rnum2][0]}",name="getConceptDetails",data=body, headers=headers)
        
    @seq_task(18)
    def getnextConceptDetails(self):
        
        rnum = randrange(len(Params)-1)    
        
        #response = self.client.get(url = f"/concepts/next/{Params[rnum][0]}",name="getnextConceptDetails",data=body, headers=headers)
        response = self.client.get(url = f"/concepts/next/new_KG4607",name="getnextConceptDetails",data=body, headers=headers)
        
    @seq_task(19)
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
    
        response = self.client.post(url = "/event",name="postLike_Event",data=json.dumps(event_data), headers=headers)
        
    @seq_task(20)
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
    
        response = self.client.post(url = "/like",name="getLikes",data=json.dumps(like_data), headers=headers)
        
    @seq_task(21)
    def getBookmark(self):
    
        rnum = randrange(len(Params)-1)
    
        bm_data = {
            "content_id":Params[rnum][1],
            "content_type":Params[rnum][2],
            "bookmarked": True,
            "timestamp": 5,
            "child_id": user_id['user_id']
        }
    
        response = self.client.post(url = "/bookmark",name="getBookmark",data=json.dumps(bm_data), headers=headers)
        
    @seq_task(22)
    def getBookmark_child(self):
 
        response = self.client.get(url = f"/bookmark?child_id={user_id['user_id']}",name="getBookmark_child",data=body, headers=headers)
        
    @seq_task(23)
    def like_child(self):
 
        response = self.client.get(url = f"/like?child_id={user_id['user_id']}",name="like_child",data=body, headers=headers)
        
    @seq_task(24)
    def connected_profiles(self):
 
        response = self.client.get(url = "/user/profile/connected_profiles",name="connected_profiles",data=body, headers=headers)
        
    @seq_task(25)
    def profiles_exists(self):
        #Checking userid here for profile id
        response = self.client.get(url = f"/user/profile/exists?id={user_id['user_id']}",name="profiles_exists",data=body, headers=headers)
        
    # @seq_task(27)
    # def forgotpwd(self):
    
        # pwd_data = {
            # "login":"9560486632"
        # }
 
        # response = self.client.post(url = "/user/forgot-password",name="forgotpwd",data=json.dumps(pwd_data), headers=headers)
        
    # @seq_task(28)
    # def resetpwd_otp(self):
    
        # #mobile no needs to be added   
        # reset_data = {
            # "new_password":"12345678",
            # "login":"9560486632"
        # }
 
        # response = self.client.put(url = "/user/reset-password-via-otp/1222",name="forgotpwd",data=json.dumps(reset_data), headers=headers)
        
    # @seq_task(29)
    # def validate_otp(self):
    
        # otp_data = {
            # "otp" : "1234",
            # "login":"9770181024"
        # }
 
        # response = self.client.get(url = "/user/is-reset-password-otp-valid",name="validate_otp",data=json.dumps(otp_data), headers=headers)
        
    @seq_task(26)
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
 
        response = self.client.post(url = "/addUser",name="add_user",data=json.dumps(user_data), headers=headers)
       
class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence
