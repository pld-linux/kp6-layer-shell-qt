#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.0.0
%define		qtver		5.15.2
%define		kf6ver		5.82.0
%define		kpname		layer-shell-qt
Summary:	layer-shell-qt
Name:		kp6-%{kpname}
Version:	6.0.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	5d02ead00aa69e96d71fb892aa941fa3
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Qml-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6WaylandClient-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-kcmutils-devel >= %{kf6ver}
BuildRequires:	kf6-kcrash-devel >= %{kf6ver}
BuildRequires:	kf6-kdeclarative-devel >= %{kf6ver}
BuildRequires:	kf6-kglobalaccel-devel >= %{kf6ver}
BuildRequires:	kf6-kidletime-devel >= %{kf6ver}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	wayland-protocols
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
kscreenlocker

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%ghost %{_libdir}/libLayerShellQtInterface.so.6
%attr(755,root,root) %{_libdir}/libLayerShellQtInterface.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/wayland-shell-integration/liblayer-shell.so
%dir %{_libdir}/qt6/qml/org/kde/layershell
%{_libdir}/qt6/qml/org/kde/layershell/LayerShellQtQml.qmltypes
%{_libdir}/qt6/qml/org/kde/layershell/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/layershell/libLayerShellQtQml.so
%{_libdir}/qt6/qml/org/kde/layershell/qmldir

%files devel
%defattr(644,root,root,755)
%{_includedir}/LayerShellQt
%{_libdir}/cmake/LayerShellQt
%{_libdir}/libLayerShellQtInterface.so
