#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		docker
%define		egg_name	docker
%define		pypi_name	docker
Summary:	A Python library for the Docker Engine API
Name:		python-%{module}
Version:	3.7.2
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	e367b2270d7eea2eccceb022e4929cde
Patch0:		unpin-requirements.patch
URL:		http://docker-py.readthedocs.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-pip
BuildRequires:	python-setuptools
BuildConflicts:	python-docker < 2.0
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-pip
BuildRequires:	python3-setuptools
BuildConflicts:	python3-docker < 2.0
%endif
# Docker can be remote, so suggest only
Suggests:	docker >= 1.3.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2016-May/024868.html
%define		_noautoreq_py3egg	backports.ssl-match-hostname ipaddress

%description
A Python 2 library for the Docker Engine API. It lets you do anything
the `docker` command does, but from within Python apps - run
containers, manage containers, manage Swarms, etc.

%package -n python3-%{module}
Summary:	An API client for docker written in Python 3
Group:		Libraries/Python
# Docker can be remote, so suggest only
Suggests:	docker >= 1.3.3

%description -n python3-%{module}
A Python 3 library for the Docker Engine API. It lets you do anything
the `docker` command does, but from within Python apps - run
containers, manage containers, manage Swarms, etc.

%prep
%setup -q -n %{pypi_name}-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
