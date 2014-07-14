import unittest2
import os
import re

import oct_schema
import oct_schema.model
from oct.utils.log import set_log_level


class TestObjects(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        fixtures_dir = os.path.join('oct_schema',
                                    'model',
                                    'tests',
                                    'fixtures')

        f = os.path.join(fixtures_dir, 'objects.json')
        oct_schema.model.Objects._batch_loader(f)

    def test_init(self):
        """Initialise a :class:`oct.model.Objects` object.
        """
        msg = 'Object is not an Objects instance'
        o = oct_schema.model.Objects()
        self.assertIsInstance(o, oct_schema.model.Objects, msg)
        o.rollback

    def test_insert_and_delete(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        kwargs = {'_id': 'facility|severomorsk naval base (test)',
                  'latitude': 33.4217,
                  'longitude': 69.0789}
        o = oct_schema.model.Objects(**kwargs)
        o.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = oct_schema.model.Objects.query.find().count()
        expected = 20
        msg = 'Objects collection search returned incorrect count'
        self.assertEqual(received, expected, msg)

        # Clean up.
        kwargs = {'_id': 'facility|severomorsk naval base (test)'}
        results = oct_schema.model.Objects.query.find(kwargs)
        set_log_level('INFO')
        for i in results:
            i.delete()
            i.flush
        set_log_level('DEBUG')

        # Restore original fixture count.
        received = oct_schema.model.Objects.query.find().count()
        expected = 19
        msg = 'Objects collection returned incorrect count after clean'
        self.assertEqual(received, expected, msg)

    def test_batch_loader(self):
        """Test the batch loader: Kirov wildcard search against _id key.
        """
        regx = re.compile('.*kirov.*', re.IGNORECASE)
        kwargs = {'_id': regx}
        results = oct_schema.model.Objects.query.find(kwargs)
        set_log_level('INFO')
        received = [i._id for i in results]
        set_log_level('DEBUG')
        expected = ['ship|Kirov CGN',
                    'observation|2006-06-10T07:03:00Z|SAMPLEIMAGEID|Kirov CGN|Petr Valikiy (099)',
                    'observation|2006-06-10T07:03:00Z|SAMPLEIMAGEID|Kirov CGN|# 001']
        msg = 'Kirov wildcard search against _id error'
        self.assertListEqual(sorted(received), sorted(expected), msg)
