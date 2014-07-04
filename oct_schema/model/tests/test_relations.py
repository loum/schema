import unittest2

import oct_schema
import oct_schema.model


class TestRelations(unittest2.TestCase):

    def test_init(self):
        """Initialise a :class:`oct.model.Relations` object.
        """
        msg = 'Object is not an Relations'
        o = oct_schema.model.Relations()
        self.assertIsInstance(o, oct_schema.model.Relations, msg)
        o.rollback

    def test_mim(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        id = 'observation|2006-06-10T07:03:00Z|SAMPLEIMAGEID|Kirov CGN|Petr Valikiy (099)'
        kwargs = {'_id': 'was observed|Kirov CGN|Petr Valikiy (099)',
                  'id': [id]}
        o = oct_schema.model.Relations(**kwargs)
        o.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = oct_schema.model.Relations.query.find().count()
        expected = 1
        msg = 'Relations collection search returned incorrect count'
        self.assertEqual(received, expected, msg)
