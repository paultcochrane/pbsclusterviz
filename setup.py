#!/usr/bin/env python

from distutils.core import setup

a=setup(name="pbsclusterviz",
      version="0.1",
      description="PBS Cluster Visualisation",
      author="Paul Cochrane",
      author_email="paultcochrane@users.sourceforge.net",
      maintainer="Paul Cochrane",
      maintainer_email="paultcochrane@users.sourceforge.net",
      url="http://pbsclusterviz.sourceforge.net",
      license="GPL",
      keywords="PBS Torque Maui Cluster HPC Visualisation",
      platforms="OS Independent",
      packages=['pbsclusterviz', 'pbsclusterviz.pbs'],
      scripts=['bin/cluster_job_status',
		'bin/cluster_load_status',
		'bin/gen_nodes_file'],
)


