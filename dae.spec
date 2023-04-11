%define _header_commit 378c3c576e0f4c785a3d5e71400b552725527f30

%global debug_package %{nil}

Name:           dae
Version:        0.1.6
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
Requires:       dae-geoip
Requires:       dae-geosite

%description
%{summary}

%package        geoip-v2raycompat
Summary:        v2ray geoip compat for dae
Provides:       %{name}-geoip = %{version}-%{release}
Requires:       v2ray-geoip

%description    geoip-v2raycompat
This package provides v2ray geoip compat for dae.

%package        geosite-v2raycompat
Summary:        v2ray geosite compat for dae
Provides:       %{name}-geosite = %{version}-%{release}
Requires:       v2ray-domain-list-community

%description    geosite-v2raycompat
This package provides v2ray geosite compat for dae.

%prep
%define     BUILD_DIR   %{_builddir}/%{name}-%{version}/
unzip %{S:0} -d %{BUILD_DIR}
%setup -T -D -n %{name}-%{version}

%build
export GOFLAGS="-buildmode=pie -trimpath -modcacherw"
export CFLAGS=""

cd %{BUILD_DIR}
make VERSION=%{version}

%install
# package dae
install -Dm755 %{BUILD_DIR}dae %{buildroot}%{_bindir}/dae
install -Dm644 %{BUILD_DIR}install/dae.service %{buildroot}%{_unitdir}/dae.service
install -Dm640 %{BUILD_DIR}install/empty.dae %{buildroot}%{_sysconfdir}/dae/config.dae
install -Dm644 %{BUILD_DIR}example.dae %{buildroot}%{_sysconfdir}/dae/config.dae.example

# package dae-geoip-v2raycompat
mkdir -p %{buildroot}%{_datadir}/dae/
ln -s %{_datadir}/v2ray/geoip.dat %{buildroot}%{_datadir}/dae/geoip.dat

# package dae-geosite-v2raycompat
mkdir -p %{buildroot}%{_datadir}/dae/
ln -s %{_datadir}/v2ray/geosite.dat %{buildroot}%{_datadir}/dae/geosite.dat

%files
%license LICENSE
%doc README.md
%{_bindir}/dae
%{_unitdir}/dae.service
%{_sysconfdir}/dae/config.dae.example
%config %{_sysconfdir}/dae/config.dae

%files geoip-v2raycompat
%{_datadir}/dae/geoip.dat

%files geosite-v2raycompat
%{_datadir}/dae/geosite.dat

%changelog
* Tue Apr 11 2023 zhullyb <zhullyb@outlook.com> - 0.1.6-1
- new version

* Fri Mar 17 2023 zhullyb <zhullyb@outlook.com> - 0.1.0-1
- First Version

