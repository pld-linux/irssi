%include	/usr/lib/rpm/macros.perl
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC ecrit en GTK
Summary(pl):	Irssi - klient IRC
Name:		irssi
Version:	0.7.28
Release:	2
Vendor:		Timo Sirainen <cras@irccrew.org>
License:	GPL
Group:		Applications/Communications
Group(pl):	Aplikacje/Komunikacja
Source0:	http://xlife.dhs.org/irssi/files/%{name}-%{version}.tar.bz2
Source1:	http://xlife.dhs.org/irssi/irssi-icon.png
BuildRequires:	libPropList-devel >= 0.9.1-2
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	imlib-devel
BuildRequires:	gtk+-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gettext-devel
BuildRequires:	mysql-devel
URL:		http://xlife.dhs.org/irssi/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME

%description
Irssi is a textUI IRC client with IPv6 support  by Timo Sirainen
<cras@irccrew.org>.

%description -l fr
Irssi est client IRC écrit en GTK.

%description -l pl
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6. Napisany zosta³
przez Timo Strainen <cras@irccrew.org>.

%package GNOME
Summary:	GNOME version of irssi IRC client
Summary(pl):	Wersja dla ¶rodowiska GNOME klienta IRC irssi
Group:		X11/Applications/Communications
Group(pl):	X11/Aplikacje/Komunikacja
Requires:	%{name} = %{version}

%description GNOME
Irssi is a GTK based (with GNOME) GUI IRC client with IPv6 support by Timo
Sirainen <cras@irccrew.org>.

%description -l pl GNOME
Irssi jest graficznym klientem IRC ze wsparciem dla IPv6 pracuj±cym w
¶rodowisku GNOME. Napisany zosta³ przez Timo Sirainen <cras@irccrew.org>.

%package sql
Summary:	MySQL plugin to Irssi
Summary(pl):	Wtyczka MySQL dla Irssi
Group:		X11/Applications/Communications
Group(pl):	X11/Aplikacje/Komunikacja
Requires:	%{name} = %{version}

%description sql
MySQL plugin to Irssi.

%description sql -l pl
Wtyczka MySQL dla Irssi.

%package speech
Summary:        speech plugin to Irssi
Summary(pl):    Wtyczka syntezatora mowy dla Irssi
Group:          X11/Applications/Communications
Group(pl):      X11/Aplikacje/Komunikacja
Requires:       %{name} = %{version}
Requires:	festival

%description speech
Speech plugin to Irssi.

%description speech -l pl
Wtyczka syntezatora mowy dla Irssi.

%prep
%setup  -q

%build
gettextize --copy --force
NOCONFIGURE=1 ./autogen.sh
CPPFLAGS="-I/usr/X11R6/include"; export CPPFLAGS
LDFLAGS="-s -L/usr/X11R6/lib"; export LDFLAGS
%configure \
	--with-gnome \
	--disable-static \
	--with-gnome-panel \
	--with-imlib \
	--enable-ipv6 \
	--with-textui=ncurses \
	--with-proplist=/usr \
	--without-socks \
	--with-plugins \
	--with-mysql \
	--enable-perl
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps

make \ 
	DESTDIR=$RPM_BUILD_ROOT \
	desktopdir=%{_applnkdir}/Network/IRC \
	install
	
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/irssi/plugins/lib*.so.*.*

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/pixmaps/irssi-icon.png
gzip -9nf AUTHORS ChangeLog README TODO NEWS

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc {AUTHORS,ChangeLog,README,TODO,NEWS}.gz

%attr(755,root,root) %{_bindir}/irssi-text

%dir %{_sysconfdir}/irssi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/irssi/*

%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/plugins
%attr(755,root,root) %{_libdir}/irssi/plugins/libbot.so.*.*
%attr(755,root,root) %{_libdir}/irssi/plugins/libbot.so
%attr(755,root,root) %{_libdir}/irssi/plugins/libexternal.so.*.*
%attr(755,root,root) %{_libdir}/irssi/plugins/libexternal.so
%attr(755,root,root) %{_libdir}/irssi/plugins/libproxy.so.*.*
%attr(755,root,root) %{_libdir}/irssi/plugins/libproxy.so
%attr(755,root,root) %{_libdir}/irssi/plugins/libsound.so.*.*
%attr(755,root,root) %{_libdir}/irssi/plugins/libsound.so

%{perl_sitearch}/*.pm
%dir %{perl_sitearch}/auto/Irssi
%{perl_sitearch}/auto/Irssi/*.bs
%attr(755,root,root) %{perl_sitearch}/auto/Irssi/*.so

%files GNOME
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/irssi

%{_sysconfdir}/CORBA/servers/irssi.gnorba
%{_applnkdir}/Network/IRC/irssi.desktop
%{_datadir}/gnome/help/irssi
%{_datadir}/pixmaps/*

%files sql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/irssi/plugins/libsql.so.*.*
%attr(755,root,root) %{_libdir}/irssi/plugins/libsql.so

%files speech
%attr(755,root,root) %{_libdir}/irssi/plugins/libspeech.so.*.*
%attr(755,root,root) %{_libdir}/irssi/plugins/libspeech.so
