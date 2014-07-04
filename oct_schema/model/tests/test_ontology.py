import unittest2

import oct_schema
import oct_schema.model


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
        kwargs = {'_id': 'ontology|abstract',
                  'name': 'abstract',
                  'gloss': g}
        o = oct_schema.model.Ontology(**kwargs)
        o.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = oct_schema.model.Ontology.query.find().count()
        expected = 1
        msg = 'Ontology collection search returned incorrect count'
        self.assertEqual(received, expected, msg)
