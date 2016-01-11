Name: nethserver-docker
Version: 0.0.0
Release: 1%{?dist}
Summary: NethServer Docker integration
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
URL: %{url_prefix}/%{name}
License: GPL

BuildRequires: nethserver-devtools
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: docker
Requires: nethserver-base

%description
Install and configure Docker on NethServer

%prep
%setup

%build
%{makedocs}
perl createlinks

%install
rm -rf %{buildroot}
(cd root   ; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update

%post
%systemd_post dckfwatch.service

%preun
%systemd_preun dckfwatch.service

%postun
%systemd_postun


%changelog
* Mon Jan 11 2016 Davide Principi <davide.principi@nethesis.it> - 0.0.0-1
- Initial version


