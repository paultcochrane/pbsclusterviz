Name: pbsclusterviz
Version: 0.7a
Release: 1%{?dist}
Summary: PBS Cluster Visualisation

Group: Applications/Engineering
License: GPL
Url: http://pbsclusterviz.sourceforge.net
Source0: http://sourceforge.net/projects/pbsclusterviz/files/pbsclusterviz%200.7/pbsclusterviz-0.7a.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python >= 2.4, vtk-python >= 5.4, libxml2-python >= 2.6.26

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README BUGS CHANGES TODO
%{_bindir}/cluster_status
%{_bindir}/gen_nodes_file

# add pbsclusterviz base files
%{python_sitelib}/pbsclusterviz/*.py
%{python_sitelib}/pbsclusterviz/*.pyc
%ghost %{python_sitelib}/pbsclusterviz/*.pyo

# config files
%config(noreplace) %{_sysconfdir}/pbsclusterviz.d/clusterviz.conf
%config(noreplace) %{_sysconfdir}/pbsclusterviz.d/nodes

%changelog
* Fri Nov 9 2012 Paul Cochrane <paultcochrane@users.sourceforge.net> 0.7-1
- New spec file for pbsclusterviz-0.7
