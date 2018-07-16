from flask import Flask
from flask import Response
import flask
import uuid
import requests
import config
import json
from flask import render_template, Flask, request, redirect, url_for, session, flash, escape, send_file, jsonify, json, make_response
#from dialogflow_v2.proto.session_pb2 import QueryResult
from QueryResultGoogle import QueryResultGoogle
import pysnow
from BusinessService import BusinessService
from JsonService import JsonService
#from google.gax.utils.metrics import stringify
import numpy
import cv2
from cv2 import imread, imreadmulti


try:
      import Image
except ImportError:
        from PIL import Image
import pytesseract

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

SESSION = requests.Session()
PORT = 5000  # A flask app by default runs on PORT 5000
AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = 'http://localhost:{}/getAToken'.format(PORT)
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' + 
                      'response_type=code&client_id={}&redirect_uri={}&' + 
                      'state={}&resource={}')


@app.route("/")
def main():
    
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    # Include the above line, if you don't have tesseract executable in your PATH
    # Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    
    # Simple image to string
    print(pytesseract.image_to_string(Image.open('C:\\Users\\Nishant_Wavhal\\Desktop\\test.png')))
    
    # French text image to string
    #print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))
    
    # Get bounding box estimates
    print(pytesseract.image_to_boxes(Image.open('C:\\Users\\Nishant_Wavhal\\Desktop\\test.png')))
    
    # Get verbose data including boxes, confidences, line and page numbers
    print(pytesseract.image_to_data(Image.open('C:\\Users\\Nishant_Wavhal\\Desktop\\test.png')))
    
    # Get informations about orientation and script detection
    print(pytesseract.image_to_osd(Image.open('C:\\Users\\Nishant_Wavhal\\Desktop\\test.png')))
     
    
    #img=cv2.imread('C:\\Users\\Nishant_Wavhal\\Desktop\\test.png')
    #string123 = pytesseract.image_to_string(Image(img))
    #print(string123)
    #print(pytesseract.image_to_string(Image(img))
    #print('imread'+imread('C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'))
    # OR explicit beforehand converting
    #print(pytesseract.image_to_string(Image.fromarray(img)))
    
    return (pytesseract.image_to_string(Image.open('C:\\Users\\Nishant_Wavhal\\Desktop\\test.png')))
    
    
    
    

