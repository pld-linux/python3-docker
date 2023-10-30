#
# Conditional build:
%bcond_with	tests	# unit/integration tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		docker
%define		egg_name	docker
%define		pypi_name	docker
Summary:	A Python 2 library for the Docker Engine API
Summary(pl.UTF-8):	Biblioteka Pythona 2 do API silnika Docker
Name:		python-%{module}
Version:	5.0.0
Release:	4
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	9cc5156a2ff6458a8f52114b9bbc0d7e
Patch0:		unpin-requirements.patch
URL:		http://docker-py.readthedocs.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-modules >= 1:3.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest >= 4.3.1
BuildRequires:	python-requests >= 2.18.1
BuildRequires:	python-websocket-client >= 0.32.0
%endif
BuildConflicts:	python-docker < 2.0
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 4.3.1
BuildRequires:	python3-requests >= 2.18.1
BuildRequires:	python3-websocket-client >= 0.32.0
%endif
BuildConflicts:	python3-docker < 2.0
%endif
# Docker can be remote, so suggest only
Suggests:	docker >= 1.3.3
# optional dep for ssh support (required by docker-compose)
Suggests:	python-paramiko >= 2.4.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2016-May/024868.html
%define		_noautoreq_py3egg	backports.ssl-match-hostname ipaddress

%description
A Python library for the Docker Engine API. It lets you do anything
the `docker` command does, but from within Python apps - run
containers, manage containers, manage Swarms, etc.

%description -l pl.UTF-8
Biblioteka Pythona do API silnika Docker. Pozwala zrobić wszystko to,
co polecenie "docker", ale z poziomu aplikacji w Pythonie: uruchamiać
kontenery, zarządzać nimi, zarządzać Swarmami itp.

%package -n python3-%{module}
Summary:	A Python 3 library for the Docker Engine API
Summary(pl.UTF-8):	Biblioteka Pythona 3 do API silnika Docker
Group:		Libraries/Python
# Docker can be remote, so suggest only
Suggests:	docker >= 1.3.3
# optional dep for ssh support (required by docker-compose)
Suggests:	python3-paramiko >= 2.4.2

%description -n python3-%{module}
A Python library for the Docker Engine API. It lets you do anything
the `docker` command does, but from within Python apps - run
containers, manage containers, manage Swarms, etc.

%description -n python3-%{module} -l pl.UTF-8
Biblioteka Pythona do API silnika Docker. Pozwala zrobić wszystko to,
co polecenie "docker", ale z poziomu aplikacji w Pythonie: uruchamiać
kontenery, zarządzać nimi, zarządzać Swarmami itp.

%prep
%setup -q -n %{pypi_name}-%{version}
%patch0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests -W ignore
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
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
