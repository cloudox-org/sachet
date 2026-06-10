%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name:    sachet
Version: 0.3.1
Release: 1%{?dist}
Summary: SMS alerts for Prometheus Alertmanager.
License: BSD
URL:     https://github.com/messagebird/sachet

Source0: https://github.com/messagebird/sachet/releases/download/%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: autogen_%{name}.unit
Source2: autogen_%{name}.default
Source3: https://raw.githubusercontent.com/messagebird/%{name}/%{version}/examples/config.yaml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Sachet is Hindi for conscious. Sachet is an SMS alerting tool for the
Prometheus Alertmanager.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}.yml

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%config(noreplace) %attr(640, -, %{group})%{_sysconfdir}/prometheus/%{name}.yml

%changelog
* Wed Jun 10 2026 Ivan Garcia <igarcia@cloudox.org> - 0.3.1
- Initial packaging for the 0.3.1 branch
