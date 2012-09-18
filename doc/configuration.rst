==========================================================================
Configuration
==========================================================================

The main configuration file is in ``etc/pbsclusterviz./clusterviz.conf``.
If you wish to use another configuration file, you can do so by specifying
the ``-c`` command line option.  Otherwise the default configuration file
will be searched for and used.  The configuration file uses the "ini" format
initially used for initialization files on Windows systems.

The pbsclusterviz configuration file is split into four sections,
``[main]``, ``[log]``, ``[job viewer]`` and ``[load viewer]``.  These
sections will be now covered in detail.

``[main]``
----------

As the section heading indicates, this is the main section of the
configuration file and where some of the general settings are set.

In this section one can set the options ``syscall`` and ``update_rate``.

``syscall``
    The system call to use when automatically generating the ``pbsnodes``
    XML file.  For example, one can obtain the XML file via ``ssh`` to a
    remote host which is able to run the ``pbsnodes`` command:

    ``ssh login-node 'pbsnodes -x' > pbsnodes.xml``

``update_rate``
    How often the display should be updated in milliseconds.


``[log]``
----------

This section controls the log to be displayed as part of the cluster status
display.  The log is able to show overloaded nodes (those whose load is over
the maximum for that node), nodes with a load imbalance (which can occur
when a node shows a nonzero load but isn't running any jobs) and nodes which
are down.  This section allows the control of the position of the log on the
display, how many log lines are to be displayed and which of the various
kinds of node problems should be mentioned.

``log_pos_h``
    Horizontal position of the log text (from the left) in absolute screen
    coordinates (ranging from 0 to 1)

``log_pos_v``
    Vertical position of the log text (from the bottom) in absolute screen
    coordinates (ranging from 0 to 1)

``max_log_lines``
    The maximum number of log lines to display

``show_overloaded``
    A boolean value (``True`` or ``False``) indicating whether or not the
    overloaded nodes should be mentioned.

``show_imbalance``
    A boolean value (``True`` or ``False``) indicating whether or not the
    imbalanced nodes should be mentioned.

``show_down``
    A boolean value (``True`` or ``False``) indicating whether or not the
    down nodes should be mentioned.

``[job viewer]``
----------------

This section controls aspects of the ``job`` display mode.

``title``
    The title text to use for ``job`` display mode.

``zoom``
    A floating point zoom factor to use to adjust how close the virtual
    camera should be to the node grid.

``window_width``
    An integer value for the window width in pixels.

``window_height``
    An integer value for the window height in pixels.

``[load viewer]``
-----------------

This section controls aspects of the ``load`` display mode.

``title``
    The title text to use for ``load`` display mode.

``zoom``
    A floating point zoom factor to use to adjust how close the virtual
    camera should be to the node grid.

``window_width``
    An integer value for the window width in pixels.

``window_height``
    An integer value for the window height in pixels.
