import time  
import boto3 
db=boto3.resource('dynamodb')
table =db.Table("simen")
