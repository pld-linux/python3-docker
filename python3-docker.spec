%define		module		docker
%define		egg_name	docker
%define		pypi_name	docker
Summary:	A Python 3 library for the Docker Engine API
Summary(pl.UTF-8):	Biblioteka Pythona 3 do API silnika Docker
Name:		python3-%{module}
Version:	7.1.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/d/docker/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	04e92a7b6dc8b88dde3c7cca6850b277
Patch0:		pyproject-syntax.patch
URL:		http://docker-py.readthedocs.org/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:54.1.1
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
%patch -P 0 -p1
cat > setup.py <<EOF
from setuptools import setup
setup(version='%{version}')
EOF

%build
%py3_build

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
