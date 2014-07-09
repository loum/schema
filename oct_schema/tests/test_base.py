import unittest2
import ming.odm
import datetime

import oct_schema
from oct.utils.log import set_log_level


class DodgeCollection(oct_schema.ModelBase):
    """A dodgy collection class that inherits from
    :class:`oct_schema.model_base.BaseModel`

    """
    class __mongometa__:
        name = 'dodgy_collection'

    text_field = ming.odm.FieldProperty(str)

ming.odm.Mapper.compile_all()


class TestInheritedModel(unittest2.TestCase):

    def _bson_utc_now(self):
        """Simple wrapper around :func:`datetime.datetime.utcnow` that
        truncates microseconds to mimic BSON datetime.

        """
        dt = datetime.datetime.utcnow()
        return dt.replace(microsecond=(dt.microsecond // 1000) * 1000)

    def test_init(self):
        """Initialise a DodgeCollection object.
        """
        dc = DodgeCollection(text_field='Banana')
        msg = 'Object is not a DodgeCollection'
        self.assertIsInstance(dc, DodgeCollection, msg)
        dc.rollback

    def test_mim(self):
        """Test the MongoDB-in-Memory Ming component.
        """
        dc = DodgeCollection(text_field='Banana')
        dc.flush

        # Find and check.
        # Here, use Ming's get() convenience method (find(kwargs).count())
        received = DodgeCollection.query.find().count()
        expected = 1
        msg = 'Inherited ODM search returned incorrect count'
        self.assertEqual(received, expected, msg)

        # Clean up.
        kwargs = {'text_field': 'Banana'}
        results = DodgeCollection.query.find(kwargs)
        set_log_level('INFO')
        for document in results:
            document.delete()
            document.flush
        set_log_level('DEBUG')

    def test_to_dict(self):
        """Convert a ming.Document object to JSON.
        """
        token = 'dictionary conversion'
        dt = self._bson_utc_now()
        kwargs = {'_id': 'xxxxxx',
                  'text_field': token,
                  'created_ts': dt}
        dc = DodgeCollection(**kwargs)
        dc.flush

        results = DodgeCollection.query.find({'_id': 'xxxxxx'})
        set_log_level('INFO')
        for document in results:
            received = document.to_dict()
            expected = kwargs.copy()
            expected.update({'modified_ts': None})
            msg = 'DodgeCollection object to_dict translation error'
            self.assertDictEqual(received, expected, msg)
        set_log_level('DEBUG')

        # Clean up.
        results = DodgeCollection.query.find({'_id': 'xxxxxx'})
        set_log_level('INFO')
        for document in results:
            document.delete()
            document.flush
        set_log_level('DEBUG')
