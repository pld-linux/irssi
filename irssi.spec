%{?_without_perl:#}%include	/usr/lib/rpm/macros.perl
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - klient IRC
Name:		irssi
Version:	0.7.98.4
Release:	2
Vendor:		Timo Sirainen <cras@irccrew.org>
License:	GPL
Group:		Applications/Communications
Group(pl):	Aplikacje/Komunikacja
Source0:	http://www.irssi.org/files/irssi-%{version}.tar.bz2
Source1:	%{name}.desktop
Source2:	%{name}.png
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	gettext-devel
BuildRequires:	glib-devel >= 1.2.0
%{?!_without_perl:BuildRequires:	perl-devel >= 5.6.1}
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

%prep
%setup -q

%build
%configure2_13 \
	--without-socks \
	--with-textui=ncurses \
	--with-bot \
	--with-proxy \
	--with-modules \
	%{?!_without_perl:--enable-perl=yes} \
	%{?_without_perl:--enable-perl=no} \
	--enable-curses-windows \
	--enable-ipv6 \
	--enable-nls
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{perl_sitearch},%{_pixmapsdir},%{_applnkdir}/Network/Communications}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/%{name}-%{version}

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%{?_without_perl:#}mv $RPM_BUILD_ROOT%{_prefix}/*-pld-*/* $RPM_BUILD_ROOT%{perl_sitearch}/

%{?_without_perl:#}(
%{?_without_perl:#}  for name in Irssi Irssi/Irc; do
%{?_without_perl:#}  cd $RPM_BUILD_ROOT%{perl_sitearch}/auto/${name}
%{?_without_perl:#}  sed -e "s#$RPM_BUILD_ROOT##" .packlist >.packlist.new
%{?_without_perl:#}  mv .packlist.new .packlist
%{?_without_perl:#}  done
%{?_without_perl:#})
      
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
%{_applnkdir}/Network/Communications/irssi.desktop
%{_pixmapsdir}/*

%{?_without_perl:#}%dir %{perl_sitearch}/Irssi
%{?_without_perl:#}%{perl_sitearch}/*.pm
%{?_without_perl:#}%{perl_sitearch}/Irssi/*.pm
%{?_without_perl:#}%dir %{perl_sitearch}/auto/Irssi
%{?_without_perl:#}%dir %{perl_sitearch}/auto/Irssi/Irc
%{?_without_perl:#}%{perl_sitearch}/auto/Irssi/*.bs
%{?_without_perl:#}%{perl_sitearch}/auto/Irssi/Irc/*.bs
%{?_without_perl:#}%attr(755,root,root) %{perl_sitearch}/auto/Irssi/*.so
%{?_without_perl:#}%attr(755,root,root) %{perl_sitearch}/auto/Irssi/Irc/*.so
