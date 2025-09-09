from enum import Enum

from box_sdk_gen.internal.base_object import BaseObject

from typing import Optional

from typing import Dict

from box_sdk_gen.internal.utils import to_string

from box_sdk_gen.serialization.json import deserialize

from box_sdk_gen.serialization.json import serialize

from box_sdk_gen.networking.fetch_options import ResponseFormat

from box_sdk_gen.schemas.task_assignments import TaskAssignments

from box_sdk_gen.schemas.client_error import ClientError

from box_sdk_gen.schemas.task_assignment import TaskAssignment

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


class CreateTaskAssignmentTaskTypeField(str, Enum):
    TASK = 'task'


class CreateTaskAssignmentTask(BaseObject):
    _discriminator = 'type', {'task'}

    def __init__(
        self,
        id: str,
        *,
        type: CreateTaskAssignmentTaskTypeField = CreateTaskAssignmentTaskTypeField.TASK,
        **kwargs
    ):
        """
        :param id: The ID of the task.
        :type id: str
        :param type: The type of the item to assign., defaults to CreateTaskAssignmentTaskTypeField.TASK
        :type type: CreateTaskAssignmentTaskTypeField, optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type


class CreateTaskAssignmentAssignTo(BaseObject):
    def __init__(
        self, *, id: Optional[str] = None, login: Optional[str] = None, **kwargs
    ):
        """
                :param id: The ID of the user to assign to the
        task.

        To specify a user by their email
        address use the `login` parameter., defaults to None
                :type id: Optional[str], optional
                :param login: The email address of the user to assign to the task.
        To specify a user by their user ID please use the `id` parameter., defaults to None
                :type login: Optional[str], optional
        """
        super().__init__(**kwargs)
        self.id = id
        self.login = login


class UpdateTaskAssignmentByIdResolutionState(str, Enum):
    COMPLETED = 'completed'
    INCOMPLETE = 'incomplete'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class TaskAssignmentsManager:
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

    def get_task_assignments(
        self, task_id: str, *, extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TaskAssignments:
        """
                Lists all of the assignments for a given task.
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
                        '/assignments',
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, TaskAssignments)

    def create_task_assignment(
        self,
        task: CreateTaskAssignmentTask,
        assign_to: CreateTaskAssignmentAssignTo,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TaskAssignment:
        """
        Assigns a task to a user.

        A task can be assigned to more than one user by creating multiple


        assignments.

        :param task: The task to assign to a user.
        :type task: CreateTaskAssignmentTask
        :param assign_to: The user to assign the task to.
        :type assign_to: CreateTaskAssignmentAssignTo
        :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
        :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'task': task, 'assign_to': assign_to}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [self.network_session.base_urls.base_url, '/2.0/task_assignments']
                ),
                method='POST',
                headers=headers_map,
                data=serialize(request_body),
                content_type='application/json',
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, TaskAssignment)

    def get_task_assignment_by_id(
        self,
        task_assignment_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TaskAssignment:
        """
                Retrieves information about a task assignment.
                :param task_assignment_id: The ID of the task assignment.
        Example: "12345"
                :type task_assignment_id: str
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
                        '/2.0/task_assignments/',
                        to_string(task_assignment_id),
                    ]
                ),
                method='GET',
                headers=headers_map,
                response_format=ResponseFormat.JSON,
                auth=self.auth,
                network_session=self.network_session,
            )
        )
        return deserialize(response.data, TaskAssignment)

    def update_task_assignment_by_id(
        self,
        task_assignment_id: str,
        *,
        message: Optional[str] = None,
        resolution_state: Optional[UpdateTaskAssignmentByIdResolutionState] = None,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> TaskAssignment:
        """
                Updates a task assignment. This endpoint can be

                used to update the state of a task assigned to a user.

                :param task_assignment_id: The ID of the task assignment.
        Example: "12345"
                :type task_assignment_id: str
                :param message: An optional message by the assignee that can be added to the task., defaults to None
                :type message: Optional[str], optional
                :param resolution_state: The state of the task assigned to the user.

        * For a task with an `action` value of `complete` this can be
        `incomplete` or `completed`.
        * For a task with an `action` of `review` this can be
        `incomplete`, `approved`, or `rejected`., defaults to None
                :type resolution_state: Optional[UpdateTaskAssignmentByIdResolutionState], optional
                :param extra_headers: Extra headers that will be included in the HTTP request., defaults to None
                :type extra_headers: Optional[Dict[str, Optional[str]]], optional
        """
        if extra_headers is None:
            extra_headers = {}
        request_body: Dict = {'message': message, 'resolution_state': resolution_state}
        headers_map: Dict[str, str] = prepare_params({**extra_headers})
        response: FetchResponse = self.network_session.network_client.fetch(
            FetchOptions(
                url=''.join(
                    [
                        self.network_session.base_urls.base_url,
                        '/2.0/task_assignments/',
                        to_string(task_assignment_id),
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
        return deserialize(response.data, TaskAssignment)

    def delete_task_assignment_by_id(
        self,
        task_assignment_id: str,
        *,
        extra_headers: Optional[Dict[str, Optional[str]]] = None
    ) -> None:
        """
                Deletes a specific task assignment.
                :param task_assignment_id: The ID of the task assignment.
        Example: "12345"
                :type task_assignment_id: str
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
                        '/2.0/task_assignments/',
                        to_string(task_assignment_id),
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
