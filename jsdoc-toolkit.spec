#
# Conditional build:
%bcond_with	system_rhino	# use system rhino, not bundled

%include	/usr/lib/rpm/macros.java
Summary:	A documentation generator for JavaScript
Name:		jsdoc-toolkit
Version:	2.4.0
Release:	0.4
License:	MIT
Group:		Applications
Source0:	https://jsdoc-toolkit.googlecode.com/files/jsdoc_toolkit-%{version}.zip
# Source0-md5:	a8f78f5ecd24b54501147b2af341a231
Source1:	jsdoc.sh
URL:		https://code.google.com/p/jsdoc-toolkit/
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
BuildRequires:	jdk
%{?with_system_rhino:Requires:	java-rhino}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jsdoc

%description
JsDoc Toolkit is an application, written in JavaScript, for
automatically generating template-formatted, multi-page HTML (or XML,
JSON, or any other text-based) documentation from commented JavaScript
source code.

%prep
%setup -q -n jsdoc_toolkit-%{version}
mv jsdoc-toolkit/* .

%if %{with system_rhino}
# replace manifest without hardcoded path to js.ar
%{__unzip} -qq jsrun.jar
%{__sed} -i -e '/Class-Path:/ s/ .*js.jar/ \/usr\/share\/java\/js.jar/' META-INF/MANIFEST.MF

%build
%jar cvfm jsdoc.jar META-INF/MANIFEST.MF *.class
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_appdir}}
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/jsdoc
cp -p jsrun.jar $RPM_BUILD_ROOT%{_appdir}/jsrun.jar
cp -a app templates $RPM_BUILD_ROOT%{_appdir}

%if %{without system_rhino}
# copy bundled rhino
install -d $RPM_BUILD_ROOT%{_appdir}/java/classes
cp -p java/classes/js.jar $RPM_BUILD_ROOT%{_appdir}/java/classes
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_appdir}/app/test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt changes.txt
%attr(755,root,root) %{_bindir}/jsdoc
%{_appdir}
