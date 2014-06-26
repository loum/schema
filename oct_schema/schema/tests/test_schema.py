import unittest2

import oct_schema.schema


class TestSchema(unittest2.TestCase):

    def test_init(self):
        """Initialise a :class:`oct.schema.Base` object
        """
        msg = 'Object is not an oct.schema.Base'
        b = oct_schema.schema.Base()
        self.assertIsInstance(b, oct_schema.schema.Base, msg)

    def test_mim(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        user = {'user': {'username': 'lupco',
                         'display_name': 'Lupco Markovski'}}
        b = oct_schema.schema.Base(user)
        b.m.insert()

        # Find and check.
        search_kwargs = {'user.username': 'lupco'}
        results = oct_schema.schema.Base.m.find(search_kwargs).first()
        received = results.get('user')
        expected = {'display_name': 'Lupco Markovski',
                    'username': 'lupco'}
        msg = 'Base document search returned incorrect results'
        self.assertDictEqual(received, expected, msg)
