__all__ = [
    'Ontology',
]
from ming.odm import FieldProperty

import oct_schema


class Ontology(oct_schema.ModelBase):
    """Ontology schema.

    .. attribute:: name

    """
    class __mongometa__:
        name = 'ontology'

    name = FieldProperty(str, if_missing='')
    gloss = FieldProperty(str, if_missing='')
