import os
import requests
import json

API_KEY = os.getenv('API_KEY', 'AIzaSyAVZhXNtFnRkq0Dzx8WZLTd4hxRo-w98q4')

def check_video_copyright(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=contentDetails,status'
    response = requests.get(url)
    data = response.json()

    if 'items' in data and data['items']:
        item = data['items'][0]
        status = item['status']
        if 'copyrightClaims' in status:
            return True
    return False

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        video_id = body['video_id']
        
        if check_video_copyright(video_id):
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'This video has copyright claims.'})
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'This video does not have copyright claims.'})
            }
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Please use POST method with video_id in body.'})
    }


# For testing
video_id = input("Enter The Video ID: ")
print("Checking copyright for video ID:", video_id)

if check_video_copyright(video_id):
    print("This video has copyright claims.")
else:
    print("This video does not have copyright claims.")