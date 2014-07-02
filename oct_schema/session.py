__all__ = [
    'Session',
]
import os
import ming
import ming.odm
import json

from oct.utils.log import log


class Session(object):
    """Based on the Borg monostate idiom, only one instance the class is
    ever created.

    """
    _state = {}

    def __new__(cls, *p, **k):
        self = object.__new__(cls)
        self.__dict__ = cls._state

        return self

    def __init__(self, **kwargs):
        if self._state.get('s') is None:
            log.debug('Creating Session state ...')

            db_kwargs = kwargs.copy()
            if len(db_kwargs.keys()) == 0:
                db_kwargs = self.parse_settings() 
            url = self.build_url(**db_kwargs)
            bind = ming.create_datastore(url)
            kwargs = {'doc_session': ming.Session(bind)}
            self._state['s'] = ming.odm.ThreadLocalODMSession(**kwargs)
            self._state['obj'] = self

            log.debug('Session state created')
        else:
            log.debug('Session state already exists')

    @property
    def state(self):
        return self._state.get('s')

    @property
    def odm_session(self):
        return Session._state.get('s')

    def build_url(self,
                  scheme='mim',
                  username=None,
                  password=None,
                  hosts='localhost',
                  ports=27017,
                  db=None,
                  dry=False):
        """Prepares the DB connection string and sets up a connection
        session to MongoDB.

        The URL connection string format follows::

            mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]

        Basic parts of the url:

        * **mongodb://**
            * required URL scheme used to define the connection format
            * the default ``mim`` will connect to the :mod:`ming`
              Mongo In Memory implementation

        * **username:password@**
            * if this optional argument is given, the driver will attempt to
              login to a database after connecting to a database server

        * **host1**
            * required argument identifies either a hostname, IP address or
              UNIX domain socket

        * **:portX**
            * optional port configuration.  Defaults to **:27017**

        * **/database**
            * optional name of the database to login to.  Only relevant if
              the **username:password@** syntax is used.  If not specified,
              the **admin** database will be used by default

        * **?options**
            * optional connection options
            * if database is absent, there is still a ``/`` required between
              the last host and the ``?`` introducing the options.
            * options are ``name=value`` pairs.  Multiple options are
              separated by ``&``.  Bit of a throwaway, but we support what
              :mod:`ming` supports

        **Kwargs:**
            *scheme*: defaults to ``mim`` which provides implementation of
            the pymongo API that allows you to perform testing of your
            application without having a dependency on a MongoDB server.
            Can be substituted with ``mongodb`` to connect to a fully
            qualified DB

            *username*: database username value

            *password*: database password value

            *hosts*: hosts to connect to.  Can be a scalar or a list of
            scalars.  Mandatory argument that defaults to ``localhost``

            *ports*: host ports to connect to.  Can be a scalar or a list.
            If provided in list context, must be same length as hosts list.

            *db*: the MongoDB database instance to connect to.  If ``None``,
            will assume the ``admin`` database

        **Returns:**
            Sets the global oct_schema.session.SESSION variable and returns
            the URL connection string if valid.  ``None`` otherwise

        """
        log.debug('Preparing MondoDB connection session ...')
        url = safe_url = None

        # Check the scheme.
        if scheme != 'mim' and scheme != 'mongodb':
            log.error('Unsupported scheme "%s"' % scheme)
        else:
            safe_url = '%s://' % scheme
            url = '%s://' % scheme

        # Username/password are optional, but we should check for a valid
        # structure if an intension to provide credentials was made.
        if username is not None or password is not None:
            valid_credentials = self._check_username_password(username,
                                                              password)
            if valid_credentials:
                safe_url += '%s:********@' % username
                url += '%s:%s@' % (username, password)
            else:
                url = safe_url = None

        # The host:port.
        if url is not None:
            host_port = self._build_hosts_string(hosts, ports)
            if host_port is not None:
                safe_url += '%s' % host_port
                url += '%s' % host_port
            else:
                url = safe_url = None

        # (Optional) database.
        if url is not None:
            if db is not None:
                safe_url += '/%s' % db
                url += '/%s' % db

        if url is not None:
            log.info('MongoDB connection string: "%s"' % safe_url)
            if not dry:
                bind = ming.create_datastore(url)
                kwargs = {'doc_session': ming.Session(bind)}
                self._state['s'] = ming.odm.ThreadLocalODMSession(**kwargs)
            else:
                log.debug('Connection skipped: dry run spefified')
        else:
            log.error('MongoDB connection string generation failed')

        return url

    def _check_username_password(self, username, password):
        """Simple, pivate helper method that just checks that a sane
        username and password combination is provided.

        **Args:**
            *username*: username value

            *password*: password value

        Returns:
            Boolean ``True`` if the username and password are a valid
            string combination.  boolean False`` otherwise

        """
        pw_string = '********'
        if password is None:
            pw_string = None
        log.debug('Checking "<username>/<password>": "%s/%s' % (username,
                                                                pw_string))

        status = False

        if (isinstance(username, basestring) and
            isinstance(password, basestring)):
            status = True

        log.debug('"<username>/<password>": "%s/%s status: %s' % (username,
                                                                pw_string,
                                                                status))

        return status

    def _build_hosts_string(self, hosts, ports):
        """Builds the ``host:port`` section of the MongoDB connection
        string.

        Format follows::

            host1[:port1][,host2[:port2],...[,hostN[:portN]

        Yes, multiple ``host:port`` combinations are supported.

        At least one host must be provided (with an optional port)

        *hosts* and *ports* can be a scalar or a list of scalars (for
        multiple ``host:port`` combinations).  Furthermore:

        * if *hosts* is a list and *ports* a scalar then the scalar *ports*
          will be applied to all *hosts*.  For example::

            >>> from oct_schema.session import _build_hosts_string
            >>> x = _build_hosts_string(['host1', 'host2'], 20718)
            >>> x
            "host1:20718,host2:20718"

        * if both *hosts* and *ports* are lists then they must be
          symmetrical in size.  For example::

            >>> from oct_schema.session import _build_hosts_string
            >>> x = _build_hosts_string(['host1', 'host2'], [20718, 20719])
            >>> x
            "host1:20718,host2:20719"

        **Args:**
            *hosts*: hosts to connect to.  Can be a scalar or a list of
            scalars.  Mandatory argument that defaults to ``localhost``

            *ports*: host ports to connect to.  Can be a scalar or a list.
            If provided in list context, must be same length as hosts list.

        **Returns:**
            The MongoDB formatted host/port string

        """
        log.debug('Building hosts string for <hosts>/<ports>: "%s/%s"' %
                (str(hosts), str(ports)))

        host_string = None

        # A host is required.  More than one is OK too.
        if not isinstance(hosts, (list, basestring)):
            log.error('At least one host is required')
        else:
            # OK, is it a list or a scalar?
            if isinstance(hosts, basestring):
                host_string = '%s' % hosts
                if isinstance(ports, (int, basestring)):
                    host_string += ':%s' % str(ports)
            elif isinstance(hosts, list):
                if isinstance(ports, (int, basestring)):
                    d = dict(zip(hosts, len(hosts) * [str(ports)]))
                    l = ['%s:%s' % (k, v) for k, v in d.iteritems()]
                    host_string = ','.join(sorted(l))
                elif isinstance(ports, list):
                    if len(hosts) != len(ports):
                        log.error('Ambiguous <hosts>/<ports>: "%s/%s"' %
                                (str(hosts), str(ports)))
                        host_string = None
                    else:
                        d = dict(zip(hosts, ports))
                        l = ['%s:%s' % (k, v) for k, v in d.iteritems()]
                        host_string = ','.join(sorted(l))

        return host_string


    def parse_settings(self):
        """Configuration file for the :class:`oct_schema.Session` class
        can be provided in the following locations (in order
        of precedence):

        * A place named by an environment variable ``SETTINGS_CONF``
        * Local directory - ``./settings.conf``
        * User's home directory - ``~<user>/settings.conf``
        * A standard system-wide directory -
          ``/etc/myproject/settings.conf`` (NOT SUPPORTED YET)
        * The ``conf`` directory of the package distribution

        This arrangement is analogous to "rc" files.  for example, "bashrc",
        "vimrc", etc.

        Typical source configuration file is formatted in JSON
        as follows::

            {
                "db":
                {
                    "scheme": "mim",
                    "username": "username",
                    "password": "password",
                    "hosts": "localhost",
                    "ports": "27018"
                    "db": "tutorial",
                }
            }

        .. note::

            The ``mim`` schema will invoke a special MongoDB In Memory
            instance.  To connect to a real MongoDB instance, substitue
            the scheme ``mim`` for ``mongodb``

        **Returns:**
            Once a source configuration is found, contents will be parsed
            and converted to a Python dictionary structure::

                {'db': {'scheme': 'mim', 'username': 'username' ...}}
            
        """
        db_kwargs = {}

        locations = [os.environ.get("SETTINGS_CONF"),
                     os.curdir,
                     os.path.expanduser("~"),
                     os.path.join(os.curdir, 'conf')]

        for loc in locations:
            if loc is None:
                continue
            conf_file = os.path.join(loc, 'settings.conf')
            log.debug('Checking if "%s" exists ...' % conf_file)

            try:
                f = open(os.path.join(loc, 'settings.conf'))
                json_settings = json.load(f)
                db_kwargs = json_settings.get('db')
                break
            except IOError:
                # Not a bad thing if the open failed.  Just means that the
                # log source does not exist.
                log.debug('"%s" was not found' % conf_file)
                continue

        return db_kwargs
