--------------------------------------------------------------------------
Development
--------------------------------------------------------------------------

Although the project is currently in beta status, it is quite usable and the
SVN trunk is in use on a ~180-node system by the `Scientific Computing Group
<http://www.rrzn.uni-hannover.de/clustersystem.html>`_ at the `Regional
Computing Centre for Lower Saxony <http://www.rrzn.uni-hannover.de>`_ in
Germany where it was initially developed.

For the most current version of the application, just check out the SVN
trunk:

.. code-block:: bash

   $ svn co https://pbsclusterviz.svn.sourceforge.net/svnroot/pbsclusterviz/trunk pbsclusterviz/trunk 

or for "bleeding edge" developments check out the branches:

.. code-block:: bash

   $ svn co https://pbsclusterviz.svn.sourceforge.net/svnroot/pbsclusterviz/branches pbsclusterviz/branches

=======
Roadmap
=======

   * interactive mode: a configurable update cycle, so that the display is
     continually updated without having to restart the application
   * interactive mode: holding the mouse over a node shows a pop-up with
     the current jobs running on that node

      * this feature now works in the "interactive" SVN-branch 

   * non-interactive mode: image resolution configurable from the .conf file

      * implemented in "interactive" SVN-branch 

   * informational and "log" output next to or underneath the image in both
     interactive and non-interactive modes
   * other ideas tend to turn up in the TODO file in SVN. 
