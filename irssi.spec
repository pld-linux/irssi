#
# Conditional build:
%bcond_without	perl	# without perl support
%bcond_without	ipv6	# without IPv6 support
%bcond_without	ssl	# without SSL  support
%bcond_without	dynamic	# without dynamic libraries

%define		idea_ver	0.1.46
%define		irssi_perl_version 20090331
%{?with_perl:%include	/usr/lib/rpm/macros.perl}
Summary:	Irssi is a IRC client
Summary(fr.UTF-8):	Irssi est un client IRC
Summary(pl.UTF-8):	Irssi - wygodny w użyciu klient IRC
Name:		irssi
Version:	0.8.13
Release:	3
License:	GPL
Group:		Applications/Communications
#Source0:	http://www.irssi.org/files/snapshots/%{name}-%{_snap}.tar.gz
Source0:	http://www.irssi.org/files/%{name}-%{version}.tar.gz
# Source0-md5:	226f194576895ff3075c164523806d06
Source1:	%{name}.desktop
Source2:	%{name}.png
# NXDOMAIN
#Source3:	http://real.irssi.org/files/plugins/idea/%{name}-idea-%{idea_ver}.tar.gz
Source3:	%{name}-idea-%{idea_ver}.tar.gz
# Source3-md5:	c326efe317b8f67593a3cd46d5557280
Patch0:		%{name}-dcc-send-limit.patch
Patch1:		%{name}-tinfo.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}.conf.patch
Patch4:		%{name}-idea-listlen.patch
Patch5:		%{name}-gcc4.patch
Patch6:		%{name}-dynamic.patch
Patch7:		%{name}-invalid_free.patch
Patch8:		%{name}-color_support_for_gui_entry.patch
Patch9:		%{name}-libs-nopoison.patch
Patch10:	%{name}-CVE-2009-1959.patch
URL:		http://www.irssi.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
# for idea only
BuildRequires:	glib-devel >= 1:1.2.10-13
BuildRequires:	glib2-devel >= 2.1.0
BuildRequires:	libtool
BuildRequires:	ncurses-devel >= 5.0
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_perl:BuildRequires:	perl-devel >= 1:5.8.4}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_perl:BuildRequires:	rpm-perlprov}
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	sed >= 4.0
Requires:	perl(DynaLoader) = %(%{__perl} -MDynaLoader -e 'print DynaLoader->VERSION')
Provides:	perl(Irssi) = %{irssi_perl_version}
Obsoletes:	irssi-speech
Obsoletes:	irssi-sql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with dynamic}
%define		filterout_ld	-Wl,--as-needed
%endif

%description
Irssi is a textUI IRC client with IPv6 support.

%description -l fr.UTF-8
Irssi est client IRC.

%description -l pl.UTF-8
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6.

%package plugin-idea
Summary:	Irssi plugin IDEA crypt
Summary(pl.UTF-8):	Wtyczka do irssi do szyfrowania IDEA
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Requires:	glib >= 1:1.2.10-13

%description plugin-idea
This package contains IDEA Crypt plugin for Irssi.

%description plugin-idea -l pl.UTF-8
Ten pakiet zawiera wtyczkę do Irssi z szyfrowaniem IDEA.

%prep
%setup -q -a3
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%if %{with dynamic}
%patch6 -p1
%endif
%patch7 -p1
%patch8 -p0
%patch9 -p1
%patch10 -p1

echo 'AC_DEFUN([AM_PATH_GLIB],[:])' > glib1.m4

mv irssi-idea{-%{idea_ver},}

# hack
%{__sed} -i -e 's#\./libtool#%{_bindir}/libtool#g' configure.in

%build
ver=$(awk '/IRSSI_VERSION_DATE/{print $3}' irssi-version.h)
if [ "$ver" != "%{irssi_perl_version}" ]; then
	: update irssi_perl_version to $ver
	exit 1
fi

%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__automake}
%configure \
	--without-socks \
	--with-bot \
	--with-textui \
	--with-proxy \
	--with-terminfo \
	--with-modules \
	%{?with_perl:--with-perl=yes} \
	%{?with_perl:--with-perl-lib=vendor} \
	%{!?with_perl:--with-perl=no} \
	%{?with_ipv6:--enable-ipv6} \
	--enable-nls \
	--%{?with_ssl:en}%{!?with_ssl:dis}able-ssl

%{__make}

# to fool idea configure script
touch irssi-config
cd irssi-idea
%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/%{name}-%{version}

# scripts packaged by irssi-scripts.spec
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/scripts/*

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} -C irssi-idea install \
	DESTDIR=$RPM_BUILD_ROOT

# -devel?
rm $RPM_BUILD_ROOT%{_libdir}/lib*.{so,la,a}
rm -r $RPM_BUILD_ROOT%{_includedir}/irssi
# cleanup
rm $RPM_BUILD_ROOT%{_libdir}/irssi/modules/lib*.{la,a}
rm $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Irssi/.packlist
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Irssi/Irc/.packlist
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Irssi/TextUI/.packlist
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Irssi/UI/.packlist
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO NEWS docs/*.{txt,html}
%attr(755,root,root) %{_bindir}/botti
%attr(755,root,root) %{_bindir}/irssi
%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/libirc_proxy.so*
%if %{with dynamic}
%attr(755,root,root) %{_libdir}/libirssi*.so.*
%endif
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/scripts
%{_datadir}/%{name}/help
%{_datadir}/%{name}/themes
%{_desktopdir}/irssi.desktop
%{_pixmapsdir}/irssi.png
%{_sysconfdir}/irssi.conf
%{_mandir}/man1/irssi.1*

%if %{with perl}
%{perl_vendorarch}/*.pm
%dir %{perl_vendorarch}/Irssi
%{perl_vendorarch}/Irssi/*.pm

%dir %{perl_vendorarch}/auto/Irssi
%{perl_vendorarch}/auto/Irssi/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Irssi/*.so

%dir %{perl_vendorarch}/auto/Irssi/Irc
%{perl_vendorarch}/auto/Irssi/Irc/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Irssi/Irc/*.so

%dir %{perl_vendorarch}/auto/Irssi/TextUI
%{perl_vendorarch}/auto/Irssi/TextUI/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Irssi/TextUI/*.so

%dir %{perl_vendorarch}/auto/Irssi/UI
%{perl_vendorarch}/auto/Irssi/UI/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Irssi/UI/*.so
%endif

%files plugin-idea
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/irssi/modules/libidea.so