def selectInfoList(incNumber,shortDescription):
    imgUrl = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAwFBMVEX////RIytkZGRdXV1ZWVlhYWFcXFykpKTRICnOAABYWFjTKTHQHSaysrLQGCLh4eH29vbt7e377e7R0dHXRkzcbG/22NnQDBnb29vw8PDPDBmJiYnn5+eUlJStra3PABB0dHTGxsaAgIBra2uZmZm+vr7mlJfUNDv56Onxxcf+9/fppqjbXmP22tvgeHzuubvhgoXnmp3sr7HUOD/YUlfhiozww8Xdb3Lzzs/dZGnge37mlZjXQ0naT1XutrhNTU1bRW+TAAAHiklEQVR4nO2Ya3OqyhKGuYsEuejaEREFUaPBXFcuS9dOdv7/vzrdA4OArhP3l1N1qt6nKhWmgWHe6ZnuHhUFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/2ckUeQHp7aw+1zQfeg84ZnuAj/yJ5eNpnh/Ly578kKSlalblqVng+OoRlNh0nqVyN50oSiDpW6aAyVZWoPm+wN9GSpTa1o1/ZVWdrduiFxnla1qPz69benf7cOLa3/c3LcH9Nnvf9SN4d93N2f03v86PNLN3e0FAudfpqaZ/GeZi9IU5g61Gd2ZsyHQTcOfCuNXtHA0Jzq+71NzkRiVLZjJV01DG8n50gyzZRt6cZwOt699z7VtN+4/NTXcj1W1Lw3DeOylf50MuvBir/+mvB4+998LdDTT0bNc45E54vu+ZtJYDGrq9LficdPgMmE0jTU3ZscOVqamB76uGfzuJNNppqgrhzSZTumygcPX8o9ncXhlq97vF0+tSO+qztix16xwyFKFQlu1va0ULy8eU1X1HpTD5/PP7wQmJDATupKVoZk5XYTkUEvYJnOdxjoQCkm1tRotpk6izFiT7CAgSSulUhjw3CzXvLSjGU8R+5V8rhkrn6eObZZfKlQ9W3XJl66QuOO+9mr8sZUKt5uxShp/0P20dNStGntX5Yp+oslJH5Xdw+HbHTu3tKUc7chy2Dc5aZnLCeAhh0Jh6SSFHo4szZIbSllYmuNLhTNd06f1nXLGQov6kOt1bQmbUKiq45en3fNrTFe2SiPdeq7qfUiFHx5NQKHs6HZ8I15mn3uf4vLDbXj2vzMzzVXdWK9o/CNH03u1aWSxXFbYMGammcnrXFyXCqNy/HV3hkmzR6qtUW3r6ezYUuH4WTiANagphYwHFvMgFf7lCWnXfZJ14OeuU54KoWvokv8/LxLICvO2hVxotpqkgBUayXHo5LeqlZC0tVS4IjFJ493sa6UETmvXhiZPlVAYP1e2A2t5UwpSYLuFVDgkafamUGzaiDY/9ncs/P4PXe7T2rHfQqtUnzXzHg+hmQzWNOkTEWmOtuDo5jkFo0AqbIcg2seRWKtOU7WYMVbovkjTO4eNXyJ6jH8eI80NKervlQfS3+fdV65sjwPrc1xvzm+hME/BL5/X2T2i3bMaHKFQaUSd8Enx06x277Jc5UJh6GjWovsBWpZ6o7sBLRGnVPhDPrLti4HzsOPtUeE9O2qn/FMJv6enXNp+V7S0eQWPLxNIPuIsYeqGmfXEVC9Ysn7E5BATtLYhTYNTxR2+iKRCmhwOlG2m1IHe7q+rcFgq/E2h5aM4KixisXi3Y5EYeLu6hx8279iCAo131/3SH/Fz3RIJX3fyUMTGlkLiixW26xhaa8KnsyrmCIUjQ9OTbvddhdzfeYWUAYStVkjhxHtTlFd2nEgb6f7NU70nZVu59XKNg+nSsViklrBCs9dmoJwopFhjUZUZGFXekD40om7npHDZ6W/xR4UcWajgce0+mYtxGU7eeNMNt5wBOcSQWt6x/ctyRU0QLrgoI4dEnchQ3u4qnJhCGgfVoFY4cRp5UkL7UDv53FmFnDVSDik7z+MCgAPmeFf+T/c/x7xWi41NYYdi'
    returnInfoList = '{"info": {"key": "'+incNumber+'",},"title": "'+incNumber+'","description": "Short Description:'+shortDescription+'","image": {"imageUri": "'+imgUrl+'","accessibilityText": "Incident Number"}},'
    return returnInfoList

def selectList(incList):
    returnSelectList = '{"listSelect":{"title": "MyList","items":['+incList+']}}'
   # returnSelectList = JsonService('listSelect',returnSelectList)
    '''print('printing list .. '+str(returnSelectList))'''
    return  returnSelectList

def userIncList(userRes,userName):
    # Create client object
    c = pysnow.Client(instance='dev34640', user='admin', password='Mohan@8391')
    # Define a resource, here we'll use the incident table API
    incident = c.resource(api_path='/table/incident')
    result = incident.get(query={'caller_id':'6033415bdb021300ea6e5c00cf961963'})
    '''print('User name for '+str(result))'''
    allUserInc = []
    count = 0 
    for record in result.all():
        incNumber = record['number']
        shortDescription = record['short_description']
        incState = record['state']
        '''print('inc '+incNumber)
        print(incState)'''
        allUserInc.append(selectInfoList(incNumber,shortDescription))
        infoList = str(''.join(allUserInc[:5]))
        '''print('array ',infoList[:-1])'''
        selectIncList = selectList(infoList[:-1])
        '''print('select list is '+str(selectIncList))
    print("All user inc/s are "+str(selectIncList))'''
    return selectIncList



