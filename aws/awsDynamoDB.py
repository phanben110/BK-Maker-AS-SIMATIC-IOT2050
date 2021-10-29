import boto3
import random
from decimal import *
from boto3.dynamodb.conditions import Key, Attr


def load_transactions(dynamodb):

    tableDevice = dynamodb.Table('Device')
    tableML = dynamodb.Table('MachineLearning')

    dataDevice = {
        "ID": 10,
        "Name": "Motor",
        "Object": {
            "Online": "True",
            "PID": {
                "Kp": 2,
                "kd": 3,
                "Ki": 3},
            "Quality": {
                "Settling time": 5,
                "Steady-state error": 4,
                "Overshoot": 3},
            "Setting": {
                "Max Settling time": 4,
                "Max Overshoot": 3,
                "Max Steady-state error": 4},
            "Time": {
                "Day": "01/10/2021",
                "Time": "13:00:00"}
        }
    }

    dataML = {
        "ID": 10,
        "Name": "Motor",
        "Object": {
            "Online": "True",
            "PID": {
                "Kp": 2,
                "kd": 5,
                "Ki": 3},
            "Control": {
                "Set point": 3,
                "Control bit": 4},
            "Quality": {
                "Settling time": 5,
                "Steady-state error": 4,
                "Overshoot": 3}, 
            "Time": {
                "Day": "01/10/2021",
                "Time": "13:00:00"}
        }
    }
    tableDevice.put_item(Item=dataDevice)
    tableML.put_item(Item=dataML)
    
    print(tableML.item_count)
    #response = tableDevice.query(KeyConditionExpression=Key('ID').eq(1))
    #response = qtableDevice.scan()
    #print ( response['Items'] )
    response= tableDevice.scan(FilterExpression = Attr('ID').eq(1))
    print (response["Items"][0]["Object"])
    #print (tableDevice.query_count() )
if __name__ == '__main__':


    dynamodb = boto3.resource('dynamodb')

    load_transactions(dynamodb)








## Create the DynamoDB table.
#table = dynamodb.create_table(
#    TableName='users',
#    KeySchema=[
#        {
#            'AttributeName': 'username',
#            'KeyType': 'HASH'
#        },
#        {
#            'AttributeName': 'last_name',
#            'KeyType': 'RANGE'
#        }
#    ],
#    AttributeDefinitions=[
#        {
#            'AttributeName': 'username',
#            'AttributeType': 'S'
#        },
#        {
#            'AttributeName': 'last_name',
#            'AttributeType': 'S'
#        },
#    ],
#    ProvisionedThroughput={
#        'ReadCapacityUnits': 5,
#        'WriteCapacityUnits': 5
#    }
#)
#
## Wait until the table exists.
#table.meta.client.get_waiter('table_exists').wait(TableName='users')
#
## Print out some data about the table.
#print(table.item_count)
