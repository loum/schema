__all__ = [
    'Objects',
]
import ming

import oct_schema


class Objects(oct_schema.ModelBase):
    """Objects schema.

    """
    class __mongometa__:
        name = 'objects'

    text_field = ming.odm.FieldProperty(str)
