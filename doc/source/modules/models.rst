.. oct.schema - Base MongoDB Model

.. toctree::
    :maxdepth: 2

The OCT MongoDB Model
=====================

:class:`oct_schema.models.base.Base` Class
------------------------------------------

The :class:`oct_schema.models.base.Base` class is the generic class that
should be inherited by all OCT Collections that will interface to MongoDB.
The default fields include:

.. autoclass:: oct_schema.models.base.Base

:class:`oct_schema.models.base.Objects` Class
---------------------------------------------

The :class:`oct_schema.models.objects.Objects` is a specialisation
of the :class:`oct_schema.models.base.Base` class that defines the
OCT Objects MongoDb Collection

.. autoclass:: oct_schema.models.objects.Objects

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
