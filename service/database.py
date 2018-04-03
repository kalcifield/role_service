import json

import boto3

with open("../config.json") as json_data:
    config = json.load(json_data)


class Dynamodb:
    def __init__(self):
        self.dynamo_db = boto3.resource(
            config["database"], region_name=config["region_name"],
            endpoint_url=config["endpoint_url"]
        )
        # boto3.set_stream_logger('botocore', level='DEBUG')
        client = boto3.client(
            config["database"], region_name=config["region_name"],
            endpoint_url=config["endpoint_url"]
        )
        try:
            client.describe_table(
                TableName=config["table_name"]
            )
        except client.exceptions.ResourceNotFoundException:
            self.dynamo_db.create_table(
                TableName=config["table_name"],
                KeySchema=[
                    {
                        'AttributeName': 'user_id',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'user_id',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
        self.table = self.dynamo_db.Table(config["table_name"])

        self.table.put_item(
            Item={
                'user_id': "example@yodafone.hu",
                'roles': ["master", "padavan", "yoda"],
            }
        )
        self.table.put_item(
            Item={
                'user_id': "csoda@yodafone.hu",
                'roles': ["padavan", "yoda"],
            }
        )
        self.table.put_item(
            Item={
                'user_id': "example3@yodafone.hu",
                'roles': ["yoda"],
            }
        )

    def load(self, user_id):
        try:
            response = self.table.get_item(
                Key={
                    'user_id': user_id,
                }
            )
            item = response['Item']
            roles = item['roles']
            return roles
        except KeyError:
            empty_list = []
            return empty_list
