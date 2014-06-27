.. oct.schema - Base MongoDB Model

.. toctree::
    :maxdepth: 2

Base MongoDB Model
==================
The :class:`oct_schema.models.Base` class is the generic class that should
be inherited by all OCT Collections that will interface to MongoDB.
The default fields include:

* ``created_ts`` - timestamp of when the Document was first created

* ``modified_ts`` - timestamp of when the document was last modified

:class:`oct_schema.models.Base` Class
-------------------------------------
.. autoclass:: oct_schema.models.Base

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
