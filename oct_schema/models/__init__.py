import ming
import ming.odm.declarative
import oct_schema.session
from datetime import datetime


class Base(ming.odm.declarative.MappedClass):
    """The :class:`oct.schema.Base` class is the generic class that
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
        session = oct_schema.session.SESSION
        name = 'base'

    _id = ming.odm.FieldProperty(ming.schema.ObjectId)
    created_ts = ming.odm.FieldProperty(datetime,
                                        if_missing=datetime.utcnow())
    modified_ts = ming.odm.FieldProperty(datetime,
                                         if_missing=datetime.utcnow())

    @property
    def session(self):
        """Session method docstring
        """
        return oct_schema.session.SESSION

    @property
    def flush(self):
        oct_schema.session.SESSION.flush()

    @property
    def rollback(self):
        oct_schema.session.SESSION.clear()

ming.odm.Mapper.compile_all()
