__all__ = [
    'Relations',
]
from ming.odm import FieldProperty

import oct_schema


class Relations(oct_schema.ModelBase):
    """Relations schema.

    .. attribute:: name

    """
    class __mongometa__:
        name = 'relations'

    to = FieldProperty([dict(id=str, if_missing=None)])
    
