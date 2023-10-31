#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module		docker
%define		egg_name	docker
%define		pypi_name	docker
Summary:	A Python 3 library for the Docker Engine API
Summary(pl.UTF-8):	Biblioteka Pythona 3 do API silnika Docker
Name:		python3-%{module}
Version:	5.0.3
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/d/docker/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	33314b2c98a1a4e3b57e7068811007c6
URL:		http://docker-py.readthedocs.org/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:54.1.1
%if %{with tests}
BuildRequires:	python3-paramiko >= 2.4.2
BuildRequires:	python3-pytest >= 4.3.1
BuildRequires:	python3-pytest-timeout >= 1.3.3
BuildRequires:	python3-requests >= 2.18.1
BuildRequires:	python3-urllib3 >= 1.24.3
BuildRequires:	python3-websocket-client >= 0.32.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildConflicts:	python3-docker < 2.0
# Docker can be remote, so suggest only
Suggests:	docker >= 1.3.3
# optional dep for ssh support (required by docker-compose)
Suggests:	python3-paramiko >= 2.4.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python library for the Docker Engine API. It lets you do anything
the `docker` command does, but from within Python apps - run
containers, manage containers, manage Swarms, etc.

%description -l pl.UTF-8
Biblioteka Pythona do API silnika Docker. Pozwala zrobić wszystko to,
co polecenie "docker", ale z poziomu aplikacji w Pythonie: uruchamiać
kontenery, zarządzać nimi, zarządzać Swarmami itp.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%py3_build

%if %{with tests}
# only unit tests (ssh and integration tests probably require docker running)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_timeout \
%{__python3} -m pytest tests/unit -k 'not TCPSocketStreamTest'
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
