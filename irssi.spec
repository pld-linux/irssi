%define	ver	0.7.97
%define	plev	2
%{?bcond_off_perl:%include	/usr/lib/rpm/macros.perl}
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - klient IRC
Name:		irssi
Version:	%{ver}.%{plev}
Release:	1
Vendor:		Timo Sirainen <cras@irccrew.org>
License:	GPL
Group:		Applications/Communications
Group(pl):	Aplikacje/Komunikacja
Source0:	http://www.irssi.org/files/irssi-%{ver}.%{plev}.tar.bz2
Source1:	http://xlife.dhs.org/irssi/%{name}-icon.png
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	gettext-devel
BuildRequires:	glib-devel >= 1.2.0
%{?!bcond_off_perl:BuildRequires:	perl}
%{?bcond_on_gnome:BuildRequires:	libPropList-devel >= 0.9.1-2}
%{?bcond_on_gnome:BuildRequires:	imlib-devel}
%{?bcond_on_gnome:BuildRequires:	gtk+-devel}
%{?bcond_on_gnome:BuildRequires:	gnome-libs-devel}
Obsoletes:	%{name}-speech
Obsoletes:	%{name}-sql
URL:		http://www.irssi.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Irssi is a textUI IRC client with IPv6 support.

%description -l fr
Irssi est client IRC.

%description -l pl
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6.

%package GNOME
Summary:	GNOME version of irssi IRC client
Summary(pl):	Wersja dla ¶rodowiska GNOME klienta IRC irssi
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Requires:	%{name} = %{version}

%description GNOME
Irssi is a GTK based (with GNOME) GUI IRC client with IPv6 support by
Timo Sirainen <cras@irccrew.org>.

%description -l pl GNOME
Irssi jest graficznym klientem IRC ze wsparciem dla IPv6 pracuj±cym w
¶rodowisku GNOME. Napisany zosta³ przez Timo Sirainen
<cras@irccrew.org>.

%prep
%setup -q -n %{name}-%{ver}

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--without-socks \
	--with-textui=ncurses \
	--with-bot \
	--with-proxy \
	--with-modules \
	%{?bcond_on_gnome:--with-gnome} \
	%{?bcond_on_gnome:--with-gnome-panel} \
	%{?!bcond_off_perl:--enable-perl=yes} \
	%{?bcond_off_perl:--enable-perl=no} \
	--enable-curses-windows \
	--enable-ipv6 \
	--enable-nls
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{perl_sitearch},/usr/X11R6/share/pixmaps}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/%{name}-%{version} \
	desktopdir=%{_applnkdir}/Network/IRC

%{?!bcond_on_gnome:#}install %{SOURCE1} $RPM_BUILD_ROOT/usr/X11R6/share/pixmaps/irssi-icon.png

%{?bcond_off_perl:#}mv $RPM_BUILD_ROOT%{_prefix}/*-pld-*/* $RPM_BUILD_ROOT%{perl_sitearch}/

%{?bcond_off_perl:#}(
%{?bcond_off_perl:#}  for name in Irssi Irssi/Irc; do
%{?bcond_off_perl:#}  cd $RPM_BUILD_ROOT%{perl_sitearch}/auto/${name}
%{?bcond_off_perl:#}  sed -e "s#$RPM_BUILD_ROOT##" .packlist >.packlist.new
%{?bcond_off_perl:#}  mv .packlist.new .packlist
%{?bcond_off_perl:#}  done
%{?bcond_off_perl:#})
      
gzip -9nf AUTHORS ChangeLog README TODO NEWS docs/*.txt

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz docs/*.txt.gz
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/irssi/*
%dir %{_sysconfdir}/irssi
%{_datadir}/irssi

%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/*.so*

%{?bcond_off_perl:#}%{perl_sitearch}/*.pm
%{?bcond_off_perl:#}%dir %{perl_sitearch}/auto/Irssi
%{?bcond_off_perl:#}%{perl_sitearch}/auto/Irssi/*.bs
%{?bcond_off_perl:#}%attr(755,root,root) %{perl_sitearch}/auto/Irssi/*.so

%{?!bcond_on_gnome:#}%files GNOME
%{?!bcond_on_gnome:#}%defattr(644,root,root,755)
%{?!bcond_on_gnome:#}%attr(755,root,root) /usr/X11R6/bin/irssi

%{?!bcond_on_gnome:#}/etc/X11/GNOME/CORBA/servers/irssi.gnorba
%{?!bcond_on_gnome:#}%{_applnkdir}/Network/IRC/irssi.desktop
%{?!bcond_on_gnome:#}/usr/X11R6/share/gnome/help/irssi
%{?!bcond_on_gnome:#}/usr/X11R6/share/pixmaps/*
