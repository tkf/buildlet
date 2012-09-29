===========================
 Buildlet datastore module
===========================

.. automodule:: buildlet.datastore


.. inheritance-diagram::
   buildlet.datastore.inmemory.DataStreamInMemory
   buildlet.datastore.directory.DataFile
   buildlet.datastore.inmemory.DataValueInMemory
   buildlet.datastore.autoserialize.DataValuePickle
   buildlet.datastore.autoserialize.DataValueJSON
   buildlet.datastore.autoserialize.DataValueYAML
   buildlet.datastore.inmemory.DataStoreNestableInMemory
   buildlet.datastore.directory.DataDirectory
   buildlet.datastore.autodirectory.DataAutoDirectory
   :parts: 1
   :private-bases:

.. autoclass:: buildlet.datastore.base.BaseDataStore
   :members:


Three kinds of datastore classes
================================

.. py:module:: buildlet.datastore.base

There are three kinds of datastore classes:
stream type (:py:class:`BaseDataStream`),
value store type (:py:class:`BaseDataValue`) and
nestable type (:py:class:`BaseDataStoreNestable`).

Stream
------

.. inheritance-diagram::
   buildlet.datastore.inmemory.DataStreamInMemory
   buildlet.datastore.directory.DataFile
   :parts: 1
   :private-bases:

.. autoclass:: buildlet.datastore.base.BaseDataStream
   :members:


Value store
-----------

.. inheritance-diagram::
   buildlet.datastore.inmemory.DataValueInMemory
   buildlet.datastore.autoserialize.DataValuePickle
   buildlet.datastore.autoserialize.DataValueJSON
   buildlet.datastore.autoserialize.DataValueYAML
   :parts: 1
   :private-bases:

.. autoclass:: buildlet.datastore.base.BaseDataValue
   :members:

Nestable
--------

.. inheritance-diagram::
   buildlet.datastore.directory.DataDirectory
   buildlet.datastore.autodirectory.DataAutoDirectory
   buildlet.datastore.inmemory.DataStoreNestableInMemory
   :parts: 1
   :private-bases:

.. autoclass:: buildlet.datastore.base.BaseDataStoreNestable
   :members:


:py:mod:`buildlet.datastore.base`
=================================

.. automodule:: buildlet.datastore.base
   :members:
   :exclude-members: BaseDataStore,
                     BaseDataStream,
                     BaseDataValue,
                     BaseDataStoreNestable

:py:mod:`buildlet.datastore.inmemory`
=====================================

.. automodule:: buildlet.datastore.inmemory
   :members:

:py:mod:`buildlet.datastore.directory`
======================================

.. automodule:: buildlet.datastore.directory
   :members:

:py:mod:`buildlet.datastore.autodirectory`
==========================================

.. automodule:: buildlet.datastore.autodirectory
   :members:

:py:mod:`buildlet.datastore.autoserialize`
==========================================

.. automodule:: buildlet.datastore.autoserialize
   :members:
