--------------------------------------------------------------------------
Usage
--------------------------------------------------------------------------

Firstly, a nodes file needs to be generated.  This specifies how the nodes
for the entire cluster system will be displayed.  The cluster nodes are
displayed as boxes laid out in a grid.  One essentially has many rows of
cluster nodes a set number of nodes wide (e.g. 40 nodes wide would be
appropriate for very large installations, the default of 10 nodes should be
OK for smaller cluster installations).  To get the right numbers one must
experiment somewhat.  

When the nodes file is initially generated, a basic structure will be
created which can be later fine tuned by hand.

***********************
Generating a nodes file
***********************

.. code-block:: bash

   $ pbsnodes -x > pbsnodes.xml
   $ gen_nodes_file -x pbsnodes.xml \
              -n <node_section_name> -p <node_prefix> -o nodes

Many cluster installations are collections of one or more smaller clusters
of computers, each with their own naming strategy.  For instance, a cluster
called "LinuxCluster" could have nodes labeled ``lcn01``, ``lcn02``, ``lcn03``... etc.
Therefore, one needs to specify a node prefix so that ``gen_nodes_file`` can
pick the relevant nodes out of the pbsnodes xml file.  The node section name
is a comment in the generated nodes file.

To account for more than one cluster in an entire cluster system one appends
to an existing nodes file with the ``-a`` option to ``gen_nodes_file``.

For example, with three clusters "TinyCluster", "LinuxCluster" and
"BigOldBull", where the nodes are labelled ``tcn<xx>``, ``lcn<xx>`` and ``bobn<xx>``
respectively, one would run ``gen_nodes_file`` like so:

.. code-block:: bash

   $ gen_nodes_file -x pbsnodes.xml -n TinyCluster -p tcn -o nodes
   $ gen_nodes_file -x pbsnodes.xml -n LinuxCluster -p lcn -o nodes -a
   $ gen_nodes_file -x pbsnodes.xml -n BigOldBull -p bobn -o nodes -a

The output is a plain text file called ``nodes`` which you can then alter to
your heart's content.  If you add a new cluster to your configuration, you
merely need to use the line

.. code-block:: bash

   $ gen_nodes_file -x pbsnodes.xml -n NewCluster -p newn -o nodes -a

to add the new cluster nodes to your load and job status visualisation.

Now that the nodes file has been generated, you're now ready to begin
visualising the load and job status of your cluster system.

**********************************
Visualising the system load status
**********************************

To generate an interactive three-dimensional view of the current load of all
nodes in your cluster system, you merely need to run the ``cluster_status``
command:

.. code-block:: bash

   $ cluster_status

To view current job-level utilisation of all nodes just press the "j" button
when viewing the cluster.

If you wish, you can specify a previously generated pbsnodes xml file:

.. code-block:: bash

   $ cluster_status -x pbsnodes.xml

The title of the output image is controlled by the configuration file
(default: ``clusterviz.conf``).  In the section ``[load viewer]`` you merely
need to set the value of the ``title`` key to the title you wish to use.
For example:

.. code-block:: ini

    [load viewer]
    title = My awesome cluster load status

To specify an alternate configuration file, you can use the ``-c`` option:

.. code-block:: bash

   $ cluster_load_status -c mycluster.conf

If you wish to use the program non-interactively and thereby generate an
image of the cluster status at that point in time, just use the ``-N`` option.

.. code-block:: bash

   $ cluster_load_status -N

When the program is called, the cluster status image appears briefly on the
screen and then disappears.  This image is then saved to the file
``cluster_load_status.png`` by default.

*********************************
Visualising the system job status
*********************************

In order to view the job status of your cluster system you merely need to
use the ``cluster_status`` command with the ``-m/--display_mode`` option, e.g.:

.. code-block:: bash

   $ cluster_status -m job

To change the default title of the generated image, you need to set the
value of the ``title`` key in the ``job viewer]`` section of the configuration
file (``clusterviz.conf``):

.. code-block:: ini

    [job viewer]
    title = My awesome cluster job status

As before, in order to generate an output image one needs to use the
``'-N/--non_interactive``' option:

.. code-block:: bash

   $ cluster_status -m job -N

By default this will generate an image with filename
``cluster_job_status.png``.

********************
Updating the display
********************

The display output can be updated by pressing the ``u`` key when in
interactive mode.

****************************************************
Generating movies of your cluster status information
****************************************************

The cluster load and job status images are saved to disk with the respective
filenames ``cluster_load_status.png`` and ``cluster_job_status.png``.  An
extra file image file with the current timestamp is also saved for each type
of status image.  These files can then be used to create movies of the
evolution of the cluster status over time and can give insight into patterns
not otherwise obvious from viewing the static images.  The best way to
produce such movies is to run ``'cluster_status -m load`` and
``cluster_status -m job`` as cron jobs.  For instance, one could save images
every ten minutes, then after a day or even a week, one can generate an mpeg
movie file from the collected images.


