#
# Conditional build:
%bcond_without	perl	# without perl support
%bcond_without	ipv6	# without IPv6 support
%bcond_without	ssl	# without SSL  support
#
%define		_snap		20041010
%define		_rc		rc5
%define		_idea_ver	0.1.46
%{?with_perl:%include	/usr/lib/rpm/macros.perl}
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - wygodny w u�yciu klient IRC
Name:		irssi
Version:	0.8.10
Release:	0.%{_snap}.2
License:	GPL
Group:		Applications/Communications
Source0:	http://real.irssi.org/files/snapshots/%{name}-%{_snap}.tar.gz
# Source0-md5:	5c243d5b8d8897cf398f9eb639236d32
# Source0-size:	1192158
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	http://real.irssi.org/files/plugins/idea/%{name}-idea-%{_idea_ver}.tar.gz
# Source3-md5:	c326efe317b8f67593a3cd46d5557280
# Source0-size:	1192158
Patch0:		%{name}-dcc-send-limit.patch
Patch1:		%{name}-tinfo.patch
Patch2:		%{name}-home_etc.patch
Patch3:		%{name}.conf.patch
Patch4:		%{name}-idea-listlen.patch
URL:		http://www.irssi.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib-devel
BuildRequires:	glib2-devel >= 2.1.0
BuildRequires:	libtool
BuildRequires:	ncurses-devel >= 5.0
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_perl:BuildRequires:	perl-devel >= 1:5.8.4}
BuildRequires:	pkgconfig
Requires:	perl(DynaLoader) = %(%{__perl} -MDynaLoader -e 'print DynaLoader->VERSION')
Obsoletes:	%{name}-speech
Obsoletes:	%{name}-sql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Irssi is a textUI IRC client with IPv6 support.

%description -l fr
Irssi est client IRC.

%description -l pl
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6.

%package plugin-idea
Summary:	Irssi plugin IDEA crypt
Summary(pl):	Wtyczka do irssi do szyfrowania IDEA
Group:		Applications/Communications
Requires:	%{name} = %{version}

%description plugin-idea
This package contains IDEA Crypt plugin for Irssi.

%description plugin-idea
Ten pakiet zawiera wtyczk� do Irssi z szyfrowaniem IDEA.

%prep
%setup -q -n %{name}-%{version}-%{_rc} -a3
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
rm -f missing
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

cd irssi-idea-%{_idea_ver}
rm -f missing
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

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%{__make} -C irssi-idea-%{_idea_ver} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO NEWS docs/*.{txt,html}
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/libirc_proxy.so*
%{_datadir}/%{name}
%{_desktopdir}/irssi.desktop
%{_pixmapsdir}/*
%{_sysconfdir}/irssi.conf
%{_mandir}/man1/*

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
