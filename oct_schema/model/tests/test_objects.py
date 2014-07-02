import unittest2

import oct_schema
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
        kwargs = {'category_code': 'Objects category_code',
                  'location': {'type': 'Point',
                               'coordinates': {'latitude': 33.4217,
                                               'longitude': 69.0789}}}
        o = oct_schema.model.Objects(**kwargs)
        o.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = oct_schema.model.Objects.query.find().count()
        expected = 1
        msg = 'Objects collection search returned incorrect count'
        self.assertEqual(received, expected, msg)
