import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
iot = boto3.client('iot-data')
print(iot)
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('simen')
    
    response = table.scan()
    items = response['Items']
    print(items)
    # TODO implement
    
    print ( event )
# import json
# import boto3
 
# # ②Functionのロードをログに出力
# print('Loading function')  
 
# # ③ AWS IoT Data Planeオブジェクトを取得
# iot = boto3.client('iot-data')
 
# # ④Lambdaのメイン関数
# def lambda_handler(event, context):
    
#     # ⑤トピックを指定
#     topic = 'test/pub'
#     # ⑥メッセージの内容
#     payload = {
#         "message": "Lambda test"
#     }
    
#     try:
#         # ⑦メッセージをPublish
#         iot.publish(
#             topic=topic,
#             qos=0,
#             payload=json.dumps(payload, ensure_ascii=False)
#         )
 
#         return "Succeeeded."
    
#     except Exception as e:
#         print(e)
#         return "Failed."

# import boto3
# client = boto3.client('iot')

# def lambda_handler(event, context):
#     name = '$aws/things/simen/shadow/name/kp'
#     print ("8888888888888888888888888")
    
#     response = client.describe_thing_registration_task(taskId=name)
#     #response = client.describe_thing_group(thingName=name)
#     print (response)
#     print ("999999999999999999999999999")
