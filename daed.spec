%global debug_package %{nil}

Name:           daed
Version:        0.9.0
Release:        1%{?dist}
Summary:        daed, a modern dashboard with dae.

License:        AGPL-3.0-or-later
URL:            https://github.com/daeuniverse/daed
Source0:        %{url}/releases/download/v%{version}/daed-full-src.zip

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

# Setup Golang
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

# Setup Node.js and pnpm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 22
corepack enable pnpm

%build
# Set PATH
\. "$HOME/.nvm/nvm.sh"
export GOROOT="$HOME/go"
export GOPATH="$HOME/go/packages"
export PATH="$GOROOT/bin:$GOPATH/bin:$PATH"

export CFLAGS="-fno-stack-protector"
export CGO_ENABLED=1
export CGO_CPPFLAGS="${CPPFLAGS}"
export CGO_CFLAGS="${CFLAGS}"
export CGO_CXXFLAGS="${CXXFLAGS}"
export CGO_LDFLAGS="${LDFLAGS}"
export GOFLAGS="-buildmode=pie -trimpath -ldflags=-linkmode=external -mod=readonly -modcacherw"
make VERSION="%{version}"

%install
install -Dm755 %{BUILD_DIR}daed %{buildroot}%{_bindir}/daed
install -Dm644 %{BUILD_DIR}install/daed.service %{buildroot}%{_unitdir}/daed.service

install -d %{buildroot}%{_datadir}/daed/
ln -vs %{_datadir}/v2ray/geoip.dat %{buildroot}%{_datadir}/daed/geoip.dat
ln -vs %{_datadir}/v2ray/geosite.dat %{buildroot}%{_datadir}/daed/geosite.dat


%files
%license LICENSE
%{_bindir}/daed
%{_unitdir}/daed.service
%{_datadir}/daed/geoip.dat
%{_datadir}/daed/geosite.dat



%changelog
* Wed Feb 19 2025 zhullyb
- Initial package
