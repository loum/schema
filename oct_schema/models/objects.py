__all__ = [
    'Objects',
]
import ming

import oct_schema.models.base


class Objects(oct_schema.models.base.Base):
    """Objects schema.

    """
    class __mongometa__:
        name = 'objects'

    text_field = ming.odm.FieldProperty(str)
