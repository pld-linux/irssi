Summary:  	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC ecrit en GTK
Summary(pl):	Irssi - klient IRC
Name: 		irssi
Version: 	0.7.20
Release: 	1
Vendor: 	Timo Sirainen <cras@irccrew.org>
Copyright: 	GPL
Group: 		Applications/Communications
Group(pl):      Aplikacje/Komunikacja
Source0: 	http://xlife.dhs.org/irssi/files/%{name}-%{version}.tar.bz2
BuildRequires:	libPropList-devel
BuildRequires:	glib-devel
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	imlib-devel
BuildRequires:	gtk+-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	XFree86-devel
BuildRequires:	gettext-devel
URL: 		http://xlife.dhs.org/irssi/
BuildRoot: 	/tmp/%{name}-%{version}-root

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME

%description
Irssi is a textUI IRC client with IPv6 support 
by Timo Sirainen <cras@irccrew.org>.
More information can be found at http://xlife.dhs.org/irssi/.

%description -l fr
Irssi est client IRC écrit en GTK.

%description -l pl
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6. Napisany zosta³
przez Timo Strainen <cras@irccrew.org>.

%package GNOME
Summary: 	GNOME version of irssi IRC client
Summary(pl):	Wersja dla ¶rodowiska GNOME klienta IRC irssi
Group:		X11/Applications/Communications
Group(pl):	X11/Aplikacje/Komunikacja
Requires:	%{name} = %{version}

%description GNOME
Irssi is a GTK based (with GNOME) GUI IRC client with IPv6 support
by Timo Sirainen <cras@irccrew.org>.
More information can be found at http://xlife.dhs.org/irssi/.

%description -l pl GNOME
Irssi jest graficznym klientem IRC ze wsparciem dla IPv6 pracuj±cym w
¶rodowisku GNOME. Napisany zosta³ przez Timo Sirainen <cras@irccrew.org>.

%prep
%setup -q

%build
gettextize --copy --force
CPPFLAGS="-I/usr/X11R6/include"; export CPPFLAGS
LDFLAGS="-s -L/usr/X11R6/lib"; export LDFLAGS
%configure \
	--with-gnome \
	--disable-static \
	--with-gnome-panel \
	--with-imlib \
	--enable-ipv6 \
	--with-textui=ncurses \
	--with-proplist \
	--without-socks \
	--with-plugins
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/irssi/plugins/lib*.so.*.*

gzip -9fn AUTHORS ChangeLog README TODO NEWS

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr (644,root,root,755)
%doc {AUTHORS,ChangeLog,README,TODO,NEWS}.gz

%attr(755,root,root) %{_bindir}/irssi-text

%dir %{_sysconfdir}/irssi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/irssi/*

%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/plugins
%attr(755,root,root) %{_libdir}/irssi/plugins/lib*.so.*.*
%attr(755,root,root) %{_libdir}/irssi/plugins/lib*.so
#%attr(755,root,root) %{_libdir}/irssi/plugins/lib*.la

%files GNOME
%defattr (644,root,root,755)
%attr(755,root,root) %{_bindir}/irssi

%{_sysconfdir}/CORBA/servers/irssi.gnorba
%{_datadir}/applets/Network/irssi.desktop
%{_datadir}/gnome/help/irssi
