from enum import Enum

from typing import Optional

from box_sdk_gen.internal.base_object import BaseObject

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.tasks import Tasks

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.task import Task

from box_sdk_gen.box.errors import BoxSDKError

from box_sdk_gen.networking.auth import Authentication

from box_sdk_gen.networking.network import NetworkSession

from box_sdk_gen.networking.fetch_options import FetchOptions

from box_sdk_gen.networking.fetch_response import FetchResponse

from box_sdk_gen.internal.utils import prepare_params

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.internal.utils import ByteStream

from box_sdk_gen.serialization.json import sd_to_json

from box_sdk_gen.serialization.json import SerializedData

from box_sdk_gen.internal.utils import DateTime


class CreateTaskItemTypeField(str, Enum):
    FILE = 'file'


class CreateTaskItem(BaseObject):
    _discriminator = 'type', {'file'}

    def __init__(
        self,
        *,
        id: Optional[str] = None,
        type: Optional[CreateTaskItemTypeField] = None,
        **kwargs
    ):
        """
        :param id: The ID of the file., defaults to None
        :type id: Optional[str], optional
        :param type: The value will always be `file`., defaults to None
        :type type: Optional[CreateTaskItemTypeField], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class CreateTaskAction(str, Enum):
    REVIEW = 'review'
    COMPLETE = 'complete'


class CreateTaskCompletionRule(str, Enum):
    ALL_ASSIGNEES = 'all_assignees'
    ANY_ASSIGNEE = 'any_assignee'


class UpdateTaskByIdAction(str, Enum):
    REVIEW = 'review'
    COMPLETE = 'complete'


class UpdateTaskByIdCompletionRule(str, Enum):
    ALL_ASSIGNEES = 'all_assignees'
    ANY_ASSIGNEE = 'any_assignee'


class TasksManager:
    def __init__(
        self,
        *,
        auth: Optional[Authentication] = None,
        network_session: NetworkSession = None
    ):
        if network_session is None:
            network_session = NetworkSession()
        self.auth = auth
        self.network_session = network_session

    def get_file_tasks(
        self, file_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Tasks:
        """
                Retrieves a list of all the tasks for a file. This

                endpoint does not support pagination.

                :param file_id: The unique identifier that represents a file.

        The ID for any file can be determined
        by visiting a file in the web application
        and copying the ID from the URL. For example,
        for the URL `https://*.app.box.com/files/123`
        the `file_id` is `123`.
        Example: "12345"
                :type file_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/files/',
                        to_string(file_id),
                        '/tasks',
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Tasks)

    def create_task(
        self,
        item: CreateTaskItem,
        *,
        action: Optional[CreateTaskAction] = None,
        message: Optional[str] = None,
        due_at: Optional[DateTime] = None,
        completion_rule: Optional[CreateTaskCompletionRule] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Task:
        """
                Creates a single task on a file. This task is not assigned to any user and

                will need to be assigned separately.

                :param item: The file to attach the task to.
                :type item: CreateTaskItem
                :param action: The action the task assignee will be prompted to do. Must be

        * `review` defines an approval task that can be approved or,
        rejected
        * `complete` defines a general task which can be completed., defaults to None
                :type action: Optional[CreateTaskAction], optional
                :param message: An optional message to include with the task., defaults to None
                :type message: Optional[str], optional
                :param due_at: Defines when the task is due. Defaults to `null` if not
        provided., defaults to None
                :type due_at: Optional[DateTime], optional
                :param completion_rule: Defines which assignees need to complete this task before the task
        is considered completed.

        * `all_assignees` (default) requires all assignees to review or
        approve the task in order for it to be considered completed.
        * `any_assignee` accepts any one assignee to review or
        approve the task in order for it to be considered completed., defaults to None
                :type completion_rule: Optional[CreateTaskCompletionRule], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'item': item,
            'action': action,
            'message': message,
            'due_at': due_at,
            'completion_rule': completion_rule,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join([self.network_session.base_urls.base_url, '/2.0/tasks']),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Task)

    def get_task_by_id(
        self, task_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Task:
        """
                Retrieves information about a specific task.
                :param task_id: The ID of the task.
        Example: "12345"
                :type task_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/tasks/',
                        to_string(task_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Task)

    def update_task_by_id(
        self,
        task_id: str,
        *,
        action: Optional[UpdateTaskByIdAction] = None,
        message: Optional[str] = None,
        due_at: Optional[DateTime] = None,
        completion_rule: Optional[UpdateTaskByIdCompletionRule] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> Task:
        """
                Updates a task. This can be used to update a task's configuration, or to

                update its completion state.

                :param task_id: The ID of the task.
        Example: "12345"
                :type task_id: str
                :param action: The action the task assignee will be prompted to do. Must be

        * `review` defines an approval task that can be approved or
        rejected,
        * `complete` defines a general task which can be completed., defaults to None
                :type action: Optional[UpdateTaskByIdAction], optional
                :param message: The message included with the task., defaults to None
                :type message: Optional[str], optional
                :param due_at: When the task is due at., defaults to None
                :type due_at: Optional[DateTime], optional
                :param completion_rule: Defines which assignees need to complete this task before the task
        is considered completed.

        * `all_assignees` (default) requires all assignees to review or
        approve the task in order for it to be considered completed.
        * `any_assignee` accepts any one assignee to review or
        approve the task in order for it to be considered completed., defaults to None
                :type completion_rule: Optional[UpdateTaskByIdCompletionRule], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {
            'action': action,
            'message': message,
            'due_at': due_at,
            'completion_rule': completion_rule,
        }
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/tasks/',
                        to_string(task_id),
                    ]
                ),
                method='PUT',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, Task)

    def delete_task_by_id(
        self, task_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Removes a task from a file.
                :param task_id: The ID of the task.
        Example: "12345"
                :type task_id: str
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/tasks/',
                        to_string(task_id),
                    ]
                ),
                method='DELETE',
                headers=headers_map,
                response_format=ResponseFormat.NO_CONTENT,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return None
