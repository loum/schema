import ming
import ming.odm
import ming.odm.declarative
import json
import re
from datetime import datetime
import inspect

import oct_schema
from oct.utils.log import log


class JSONDatetimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


class ModelBase(ming.odm.declarative.MappedClass):
    """The :class:`oct.schema.ModelBase` class is the generic class that
    should be inherited by all OCT Collections that will interface to
    MongoDB.

    .. attribute:: created_ts

        :mod:`datetime` object that captures the timestamp of when
        the Document was first created

    .. attribute:: modified_ts

        :mod:`datetime` object that captures the timestamp of when
        the Document was modified

    """
    def __str__(self):
        return type(self).__name__

    __metaclass__ = ming.odm.declarative._MappedClassMeta

    class __mongometa__:
        s = oct_schema.Session()
        session = s.odm_session
        name = 'base'

    # TODO: Part of us-99, we need to work out whether _id will
    # be the native MongoDB UID or the value provided in the data.
    #_id = ming.odm.FieldProperty(ming.schema.ObjectId)
    _id = ming.odm.FieldProperty(str)
    created_ts = ming.odm.FieldProperty(datetime,
                                        if_missing=datetime.utcnow)
    modified_ts = ming.odm.FieldProperty(datetime)

    @property
    def flush(self):
        log.debug(self.__mongometa__.session)
        self.__mongometa__.session.flush()

    @property
    def rollback(self):
        self.__mongometa__.session.clear()

    @classmethod
    def _batch_loader(cls, file):
        """Helper method that takes a filename and attempts to parse
        its contents as a JSON object and load into the Collection
        context.

        .. note::

            The loader falls back to the base :mod:`ming` database
            ``Manager`` and by-passes the Collection validation.  In short,
            you can load whatever you like in the collection as this may be
            useful during the test process.

        Each JSON item in the file represents a Collection Document

        **Args:**
            *file*: the path to the JSON file that will be loaded
            into the Collection context

        """
        log.debug('Loading fixture file: "%s" ...' % file)

        m = ming.odm.mapper(cls)
        with open(file) as f:
            record_count = 0
            data = json.load(f)

            for d in data:
                m.collection.m.collection.insert(d)
                record_count += 1

        log.debug('Fixture-based records loaded: %d' % record_count)

    @classmethod
    def search(cls, token, regex=False, case_sensitive=True):
        """Extract documents from the Collection context associated with
        the *token*.  If *regex* is ``True`` then the token is applied
        as a regular expression to the search (the default is that
        *token* is used as a literal).  Similarly, if
        *case_sensitive* is ``False`` then the token search is case
        insensitive (default is case sensitive).

        **Args:**
            *token*: the search token to build into the regular expression
            to search against the Collection context

        **Kwargs:**
            *regex*: Control whether *token* is to be built as a regular
            expression in the search criteria.  Defaults to ``False``

            *case_sensitive*: Control whether *token* is to be used
            as a case-sensitive search criteria.  Defaults to ``True``

        """
        log.info('Searching Collection: "%s" with token "%s"' %
                 (str(cls), str(token)))

        kwargs = {}
        if regex:
            r = re.compile('.*%s.*' % token, re.IGNORECASE)
            kwargs['_id'] = r
        else:
            kwargs['_id'] = token

        results = cls.query.find(kwargs)

        return results

    def to_dict(self):
        """Helper method to convert the Collection Document context
        into a Python dictionary structure.

        Makes every effort to exclude all but valid Collection attributes

        .. note::

            **TODO**: filtering is based on some hard-wired object
            names.  It would be better if we could leverage the object
            type (probably more important if Project gains traction)

        **Returns:**
            dictionary of the Collection Document's attributes.  For
            example::

                {'_id': 'xxxxxx',
                 'text_field': token,
                 'created_ts': datetime.datetime(2014, 7, 9, ... )}

        """
        new_dict = {}
        for item in dir(self):
            is_attr = True
            # TODO: get rid of these hard-wired comparisons.
            if (not item.startswith("__") and
                item not in ['_registry', 'query', '_compiled']):

                # Separating if constructs here to clarify actions.

                # Check for object methods.
                if inspect.ismethod(getattr(type(self), item)):
                    is_attr = False
                    continue

                # Check for object properties.
                if isinstance(getattr(type(self), item), property):
                    is_attr = False
                    continue

                if is_attr:
                    new_dict[item] = getattr(self, item)

        return new_dict

    def to_json(self):
        """Wrapper around the :meth:`oct_schema.ModelBase.to_dict`
        method that converts a Collection Document context into JSON.

        **Returns:**
            JSON string of the Collection Document's attributes.  For
            example::

                '{"created_ts": "%s", "_id": "aaaaaa", "modified_ts": ... }'

        """
        tmp_dict = self.to_dict()

        import json
        encoded_json = json.dumps(tmp_dict, cls=JSONDatetimeEncoder)

        return encoded_json

ming.odm.Mapper.compile_all()