def webhookResponse(fullfillmentText,followup,fullfillmentMsg=JsonService()):
    
    
    #print('Fulfilllment card'+fullfillmentMsg.jsonRichResMsg)
    if((fullfillmentMsg != None) and ((str(fullfillmentMsg.jsonRichResMsg)=='card') or (str(fullfillmentMsg.jsonRichResMsg)=='Listselect'))):
        RichMsg=fullfillmentMsg.jsonRestStr
    else:
        '''RichMsg={
            "text": {
                "text": [
                   fullfillmentText
                ]
            }
        }'''
        RichMsg={
            "simpleResponses": {
                "simpleResponses": [{
                   "textToSpeech": fullfillmentText,
                      "ssml": False,
                      "displayText": fullfillmentText}
                ]
            }
        }
        
        
    if((fullfillmentMsg != None) and (str(fullfillmentMsg.jsonRichResMsg)=='googlelist')):
        RichMsgGoogle=fullfillmentMsg.jsonRestStr   
    else:  
      RichMsgGoogle={}
    res =jsonify({"fulfillmentText": fullfillmentText,
                    "fulfillmentMessages":[RichMsg],
                    "source": "example.com",
                    "payload": {
                    "google": {}
                         },
                        "outputContexts": [
                          
                        ],
                        "followupEventInput": {
                          
                        }
                        
                        
     })
    
                        
                                
               
    print(res)
    
    return res


def createIncident(userInput,sessionID,q=QueryResultGoogle()):
    
    # call function to find assignment group
    # Set the payload
    # Create client object
    client = pysnow.Client(instance='dev34640', user='admin', password='Mohan@8391')
    param=q.parameters
    qtext=q.querytext
    # Define a resource, here we'll use the incident table API
    incident = client.resource(api_path='/table/incident')
    businessName = findAssignmentGroup(param['Application'],client)
    
    SupportGroup=str(businessName.supportGroup['value'])   
    
    print('sys idddd'+businessName.appName)
    new_record = {
        'short_description': str(qtext),
         'business_service':str(businessName.appName),
        'description': '',
        'u_dialogflow_session':sessionID,
        'assignment_group':SupportGroup,
        'caller_id':'6033415bdb021300ea6e5c00cf961963',
        'contact_type':'Bot',
    }
    # Create a new incident record
    result = incident.create(payload=new_record)
    
    ''' print('application name for assignment group '+str(param['Application']))'''
    #updateIncident(client,incident,userInput,applicationName)
    #print('printing result '+str(result))
    for record in result.all():
        incNumber = (record['number'])
        print("test this inc",record['number'])
        shortDescription = (record['short_description'])
        '''print(record['u_dialogflow_session'])
        print(record['assignment_group'])
        print(record['caller_id'])'''
    #updateIncident(incNumber)
    #Msg= returnCardRes(incNumber,shortDescription)
    return result
    
def returnCardRes(incNumber,shortDescription):
    imgUrl = 'data:image/png;base64,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'
    desc="short description: "+shortDescription
    serNowUrl = 'https://dev34640.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number='+incNumber
    returnResponse ={"card":{"title":incNumber,"subtitle":desc,"imageUri":imgUrl,"buttons":[{"text":"Visit URL","postback":serNowUrl}]}}
    jRichMsg = JsonService('card',returnResponse)
    #print('jRich message '+str(jRichMsg.jsonRichResMsg))
    #print(returnResponse)
    return  jRichMsg



