import ming
import ming.odm.declarative
from datetime import datetime

import oct_schema


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
    __metaclass__ = ming.odm.declarative._MappedClassMeta

    class __mongometa__:
        s = oct_schema.Session()
        session = s.odm_session
        name = 'base'

    _id = ming.odm.FieldProperty(ming.schema.ObjectId)
    created_ts = ming.odm.FieldProperty(datetime,
                                        if_missing=datetime.utcnow())
    modified_ts = ming.odm.FieldProperty(datetime)

    @property
    def flush(self):
        self.__mongometa__.session.flush()

    @property
    def rollback(self):
        self.__mongometa__.session.clear()

ming.odm.Mapper.compile_all()
