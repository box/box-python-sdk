import hashlib
import os

from boxsdk import OAuth2
from boxsdk import DevelopmentClient

oauth = OAuth2(client_id='g4cz3htv6mp6sdlv9ft84izffbxicsj5', client_secret='4Qa7WxGwsp7m4aLmEdm9doOpKFs0jXS1', access_token='hvRp0vjDuVZatk7OwScaBU1ioOUBCQZ1')
client = DevelopmentClient(oauth)
copied_length = 0
test_file_path = '/Users/ccheng/Desktop/CLICCOSXLinux.mp4'
total_size = os.stat(test_file_path).st_size
sha1 = hashlib.sha1()
content_stream = open(test_file_path, 'rb')
file_to_upload = client.file('330568970271').get()
upload_session = file_to_upload.create_upload_session(total_size)
chunk = None
while_loop_counter = 0

for part_num in range(upload_session.total_parts):

    copied_length = 0
    while copied_length < upload_session.part_size:
        print('INNER WHILEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

        chunk = content_stream.read(upload_session.part_size - copied_length)
        if chunk is None:
            continue
        if len(chunk) == 0:
            break
        copied_length += len(chunk)
        if copied_length < upload_session.part_size and copied_length > 0:
            break
        print('Copied Length: ' + str(copied_length))
        print('CHUNK SIZE: ' + str(len(chunk)))
        while_loop_counter += 1

    uploaded_part = upload_session.upload_part(chunk, part_num*upload_session.part_size, total_size)
    print('PART: ' + str(uploaded_part))
    print('LOOP_COUNTER: ' + str(while_loop_counter))
    updated_sha1 = sha1.update(chunk)
content_sha1 = sha1.digest()
uploaded_file = upload_session.commit(content_sha1)
