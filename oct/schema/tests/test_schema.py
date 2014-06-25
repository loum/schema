import unittest2

import oct.schema


class TestSchema(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._bp = oct.schema.BlogPost()

    def test_init(self):
        """Initialise a :class:`oct.schema.BlogPost` object
        """
        msg = 'Object is not an oct.schema.BlogPost'
        self.assertIsInstance(self._bp, oct.schema.BlogPost, msg)

    def test_mim(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        x = oct.schema.BlogPoster(dict(title='Title', banana='xxx'))
        #self.assertDictEqual(x, {'title': 'Title'})

        x.m.save()
        print('xxx: %s' % x)

    @classmethod
    def tearDownClass(cls):
        del cls._bp
