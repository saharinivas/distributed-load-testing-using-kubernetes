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
        response = self.client.post('/user_ms_lt/auth/sign_in', data=json.dumps(login_data), headers=headers)
        headers ['embibe-token']= response.headers['embibe-token']
     

    @seq_task(2)
    def TestSelection(self):
      
        response = self.client.get(url = "/content_ms_lt/v2/mocktest-bundles/get-latest-version-meta?mocktest_bundle_path="+ mocktest_bundle_path,
        headers=headers, data = body)
        
    @seq_task(3)
    def StartTest(self):  
        
        response = self.client.get(url = "/testsubmission_ms/now", headers=headers, data = body)

        global starttime
        starttime = "".join(chr(x) for x in response.content)
        
    @seq_task(4)
    def TestWindow(self):    
    
        response = self.client.get(url = "/testsubmission_ms/v1/test/mb118/session", headers=headers, data = body)
        headers ['browser-id']= '1588163045400.5'
    
    @seq_task(5)
    def TestSession(self):    
        
        TestSession_data = '{"mocktest_session":{"goal_code":"engineering","t_started":'+starttime+'}}'
        response = self.client.post(url = "/testsubmission_ms/v1/test/mb118/session", headers=headers, data = TestSession_data)
        global session_id 
        session_id = response.json().get("id","")
      
    @seq_task(6)
    def TestQuestionCode(self):

        response = self.client.get(url = "/testsubmission_ms/v1/test/mb118/questions", headers=headers, data = body)
        
    @seq_task(7)
    def TestAnswer(self):
            
        TestAnswer_data= "[{\"eorder\":1,\"event_type\":\"load_paper\",\"sequence\":\"\",\"sent\":false,\"section\":\"\",\"event_info\":\"\",\"t\":1588163054.363,\"question_code\":\"\"},{\"eorder\":2,\"event_type\":\"view_question\",\"sequence\":1,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163054.769,\"question_code\":\"EM0076224\"},{\"eorder\":3,\"event_type\":\"select_answer\",\"sequence\":1,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0076224-b\",\"t\":1588163060.747,\"question_code\":\"EM0076224\"},{\"eorder\":4,\"event_type\":\"save_attempt\",\"sequence\":1,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0076224-b\",\"t\":1588163062.573,\"question_code\":\"EM0076224\"},{\"eorder\":5,\"event_type\":\"view_question\",\"sequence\":2,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163062.574,\"question_code\":\"EM0079578\"},{\"eorder\":6,\"event_type\":\"select_answer\",\"sequence\":2,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0079578-d\",\"t\":1588163063.3915,\"question_code\":\"EM0079578\"},{\"eorder\":7,\"event_type\":\"save_attempt\",\"sequence\":2,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0079578-d\",\"t\":1588163064.1645,\"question_code\":\"EM0079578\"},{\"eorder\":8,\"event_type\":\"view_question\",\"sequence\":3,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163064.1665,\"question_code\":\"EM0017239\"},{\"eorder\":9,\"event_type\":\"select_answer\",\"sequence\":3,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0017239-d\",\"t\":1588163064.8975,\"question_code\":\"EM0017239\"},{\"eorder\":10,\"event_type\":\"save_attempt\",\"sequence\":3,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0017239-d\",\"t\":1588163065.4985,\"question_code\":\"EM0017239\"},{\"eorder\":11,\"event_type\":\"view_question\",\"sequence\":4,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163065.5005,\"question_code\":\"EM0131889\"},{\"eorder\":12,\"event_type\":\"select_answer\",\"sequence\":4,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0131889-c\",\"t\":1588163066.0635,\"question_code\":\"EM0131889\"},{\"eorder\":13,\"event_type\":\"save_attempt\",\"sequence\":4,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0131889-c\",\"t\":1588163066.6655,\"question_code\":\"EM0131889\"},{\"eorder\":14,\"event_type\":\"view_question\",\"sequence\":5,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163066.6665,\"question_code\":\"EM0040436\"},{\"eorder\":15,\"event_type\":\"select_answer\",\"sequence\":5,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0040436-d\",\"t\":1588163067.1775,\"question_code\":\"EM0040436\"},{\"eorder\":16,\"event_type\":\"save_attempt\",\"sequence\":5,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0040436-d\",\"t\":1588163067.6725,\"question_code\":\"EM0040436\"},{\"eorder\":17,\"event_type\":\"view_question\",\"sequence\":6,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163067.6745,\"question_code\":\"EM0006429\"},{\"eorder\":18,\"event_type\":\"select_answer\",\"sequence\":6,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0006429-c\",\"t\":1588163068.2625,\"question_code\":\"EM0006429\"},{\"eorder\":19,\"event_type\":\"save_attempt\",\"sequence\":6,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0006429-c\",\"t\":1588163068.9175,\"question_code\":\"EM0006429\"},{\"eorder\":20,\"event_type\":\"view_question\",\"sequence\":7,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163068.9195,\"question_code\":\"EM0016877\"}]"
        
        response = self.client.post(url = f"/testsubmission_ms/v1/test/{session_id}/events",name ="test_answer", headers=headers, data = TestAnswer_data)
        
    @seq_task(8)
    def TestResume(self):   
    
        response = self.client.post(url = "/testsubmission_ms/v1/test/mb118/resume", headers=headers, data = body)
        
    @seq_task(9)
    def TestCheck(self):
    
        response = self.client.get(url = "/testsubmission_ms/v1/test/mb118/check", headers=headers, data = body)

        
    @seq_task(10)
    def TestEvent(self):
    
        TestEvent_data = "[{\"eorder\":6,\"event_type\":\"user_active\",\"sequence\":\"\",\"sent\":false,\"section\":\"\",\"event_info\":\"\",\"t\":1588430261.484,\"question_code\":\"\"},{\"eorder\":7,\"event_type\":\"select_answer\",\"sequence\":1,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0131893-b\",\"t\":1588430262.243,\"question_code\":\"EM0131893\"},{\"eorder\":8,\"event_type\":\"save_attempt\",\"sequence\":1,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0131893-b\",\"t\":1588430264.2805,\"question_code\":\"EM0131893\"},{\"eorder\":9,\"event_type\":\"view_question\",\"sequence\":2,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430264.2815,\"question_code\":\"EM0132079\"},{\"eorder\":10,\"event_type\":\"select_answer\",\"sequence\":2,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0132079-d\",\"t\":1588430265.8865,\"question_code\":\"EM0132079\"},{\"eorder\":11,\"event_type\":\"save_attempt\",\"sequence\":2,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0132079-d\",\"t\":1588430267.7745,\"question_code\":\"EM0132079\"},{\"eorder\":12,\"event_type\":\"view_question\",\"sequence\":3,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430267.7755,\"question_code\":\"EM0017321\"},{\"eorder\":13,\"event_type\":\"select_answer\",\"sequence\":3,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0017321-b\",\"t\":1588430268.8505,\"question_code\":\"EM0017321\"},{\"eorder\":14,\"event_type\":\"save_attempt\",\"sequence\":3,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0017321-b\",\"t\":1588430269.8185,\"question_code\":\"EM0017321\"},{\"eorder\":15,\"event_type\":\"view_question\",\"sequence\":4,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430269.8195,\"question_code\":\"EM0132187\"}]"
        
        response = self.client.post(url = f"/testsubmission_ms/v1/test/{session_id}/events", name="test_event", headers=headers, data = TestEvent_data)

        
    @seq_task(11)
    def TestEvent1(self):
    
        TestEvent1_data = "[{\"eorder\":19,\"event_type\":\"save_attempt\",\"sequence\":5,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430294.1555,\"question_code\":\"EM0131900\"},{\"eorder\":20,\"event_type\":\"view_question\",\"sequence\":6,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430294.1565,\"question_code\":\"EM0016143\"},{\"eorder\":21,\"event_type\":\"select_answer\",\"sequence\":6,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0016143-c\",\"t\":1588430295.1745,\"question_code\":\"EM0016143\"},{\"eorder\":22,\"event_type\":\"save_attempt\",\"sequence\":6,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0016143-c\",\"t\":1588430296.1545,\"question_code\":\"EM0016143\"},{\"eorder\":23,\"event_type\":\"view_question\",\"sequence\":7,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430296.1545,\"question_code\":\"EM0131903\"}]"
        response = self.client.post(url = f"/testsubmission_ms/v1/test/{session_id}/events",name ="test_event1",headers=headers, data = TestEvent1_data)

        
    @seq_task(12)
    def TestEventFreeze(self):
    
        TestEventFreeze_data = "[{\"eorder\":24,\"event_type\":\"freeze\",\"sequence\":\"\",\"sent\":false,\"section\":\"\",\"event_info\":\"\",\"t\":1588430329.112,\"question_code\":\"\"}]"
        response = self.client.post(url = f"/testsubmission_ms/v1/test/{session_id}/events",name = "TestEventFreeze" ,headers=headers, data = TestEventFreeze_data)

        
    @seq_task(13)
    def TestSubmission(self):
    
        response = self.client.get(url = "/testsubmission_ms/v1/test/mb118/session", headers=headers, data = body)

        
    @seq_task(14)
    def TestSummary(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/{session_id}/summary", name = "TestSummary" ,headers=headers, data = body)
        global user_id
        user_id = response.json()["userId"]
        
        
    @seq_task(15)
    def ExamSubmit(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/{session_id}/behaviour?examCode=ex4&level=exam&levelCode=ex4",name = "exam_submit" ,headers=headers, data = body)

        
    @seq_task(16)
    def ExamQuestions(self):
    
        response = self.client.get(url = "/testsubmission_ms/v1/test/mb118/questions", headers=headers, data = body)

        
    @seq_task(17)
    def TopPerformer(self):
    
        response = self.client.get(url = "/testsubmission_ms/v1/test/mb118/topPerformers", headers=headers, data = body)

        
    @seq_task(18)
    def TestSubmission1(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/{session_id}/timeSpent/summary?timeIntervalInMins=10",name = "TestSubmission1", headers=headers, data = body)

        
    @seq_task(19)
    def ChatMessages(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/{session_id}/chatMessages/history?page=1&pageSize=50", name = "ChatMessages", headers=headers, data = body)
 
        
    @seq_task(20)
    def TimeSpent(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/{session_id}/timeSpent/summary?timeIntervalInMins=180", name = "TimeSpent", headers=headers, data = body)

        
    @seq_task(21)
    def TestSummary1(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/{session_id}/concept/summary", name = "TestSummary1",headers=headers, data = body)

        
    @seq_task(22)
    def ChapterSummary1(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/{session_id}/chapter/summary",name = "ChapterSummary1", headers=headers, data = body)

        
    @seq_task(23)
    def TrueScore(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/mb118/trueScore", headers=headers, data = body)

        
    @seq_task(24)
    def Trend(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/test/{session_id}/trend",name = "Trend", headers=headers, data = body)

        
    @seq_task(25)
    def UserRank(self):
    
        response = self.client.get(url = f"/testsubmission_ms/v1/mocktest-ranks/get-user-rank?user_id={user_id}&testCode=mb118", name = "UserRank",headers=headers, data = body)

        
    @seq_task(26)
    def SocialAccuracy(self):
    
        response = self.client.get(url = "/testsubmission_ms/v1/test/mb118/socialAccuracy", headers=headers, data = body)

        
    @seq_task(27)
    def chatmessages1(self):
    
        chat_data = "{\"context\":null,\"intent\":\"FirstGreet\",\"update\":null}"
        response = self.client.post(url = f"/testsubmission_ms/v1/test/{session_id}/chatMessages", name = "chatmessages1", headers=headers, data = chat_data)

     
class WebsiteTest(HttpLocust):
    task_set = MyTaskSequence

               
              
        

