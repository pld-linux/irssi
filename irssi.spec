%{?_without_perl:#}%include	/usr/lib/rpm/macros.perl
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - wygodny w u¿yciu klient IRC
Name:		irssi
Version:	0.8.4
Release:	2
License:	GPL
Vendor:		Timo Sirainen <cras@irccrew.org>
Group:		Applications/Communications
Source0:	http://www.irssi.org/files/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-dcc-send-limit.patch
Patch1:		%{name}-channel_auto_who.patch
URL:		http://www.irssi.org/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	glib-devel >= 1.2.0
BuildRequires:	gnome-libs-devel
BuildRequires:	ncurses-devel >= 5.0
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
%patch0 -p1
%patch1 -p1

%build
rm -f missing
libtoolize --copy --force
aclocal -I %{_aclocaldir}/gnome
autoconf
automake -a -c
%configure \
	--without-socks \
	--with-bot \
	--with-textui \
	--with-proxy \
	--with-modules \
	%{?!_without_perl:--enable-perl=shared} \
	%{?_without_perl:--enable-perl=no} \
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

%{?_without_perl:#}(
%{?_without_perl:#}  for name in Irssi Irssi/Irc Irssi/TextUI Irssi/UI; do
%{?_without_perl:#}  cd $RPM_BUILD_ROOT%{perl_archlib}/auto/${name}
%{?_without_perl:#}  sed -e "s#$RPM_BUILD_ROOT##" .packlist >.packlist.new
%{?_without_perl:#}  mv .packlist.new .packlist
%{?_without_perl:#}  done
%{?_without_perl:#})

gzip -9nf AUTHORS ChangeLog README TODO NEWS docs/*.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/*.txt.gz
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/*.so*
%{_datadir}/%{name}
%{_applnkdir}/Network/Communications/irssi.desktop
%{_pixmapsdir}/*

%{?_without_perl:#}%{perl_archlib}/*.pm
%{?_without_perl:#}%dir %{perl_archlib}/Irssi
%{?_without_perl:#}%{perl_archlib}/Irssi/*.pm

%{?_without_perl:#}%dir %{perl_archlib}/auto/Irssi
%{?_without_perl:#}%{perl_archlib}/auto/Irssi/*.bs
%{?_without_perl:#}%attr(755,root,root) %{perl_archlib}/auto/Irssi/*.so

%{?_without_perl:#}%dir %{perl_archlib}/auto/Irssi/Irc
%{?_without_perl:#}%{perl_archlib}/auto/Irssi/Irc/*.bs
%{?_without_perl:#}%attr(755,root,root) %{perl_archlib}/auto/Irssi/Irc/*.so

%{?_without_perl:#}%dir %{perl_archlib}/auto/Irssi/TextUI
%{?_without_perl:#}%{perl_archlib}/auto/Irssi/TextUI/*.bs
%{?_without_perl:#}%attr(755,root,root) %{perl_archlib}/auto/Irssi/TextUI/*.so

%{?_without_perl:#}%dir %{perl_archlib}/auto/Irssi/UI
%{?_without_perl:#}%{perl_archlib}/auto/Irssi/UI/*.bs
%{?_without_perl:#}%attr(755,root,root) %{perl_archlib}/auto/Irssi/UI/*.so
