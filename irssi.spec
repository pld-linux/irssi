%define	ver	0.7.96
%define	plev	2
%include	/usr/lib/rpm/macros.perl
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - klient IRC
Name:		irssi
Version:	%{ver}p%{plev}
Release:	1
Vendor:		Timo Sirainen <cras@irccrew.org>
License:	GPL
Group:		Applications/Communications
Group(pl):	Aplikacje/Komunikacja
Source0:	http://www.irssi.org/files/irssi-%{ver}-%{plev}.tar.bz2
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:	gettext-devel
BuildRequires:	glib-devel >= 1.2.0
BuildRequires:	perl
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
%setup -q -n %{name}-%{ver}

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--without-socks \
	--with-textui=ncurses \
	--with-bot \
	--with-proxy \
	--with-modules \
	--enable-perl=yes \
	--enable-curses-windows \
	--enable-ipv6 \
	--enable-nls
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{perl_sitearch}/

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/%{name}-%{version}

mv $RPM_BUILD_ROOT%{_prefix}/*-pld-*/* $RPM_BUILD_ROOT%{perl_sitearch}/

(
  for name in Irssi Irssi/Irc; do
  cd $RPM_BUILD_ROOT%{perl_sitearch}/auto/${name}
  sed -e "s#$RPM_BUILD_ROOT##" .packlist >.packlist.new
  mv .packlist.new .packlist
  done
)
      
gzip -9nf AUTHORS ChangeLog README TODO NEWS

%find_lang %{name}

%clean
#rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/irssi/*
%dir %{_sysconfdir}/irssi
%{_datadir}/irssi

%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/*.so*

%{perl_sitearch}/*.pm
%dir %{perl_sitearch}/auto/Irssi
%{perl_sitearch}/auto/Irssi/*.bs
%attr(755,root,root) %{perl_sitearch}/auto/Irssi/*.so
