import unittest2

import oct_schema


class TestSession(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        # Should parse the content from ./conf/settings.py
        cls._session = oct_schema.Session()
        cls._s = cls._session.state

    def test_init(self):
        """Initialise a :mod:`oct_schema.Session` object.
        """
        msg = 'Object is not a oct_schema.Session'
        self.assertIsInstance(self._session,
                              oct_schema.Session,
                              msg)

    def test_build_url_default_min_scheme(self):
        """Test build_url(): default mim scheme.
        """
        received = self._session.build_url()
        expected = 'mim://localhost:27017'
        msg = 'Default scheme URL error'
        self.assertEqual(received, expected, msg)

    def test_build_url_user_pw(self):
        """Test build_url(): valid user/pw.
        """
        kwargs = {'username': 'user',
                  'password': 'pw',
                  'dry': True}
        received = self._session.build_url(**kwargs)
        expected = 'mim://user:pw@localhost:27017'
        msg = 'Connection string with valid username/password error'
        self.assertEqual(received, expected, msg)

    def test_build_url_hosts_ports_as_lists(self):
        """Test build_url(): valid user/pw.
        """
        kwargs = {'hosts': ['host1', 'host2'],
                  'ports': ['27017', 27018],
                  'dry': True}
        received = self._session.build_url(**kwargs)
        expected = 'mim://host1:27017,host2:27018'
        msg = 'Connection string with hosts/ports lists error'
        self.assertEqual(received, expected, msg)

    def test_build_url_hosts_database(self):
        """Test build_url(): with database.
        """
        kwargs = {'db': 'tutorial'}
        received = self._session.build_url(**kwargs)
        expected = 'mim://localhost:27017/tutorial'
        msg = 'Connection string with database error'
        self.assertEqual(received, expected, msg)

    def test_build_url_invalid_user_pw_combo(self):
        """Test build_url(): invalid user/pw combo.
        """
        received = self._session.build_url(username='user')
        msg = 'Connection string with invalid username/password error'
        self.assertIsNone(received, msg)

    def test_build_url_invalid_host(self):
        """Test build_url(): invalid host.
        """
        received = self._session.build_url(hosts=None)
        msg = 'Connection string with invalid host error'
        self.assertIsNone(received, msg)

    def test_build_url_mongodb_scheme(self):
        """Test build_url(): mongodb scheme.
        """
        kwargs = {'scheme': 'mongodb',
                  'dry': True}
        received = self._session.build_url(**kwargs)
        expected = 'mongodb://localhost:27017'
        msg = 'mongodb scheme URL error'
        self.assertEqual(received, expected, msg)

    def test_build_url_unknown_scheme(self):
        """Test build_url(): unknown scheme.
        """
        received = self._session.build_url(scheme='banana')
        msg = 'Unknown scheme URL error'
        self.assertIsNone(received, msg)

    def test_check_username_password_combo(self):
        """Test _check_username_password().
        """
        kwargs = {'username': 'user',
                  'password': 'pw'}
        received = self._session._check_username_password(**kwargs)
        msg = 'Valid username/password combo should be True'
        self.assertTrue(received, msg)

        kwargs = {'username': None,
                  'password': 'pw'}
        received = self._session._check_username_password(**kwargs)
        msg = 'None/password combo should be False'
        self.assertFalse(received, msg)

        kwargs = {'username': 'user',
                  'password': None}
        received = self._session._check_username_password(**kwargs)
        msg = 'username/None combo should be False'
        self.assertFalse(received, msg)

    def test_build_hosts_string(self):
        """Test _build_hosts_string(): hosts scalar only.
        """
        kwargs = {'hosts': 'localhost',
                  'ports': None}
        received = self._session._build_hosts_string(**kwargs)
        expected = 'localhost'
        msg = 'Valid host should return a sane host string'
        self.assertEqual(received, expected, msg)

    def test_build_hosts_string_scalar_host_and_port(self):
        """Test _build_hosts_string(): hosts and ports scalar.
        """
        kwargs = {'hosts': 'localhost',
                  'ports': 27017}
        received = self._session._build_hosts_string(**kwargs)
        expected = 'localhost:27017'
        msg = 'Scalar host and port should return a sane host string'
        self.assertEqual(received, expected, msg)

    def test_build_hosts_string_host_list_and_scalar_port(self):
        """Test _build_hosts_string(): host list and scalar port.
        """
        kwargs = {'hosts': ['host1', 'host2'],
                  'ports': 27017}
        received = self._session._build_hosts_string(**kwargs)
        expected = 'host1:27017,host2:27017'
        msg = 'Host list and port scalar should return a sane host string'
        self.assertEqual(received, expected, msg)

    def test_build_hosts_string_host_and_port_list_unsymmetrical(self):
        """Test _build_hosts_string(): host/port list unsymmetrical.
        """
        kwargs = {'hosts': ['host1', 'host2'],
                  'ports': [27017]}
        received = self._session._build_hosts_string(**kwargs)
        msg = 'Host/port lists unsymmetrical should return None'
        self.assertIsNone(received, msg)

    def test_build_hosts_string_host_and_port_list_symmetrical(self):
        """Test _build_hosts_string(): host/port list symmetrical.
        """
        kwargs = {'hosts': ['host1', 'host2'],
                  'ports': [27017, '27018']}
        received = self._session._build_hosts_string(**kwargs)
        expected = 'host1:27017,host2:27018'
        msg = 'Host/port lists unsymmetrical should a sane host string'
        self.assertEqual(received, expected, msg)

    @classmethod
    def tearDownClass(cls):
        del cls._s
        del cls._session
