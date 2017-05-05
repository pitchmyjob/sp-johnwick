import boto3
import json


class States():
    states = None
    user = None
    datas = None

    def __init__(self, user=None):
        self.user = user
        self.sfn = boto3.client('stepfunctions')

    def execute(self):
        self.sfn.start_execution(
             stateMachineArn=self.states,
             input=json.dumps(self.get_input())
        )

    def get_input(self):
        input = {}
        if self.user:
            input['id'] = self.user
        if self.datas:
            input = {**input, **self.datas}
        return input


class SyncUser(States):
    states = 'arn:aws:states:eu-west-1:074761588836:stateMachine:syncUser-KV3A7ZQ1H2XB'

    def createUser(self, user):
        self.datas = {
            "type" : "add",
            "datas" : {
                "first_name" : user.first_name,
                "last_name" : user.last_name,
                "username" : user.username,
                "email" : user.email,
                "photo": str(user.photo.url),
                "lang" : user.lang
            }
        }
        self.execute()

    def updateFcm(self, fcm):
        self.datas = {
            "type": "fcm",
            "datas": fcm
        }
        self.execute()

    def updateUser(self, datas):
        self.datas = {
            "type": "update",
            "datas": datas
        }
        self.execute()


class FollowUser(States):
    states = 'arn:aws:states:eu-west-1:074761588836:stateMachine:followUser-AJFXMBBSNJYJ'

    def follow(self, follow):
        self.datas = {
            "follow" : [follow] if isinstance(follow, int) else follow
        }
        self.execute()


class AskUser(States):
    states = 'arn:aws:states:eu-west-1:074761588836:stateMachine:askUser-ACPYDJCWGKMR'

    def ask(self, ask, tags):
        self.datas = {
            "ask" : {
                "id" : ask.id,
                "text": ask.text,
                "tags": list(tags)
            }
        }
        self.execute()