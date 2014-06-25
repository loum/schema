.. oct.schema - Base MongoDB Schema Object

.. toctree::
    :maxdepth: 2

MongoDB Schema Enforcement
==========================
Yeah, yeah ...  MongoDB Schema Enforcement seems like a contradiction
of the MongoDB NoSQL philosophy.  But we probably want some control over
what people will be putting into our Collections (especially if we are
opening this to a RESTful interface).

Built over the :mod:`ming` framework, the object here is to provide
a layer of separation from the actual MongoDB interface so that we can
intercept the Document and provide validation, sanitisation, default
settings etc.  :mod:`ming` also supports a migration context that will
ensure that our interface remains consistent as the Collection schema
changes.

Base MongoDB Schema Object
--------------------------
The :class:`oct.schema.Base` class is the generic class that should be
inherited by all OCT Collections that will interface to MongoDB.
The default fields include:

* ``created_ts`` - timestamp of when the Document was first created

* ``modified_ts`` - timestamp of when the document was last modified

* ``user`` - name of the user that created/modified the Document

.. automodule:: oct.schema
    :members:

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
