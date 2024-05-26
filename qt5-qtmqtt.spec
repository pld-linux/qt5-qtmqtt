#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtmqtt
%define		qtbase_ver	%{version}
%define		qttools_ver	%{version}
Summary:	The Qt5 Mqtt library
Summary(pl.UTF-8):	Biblioteka Qt5 Mqtt
Name:		qt5-%{orgname}
Version:	5.15.14
Release:	1
License:	GPL v3+ or commercial
Group:		Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	6c5c69d6ebcf5261925eaeafadb7ee70
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	openssl-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Mqtt library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Mqtt.

%package -n Qt5Mqtt
Summary:	The Qt5 Mqtt library
Summary(pl.UTF-8):	Biblioteka Qt5 Mqtt
Group:		Libraries
%requires_eq_to	Qt5Core Qt5Core-devel
Requires:	Qt5Network >= %{qtbase_ver}

%description -n Qt5Mqtt
Qt Mqtt module contains a library that supports the MQTT protocol.
MQTT is a machine-to-machine (M2M) protocol utilizing the
publish-and-subscribe paradigm. Its purpose is to provide a channel
with minimal communication overhead.

%description -n Qt5Mqtt -l pl.UTF-8
Moduł Qt Mqtt zawiera bibliotekę obsługującą protokół MQTT. Jest to
protokół międzymaszynowy (M2M), korzystający z paradygmatu publikacji
i subskrypcji. Celem jest zapewnienie kanału z minimalnym narzutem na
komunikację.

%package -n Qt5Mqtt-devel
Summary:	Qt5 Mqtt library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Mqtt - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Mqtt = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}

%description -n Qt5Mqtt-devel
Qt5 Mqtt library - development files.

%description -n Qt5Mqtt-devel -l pl.UTF-8
Biblioteka Qt5 Mqtt - pliki programistyczne.

%package doc
Summary:	Qt5 Mqtt documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Mqtt w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Mqtt documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Mqtt w formacie HTML.

%package doc-qch
Summary:	Qt5 Mqtt documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Mqtt w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Mqtt documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Mqtt w formacie QCH.

%package examples
Summary:	Qt5 Mqtt examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Mqtt
License:	BSD or commercial
Group:		Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Mqtt examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Mqtt.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt5/mqtt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5Mqtt -p /sbin/ldconfig
%postun	-n Qt5Mqtt -p /sbin/ldconfig

%files -n Qt5Mqtt
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT dist/changes-*
# R: Qt5Core Qt5Network
%attr(755,root,root) %{_libdir}/libQt5Mqtt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5Mqtt.so.5

%files -n Qt5Mqtt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5Mqtt.so
%{_libdir}/libQt5Mqtt.prl
%{_includedir}/qt5/QtMqtt
%{_pkgconfigdir}/Qt5Mqtt.pc
%{_libdir}/cmake/Qt5Mqtt
%{qt5dir}/mkspecs/modules/qt_lib_mqtt.pri
%{qt5dir}/mkspecs/modules/qt_lib_mqtt_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtmqtt

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtmqtt.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
