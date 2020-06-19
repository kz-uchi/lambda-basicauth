import json
import base64

accounts = [
  {
    "user": "username",
    "password": "passwordstring"
  }
]

def lambda_handler(event, context):
  request = event.get("Records")[0].get("cf").get("request")
  headers = request.get("headers")

  authorization_header = headers.get("authorization")

  if not check_authorization_header(authorization_header):
    return (
      'headers': {
        'www-authenticate': [
          {
            'key': 'WWW-Authenticate',
            'value': 'Basic'
          }
        ]
      },
      'status': 401,
      'body': 'Unauthorized'
    )
  return request

def check_authorization_header(authorization_header: list) -> bool:
  if not authorization_header:
    return False
  
  for account in accounts:
    encode_value = base64.b64decode("{}.{}".format(account.get("user"),account.get("password")).encode('utf-8'))
    check_value = "Basic {}".format(encode_value.decode(encoding='utf-8'))

    if authorization_header[0].get("value") == check_value:
      return True
  
  return False