def findAssignmentGroup(applicationName,client):
    # Define a resource, here we'll use the incident table API
    bs=BusinessService()
    incident = client.resource(api_path='/table/cmdb_ci_service')
    response = incident.get(query={'name':applicationName})
    #print('Application name for '+str(response))
    for record in response.all():
          if( record['sys_id']!=None):
            bs.appName = record['sys_id']
            bs.ownedBy = record['owned_by']
            bs.supportGroup = record['support_group']
          else:
            bs.appName = 'ServiceExchange'
            bs.ownedBy = 'Nishant Wavhal'
            bs.supportGroup = '0873d3fcdbd21300ea6e5c00cf9619af'
            #print(applicationName)
    #print('applicationName'+str(bs.appName))
    #print('ownedBy'+str(bs.ownedBy))
    #print('supportGroup'+str(bs.supportGroup))
    
    return bs


def queryResult(qResult):
    q=QueryResultGoogle()
    for the_key, the_value in  qResult.items():
            if(the_key=='action'):
                q.action=the_value
                print(q.action)
            if(the_key=='parameters'):
                q.parameters=the_value
                print(q.parameters)
            if(the_key=='allRequiredParamsPresent'):
                q.allRequiredParamsPresent=the_value
                print(q.allRequiredParamsPresent)
            if(the_key=='outputContexts'):
                q.outputContexts=the_value
                print(q.outputContexts)
            if(the_key=='intent'):
                q.intent=the_value
                print(q.intent)
            if(the_key=='intentDetectionConfidence'):
                q.intentDetectionConfidence=the_value
                print(q.intentDetectionConfidence)
            if(the_key=='diagnosticInfo'):
                q.diagnosticInfo=the_value
                print(q.diagnosticInfo)
            if(the_key=='languageCode'):
                q.languageCode=the_value
                print(q.languageCode)
            if(the_key=='queryText'):
                q.querytext=the_value
                print(q.querytext)
                
    return q 

def updateIncident(sessionID, fieldName, fieldValue):

    # Create client object
    c = pysnow.Client(instance='dev34640', user='admin', password='Mohan@8391')
    
    # Define a resource, here we'll use the incident table API
    incident = c.resource(api_path='/table/incident')
    print('in FieldName ',fieldName)
    print('in FieldValue ',fieldValue)
    
    #update = {'short_description': shortDescription,'priority':priority,'assignment_group':assignGroup, 'state': 5,'assignment_group':'17bec564db521300ea6e5c00cf961918'}
    update = {fieldName:fieldValue}
    # Update 'short_description' and 'state' for 'INC012345'
    #updated_record = incident.update(query={'number': incNumber}, payload=update)
    updated_record = incident.update(query={'u_dialogflow_session': sessionID}, payload=update)
    print('in update session id is '+sessionID)
    # Print out the updated record
    print('in update record '+str(updated_record))

def getIncDetails(sessionID):
    # Create client object
    c = pysnow.Client(instance='dev34640', user='admin', password='Mohan@8391')
    
    # Define a resource, here we'll use the incident table API
    incident = c.resource(api_path='/table/incident')
    
    # Query for incidents with session ID
    response = incident.get(query={'u_dialogflow_session': sessionID})
    
    # Iterate over the result and print out `sys_id` of the matching records.
    for record in response.all():
        incNumber = (record['number'])
        shortDescription = (record['short_description'])
        print(record['u_dialogflow_session'])
        print(record['assignment_group'])
        print(record['caller_id'])
    #updateIncident(incNumber)
    return response


