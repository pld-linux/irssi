%{!?_without_perl:%include	/usr/lib/rpm/macros.perl}
%define		_idea_ver	0.1.46

Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - wygodny w u¿yciu klient IRC
Name:		irssi
Version:	0.8.6
Release:	2
License:	GPL
Group:		Applications/Communications
Source0:	http://real.irssi.org/files/%{name}-%{version}.tar.bz2
# Source0-md5: 6d66982723e2eb8780ae3b8b3a7ba08d
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:        http://www.irssi.org/files/plugins/idea/%{name}-idea-%{_idea_ver}.tar.gz
# Source3-md5: c326efe317b8f67593a3cd46d5557280
#Patch0:		%{name}-dcc-send-limit.patch
Patch1:		%{name}-channel_auto_who.patch
Patch2:		%{name}.conf.patch
Patch3:		%{name}-tinfo.patch
URL:		http://www.irssi.org/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.1.0
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	glib-devel
%{?!_without_perl:BuildRequires:	perl-devel >= 5.6.1}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	%{name}-speech
Obsoletes:	%{name}-sql

%description
Irssi is a textUI IRC client with IPv6 support.

%description -l fr
Irssi est client IRC.

%description -l pl
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6.

%package plugin-idea
Summary:        Irssi plugin IDEA crypt
Summary(pl):    Wtyczka do irssi do szyfrowania IDEA
Group:          Applications/Communications
Requires:	%{name} = %{version}

%description plugin-idea
This package contains IDEA Crypt plugin for Irssi.

%description plugin-idea
Ten pakiet zawiera wtyczkê do Irssi z szyfrowaniem IDEA.

%prep
%setup -q -a3
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
	%{?!_without_perl:--with-perl=yes} \
	%{?!_without_perl:--with-perl-lib=vendor} \
	%{?_without_perl:--with-perl=no} \
	--enable-ipv6 \
	--enable-nls

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
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_applnkdir}/Network/Communications}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/%{name}-%{version}

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

cd irssi-idea-%{_idea_ver}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO NEWS docs/*.txt
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/libirc_proxy.so*
%{_datadir}/%{name}
%{_applnkdir}/Network/Communications/irssi.desktop
%{_pixmapsdir}/*
%{_sysconfdir}/irssi.conf
%{_mandir}/man1/*

%if %{?!_without_perl:1}0
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
