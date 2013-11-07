Name: pbsclusterviz
Version: 0.7a
Release: 4%{?dist}
Summary: PBS Cluster Visualisation

Group: Applications/Engineering
License: GPLv2+
Url: https://github.com/paultcochrane/pbsclusterviz
Source0: https://github.com/paultcochrane/%{name}/archive/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python, vtk-python, libxml2-python
Requires: python, vtk-python, libxml2-python
BuildArch: noarch

# define python_sitelib
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%description
PBS Cluster Viz is a project to display information useful to admins and
users about a computing cluster managed by a PBS-compatible resource
manager. Information includes load and job distribution. Interactive as well
as static output is available.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT

%files
%doc README.md BUGS CHANGES TODO AUTHORS COPYING
%{_bindir}/cluster_status
%{_bindir}/gen_nodes_file

# add pbsclusterviz base files
%{python_sitelib}/pbsclusterviz/*.py
%{python_sitelib}/pbsclusterviz/*.pyc
%ghost %{python_sitelib}/pbsclusterviz/*.pyo

# the egg-info file built from distutils needs to be put into
# %{python_sitelib} as per the Fedora packaging guidelines
%{python_sitelib}/pbsclusterviz-0.7a-py2.6.egg-info

# config files
%config(noreplace) %{_sysconfdir}/pbsclusterviz.d/clusterviz.conf
%config(noreplace) %{_sysconfdir}/pbsclusterviz.d/nodes

%changelog
* Fri Nov 7 2013 Paul Cochrane <paul@liekut.de> 0.7-4
- packaging python egg-info file as per Fedorag packaging guidelines
- corrected changelog order as noted by Orion Poplawski (Fedora)
- updated source and url info to new GitHub repository location

* Thu Aug 1 2013 Paul Cochrane <paultcochrane@users.sourceforge.net> 0.7-3
- removed %clean as recommended by Veaceslav Mindru (Fedora)

* Fri Nov 30 2012 Paul Cochrane <paultcochrane@users.sourceforge.net> 0.7-1
- made corrections to spec file after comments from Volker Fröhlich (Fedora)
  - added COPYING and AUTHORS
  - updated GPL text
  - using Name and Version macros in Source0
  - corrected license value
  - removed version dependencies from BuildRequires
  - added Requires packages

* Fri Nov 9 2012 Paul Cochrane <paultcochrane@users.sourceforge.net> 0.7-1
- New spec file for pbsclusterviz-0.7
