.. PBS Cluster Viz documentation master file, created by
   sphinx-quickstart on Sat Jul  9 12:59:20 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the PBS Cluster Viz documentation!
=============================================

PBS Cluster Viz is a project to display information useful to admins and
users about a computing cluster managed by a PBS-compatible resource
manager. Information includes load and job distribution. 

--------------------------------------------------------------------------
Contents:
--------------------------------------------------------------------------

.. toctree::
   :maxdepth: 2

   installation.rst
   usage.rst
   examples.rst
   development.rst
   api.rst

Project page:
    http://sourceforge.net/projects/pbsclusterviz/

--------------------------------------------------------------------------
For the impatient:
--------------------------------------------------------------------------

.. code-block:: bash

    $ python setup.py install
    $ pbsnodes -x > pbsnodes.xml
    # assuming your cluster nodes all start with 'lcn'
    $ gen_nodes_file -x pbsnodes.xml -n Cluster -p lcn -o nodes
    $ cluster_status

--------------------------------------------------------------------------
Example output
--------------------------------------------------------------------------

+-------------------------------------+--------------------------------------+
|     Job fill level                  |     Load status                      |
+=====================================+======================================+
| .. image:: job_status_july_2011.png | .. image:: load_status_july_2011.png |
|    :width: 300pt                    |    :width: 300pt                     |
+-------------------------------------+--------------------------------------+

--------------------------------------------------------------------------
Indices and tables
--------------------------------------------------------------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

