--------------------------------------------------------------------------
Installation
--------------------------------------------------------------------------

Installation in a central location:

.. code-block:: bash

   $ python setup.py install

Installation in your home directory:

.. code-block:: bash

   $ python setup.py install --prefix=$HOME/pbsclusterviz

Then you need to extend your PYTHONPATH environment variable so:

.. code-block:: bash

   $ export PYTHONPATH=$PYTHONPATH:$HOME/pbsclusterviz/lib/python2.5/site-packages

and extend your PATH so:

.. code-block:: bash

   $ export PATH=$PATH:$HOME/pbsclusterviz/bin


Dependencies:
   * Python Version 2.5+

     ``$ aptitude install python``

   * The Visualisation Toolkit Version 5.2+ with Python bindings

     ``$ aptitude install python-vtk``

   * Python XML libraries

     ``$ aptitude install python-xml``

   * Sphinx (in order to build the html docs)

     ``$ aptitude install python-sphinx``
