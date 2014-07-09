__all__ = [
    'Objects',
]
import ming
from ming.odm import FieldProperty
from ming.odm import FieldPropertyWithMissingNone

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
        dictionary structure that features embedded data:
        * ``type_id``
        * ``latitude``
        * ``longitude``
        * ``name``
        * ``facility_description``

    .. attribute:: *facility_status*

    .. attribute:: *type*

    .. attribute:: *be_number*

    """
    class __mongometa__:
        name = 'objects'
        unique_indexes = [('_id',),]

    #__e = dict(_id=ming.schema.String(if_missing=None),
    #           type_id=ming.schema.String(if_missing=None),
    #           latitude=ming.schema.Float(if_missing=None),
    #           longitude=ming.schema.Float(if_missing=None),
    #           name=ming.schema.String(if_missing=None),
    #           facility_description=ming.schema.String(if_missing=None))

    # Attributes have been altered to suit the observation context.
    #category_code = FieldProperty(str, if_missing='')
    type_id = FieldProperty(str, if_missing='')
    source_id = FieldProperty(str, if_missing='')
    occurred_start = FieldProperty(str, if_missing='')
    observation_by = FieldProperty(str, if_missing='')
    observation_at = FieldProperty(str, if_missing='')
    activity = FieldProperty(str, if_missing='')
    description = FieldProperty(str, if_missing='')
    latitude = FieldProperty(float, if_missing='')
    longitude = FieldProperty(float, if_missing='')
    #name = FieldProperty(str, if_missing='')
    #country = FieldProperty(str, if_missing='')
    #osuffix = FieldProperty(str, if_missing='')
    #facility_description = FieldProperty(str, if_missing='')
    #record_status = FieldProperty(str, if_missing='')
    #entities = FieldPropertyWithMissingNone([__e])
    #facility_status = FieldProperty(str, if_missing='')
    #type = FieldProperty(str, if_missing='')
    #be_number = FieldProperty(str)
