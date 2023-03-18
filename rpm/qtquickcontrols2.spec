%global qt_version 5.15.8

Name:    qt5-qtquickcontrols2
Summary: Qt5 - module with set of QtQuick controls for embedded
Version: 5.15.8
Release: 1%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_opt_qt5_archdatadir}/qml/.*\\.so$

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel

Requires: qt5-qtdeclarative%{?_isa} >= %{qt_version}
Requires: qt5-qtgraphicaleffects%{_isa} >= %{qt_version}

%description
The Qt Labs Controls module provides a set of controls that can be used to
build complete interfaces in Qt Quick.

Unlike Qt Quick Controls, these controls are optimized for embedded systems
and so are preferred for hardware with limited resources.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
Requires: opt-qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary:        Examples for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5}

# have to restart build several times due to bug in sb2
%make_build  -k || chmod -R ugo+r . || true
%make_build

# bug in sb2 leading to 000 permission in some generated plugins.qmltypes files
chmod -R ugo+r .

%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# Remove .la leftovers
rm -f %{buildroot}%{_opt_qt5_libdir}/libQt5*.la


%ldconfig_scriptlets

%files
%license LICENSE.LGPLv3 LICENSE.GPLv3
%{_opt_qt5_libdir}/libQt5QuickTemplates2.so.5*
%{_opt_qt5_libdir}/libQt5QuickControls2.so.5*
%{_opt_qt5_qmldir}/Qt/labs/calendar
%{_opt_qt5_qmldir}/Qt/labs/platform
%{_opt_qt5_archdatadir}/qml/QtQuick/Controls.2/
%{_opt_qt5_archdatadir}/qml/QtQuick/Templates.2/

%files examples
%{_opt_qt5_examplesdir}/quickcontrols2/

%files devel
%{_opt_qt5_headerdir}/
%{_opt_qt5_libdir}/pkgconfig/*.pc
%{_opt_qt5_libdir}/libQt5QuickTemplates2.so
%{_opt_qt5_libdir}/libQt5QuickControls2.so
%{_opt_qt5_libdir}/libQt5QuickTemplates2.prl
%{_opt_qt5_libdir}/libQt5QuickControls2.prl
%{_opt_qt5_libdir}/qt5/mkspecs/modules/*
%{_opt_qt5_libdir}/cmake/Qt5QuickControls2/
%{_opt_qt5_libdir}/cmake/Qt5QuickTemplates2/
