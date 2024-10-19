import json
import boto3
from boto3.dynamodb.conditions import Key
#imports are used in the AWS Lambda editor

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ToDoItems')

def lambda_handler(event, context):
    http_method = event.get('httpMethod')

    if http_method == 'GET':
        return get_all_todos()
    elif http_method == 'POST':
        return create_todo_item(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported HTTP method')
        }
        
def get_all_todos():
    response = table.scan()
    items = response['Items']
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
    

def create_todo_item(event):
    body = json.loads(event['body'])
    item_id = body.get('ItemId')
    task = body.get('Task')

    table.put_item(Item={
        'ItemId': item_id,
        'Task': task
    })

    return {
        'statusCode': 201,
        'body': json.dumps('Item created successfully')
    }
    
    
