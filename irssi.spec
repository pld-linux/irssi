%{?_without_perl:#}%include	/usr/lib/rpm/macros.perl
%define	snap	20020522
%define xsnap   20020521
%define ver	0.8.4
%define ver_icq 0.1
Summary:	Irssi is a IRC client
Summary(fr):	Irssi est un client IRC
Summary(pl):	Irssi - wygodny w u¿yciu klient IRC
Name:		irssi
Version:	%{ver}.%{snap}
Release:	1
License:	GPL
Vendor:		Timo Sirainen <cras@irccrew.org>
Group:		Applications/Communications
Source0:	http://irssi.org/files/snapshots/%{name}-%{snap}.tar.gz
Source1:	xirssi-%{xsnap}.tar.bz2
Source2:	%{name}.desktop
Source3:	%{name}.png
Source4:	http://irssi.org/files/plugins/icq/%{name}-icq-%{ver_icq}.tgz
URL:		http://www.irssi.org/
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.0.1
BuildRequires:	gnome-libs-devel
BuildRequires:	ncurses-devel >= 5.0
BuildRequires:  gtk+2-devel
BuildRequires:	freetype-devel
%{?!_without_perl:BuildRequires:	perl-devel >= 5.6.1}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	%{name}-speech
Obsoletes:	%{name}-sql
%define         _prefix_x11        %{_prefix}/X11R6

%description
Irssi is a textUI IRC client with IPv6 support.

%description -l fr
Irssi est client IRC.

%description -l pl
Irssi jest tekstowym klientem IRC ze wsparciem dla IPv6.

%package -n xirssi
Summary:	GTK+2 frontend for irssi
Summary(pl):	Nak³adka na irssi w GTK+2
Group:		Applications/Communications
Requires:	irssi >= %{ver}.%{snap}

%description -n xirssi
xirssi is a GTK+2 frontend for irssi.

%description -n xirssi -l pl
xirssi jest nak³adk± w GTK+2 na irssi

#%package icq
#Summary:	ICQ plugin for irssi
#Summary(pl):	Wtyczka ICQ do irssi
#Group:		Applications/Communications
#Requires:	irssi

#%description icq
#With this plugin you can have all irc-chats and icq chats in one window.

#%description icq -l pl
#Dziêki temu pluginowi mo¿esz ircowaæ i u¿ywaæ icq - i to wszystko w jednym oknie.

%prep
#%setup -q -n %{name}-%{ver}.CVS
%setup -q -c -b 0 -b 1 -b 4

%build
cd %{name}-%{ver}.CVS
rm -f missing
libtoolize --copy --force
aclocal -I %{_aclocaldir}/gnome
autoconf
automake -a -c -f
%configure \
	--without-socks \
	--with-bot \
	--with-textui \
	--with-proxy \
	--with-modules \
	%{?!_without_perl:--enable-perl=shared} \
	%{?_without_perl:--enable-perl=no} \
	--enable-ipv6 \
	--enable-nls \
	--with-glib2

%{__make}
cd ../xirssi
rm -f missing
libtoolize --copy --force
aclocal -I %{_aclocaldir}/gnome
autoheader
autoconf
automake -a -c -f
%configure -with-irssi=../irssi-0.8.4.CVS

# Disabled, becouse there's in irssi new connect function...
#%{__make}
#cd ../%{name}-icq
#libtoolize --copy --force
#aclocal -I %{_aclocaldir}/gnome
#autoheader
#autoconf
#automake -a -c -f
#%configure -with-irssi=../irssi-0.8.4.CVS
#%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{perl_sitearch},%{_pixmapsdir},%{_applnkdir}/Network/Communications}

cd %{name}-%{ver}.CVS
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	docdir=%{_datadir}/%{name}-%{version}

install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Network/Communications
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}

%{?_without_perl:#}(
%{?_without_perl:#}  for name in Irssi Irssi/Irc Irssi/TextUI Irssi/UI; do
%{?_without_perl:#}  cd $RPM_BUILD_ROOT%{perl_archlib}/auto/${name}
%{?_without_perl:#}  sed -e "s#$RPM_BUILD_ROOT##" .packlist >.packlist.new
%{?_without_perl:#}  mv .packlist.new .packlist
%{?_without_perl:#}  done
%{?_without_perl:#})

gzip -9nf AUTHORS ChangeLog README TODO NEWS docs/*.txt

cd ../xirssi
install -d $RPM_BUILD_ROOT/usr/X11R6/bin
install src/xirssi $RPM_BUILD_ROOT/usr/X11R6/bin/
install pixmaps/irssilogo.jpg $RPM_BUILD_ROOT/%{_pixmapsdir}

gzip -9nf AUTHORS ChangeLog TODO

cd ../irssi-icq
install src/core/.libs/libicq_core.so $RPM_BUILD_ROOT/%{_libdir}/irssi/modules/
install src/fe-common/.libs/libfe_icq.so $RPM_BUILD_ROOT/%{_libdir}/irssi/modules/
gzip -9nf AUTHORS ChangeLog README
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{name}-%{ver}.CVS/*.gz %{name}-%{ver}.CVS/docs/*.txt.gz
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/irssi
%dir %{_libdir}/irssi/modules
%attr(755,root,root) %{_libdir}/irssi/modules/*proxy*.so*
%{_datadir}/%{name}
%{_applnkdir}/Network/Communications/irssi.desktop
%{_pixmapsdir}/*.png

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

%files -n xirssi
%defattr(644,root,root,755)
%attr(755,root,root) /usr/X11R6/bin/*
%{_pixmapsdir}/*.jpg
%doc xirssi/*.gz

#%files icq
#%defattr(644,root,root,755)
#%attr(755,root,root)%{_libdir}/irssi/modules/*icq*so
#%doc irssi-icq/*.gz
