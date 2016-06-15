from boxsdk.auth.developer_token_auth import DeveloperTokenAuth

from boxsdk.client.development_client import DevelopmentClient
from boxsdk.client.developer_token_client import DeveloperTokenClient
from boxsdk.client.logging_client import LoggingClient

from boxsdk.session.box_session import BoxSession
from boxsdk.network.default_network import DefaultNetwork
from boxsdk.object.events import Events

oauth = DeveloperTokenAuth()

# Input developer token here

client = DevelopmentClient()

# Input developer token here

box_session = BoxSession(oauth, DefaultNetwork())
events = Events(box_session)
