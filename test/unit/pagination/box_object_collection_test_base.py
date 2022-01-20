# coding: utf-8

from abc import ABC, abstractmethod
from typing import Any, Union, List, TYPE_CHECKING

import pytest

from boxsdk.util.translator import Translator

if TYPE_CHECKING:
    from boxsdk.object.base_object import BaseObject
    from boxsdk.pagination.box_object_collection import BoxObjectCollection
    from boxsdk.session.session import Session


class BoxObjectCollectionTestBase(ABC):
    NUM_ENTRIES = 25

    @staticmethod
    @pytest.fixture()
    def translator():
        return Translator()

    @pytest.fixture()
    def entries(self):
        all_entries = []
        for i in range(self.NUM_ENTRIES):
            all_entries.append({
                "type": "file",
                "id": str(1000 + i),
                "sequence_id": str(i),
                "etag": str(10 + i),
                "name": f"file_{i}.txt",
            })
        return all_entries

    @abstractmethod
    @pytest.fixture()
    def mock_items_response(self, entries):
        raise NotImplementedError

    @abstractmethod
    @pytest.fixture()
    def mock_session(self, translator, mock_items_response):
        raise NotImplementedError

    @abstractmethod
    def _object_collection_instance(
            self,
            session: 'Session',
            limit: int,
            return_full_pages: bool = False,
            starting_pointer: Any = None
    ) -> 'BoxObjectCollection':
        raise NotImplementedError

    @staticmethod
    def _assert_items_dict_and_objects_same(
            expected_items_dict: Union[list, dict],
            returned_item_objects: List['BaseObject']
    ) -> None:
        """
        A fixture very specific to this test class. Asserts that the list of items in dictionary form are the
        same (at least in name, and in quantity) as a list of BaseObjects.

        :param expected_items_dict: List of expected items, represented as a dictionary.
        :param returned_item_objects: List of item instances (BaseObject) returned by SUT.
        """
        expected_num = len(expected_items_dict)
        actual_num = len(returned_item_objects)
        assert actual_num == expected_num, f'Expected {expected_num} items, got {actual_num}'
        returned_item_names = [item.name for item in returned_item_objects]
        for expected_item_dict in expected_items_dict:
            assert expected_item_dict['name'] in returned_item_names, f'Missing item: {expected_item_dict["name"]}'

    @pytest.mark.parametrize('return_full_pages', (True, False))
    @pytest.mark.parametrize('limit', (1, 3, 5, NUM_ENTRIES, 1000))
    def test_object_collection_pages_through_all_entries(self, mock_session, entries, limit, return_full_pages):
        """
        Tests the basic iteration functionality of the box object collection.
        """
        object_collection = self._object_collection_instance(mock_session, limit, return_full_pages)
        iterated_items = []
        for item_or_page in object_collection:
            if return_full_pages:
                iterated_items.extend(item_or_page)
            else:
                iterated_items.append(item_or_page)
        self._assert_items_dict_and_objects_same(entries, iterated_items)

    def test_new_object_collection_starts_off_from_last_pointer(self, mock_session, entries):
        """
        Start paging with one object collection instance, and then finish paging with a new object collection
        instance, starting off from the next_pointer() of the previous instance.

        The iterated items should be identical as if it were iterated through with just one object collection
        instance.
        """
        iterated_items = []
        object_collection = self._object_collection_instance(mock_session, limit=5, return_full_pages=True)
        iterated_items.extend(object_collection.next())
        next_pointer = object_collection.next_pointer()

        # Create a new object collection, starting off where the previous collection left off.
        new_object_collection = self._object_collection_instance(
            mock_session,
            limit=5,
            return_full_pages=True,
            starting_pointer=next_pointer
        )
        for page in new_object_collection:
            iterated_items.extend(page)

        self._assert_items_dict_and_objects_same(entries, iterated_items)