def getIncident(incNumber,shortDescription):
    returnResponse = '"followupEventInput":{"name": "GetIncidentValue","languageCode": "en-US","parameters":{"number": "'+incNumber+'","short_description":"'+shortDescription+'"}'
    return returnResponse
    

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    print('Query Result'+json.dumps(req["queryResult"]))
    print('session Result'+json.dumps(req["session"]))
    sess=req["session"]
    qres= req["queryResult"]
    q=queryResult(qres)
    param=q.parameters   
 
       
    if(q.action=='IncidentCreation'):
       '''CardRes= createIncident('create',param['Application'])'''
       CardRes= createIncident('create',sess.replace('projects/serbot-636d7/agent/sessions/',''),q=queryResult(qres))
       '''res=webhookResponse('Thank You for short description ! Can you please elaborate the issue for us ?', CardRes)'''
       res=webhookResponse('Thank You   ! Can you please elaborate the issue for us ?', None,None)
       
    if(q.action=='IncidentList'):
       ListRes=userIncList('find inc','nishant_wavhal')
       print('Check'+str(ListRes))
       res=webhookResponse('Thank You ! Can you please elaborate the issue for us ?',None,ListRes)
    if(q.action=='Issues.Issues-description'):
        res = updateIncident(sess.replace('projects/serbot-636d7/agent/sessions/',''),'description',q.querytext)
        res=webhookResponse('Are you carrying any particular steps (yes/no) ?', None,None)
    if(q.action=='Issues.Issues-custom.Issues-Detail-no'):
        res1=getIncDetails(sess.replace('projects/serbot-636d7/agent/sessions/',''))
        CardRes = returnCardRes(res1['number'],res1['short_description'])
        res=webhookResponse('I have a created Incident for you ,please visit  url for more details \n :'+
         'https://dev34640.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number='+res1['number'],getIncident(res1['number'],res1['short_description']),CardRes)
    if(q.action=='Issues.Detail-yes-steps'):
        res = updateIncident(sess.replace('projects/serbot-636d7/agent/sessions/',''),'u_steps_to_reproduce',q.querytext)
        res1=getIncDetails(sess.replace('projects/serbot-636d7/agent/sessions/',''))
        CardRes = returnCardRes(res1['number'],res1['short_description'])
        res=webhookResponse('Thank You ! Can you please elaborate the issue for us ?',getIncident(res1['number'],res1['short_description']),CardRes)
    r = make_response(res)
    '''r1=str(res)
    print('Response'+stringify(res))
    print('Response'+json.loads(r1))'''
    r.headers['Content-Type'] = 'application/json'
    
    print('Final Response ',r)
    '''for record in r.items():
        print('res record '+record)'''
    
    return r
    
        
    '''if(q.action=='UpdateIncident'):
        print
    if(q.action=='Display'):
        print  '''
    

        
def login():
 
    auth_state = str(uuid.uuid4())
    SESSION.auth_state = auth_state
   
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
        
    resp = Response(status=307)
    resp.headers['location'] = authorization_url
 
    return resp



def googleResList(incNumber):
    returnResList = "{'optionInfo':{'key': "+incNumber+",'synonyms':["+incNumber+"]},'title': 'Incident Number'}"
    #jRichMsg = JsonService('googlelist',returnResList)  
    #print('jRich message '+str(jRichMsg))
    print(returnResList)
    return  returnResList


def googleCreateList(userName):
    # Create client object
    c = pysnow.Client(instance='dev34640', user='admin', password='Mohan@8391')
    # Define a resource, here we'll use the incident table API
    incident = c.resource(api_path='/table/incident')
    result = incident.get(query={'caller_id':'6033415bdb021300ea6e5c00cf961963'})
    print('User name for '+str(result))
    allUserInc = None
    count = 0 
    for record in result.all():
        incNumber = record['number']
        shortDescription = record['short_description']
        incState = record['state']
        print(incNumber)
        print(incState)
        while count != 5:
            print(incNumber)
            print(incState)
            if(allUserInc != None):
              allUserInc +=','+googleResList(incNumber)
            elif(allUserInc == None):
              allUserInc =googleResList(incNumber)
            print(count)
            count += 1
    print("All user inc/s are "+str(allUserInc))
    lser=JsonService('googlelist',str(allUserInc))
    print('iNSIDE'+str(lser))
    print('iNSIDE1'+str(lser.jsonRestStr))
    print('iNSIDE2'+str(lser.jsonRichResMsg))
    return lser

