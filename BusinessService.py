class BusinessService(object):
    appName=''
    ownedBy=''
    supportGroup=''


    def __init__(self, appName=None,ownedBy=None,supportGroup=None):
        self.appName=appName
        self.ownedBy=ownedBy
        self.supportGroup=supportGroup