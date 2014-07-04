.. oct.schema - Base MongoDB Model

.. toctree::
    :maxdepth: 2

The OCT MongoDB Model
=====================

:class:`oct_schema.ModelBase` Class
-----------------------------------

The :class:`oct_schema.ModelBase` class is the generic class that
should be inherited by all OCT Collections that will interface to MongoDB.
The default fields include:

.. autoclass:: oct_schema.ModelBase

:class:`oct_schema.model.Objects` Class
----------------------------------------

The :class:`oct_schema.model.Objects` is a specialisation
of the :class:`oct_schema.ModelBase` class that defines the
OCT Objects MongoDb Collection.

.. autoclass:: oct_schema.model.Objects

:class:`oct_schema.model.Ontology` Class
----------------------------------------

The :class:`oct_schema.model.Ontology` is a specialisation
of the :class:`oct_schema.ModelBase` class that defines the
OCT Ontology MongoDb Collection.

.. autoclass:: oct_schema.model.Objects
