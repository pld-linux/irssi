Name: 		irssi
Version: 	0.7.16
Release: 	1
Vendor: 	Timo Sirainen <cras@irccrew.org>
Summary:  	Irssi is a IRC client
Copyright: 	GPL
Group: 		Applications/Communications
Group(pl):      Aplikacje/Komunikacja
URL: 		http://xlife.dhs.org/irssi/
Source0: 	http://xlife.dhs.org/irssi/files/%{name}-%{version}.tar.gz
BuildRequires:	libPropList-devel
BuildRequires:	glib-devel
BuildRequires:	ncurses-devel
BuildRequires:	imlib-devel
BuildRequires:	gtk+-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	XFree86-devel
BuildRoot: 	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc

%description
Irssi is a textUI IRC client with IPv6 support 
by Timo Sirainen <cras@irccrew.org>.
More information can be found at http://xlife.dhs.org/irssi/.

%package GNOME
Summary: 	GNOME version of irssi IRC client
Group:		X11/Applications/Communications
Group(pl):	X11/Aplikacje/Komunikacja
Requires:	%{name} = %{version}

%description GNOME
Irssi is a GTK based (with GNOME) GUI IRC client with IPv6 support
by Timo Sirainen <cras@irccrew.org>.
More information can be found at http://xlife.dhs.org/irssi/.

%prep
%setup -q

%build
CPPFLAGS="-I/usr/X11R6/include"; export CPPFLAGS
LDFLAGS="-s -L/usr/X11R6/lib"; export LDFLAGS
%configure \
	--with-gnome \
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

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (644,root,root,755)
%doc {AUTHORS,ChangeLog,README,TODO,NEWS}.gz

%attr(755,root,root) %{_bindir}/irssi-text
%attr(755,root,root) %{_bindir}/irssi-bot

%dir %{_sysconfdir}/irssi
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/irssi/*

%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/plugins
%attr(755,root,root) %{_libdir}/irssi/plugins/lib*.so.*.*
%attr(755,root,root) %{_libdir}/irssi/plugins/lib*.so
#%attr(755,root,root) %{_libdir}/irssi/plugins/lib*.la
#%attr(755,root,root) %{_libdir}/irssi/plugins/lib*.a

%files GNOME
%defattr (644,root,root,755)
%attr(755,root,root) %{_bindir}/irssi

%{_sysconfdir}/CORBA/servers/irssi.gnorba
%{_datadir}/applets/Network/irssi.desktop
%{_datadir}/gnome/help/irssi
