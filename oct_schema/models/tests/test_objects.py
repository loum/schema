import unittest2

import oct_schema.models.objects


class TestObjectsModel(unittest2.TestCase):

    def test_init(self):
        """Initialise a :class:`oct.models.objects.Objects` object.
        """
        msg = 'Object is not an Objects'
        o = oct_schema.models.objects.Objects()
        self.assertIsInstance(o, oct_schema.models.objects.Objects, msg)
        o.rollback

    def test_mim(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        dc = oct_schema.models.objects.Objects(text_field='Objects collection text')
        dc.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = oct_schema.models.objects.Objects.query.find().count()
        expected = 1
        msg = 'Objects collection search returned incorrect count'
        self.assertEqual(received, expected, msg)
