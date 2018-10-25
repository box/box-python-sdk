# coding: utf-8

from __future__ import unicode_literals, absolute_import

import json

from .base_object import BaseObject
from ..util.api_call_decorator import api_call
from ..util.text_enum import TextEnum


class MetadataTemplateUpdate(object):
    """Represents a set of update operations to a metadata template."""

    def __init__(self):
        self.ops = []

    def add_enum_option(self, field_key, option_key):
        """
        Adds a new option to an enum field.

        :param field_key:
            The key of the template field to add the option to
        :type field_key:
            `unicode`
        :param option_key:
            The option to add
        :type option_key:
            `unicode`
        """
        self.ops.append({
            'op': 'addEnumOption',
            'fieldKey': field_key,
            'data': {
                'key': option_key,
            },
        })

    def add_field(self, field):
        """
        Add a new field to the template.

        :param field:
            The new field to add
        :type field:
            :class:`MetadataField`
        """
        self.ops.append({
            'op': 'addField',
            'data': field.json(),
        })

    def edit_template(self, data):
        """
        Edit top-level template properties.

        :param data:
            The properties to modify
        :type data:
            `dict`
        """
        self.ops.append({
            'op': 'editTemplate',
            'data': data,
        })

    def reorder_enum_options(self, field_key, option_keys):
        """
        Reorders the options in an enum field, which affects their display in UI.

        :param field_key:
            The key of the enum field to reorder
        :type field_key:
            `unicode`
        :param option_keys:
            The option keys in the desired order
        :type option_keys:
            `list` of `unicode`
        """
        self.ops.append({
            'op': 'reorderEnumOptions',
            'fieldKey': field_key,
            'enumOptionKeys': option_keys,
        })

    def reorder_fields(self, field_keys):
        """
        Reorders the fields in a metadata template, which affects their display in UI.

        :param field_keys:
            The field keys in the desired order
        :type field_keys:
            `list` of `unicode`
        """
        self.ops.append({
            'op': 'reorderFields',
            'fieldKeys': field_keys,
        })

    def edit_field(self, field_key, field):
        """
        Edits a field in the template.

        :param field_key:
            The key of the field to update
        :type field_key:
            `unicode`
        :param field:
            The updated field values
        :type field:
            :class:`MetadataField`
        """
        self.ops.append({
            'op': 'editField',
            'fieldKey': field_key,
            'data': field.json(),
        })

    def edit_enum_option_key(self, field_key, old_option_key, new_option_key):
        """
        Change the key of an enum field option.

        :param field_key:
            The key of the template field in which the option appears
        :type field_key:
            `unicode`
        :param old_option_key:
            The old option key
        :type old_option_key:
            `unicode`
        :param new_option_key:
            The new option key
        :type new_option_key:
            `unicode`
        """
        self.ops.append({
            'op': 'editEnumOption',
            'fieldKey': field_key,
            'enumOptionKey': old_option_key,
            'data': {
                'key': new_option_key,
            },
        })

    def remove_enum_option(self, field_key, option_key):
        """
        Remove an option from an enum field.

        :param field_key:
            The key of the template field in which the option appears
        :type field_key:
            `unicode`
        :param option_key:
            The key of the enum option to remove
        :type option_key:
            `unicode`
        """
        self.ops.append({
            'op': 'removeEnumOption',
            'fieldKey': field_key,
            'enumOptionKey': option_key,
        })

    def remove_field(self, field_key):
        """
        Remove a field from the metadata template.

        :param field_key:
            The key of the field to remove
        :type field_key:
            `unicode`
        """
        self.ops.append({
            'op': 'removeField',
            'fieldKey': field_key,
        })


class MetadataFieldType(TextEnum):
    STRING = 'string'
    DATE = 'date'
    ENUM = 'enum'
    MULTISELECT = 'multiSelect'
    FLOAT = 'float'


class MetadataField(object):
    """Represents a metadata field when creating or updating a metadata template."""

    def __init__(self, field_type, display_name, key=None, options=None):
        self.type = field_type
        self.name = display_name
        self.key = key
        self.options = options

    def json(self):
        """
        Returns the correct representation of the temnplate field for the API.

        :rtype:
            `dict`
        """
        values = {}

        if self.type is not None:
            values['type'] = self.type

        if self.name is not None:
            values['displayName'] = self.name

        if self.key is not None:
            values['key'] = self.key

        if self.type in ['enum', 'multiSelect']:
            values['options'] = [{'key': opt} for opt in self.options] if self.options is not None else []

        return values


class MetadataTemplate(BaseObject):
    """Represents a metadata template, which contains the the type information for associated metadata fields."""

    _item_type = 'metadata_template'
    _scope = None
    _template_key = None

    def __init__(self, session, object_id, response_object=None):
        super(MetadataTemplate, self).__init__(session, object_id, response_object)
        self._scope, self._template_key = object_id.split('/')

    def get_url(self, *args):
        """
        Base class override, since metadata templates have a weird compound ID and non-standard URL format

        :rtype:
            `unicode`
        """
        return self._session.get_url('metadata_templates', self._scope, self._template_key, 'schema', *args)

    @staticmethod
    def start_update():
        """
        Start an update operation on the template.

        :returns:
            An update object to collect the desired update operations.
        :rtype:
            :class:`MetadataTemplateUpdate`
        """
        return MetadataTemplateUpdate()

    @api_call
    def update_info(self, updates):
        # pylint: disable=arguments-differ
        """
        Update a metadata template with a set of update operations.

        :param updates:
            The update operations to apply to the template
        :type updates:
            :class:`MetadataTemplateUpdate`
        :returns:
            The updated metadata template object
        :rtype:
            :class:`MetadataTemplate`
        """
        url = self.get_url()
        response = self._session.put(url, data=json.dumps(updates.ops)).json()
        return self.__class__(
            session=self._session,
            object_id=self.object_id,
            response_object=response,
        )