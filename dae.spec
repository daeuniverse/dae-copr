%global debug_package %{nil}

Name:           dae
Version:        null
Release:        1%{?dist}
Summary:        A Linux lightweight and high-performance transparent proxy solution based on eBPF.
License:        AGPL-3.0-or-later
URL:            https://github.com/daeuniverse/dae
Source0:        %{url}/releases/download/v%{version}/dae-full-src.zip
BuildRequires:  clang-devel
BuildRequires:  llvm-devel
BuildRequires:  systemd-rpm-macros
Requires:       glibc
Requires:       v2ray-geoip
Requires:       v2ray-domain-list-community

%description
%{summary}

%prep
%define     BUILD_DIR   %{_builddir}/%{name}-%{version}/
unzip %{S:0} -d %{BUILD_DIR}
%setup -T -D -n %{name}-%{version}

ARCH=$(uname -m)
if [ "$ARCH" == "x86_64" ]; then
    ARCH="amd64"
elif [ "$ARCH" == "aarch64" ]; then
    ARCH="arm64"
fi
LATEST_GO_VERSION="$(curl --silent https://go.dev/VERSION?m=text | head -n 1)";
LATEST_GO_DOWNLOAD_URL="https://go.dev/dl/${LATEST_GO_VERSION}.linux-${ARCH}.tar.gz"
cd $HOME
curl -OJ -L --progress-bar $LATEST_GO_DOWNLOAD_URL
tar -xf ${LATEST_GO_VERSION}.linux-${ARCH}.tar.gz

%build
export GOROOT="$HOME/go"
export GOPATH="$HOME/go/packages"
export PATH="$GOROOT/bin:$GOPATH/bin:$PATH"

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
* Fri Jan 17 2025 zhullyb <zhullyb@outlook.com> - null-1
- new version

* Wed Jan 08 2025 zhullyb <zhullyb@outlook.com> - 0.9.0-1
- new version

* Sat Oct 12 2024 zhullyb <zhullyb@outlook.com> - 0.8.0-1
- new version

* Fri Sep 27 2024 zhullyb <zhullyb@outlook.com> - 0.7.4-1
- new version

* Fri Sep 27 2024 zhullyb <zhullyb@outlook.com> - 0.7.3-1
- new version

* Fri Sep 27 2024 zhullyb <zhullyb@outlook.com> - 0.7.2-1
- new version

* Wed Aug 21 2024 zhullyb <zhullyb@outlook.com> - 0.7.1-1
- new version

* Mon Jul 22 2024 zhullyb <zhullyb@outlook.com> - 0.7.0-2
- install golang manually

* Mon Jul 22 2024 zhullyb <zhullyb@outlook.com> - 0.7.0-1
- new version

* Wed Jun 12 2024 zhullyb <zhullyb@outlook.com> - 0.6.0-1
- new version

* Tue Apr 30 2024 zhullyb <zhullyb@outlook.com> - 0.5.1-1
- new version
- drop split package, depend on v2ray-geoip and v2ray-domain-list-community

* Tue Apr 11 2023 zhullyb <zhullyb@outlook.com> - 0.1.6-1
- new version

* Fri Mar 17 2023 zhullyb <zhullyb@outlook.com> - 0.1.0-1
- First Version

