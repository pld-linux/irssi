%{!?_without_perl:%include	/usr/lib/rpm/macros.perl}
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - wygodny w u¿yciu klient IRC
Name:		irssi
Version:	0.8.6
Release:	2
License:	GPL
Group:		Applications/Communications
Source0:	http://real.irssi.org/files/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Source2:	%{name}.png
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

%prep
%setup -q
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
	%{?!_without_perl:--with-perl=module} \
	%{?!_without_perl:--with-perl-lib=vendor} \
	%{?_without_perl:--with-perl=no} \
	--enable-ipv6 \
	--enable-nls

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_applnkdir}/Network/Communications}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/%{name}-%{version}

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO NEWS docs/*.txt
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/*.so*
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
