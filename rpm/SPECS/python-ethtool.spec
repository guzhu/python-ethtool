%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_ver: %define python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary: Ethernet settings python bindings
Name: python-ethtool
Version: 0.13
Release: 5%{?dist}
URL: http://git.fedorahosted.org/cgit/python-ethtool.git
Source: https://fedorahosted.org/releases/p/y/python-ethtool/python-ethtool-%{version}.tar.bz2
License: GPLv2
Group: System Environment/Libraries
BuildRequires: python-devel libnl3-devel asciidoc
%if 0%{?rhel} && 0%{?rhel} < 5
BuildRequires: pkgconfig gcc
%endif
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Python bindings for the ethtool kernel interface, that allows querying and
changing of Ethernet card settings, such as speed, port, auto-negotiation, and
PCI locations.

%prep
%setup -q

%build
%{__python} setup.py build
a2x -d manpage -f manpage man/pethtool.8.asciidoc
a2x -d manpage -f manpage man/pifconfig.8.asciidoc

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_bindir}  %{buildroot}%{_mandir}/man8
cp -p scripts/pethtool %{buildroot}%{_bindir}/pethtool
cp -p scripts/pifconfig %{buildroot}%{_bindir}/pifconfig
%{__gzip} -c man/pethtool.8 > %{buildroot}%{_mandir}/man8/pethtool.8.gz
%{__gzip} -c man/pifconfig.8 > %{buildroot}%{_mandir}/man8/pifconfig.8.gz

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/pethtool
%{_bindir}/pifconfig
%doc %{_mandir}/man8/*
%{python_sitearch}/ethtool.so
%if "%{python_ver}" >= "2.5"
%{python_sitearch}/*.egg-info
%endif

%changelog
