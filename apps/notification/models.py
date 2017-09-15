import boto3
import base64
import json
from boto3.dynamodb.conditions import Key, Attr
from django.conf import settings


class Notification():
    index_name = 'id-timestamp-index'
    limit = 50
    ordering = False  # False = sort order descending
    args = {}

    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name=settings.DYNAMODB_REGION)
        self.table = dynamodb.Table(settings.DYNAMODB_TABLE)

    def execute(self):
        results = self.table.query(**self.args)
        output={
            "items": results['Items']
        }
        if "LastEvaluatedKey" in results:
            output["next"] = self.encode_pagination(results["LastEvaluatedKey"])

        return output

    def query(self, id):
        args = {
            "IndexName" : self.index_name,
            "ScanIndexForward": self.ordering,
            "Limit": self.limit,
            "KeyConditionExpression": Key('id').eq(str(id))
        }
        return args

    def encode_pagination(self, key):
        key['timestamp'] = int(key['timestamp'])
        b64key = json.dumps(key)
        return base64.b64encode(b64key.encode()).decode()

    def decode_pagination(self, data):
        key = base64.b64decode(data)
        return json.loads(key.decode())


    def run(self, id, page=None):
        self.args = self.query(id)
        if page:
            self.args['ExclusiveStartKey'] = self.decode_pagination(page)
        return self.execute()


    def update(self, id):
        print('ok')


