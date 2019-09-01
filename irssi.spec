# TODO:
# - color_support_for_gui_entry needs update or to eb removed
#
# Conditional build:
%bcond_without	perl	# without perl support
%bcond_without	dynamic	# without dynamic libraries
%bcond_without	xmpp	# without plugin

%define		no_install_post_check_so	1

%define		idea_ver	0.1.46
%define		xmpp_ver	0.53
%define		irssi_perl_version 20190829
%{?with_perl:%include	/usr/lib/rpm/macros.perl}
Summary:	Irssi is a IRC client
Summary(fr.UTF-8):	Irssi est un client IRC
Summary(hu.UTF-8):	Irssi egy IRC kliens
Summary(pl.UTF-8):	Irssi - wygodny w użyciu klient IRC
Name:		irssi
Version:	1.2.2
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	https://github.com/irssi/irssi/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	062049c73ad2dd54b614e80d0137b737
Source1:	%{name}.desktop
Source2:	%{name}.png
# NXDOMAIN
#Source3:	http://real.irssi.org/files/plugins/idea/%{name}-idea-%{idea_ver}.tar.gz
Source3:	%{name}-idea-%{idea_ver}.tar.gz
# Source3-md5:	c326efe317b8f67593a3cd46d5557280
Source4:	http://cybione.org/~irssi-xmpp/files/irssi-xmpp-%{xmpp_ver}.tar.gz
# Source4-md5:	8c9906e4efbd6f3c8bd8420f0ac8fd91
Patch0:		%{name}-dcc-send-limit.patch
Patch1:		%{name}-home_etc.patch
Patch2:		%{name}-idea-listlen.patch
Patch3:		%{name}-gcc4.patch
Patch4:		%{name}-dynamic.patch

Patch6:		%{name}-color_support_for_gui_entry.patch
Patch7:		%{name}-libs-nopoison.patch
Patch8:		am.patch
Patch9:		%{name}-idea-glib.patch
Patch10:	%{name}-xmpp.patch
URL:		http://www.irssi.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
# for idea only
BuildRequires:	glib-devel
BuildRequires:	glib2-devel >= 2.24.0
BuildRequires:	libgcrypt-devel >= 1.2.0
BuildRequires:	libotr-devel >= 4.1.0
BuildRequires:	libtool
BuildRequires:	libutf8proc-devel
%{?with_xmpp:BuildRequires:	loudmouth-devel}
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	openssl-devel >= 0.9.7d
%{?with_perl:BuildRequires:	perl-devel >= 1:5.8.4}
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_perl:BuildRequires:	rpm-perlprov}
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	sed >= 4.0
Requires:	glib2 >= 2.24.0
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

%description -l hu.UTF-8
Irssi egy szöveges felületű IRC kliens IPv6 támogatással.

%description -l pl.UTF-8
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6.

%package plugin-idea
Summary:	Irssi plugin IDEA crypt
Summary(hu.UTF-8):	Irssi IDEA plugin
Summary(pl.UTF-8):	Wtyczka do irssi do szyfrowania IDEA
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}
Requires:	glib >= 1:1.2.10-13

%description plugin-idea
This package contains IDEA Crypt plugin for Irssi.

%description plugin-idea -l hu.UTF-8
Ez a csomag tartalmazza az IDEA titkosítási plugint Irssi-hez.

%description plugin-idea -l pl.UTF-8
Ten pakiet zawiera wtyczkę do Irssi z szyfrowaniem IDEA.

%package plugin-xmpp
Summary:	Irssi XMPP support plugin
Summary(pl.UTF-8):	Wtyczka do irssi do obsługi XMPP
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description plugin-xmpp
This package contains XMPP support plugin for Irssi.

%description plugin-xmpp -l pl.UTF-8
Ten pakiet zawiera wtyczkę do Irssi z obsługą XMPP.

%prep
%setup -q -a3 -a4
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%if %{with dynamic}
%patch4 -p1
%endif

#%patch6 -p0
%patch7 -p1

echo 'AC_DEFUN([AM_PATH_GLIB],[:])' > glib1.m4

mv irssi-idea{-%{idea_ver},}
mv irssi-xmpp{-%{xmpp_ver},}
%patch8 -p1
%patch9 -p0
%patch10 -p0

# hack
%{__sed} -i -e 's#\./libtool#%{_bindir}/libtool#g' 'configure.ac'

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
	--disable-silent-rules \
	--without-socks \
	--with-bot \
	--with-textui \
	--with-proxy \
	--with-modules \
	--with-otr \
	%{?with_perl:--with-perl=yes} \
	%{?with_perl:--with-perl-lib=vendor} \
	%{!?with_perl:--with-perl=no} \
	--enable-true-color

%{__make}

# to fool idea configure script
touch irssi-config
cd irssi-idea
%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}
cd ..

export IRSSI_INCLUDE=`pwd`
cd irssi-xmpp
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}
%{__make} install \
	docdir=%{_datadir}/%{name}-%{version} \
	DESTDIR=$RPM_BUILD_ROOT

# scripts packaged by irssi-scripts.spec
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/scripts/*

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} -C irssi-idea install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C irssi-xmpp install \
	PREFIX=%{_prefix} \
	IRSSI_LIB=%{_libdir}/%{name} \
	DESTDIR=$RPM_BUILD_ROOT

# -devel?
rm $RPM_BUILD_ROOT%{_libdir}/lib*.{so,la,a}
rm -r $RPM_BUILD_ROOT%{_includedir}/irssi
# cleanup
rm $RPM_BUILD_ROOT%{_libdir}/irssi/modules/lib*.{la,a}
%if %{with perl}
rm $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Irssi/.packlist
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Irssi/Irc/.packlist
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Irssi/TextUI/.packlist
rm $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Irssi/UI/.packlist
%endif
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md TODO NEWS docs/*.{txt,html}
%attr(755,root,root) %{_bindir}/botti
%attr(755,root,root) %{_bindir}/irssi
%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/libirc_proxy.so*
%attr(755,root,root) %{_libdir}/irssi/modules/libotr_core.so*
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
%attr(755,root,root) %{perl_vendorarch}/auto/Irssi/*.so

%dir %{perl_vendorarch}/auto/Irssi/Irc
%attr(755,root,root) %{perl_vendorarch}/auto/Irssi/Irc/*.so

%dir %{perl_vendorarch}/auto/Irssi/TextUI
%attr(755,root,root) %{perl_vendorarch}/auto/Irssi/TextUI/*.so

%dir %{perl_vendorarch}/auto/Irssi/UI
%attr(755,root,root) %{perl_vendorarch}/auto/Irssi/UI/*.so
%endif

%files plugin-idea
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/irssi/modules/libidea.so

%files plugin-xmpp
%defattr(644,root,root,755)
%doc irssi-xmpp/{docs/*,NEWS,README,TODO}
%attr(755,root,root) %{_libdir}/irssi/modules/libfe_xmpp.so
%attr(755,root,root) %{_libdir}/irssi/modules/libtext_xmpp.so
%attr(755,root,root) %{_libdir}/irssi/modules/libxmpp_core.so
