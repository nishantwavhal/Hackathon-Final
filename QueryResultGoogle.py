'''
Created on May 23, 2018

@author: Nishant_Wavhal
'''

class QueryResultGoogle(object):
    action=''
    parameters=''
    allRequiredParamsPresent=''
    outputContexts=''
    intent=''
    intentDetectionConfidence=''
    diagnosticInfo=''
    languageCode=''
    querytext=''


    def __init__(self, action=None,parameters=None,allRequiredParamsPresent=None,outputContexts=None,intent=None,intentDetectionConfidence=None,diagnosticInfo=None,languageCode=None,querytext=None):
        self.action=action
        self.parameters=parameters
        self.allRequiredParamsPresent=allRequiredParamsPresent
        self.outputContexts=outputContexts
        self.intent=intent
        self.intentDetectionConfidence=intentDetectionConfidence
        self.diagnosticInfo=diagnosticInfo
        self.languageCode=languageCode
        self.querytext=querytext
        