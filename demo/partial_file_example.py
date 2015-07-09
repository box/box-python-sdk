# Example of the following api call
# curl -L https://api.box.com/2.0/files/FILE_ID/content -H "Authorization: Bearer ACCESS_TOKEN" -H "Range: bytes=0-60"

from boxsdk import OAuth2
from boxsdk import Client


oauth = OAuth2(
    client_id='client_id',
    client_secret='client_secret'
)
dev_access_code = 'Developer_token'
oauth._access_token =dev_access_code

client = Client(oauth)
items = client.folder(folder_id='0').get_items(limit=100, offset=0)

# prints items for later user
for i in items:
    print i.id

def range_test(id):
    bytes = [0,60]
    k = client.file(file_id=id).content(bytes=bytes)
    print k


if __name__ =='__main__':
    range_test('FILE_ID')
