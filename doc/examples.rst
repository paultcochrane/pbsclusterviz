--------------------------------------------------------------------------
Examples
--------------------------------------------------------------------------

In the ``examples/`` directory of the distribution you will find some
pre-generated pbsnodes xml files and an example configuration file.

The first example works for the RRZN cluster system
(http://www.rrzn.uni-hannover.de/computeserver.html).  Change into the
examples/ directory and run the following command:

.. code-block:: bash

   $ pbs_cluster_status -x pbsnodes_rrzn.xml -n nodes.rrzn -c rrznviz.conf -i