@app.route("/getAToken")
def main_logic():
    
    

   
    # Need to install requests package for python
    # easy_install requests

    # Set the request parameters
    url = 'https://dev34640.service-now.com/api/now/v1/table/incident'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'admin'
    pwd = 'Mohan@8391'

    # Set proper headers
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    # Do the HTTP request
    auth = (user,pwd)
    '''response = requests.post(url, auth=(user, pwd), headers=headers)'''
    response = make_api_call('POST',url,auth,"","")

    # Check for HTTP codes other than 200
    # Decode the JSON response into a dictionary and use the data
    
    data = response.json()
    print(data)
    print(str(response))
    return jsonify(data)
   

def createApiUrl(roomName, response):
    
    r = make_api_call('GET', 'https://outlook.office.com/api/v2.0/users/' + roomName + '/events' , str(response['access_token']), "", "").json()
    jsonString = json.dumps(r)
    valueArray = json.loads(jsonString)
    print(len(valueArray))
    '''for index in range(len(valueArray)):
     getValuesCal(index, valueArray)'''
    print('data is ' + str(r))
    
    return jsonify(r)


def getValuesCal(index, valueArray):
    valueArray = valueArray["meetingTimeSuggestions"][index]
    meetingTimeSlotData = valueArray["meetingTimeSlot"]
    '''roomLocationsName = meetingTimeSlotData["locations"]
    roomName = roomLocationsName["displayName"]'''
    locationValue = valueArray["locations"]
    for index in range(0, len(locationValue)):
     findMeetingRoom(index, locationValue, meetingTimeSlotData)
     
    print(len(locationValue))

     
def findMeetingRoom(index, locationValue, meetingTimeSlotData):
     address = locationValue[index]
     roomName = address["displayName"]
     roomEmailAddress = address["locationEmailAddress"]
     endData = meetingTimeSlotData["end"]
     endDateTime = endData["dateTime"]
     startData = meetingTimeSlotData["start"]
     startDateTime = startData["dateTime"]
     print('Meeting room name is ' + str(roomName))
     print('Meeting room email address ' + roomEmailAddress)
     print('Start Time is ' + startDateTime)
     print('End Time is ' + endDateTime)
     print ('Index is:', index)
     print (meetingTimeSlotData)
     print('**********************************End*********************************')


def getValues(index, valueArray):
    print('printing values')
    valueArray = valueArray["value"][index]
    ownerData = valueArray["Owner"]
    addressData = ownerData["Address"]
    print('email address of the owner is ' + addressData)
    print ('Owner data index is:', index)
    print (ownerData)


def make_api_call(method, url, auth,payload=None, parameters=None):
      # Send these headers with all API calls
      headers = { "Content-Type":"application/json", "Accept":"application/json"}
    
      # Use these headers to instrument calls. Makes it easier
      # to correlate requests and responses in case of problems
      # and is a recommended best practice.
      request_id = str(uuid.uuid4())
      instrumentation = { 'client-request-id' : request_id,
                          'return-client-request-id' : 'true' }
    
      headers.update(instrumentation)
    
      response = None
    
      if (method.upper() == 'GET'):
          response = requests.get(url, auth=auth, headers=headers)
      elif (method.upper() == 'DELETE'):
          response = requests.delete(url, auth=auth, headers=headers)
      elif (method.upper() == 'PATCH'):
          headers.update({ 'Content-Type' : 'application/json' })
          response = requests.patch(url, auth=auth, headers=headers)
      elif (method.upper() == 'POST'):
          headers.update({ 'Content-Type' : 'application/json' })
          response = requests.post(url, auth=auth, headers=headers)
    
      return response  


if __name__ == "__main__":
    app.run()
