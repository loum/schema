import unittest2

import oct_schema.model


class TestObjects(unittest2.TestCase):

    def test_init(self):
        """Initialise a :class:`oct.model.Objects` object.
        """
        msg = 'Object is not an Objects'
        o = oct_schema.model.Objects()
        self.assertIsInstance(o, oct_schema.model.Objects, msg)
        o.rollback

    def test_mim(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        dc = oct_schema.model.Objects(text_field='Objects collection text')
        dc.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = oct_schema.model.Objects.query.find().count()
        expected = 1
        msg = 'Objects collection search returned incorrect count'
        self.assertEqual(received, expected, msg)
