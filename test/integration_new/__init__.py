from boxsdk.client import Client
from boxsdk import JWTAuth


config = JWTAuth.from_settings_file('/Users/lsocha/demo-jwt.json')
client = Client(config)
user_to_impersonate = client.user(user_id='17815542202')
client = client.as_user(user_to_impersonate)
