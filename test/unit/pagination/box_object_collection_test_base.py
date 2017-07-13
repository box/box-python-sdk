# coding: utf-8

from __future__ import unicode_literals, absolute_import
from abc import ABCMeta, abstractmethod
from six import add_metaclass
from six.moves import range   # pylint:disable=redefined-builtin
import pytest

from boxsdk.util.translator import Translator


@add_metaclass(ABCMeta)
class BoxObjectCollectionTestBase(object):
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
                "name": "file_{0}.txt".format(i),
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
    def _object_collection_instance(self, session, limit, return_full_pages=False, starting_pointer=None):
        """
        :type session: :class:`BoxSession`
        :type limit: `int`
        :type return_full_pages: `bool`
        :type starting_pointer: varies
        :rtype: :class:`BoxObjectCollection`
        """
        raise NotImplementedError

    @staticmethod
    def _assert_items_dict_and_objects_same(expected_items_dict, returned_item_objects):
        """
        A fixture very specific to this test class. Asserts that the list of items in dictionary form are the
        same (at least in name, and in quantity) as a list of BaseObjects.

        :param expected_items_dict: List of expected items, represented as a dictionary.
        :type expected_items_dict: `list` of `dict`
        :param returned_item_objects: List of item instances (BaseObject) returned by SUT.
        :type returned_item_objects: `list` of class:`BaseObject`
        """
        expected_num = len(expected_items_dict)
        actual_num = len(returned_item_objects)
        assert actual_num == expected_num, 'Expected {0} items, got {1}'.format(expected_num, actual_num)
        returned_item_names = [item.name for item in returned_item_objects]
        for expected_item_dict in expected_items_dict:
            assert expected_item_dict['name'] in returned_item_names, 'Missing item: {0}'.format(expected_item_dict['name'])

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
