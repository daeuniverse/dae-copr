%global debug_package %{nil}

Name:           dae
Version:        0.6.0
Release:        1%{?dist}
Summary:        A Linux lightweight and high-performance transparent proxy solution based on eBPF.
License:        AGPL
URL:            https://github.com/daeuniverse/dae
Source0:        %{url}/releases/download/v%{version}/dae-full-src.zip
BuildRequires:  clang-devel
BuildRequires:  golang
BuildRequires:  llvm-devel
BuildRequires:  git
BuildRequires:  systemd
Requires:       glibc
Requires:       v2ray-geoip
Requires:       v2ray-domain-list-community

%description
%{summary}

%prep
%define     BUILD_DIR   %{_builddir}/%{name}-%{version}/
unzip %{S:0} -d %{BUILD_DIR}
%setup -T -D -n %{name}-%{version}

%build
export GOFLAGS="-buildmode=pie -trimpath -modcacherw"
export CFLAGS="-fno-stack-protector"

cd %{BUILD_DIR}
make VERSION=%{version}

%install
# package dae
install -Dm755 %{BUILD_DIR}dae %{buildroot}%{_bindir}/dae
install -Dm644 %{BUILD_DIR}install/dae.service %{buildroot}%{_unitdir}/dae.service
install -Dm640 %{BUILD_DIR}install/empty.dae %{buildroot}%{_sysconfdir}/dae/config.dae
install -Dm644 %{BUILD_DIR}example.dae %{buildroot}%{_sysconfdir}/dae/config.dae.example

install -d %{buildroot}%{_datadir}/dae/
ln -vs %{_datadir}/v2ray/geoip.dat %{buildroot}%{_datadir}/dae/geoip.dat
ln -vs %{_datadir}/v2ray/geosite.dat %{buildroot}%{_datadir}/dae/geosite.dat

%files
%license LICENSE
%doc README.md
%{_bindir}/dae
%{_unitdir}/dae.service
%{_sysconfdir}/dae/config.dae.example
%config %{_sysconfdir}/dae/config.dae
%{_datadir}/dae/geoip.dat
%{_datadir}/dae/geosite.dat

%changelog
* Wed Jun 12 2024 zhullyb <zhullyb@outlook.com> - 0.6.0-1
- new version

* Tue Apr 30 2024 zhullyb <zhullyb@outlook.com> - 0.5.1-1
- new version
- drop split package, depend on v2ray-geoip and v2ray-domain-list-community

* Tue Apr 11 2023 zhullyb <zhullyb@outlook.com> - 0.1.6-1
- new version

* Fri Mar 17 2023 zhullyb <zhullyb@outlook.com> - 0.1.0-1
- First Version
