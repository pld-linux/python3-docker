#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	docker
Summary:	An API client for docker written in Python
Name:		python-%{module}
Version:	0.7.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/d/docker-py/docker-py-%{version}.tar.gz
# Source0-md5:	3950ac21f7f2a9723759dd95e5f77b89
URL:		http://docker-py.readthedocs.org/
#BuildRequires:	docker >= 1.3.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
#BuildRequires:	python-requests >= 2.2.1
BuildRequires:	python-setuptools
#BuildRequires:	python-tools
#BuildRequires:	python-websocket-client >= 0.11.0
%endif
%if %{with python3}
BuildRequires:	python3-devel
#BuildRequires:	python3-requests
BuildRequires:	python3-setuptools
#BuildRequires:	python3-tools
#BuildRequires:	python3-websocket-client >= 0.11.0
%endif
Requires:	docker >= 1.3.3
Requires:	python-requests >= 2.2.1
Requires:	python-six >= 1.3.0
Requires:	python-websocket-client >= 0.11.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An API client for docker written in Python.

%package -n python3-%{module}
Summary:	An API client for docker written in Python 3
Requires:	python3-requests
Requires:	python3-six >= 1.3.0
Requires:	python3-websocket-client >= 0.11.0

%description -n python3-%{module}
A Python 3 interface to Docker.

%prep
%setup -q -n docker-py-%{version}

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
%{py_sitescriptdir}/docker_py-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/docker_py-%{version}-py*.egg-info
%endif
