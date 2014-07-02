__all__ = [
    'Objects',
]
from ming.odm import FieldProperty

import oct_schema


class Objects(oct_schema.ModelBase):
    """Objects schema.

    .. attribute:: *category_code*

    .. attribute:: *name*

    .. attribute:: *type_id*

    .. attribute:: *country*

    .. attribute:: *osuffix*

    .. attribute:: *facility_description*

    .. attribute:: *record_status*

    .. attribute:: *entities*

    .. attribute:: *location*

        dictionary structure that features an embedded ``type``
        and ``coordinates``

    .. attribute:: *facility_status*

    .. attribute:: *type*

    .. attribute:: *be_number*

    """
    class __mongometa__:
        name = 'objects'

    category_code = FieldProperty(str, if_missing='')
    name = FieldProperty(str, if_missing='')
    type_id = FieldProperty(str, if_missing='')
    country = FieldProperty(str, if_missing='')
    osuffix = FieldProperty(str, if_missing='')
    facility_description = FieldProperty(str, if_missing='')
    record_status = FieldProperty(str, if_missing='')
    entities = FieldProperty(str, if_missing='')
    location = FieldProperty(dict(type=str,
                                  coordinates=dict(latitude=float,
                                                   longitude=float)))
    facility_status = FieldProperty(str, if_missing='')
    type = FieldProperty(str, if_missing='')
    be_number = FieldProperty(str)
