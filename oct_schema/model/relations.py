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

    @classmethod
    def observation_search(cls, token):
        """Wrapper around a Relations Collection context that filters
        out ``was observed`` elements from the ``_id`` key with a
        *token* regular expression.

        """
        obs_token = 'was observed|' + token

        # These are the Relations Collection results.
        # According to the Document map, the results each have an
        # Objects Document.
        results = cls.search(token=obs_token, regex=True)

        if results is not None:
            objects = []
            for i in results:
                for j in i.to:
                    objects_cursor = oct_schema.model.Objects.search(j.id)
                    objects.extend([k for k in objects_cursor])

        return objects
