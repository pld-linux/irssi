# _with_glib1	use glib1 instead of glib2
#
#
%{!?_without_perl:%include	/usr/lib/rpm/macros.perl}
%define         snap 20030302
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - wygodny w u¿yciu klient IRC
Name:		irssi
Version:	0.8.6.%{snap}
Release:	1
License:	GPL
Vendor:		Timo Sirainen <cras@irccrew.org>
Group:		Applications/Communications
Source0:	http://real.irssi.org/files/snapshots/%{name}-%{snap}.tar.gz
URL:		http://www.irssi.org/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	gettext-devel
%{?_with_glib1:BuildRequires:	glib-devel >= 1.2.0}
%{!?_with_glib1:BuildRequires:	glib2-devel}
BuildRequires:	ncurses-devel >= 5.0
%{?!_without_perl:BuildRequires:	perl-devel >= 5.6.1}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%description
Irssi is a textUI IRC client with IPv6 support.

%description -l fr
Irssi est client IRC.

%description -l pl
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6.

%prep
%setup -q -n %{name}-0.8.6.CVS

%build
rm -f missing
%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__automake}
%configure \
	%{!?_without_perl:--with-perl=module} \
	%{!?_without_perl:--with-perl-lib=vendor} \
	%{?_without_perl:--with-perl=no} \
	--enable-ipv6 \
	%{?_with_glib1:--with-glib1}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{perl_sitearch},%{_pixmapsdir},%{_applnkdir}/Network/Communications}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/%{name}-%{version}

install %{SOURCE0} $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO NEWS docs/*.txt
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/irssi
%{_datadir}/%{name}
%{_sysconfdir}/irssi.conf
%{_mandir}/man1/*

%if %{!?_without_perl:1}0
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
