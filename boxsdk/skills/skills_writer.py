from datetime import datetime
import json
import logging

from ..client.client import Client
from ..auth.oauth2 import OAuth2

from .skills_error_enum import SkillsErrorEnum

class SkillsWriter:
    """
    SkillsWriter :- A helpful class to write back Metadata Cards for
    Topics, Transcripts, Timelines, Errors and Statuses back to Box for
    any file for which a Skills Event is sent out.

    API:-
    SkillsWriter.create_topics_card ( topicsDataList, optionalFileDuration, optionalCardTitle ) : DataCard json
    SkillsWriter.createTranscriptsCard ( transcriptsDataList, optionalFileDuration, optionalCardTitle ): DataCard json
    SkillsWriter.createFacesCard ( facesDataList, optionalFileDuration, optionalCardTitle ) : DataCard json
    SkillsWriter.save_processing_card ( optionalCallback ) : null
    SkillsWriter.save_error_card ( error, optionalCustomMessage, optionalCallback ): null
    SkillsWriter.save_data_cards ( listofDataCardJSONs, optionalCallback): null
    """

    # Constant values for writing cards to skill_invocations service
    BASE_PATH = 'skill_invocations' # Base path for all files endpoints
    SKILLS_SERVICE_TYPE = 'service'
    SKILLS_METADATA_CARD_TYPE = 'skill_card'
    SKILLS_METADATA_INVOCATION_TYPE = 'skill_invocation'

    BOXSDK_CLIENT_ID = 'BoxSkillsClientId'
    BOXSDK_CLIENT_SECRET = 'BoxSkillsClientSecret'

    def __init__(self, json_event_body):
        self.request_id = json_event_body['id']
        self.skill_id = json_event_body['skill']['id']
        self.file_id = json_event_body['source']['id']
        self.file_write_token = json_event_body['token']['write']['access_token']
        self.file_write_client = Client(OAuth2(
            self.BOXSDK_CLIENT_ID,
            self.BOXSDK_CLIENT_SECRET,
            access_token=self.file_write_token))

    # SkillsWriter private dictionary
    cardType = {
        'TRANSCRIPT': 'transcript',
        'TOPIC': 'keyword',
        'FACES': 'timeline',
        'STATUS': 'status',
        'ERROR': 'error'
    }

    cardTitle = {
        'TRANSCRIPT': 'Transcript',
        'TOPIC': 'Topics',
        'FACES': 'Faces',
        'STATUS': 'Status',
        'ERROR': 'Error'
    }

    usageUnit = {
        'FILES': 'files',
        'SECONDS': 'seconds',
        'PAGES': 'pages',
        'WORDS': 'words'
    }

    skillInvocationStatus = {
        'INVOKED': 'invoked',
        'PROCESSING': 'processing',
        'TRANSIENT_FAILURE': 'transient_failure',
        'PERMANENT_FAILURE': 'permanent_failure',
        'SUCCESS': 'success'
    }

    # SkillsWriter private functions

    def __validate_enum(self, input_value, enum_name):
        """
        Validates if Enum value passed exists in the enums

        Arguments:
            input_value {str} -- value
            enum_name {dict} -- dictionary

        Returns:
            bool -- True if it contains a value
        """
        return input_value in enum_name.values()

    def __validate_usage(self, usage):
        """
        Validates if usage object is of allowed format: { 'unit': <usageUnit>, 'value': <Integer> }

        Arguments:
            usage {dict} -- Usage
        
        Returns:
            bool -- Validates usage object
        """
        if usage is None or not usage == 0:
            return False
        if self.__validate_enum(usage['unit'], self.usageUnit) == 0:
            return False
        if isinstance(usage['value'], int):
            return False
        return True
    
    def __process_card_data(self, card_data, duration):
        """
       Private function to validate and update card template data to have expected fields
        
        Arguments:
            card_data {dict} -- card data
            duration {float} -- total duration of file in seconds
        
        Raises:
            TypeError -- Missing required "text" field in card_data
        """

        if 'text' not in card_data.keys():
            raise TypeError('Missing required "text" field in {}'.format(json.dumps(card_data)))
        card_data['type'] = 'image' if 'image_url' in card_data.keys() and type(card_data['image_url']) is str else 'text'
        if duration and card_data['appears'] is list and card_data['appears']:
            logging.warning('Missing optional "appears" field in {} which is list of "start" and "end" fields'.format(json.dumps(card_data)))
        return
    
    def __put_data(self, client, skill_id, body):
        """
        Private function, for underlying call to saving data to skills invocation api
        Will add metadata cards to the file and log other values for analysis purposes

        API Endpoint: '/skill_invocations/:skillID'
        Method: PUT
        
        Arguments:
            client {boxsdk.Client} -- Box SDK client to call skill invocations apiId
            skillId {str} -- id of the skill for the '/skill_invocations/:skillID' call
            body {dict} -- json data to put
        
        Returns:
            BoxResponse -- The network response for the given request.
        """
        api_path = client.get_url(self.BASE_PATH, skill_id)
        return client.make_request(
            'PUT',
            api_path,
            data=json.dumps(body),
            expect_json_response=False
        )

    # SkillsWriter public functions

    def create_metadata_card(self, card_type, title, \
        optional_status=None, optional_entries=None, optional_file_duration=None):
        """
        Public function to return a complete metadata card
        
        Arguments:
            cardType {str} -- type of metadata card (status, transcript, etc.)
            title {str} -- title of metadata card (Status, Transcript, etc.)
        
        Keyword Arguments:
            optionalStatus {dict} -- (optional) status object with code and message (default: {None})
            optionalEntries {dict} -- (optional) list of cards being saved (default: {None})
            optionalfileDuration {float} -- (optional) total duration of file in seconds (default: {None})
        
        Returns:
            dict -- metadata card template
        """
        if optional_status is None:
            optional_status = {}
        title_code = 'skills_{}'.format(title.lower().replace(' ', '_'))
        template = {
            'created_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'type': self.SKILLS_METADATA_CARD_TYPE, # skill_card
            'skill': {
                'type': self.SKILLS_SERVICE_TYPE, # service
                'id': self.skill_id
            },
            'skill_card_type': card_type,
            'skill_card_title': {
                'code': title_code,
                'message': title
            },
            'invocation': {
                'type': self.SKILLS_METADATA_INVOCATION_TYPE, # skill_invocation
                'id': self.request_id
            },
            'status': optional_status
        }
        if optional_entries:
            template['entries'] = optional_entries
        if optional_file_duration:
            template['duration'] = float(optional_file_duration)
        return template

    def create_topics_card(self, topics_data_list, optional_file_duration=None, optional_card_title=None):
        """
        Public function to return a complete topic card
        
        Arguments:
            topics_data_list {list} -- List of names and value dictionaries
        
        Keyword Arguments:
            optional_file_duration {float} -- (optional) total duration of file in seconds (default: {None})
            optional_card_title {str} -- (optional) title of metadata card (Status, Transcript, etc.)
        
        Returns:
            BoxResponse -- The network response for the given request.
        """
        for topic in topics_data_list:
            self.__process_card_data(topic, optional_file_duration)
        optional_card_title = self.cardTitle['TOPIC']
        if optional_card_title:
            selected_card_title = optional_card_title
        return self.create_metadata_card(
            self.cardType['TOPIC'],
            selected_card_title,
            {}, # Empty status value, since this is a data card
            topics_data_list,
            optional_file_duration)

    def create_transcripts_card(self, transcripts_data_list, optional_file_duration=None, optional_card_title=None):
        """
        Public function to return a complete transcripts card
        
        Arguments:
            transcripts_data_list {list} -- List of names and value dictionaries
        
        Keyword Arguments:
            optional_file_duration {float} -- (optional) total duration of file in seconds (default: {None})
            optional_card_title {str} -- (optional) title of metadata card (Status, Transcript, etc.) (default: {None})
        
        Returns:
            BoxResponse -- The network response for the given request.
        """
        for transcript in transcripts_data_list:
            self.__process_card_data(transcript, optional_file_duration)
        return self.create_metadata_card(
            self.cardType['TRANSCRIPT'],
            self.cardTitle['TRANSCRIPT'] if optional_card_title is None else optional_card_title,
            {}, # Empty status value, since this is a data card
            transcripts_data_list,
            optional_file_duration)
    
    def create_faces_card(self, faces_data_list, optional_file_duration=None, optional_card_title=None):
        """
        Public function to return a complete face card
        
        Arguments:
            faces_data_list {list} -- List of names and value dictionaries
        
        Keyword Arguments:
            optional_file_duration {float} -- (optional) total duration of file in seconds (default: {None})
            optional_card_title {str} -- (optional) title of metadata card (Status, Transcript, etc.) (default: {None})
        
        Returns:
            BoxResponse -- The network response for the given request.
        """

        for face in faces_data_list:
            self.__process_card_data(face, optional_file_duration)
        return self.create_metadata_card(
            self.cardType['FACES'],
            self.cardTitle['FACES'] if optional_card_title is None else optional_card_title,
            {}, # Empty status value, since this is a data card
            faces_data_list,
            optional_file_duration)

    def save_processing_card(self):
        """
        Shows UI card with message: "We're preparing to process your file. Please hold on!".
        This is used for temporarily letting your users know that your skill is under progress.
        You can pass an optionalCallback function to print or log success in your code once the
        card has been saved.
        
        Returns:
            BoxResponse -- The network response for the given request.
        """
        status = {
            'code': 'skills_pending_status',
            'message': "We're preparing to process your file. Please hold on!"
        }
        status_card = self.create_metadata_card(self.cardType['STATUS'], self.cardTitle['STATUS'], status)
        return self.save_data_cards([status_card], optional_status=self.skillInvocationStatus['PROCESSING'])

    def save_error_card(self, error, optional_custom_error_message=None, optional_failure_type=None):
        """
        Show UI card with error message. See Table: ErrorCode Enum for potential errorCode values,
        to notify user if any kind of failure occurs while running your skills code. Shows card as
        per the default message with each code, unless 'optionMessage' is provided. You can pass an
        optionalCallback function to print or log success in your code once the card has been saved.
        
        Arguments:
            error {SkillsErrorEnum} -- error code
        
        Keyword Arguments:
            optional_custom_error_message {string} -- (optional) custom error message (default: {None})
            optional_failure_type {string} -- (optional) status object with code and message (default: {None})
        
        Returns:
            [type] -- [description]
        """
        failure_type = optional_failure_type \
            if optional_failure_type == self.skillInvocationStatus['TRANSIENT_FAILURE'] \
            else self.skillInvocationStatus['PERMANENT_FAILURE']
        error_code = error if SkillsErrorEnum.has(error) else SkillsErrorEnum.UNKNOWN
        error_obj = {'code': error_code.value}
        if optional_custom_error_message:
            error_obj = {'code': 'custom_error', 'message': optional_custom_error_message}
        error_card = self.create_metadata_card(self.cardType['STATUS'], self.cardTitle['ERROR'], error_obj)
        return self.save_data_cards([error_card], optional_status=failure_type)

    DEFAULT_USAGE = {'unit': usageUnit['FILES'], 'value': 1}
    def save_data_cards(self, list_of_data_card_jsons, optional_status=None, optional_usage=None):
        """
        Shows all the cards passed in list_of_data_card_jsons which can be of formatted as Topics,Transcripts
        or Faces. Will override any existing pending or error status cards in the UI for that file version.
        
        Arguments:
            list_of_data_card_jsons {list} -- List of card dictionaries
        
        Keyword Arguments:
            optional_status {string} -- (optional) status object with code and message (default: {None})
            optional_usage {dict} -- (optional) usage (default: {None})

        Returns:
            BoxResponse -- The network response for the given request.
        """
        status = optional_status if self.__validate_enum(optional_status, self.skillInvocationStatus) else self.skillInvocationStatus['SUCCESS']
        usage = None
        if status == self.skillInvocationStatus['SUCCESS']:
            usage = optional_usage if self.__validate_usage(optional_usage) else self.DEFAULT_USAGE
        # create skill_invocations body
        body = {
            'status': status,
            'file': {
                'type': 'file',
                'id': self.file_id
            },
            'metadata': {
                'cards': list_of_data_card_jsons
            },
            'usage': usage
        }
        return self.__put_data(self.file_write_client, self.skill_id, body)
