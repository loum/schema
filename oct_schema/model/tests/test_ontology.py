import unittest2
import os
import re

import oct_schema
import oct_schema.model
from oct.utils.log import set_log_level


class TestOntology(unittest2.TestCase):

    def test_init(self):
        """Initialise a :class:`oct.model.Ontology` object.
        """
        msg = 'Object is not an Ontology'
        o = oct_schema.model.Ontology()
        self.assertIsInstance(o, oct_schema.model.Ontology, msg)
        o.rollback

    def test_mim(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        g = 'The parent type from which all types derive'
        kwargs = {'_id': 'ontology|tester',
                  'name': 'abstract',
                  'gloss': g}
        o = oct_schema.model.Ontology(**kwargs)
        o.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = oct_schema.model.Ontology.query.find().count()
        expected = 62
        msg = 'Ontology collection search returned incorrect count'
        self.assertEqual(received, expected, msg)

    def test_batch_loader(self):
        """Test the batch loader: actor wildcard search against _id key.
        """
        fixtures_dir = os.path.join('oct_schema',
                                    'model',
                                    'tests',
                                    'fixtures')

        f = os.path.join(fixtures_dir, 'ontology.json')
        oct_schema.model.Ontology()._batch_loader(f)

        regx = re.compile('.*actor.*', re.IGNORECASE)
        kwargs = {'_id': regx}
        results = oct_schema.model.Ontology.query.find(kwargs)
        set_log_level('INFO')
        received = [i._id for i in results]
        set_log_level('DEBUG')
        expected = ['ontology|actor']
        msg = 'actor wildcard search against _id error'
        self.assertListEqual(sorted(received), sorted(expected), msg)
