# coding: utf-8

from __future__ import unicode_literals
import os
from boxsdk.client import Client
from boxsdk.object.collaboration import CollaborationRole
from boxsdk.exception import BoxAPIException
from demo.auth import authenticate


def run_user_example(client):
    # 'me' is a handy value to get info on the current authenticated user.
    me = client.user(user_id='me').get(fields=['login'])
    print 'The email of the user is: {}'.format(me['login'])


def run_folder_examples(client):
    root_folder = client.folder(folder_id='0').get()
    print 'The root folder is owned by: {}'.format(root_folder.owned_by['login'])

    items = root_folder.get_items(limit=100, offset=0)
    print 'This is the first 100 items in the root folder:'
    print items


def run_collab_examples(client):
    root_folder = client.folder(folder_id='0')
    collab_folder = root_folder.create_subfolder('collab folder')
    print 'Folder {} created'.format(collab_folder.get()['name'])
    collaboration = collab_folder.add_collaborator('someone@example.com', CollaborationRole.VIEWER)
    print 'Created a collaboration'
    modified_collaboration = collaboration.update_info(role=CollaborationRole.EDITOR)
    print 'Modified a collaboration'
    modified_collaboration.delete()
    print 'Deleted a collaboration'
    # Clean up
    print 'Delete folder collab folder succeeded: {}'.format(collab_folder.delete())


def rename_folder(client):
    root_folder = client.folder(folder_id='0')
    foo = root_folder.create_subfolder('foo')
    print 'Folder {} created'.format(foo.get()['name'])

    bar = foo.rename('bar')
    print 'Renamed to {}'.format(bar.get()['name'])

    print 'Delete folder bar succeeded: {}'.format(bar.delete())


def get_folder_shared_link(client):
    root_folder = client.folder(folder_id='0')
    collab_folder = root_folder.create_subfolder('collab folder')
    print 'Folder {} created'.format(collab_folder.get()['name'])

    shared_link = collab_folder.get_shared_link()
    print 'Got shared link:' + shared_link

    print 'Delete folder collab folder succeeded: {}'.format(collab_folder.delete())


def upload_file(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='i-am-a-file.txt')
    print '{} uploaded: '.format(a_file.get()['name'])
    print 'Delete i-am-a-file.txt succeeded: {}'.format(a_file.delete())


def rename_file(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    foo = root_folder.upload(file_path, file_name='foo.txt')
    print '{} uploaded '.format(foo.get()['name'])
    bar = foo.rename('bar.txt')
    print 'Rename succeeded: {}'.format(bool(bar))
    bar.delete()


def update_file(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    file_v1 = root_folder.upload(file_path, file_name='file_v1.txt')
    # print 'File content after upload: {}'.format(file_v1.content())
    file_v2_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file_v2.txt')
    file_v2 = file_v1.update_contents(file_v2_path)
    # print 'File content after update: {}'.format(file_v2.content())
    file_v2.delete()


def search_files(client):
    search_results = client.search(
        'i-am-a-file.txt',
        limit=2,
        offset=0,
        ancestor_folders=[client.folder(folder_id='0')],
        file_extensions=['txt'],
    )
    for item in search_results:
        item_with_name = item.get(fields=['name'])
        print item_with_name.id


def copy_item(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='a file.txt')
    subfolder1 = root_folder.create_subfolder('sub')
    a_file.copy(subfolder1)
    print subfolder1.get_items(limit=10, offset=0)
    subfolder2 = root_folder.create_subfolder('sub2')
    subfolder1.copy(subfolder2)
    print subfolder2.get_items(limit=10, offset=0)

    [item.delete() for item in [a_file, subfolder2, subfolder1]]


def move_item(client):
    root_folder = client.folder(folder_id='0')
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'file.txt')
    a_file = root_folder.upload(file_path, file_name='a file.txt')
    subfolder1 = root_folder.create_subfolder('sub')
    a_file.move(subfolder1)
    print subfolder1.get_items(limit=10, offset=0)
    subfolder2 = root_folder.create_subfolder('sub2')
    subfolder1.move(subfolder2)
    print subfolder2.get_items(limit=10, offset=0)

    subfolder2.delete()


def get_events(client):
    print client.events().get_events(limit=100, stream_position='now')


def get_latest_stream_position(client):
    print client.events().get_latest_stream_position()


def long_poll(client):
    print client.events().long_poll()


def _delete_leftover_group(existing_groups, group_name):
    """
    delete group if it already exists
    """
    existing_group = next((g for g in existing_groups if g.name == group_name), None)
    if existing_group:
        existing_group.delete()


def run_groups_example(client):
    """
    Shows how to interact with 'Groups' in the Box API. How to:
    - Get info about all the Groups to which the current user belongs
    - Create a Group
    - Rename a Group
    - Add a member to the group
    - Remove a member from a group
    - Delete a Group
    """
    original_groups = client.groups()

    try:
        # First delete group if it already exists
        _delete_leftover_group(original_groups, 'box_sdk_demo_group')
        _delete_leftover_group(original_groups, 'renamed_box_sdk_demo_group')

        new_group = client.create_group('box_sdk_demo_group')
    except BoxAPIException as ex:
        if ex.status != 403 or ex.code != 'access_denied_insufficient_permissions':
            raise
        print 'The authenticated user does not have permissions to manage groups. Skipping the test of this demo.'
        return

    print "New group:", new_group.name, new_group.id

    new_group = new_group.update_info({'name': 'renamed_box_sdk_demo_group'})
    print "Group's new name:", new_group.name

    me_dict = client.user().get(fields=['login'])
    me = client.user(user_id=me_dict['id'])
    group_membership = new_group.add_member(me, 'member')

    members = list(new_group.membership())

    print "The group has a membership of:", len(members)
    print "The id of that membership:", group_membership.object_id

    group_membership.delete()
    print "After deleting that membership, the group has a membership of:", len(list(new_group.membership()))

    new_group.delete()
    groups_after_deleting_demo = client.groups()
    has_been_deleted = not any(g.name == 'renamed_box_sdk_demo_group' for g in groups_after_deleting_demo)
    print "The new group has been deleted:", has_been_deleted


def run_examples(oauth):

    client = Client(oauth)

    run_user_example(client)
    run_groups_example(client)
    run_folder_examples(client)
    run_collab_examples(client)
    rename_folder(client)
    get_folder_shared_link(client)
    upload_file(client)
    rename_file(client)
    update_file(client)
    search_files(client)
    copy_item(client)
    move_item(client)
    get_events(client)
    get_latest_stream_position(client)
    # long_poll(client)


def main():

    oauth = authenticate()
    run_examples(oauth)
    os._exit(0)

if __name__ == '__main__':
    main()
