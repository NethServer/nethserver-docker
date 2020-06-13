Name:           nethserver-docker
Version: 1.0.2
Release: 1%{?dist}
Summary:        NethServer Docker configuration

License:        GPLv3+
URL: %{url_prefix}/%{name}
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  nethserver-devtools
Requires:       docker-ce

%description
NethServer configuration for Docker CE

%prep
%setup

%build
%{makedocs}
perl createlinks


%install
(cd root   ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-filelist
mkdir -p %{buildroot}%{_nsstatedir}/portainer
mkdir -p ${RPM_BUILD_ROOT}/var/log/docker


%files -f %{name}-%{version}-filelist
%doc COPYING
%doc README.rst
%config(noreplace) %attr (0644,root,root) %{_sysconfdir}/docker/docker.conf
%attr(0750,root,root) %dir /var/log/docker
%dir %{_nseventsdir}/%{name}-update
%dir %{_nsstatedir}/portainer

%changelog
* Sat Jun 13 2020 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.0.2-1
  - Merge pull request #13 from stephdl/docker0
  - Merge pull request #14 from stephdl/disableUpdate
  - Disable by default docker-ce-stable
  - Enable default bridge docker0

* Sat May 16 2020 Stephane de Labrusse <stephdl@de-labrusse.fr> 1.0.1-1 
  - Merge pull request #11 from stephdl/fixRuletemplate
  - Rule template must output a comment

* Fri May 15 2020 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.0.0-1
- First stable release to NethForge
- Code from mrmarkuz & stephdl

* Mon Sep 10 2018 Davide Principi <davide.principi@nethesis.it> - 0.0.0
- Initial version
