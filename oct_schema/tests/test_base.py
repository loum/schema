import unittest2
import ming.odm

import oct_schema

class DodgeCollection(oct_schema.ModelBase):
    """A dodgy collection class that inherits from
    :class:`oct_schema.model_base.BaseModel`

    """
    class __mongometa__:
        name = 'dodgy_collection'

    text_field = ming.odm.FieldProperty(str)

ming.odm.Mapper.compile_all()


class TestInheritedModel(unittest2.TestCase):

    def test_init(self):
        """Initialise a DodgeCollection object.
        """
        dc = DodgeCollection(text_field='Banana')
        msg = 'Object is not a DodgeCollection'
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
