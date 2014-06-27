import unittest2
import ming.odm

import oct_schema.models.base


class DodgeCollection(oct_schema.models.base.Base):
    """A dodgy collection class that inherits from
    :class:`oct_schema.models.Base`

    .. attribute:: created_ts
        :mod:`datetime` object that captures the timestamp of when
        the Document was first created

    """
    class __mongometa__:
        name = 'dodgy_collection'

    text_field = ming.odm.FieldProperty(str)


class TestInheritedModel(unittest2.TestCase):

    def test_init(self):
        """Initialise a :class:`oct.models.DodgeCollection` object.
        """
        msg = 'Object is not a DodgeCollection'
        dc = DodgeCollection(text_field='Banana')
        self.assertIsInstance(dc, DodgeCollection, msg)
        dc.rollback

    def test_mim(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        dc = DodgeCollection(text_field='Banana')
        dc.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = DodgeCollection.query.find().count()
        expected = 1
        msg = 'Inherited ODM search returned incorrect count'
        self.assertEqual(received, expected, msg)
