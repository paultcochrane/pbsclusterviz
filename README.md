PBS Cluster Viz
===============

Project page:
    https://github.com/paultcochrane/pbsclusterviz

--------------------------------------------------------------------------
For the impatient:
--------------------------------------------------------------------------

    $ python setup.py install
    $ pbsnodes -x > pbsnodes.xml
    # assuming your cluster nodes all start with 'lcn'
    # and your cluster name is "Cluster"
    $ gen_nodes_file -x pbsnodes.xml -n Cluster -p lcn -o nodes
    $ cluster_status

--------------------------------------------------------------------------
Installation
--------------------------------------------------------------------------

Installation in a central location:

    $ python setup.py install

Installation in your home directory:

    $ python setup.py install --prefix=$HOME/pbsclusterviz

Then you need to extend your PYTHONPATH environment variable so:

    $ export PYTHONPATH=$PYTHONPATH:$HOME/pbsclusterviz/lib/python2.x/site-packages

and extend your PATH so:

    $ export PATH=$PATH:$HOME/pbsclusterviz/bin


Dependencies:
    * Python Version 2.4+
        $ aptitude install python
        or
        $ yum install python
    * The Visualisation Toolkit Version 5.4+ with Python bindings
        $ aptitude install python-vtk
        or
        $ yum install vtk-python (in the EPEL repository)
    * Python XML libraries
        $ aptitude install python-libxml2
        or
        $ yum install libxml2-python
    * Python TkInter (for full interactive usage)
        $ aptitude install python-tk
        or
        $ yum install tkinter
    * Sphinx (in order to build the html docs)
        $ aptitude install python-sphinx
        or
        $ yum install python-sphinx

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

    $ pbsnodes -x > pbsnodes.xml
    $ gen_nodes_file -x pbsnodes.xml \
               -n <node_section_name> -p <node_prefix> -o nodes

Many cluster installations are collections of one or more smaller clusters
of computers, each with their own naming strategy.  For instance, a cluster
called "LinuxCluster" could have nodes labeled lcn01, lcn02, lcn03... etc.
Therefore, one needs to specify a node prefix so that gen_nodes_file can
pick the relevant nodes out of the pbsnodes xml file.  The node section name
is a comment in the generated nodes file.

To account for more than one cluster in an entire cluster system one appends
to an existing nodes file with the -a option to gen_nodes_file.

For example, with three clusters "TinyCluster", "LinuxCluster" and
"BigOldBull", where the nodes are labelled tcn<xx>, lcn<xx> and bobn<xx>
respectively, one would run gen_nodes_file like so:

    $ gen_nodes_file -x pbsnodes.xml -n TinyCluster -p tcn -o nodes
    $ gen_nodes_file -x pbsnodes.xml -n LinuxCluster -p lcn -o nodes -a
    $ gen_nodes_file -x pbsnodes.xml -n BigOldBull -p bobn -o nodes -a

The output is a plain text file called 'nodes' which you can then alter to
your heart's content.  If you add a new cluster to your configuration, you
merely need to use the line

    $ gen_nodes_file -x pbsnodes.xml -n NewCluster -p newn -o nodes -a

to add the new cluster nodes to your load and job status visualisation.

Now that the nodes file has been generated, you're now ready to begin
visualising the load and job status of your cluster system.

**********************************
Visualising the system load status
**********************************

To generate an interactive three-dimensional view of the current load of all
nodes in your cluster system, you merely need to run the 'cluster_status'
command:

    $ cluster_status

To view current job-level utilisation of all nodes just press the "j" button
when viewing the cluster.

If you wish, you can specify a previously generated pbsnodes xml file:

    $ cluster_status -x pbsnodes.xml

The title of the output image is controlled by the configuration file
(default: clusterviz.conf).  In the section [load viewer] you merely need to
set the value of the 'title' key to the title you wish to use.  For example:

    [load viewer]
    title = My awesome cluster load status

To specify an alternate configuration file, you can use the '-c' option:

    $ cluster_load_status -c mycluster.conf

If you wish to use the program non-interactively and thereby generate an
image of the cluster status at that point in time, just use the '-N' option.

    $ cluster_load_status -N

When the program is called, the cluster status image appears briefly on the
screen and then disappears.  This image is then saved to the file
'cluster_load_status.png' by default.

*********************************
Visualising the system job status
*********************************

In order to view the job status of your cluster system you merely need to
use the 'cluster_status' command with the '-m/--display_mode' option, e.g.:

    $ cluster_status -m job

To change the default title of the generated image, you need to set the
value of the 'title' key in the [job viewer] section of the configuration
file (clusterviz.conf):

    [job viewer]
    title = My awesome cluster job status

As before, in order to generate an output image one needs to use the
'-N/--non_interactive' option:

    $ cluster_status -m job -N

By default this will generate an image with filename
'cluster_job_status.png'.

********************
Updating the display
********************

The display output can be updated by pressing the u key when in interactive
mode.

***********************************
Remote pbsnodes XML file generation
***********************************

Instead of just using a local 'pbsnodes.xml' file one can also get this file
from a remote host.  This is a practical solution when the computer where
the cluster status is being visualised is not part of PBS-based cluster
system and so is not able to extract the pbsnodes information itself.  With
the '-s' option to 'cluster_status' it is now possible to generate the
'pbsnodes.xml' file on a remote host and have it read at the local host.
Normally this would occur via 'ssh', and after having added a line similar
to the following to the '[main]' section of the configuration file

    [main]
    syscall = ssh login-node 'pbsnodes -x' > pbsnodes.xml

one then merely needs to start 'cluster_status' like so:

    $ cluster_status -s

For this to run smoothly (and without you needing to enter your password
each time the display is updated) you should enable password-less 'ssh'
access to the remote server.  This article gives a good overview:

http://www.howtoforge.com/ssh-best-practices

****************************************************
Generating movies of your cluster status information
****************************************************

The cluster load and job status images are saved to disk with the respective
filenames cluster_load_status.png and cluster_job_status.png.  An extra file
image file with the current timestamp is also saved for each type of status
image.  These files can then be used to create movies of the evolution of
the cluster status over time and can give insight into patterns not
otherwise obvious from viewing the static images.  The best way to produce
such movies is to run 'cluster_status -m load' and 'cluster_status -m job'
as cron jobs.  For instance, one could save images every ten minutes, then
after a day or even a week, one can generate an mpeg movie file from the
collected images.

--------------------------------------------------------------------------
Example
--------------------------------------------------------------------------

In the examples/ directory of the distribution you will find some
pre-generated pbsnodes xml files and an example configuration file.

The first example works for the RRZN cluster system
(http://www.rrzn.uni-hannover.de/computeserver.html).  Change into the
examples/ directory and run the following command:

    $ cluster_status -x pbsnodes_rrzn.xml -n nodes.rrzn -c rrznviz.conf -i

--------------------------------------------------------------------------
Documentation
--------------------------------------------------------------------------

The documentation is distributed with 'pbsclusterviz' in the 'doc/'
directory.  Make sure that you have installed the 'sphinx' package so that
you can build the documentation.

To build the html documentation change into the 'doc/' directory and run

    $ make html

then point your browser to '.../doc/_build/html/index.html'.

To build the pdf documentation change into the 'doc/' directory and run

    $ make latex
    $ cd _build/latex
    $ make all-pdf

then open the file 'PBSClusterViz.pdf' with your favourite PDF-viewer.
