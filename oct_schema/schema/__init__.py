from datetime import datetime
import ming
from ming.declarative import Document
from oct_schema.session import SESSION


class Base(Document):
    """The :class:`oct.schema.Base` class is the generic class that
    should be inherited by all OCT Collections that will interface to
    MongoDB.

    .. attribute:: created_ts
        :mod:`datetime` object that captures the timestamp of when
        the Document was first created

    .. attribute:: modified_ts
        :mod:`datetime` object that captures the timestamp of when
        the Document was modified

    .. attribute:: user
        dictionary structure that capture details around the user
        that invoked a Document insert/update

    """

    class __mongometa__:
        session = SESSION
        name = 'base'

    _id = ming.Field(ming.schema.ObjectId)
    created_ts = ming.Field(datetime, if_missing=datetime.utcnow())
    modified_ts = ming.Field(datetime, if_missing=datetime.utcnow())
    user = ming.Field(dict(username=str, display_name=str))
