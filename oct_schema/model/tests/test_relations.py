import unittest2
import os
import re

import oct_schema
import oct_schema.model
from oct.utils.log import set_log_level


class TestRelations(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        fixtures_dir = os.path.join('oct_schema',
                                    'model',
                                    'tests',
                                    'fixtures')

        f = os.path.join(fixtures_dir, 'relations.json')
        oct_schema.model.Relations._batch_loader(f)

        f = os.path.join(fixtures_dir, 'objects.json')
        oct_schema.model.Objects._batch_loader(f)

    def test_init(self):
        """Initialise a :class:`oct.model.Relations` object.
        """
        msg = 'Object is not an Relations instance'
        o = oct_schema.model.Relations()
        self.assertIsInstance(o, oct_schema.model.Relations, msg)
        o.rollback

    def test_insert_and_delete(self):
        """Test Relations collection insert and delete.
        """
        event = 'observation'
        date = '2006-06-10T07:03:00Z'
        image = 'SAMPLEIMAGEID'
        type = 'Kirov CGN'
        name = 'Petr Valikiy (test)'
        id = '%s|%s|%s|%s|%s' % (event, date, image, type, name)
        kwargs = {'_id': 'was observed|Kirov CGN|Petr Valikiy (test)',
                  'id': [id]}
        o = oct_schema.model.Relations(**kwargs)
        o.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = oct_schema.model.Relations.query.find().count()
        expected = 13
        msg = 'Relations collection search returned incorrect count'
        self.assertEqual(received, expected, msg)

        # Clean up.
        kwargs = {'_id': 'was observed|Kirov CGN|Petr Valikiy (test)'}
        results = oct_schema.model.Relations.query.find(kwargs)
        set_log_level('INFO')
        for i in results:
            i.delete()
            i.flush
        set_log_level('DEBUG')

        # Restore original fixture count.
        received = oct_schema.model.Relations.query.find().count()
        expected = 12
        msg = 'Objects collection returned incorrect count after clean'
        self.assertEqual(received, expected, msg)

    def test_batch_loader(self):
        """Test the batch loader: Kirov CGN wildcard search against _id key.
        """
        regx = re.compile('.*kirov.*', re.IGNORECASE)
        kwargs = {'_id': regx}
        results = oct_schema.model.Relations.query.find(kwargs)
        set_log_level('INFO')
        received = [i._id for i in results]
        set_log_level('DEBUG')
        expected = ['has component|Kirov CGN|Petr Valikiy (099)',
                    'was observed|Kirov CGN|Petr Valikiy (099)',
                    'was observed|Kirov CGN|Unidentified']
        msg = 'Kirov wildcard search against _id error'
        self.assertListEqual(sorted(received), sorted(expected), msg)

    def test_search(self):
        """Test the Relations context search method.
        """
        set_log_level('INFO')
        results = oct_schema.model.Relations.search(token='Kirov',
                                                    regex=True)
        dict_documents = [d.to_dict() for d in results]
        received = []
        for i in dict_documents:
            for k, v in i.iteritems():
                if k == '_id':
                    received.append({k: v})
        set_log_level('DEBUG')
        expected = [{'_id': u'has component|Kirov CGN|Petr Valikiy (099)'},
                    {'_id': u'was observed|Kirov CGN|Petr Valikiy (099)'},
                    {'_id': u'was observed|Kirov CGN|Unidentified'}]
        msg = 'Kirov wildcard search against _id error'
        self.assertListEqual(sorted(received), sorted(expected), msg)

    def test_observation_search(self):
        """Test the Relations observation search method.
        """
        token = 'Kirov CGN'

        set_log_level('INFO')
        results = oct_schema.model.Relations.observation_search(token)
        dict_documents = [d.to_dict() for d in results]
        received = []
        for i in dict_documents:
            for k, v in i.iteritems():
                if k == 'description':
                    received.append({k: v})
        set_log_level('DEBUG')
        expected = [{'description': u'The Top Pair radar was observed removed from its mount position'},
                    {'description': ''}]
        msg = 'Observation document to_dict translation error'
        self.assertListEqual(sorted(received), sorted(expected), msg)
