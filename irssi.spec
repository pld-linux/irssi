Name: irssi
Version: 0.7.15
Release: 1
Packager: Red Hat Contrib|Net <rhcn-bugs@redhat.com>
Vendor: Timo Sirainen <cras@irccrew.org>
Distribution: Red Hat Contrib|Net
Summary:  Irssi is a GTK based IRC client
Copyright: GPL
Group: X11/Applications/Networking
URL: http://xlife.dhs.org/irssi/
Source: http://xlife.dhs.org/irssi/files/%{name}-%{version}.tar.bz2
Requires: gtk+
Prefix: /usr
BuildRoot: /tmp/%{name}-%{version}

%changelog
* Thu Mar 25 1999 JT Traub <jtraub@dragoncat.net>
- Updated sources

* Sat Mar 13 1999 JT Traub <jtraub@dragoncat.net>
- Updated to 0.7.4 sources
- Added the irssi-text bin to the package.

* Mon Feb 22 1999 JT Traub <jtraub@dragoncat.net>
- Made spec file compliant with RHCN guidelines.

* Sun Feb 13 1999 JT Traub <jtraub@dragoncat.net>
- Updated to 0.6.0 sources.
- Cleaned up spec file to make it relocatable on install

* Sun Feb 7 1999  JT Traub <jtraub@dragoncat.net>
- Updated sources to 0.5.0
- removed obsolete patch lines

* Sat Feb 3 1999  JT Traub <jtraub@dragoncat.net>
- Updated sources to 0.4.0
- Deleted old patch line

* Sat Jan 30 1999  JT Traub <jtraub@dragoncat.net>
- Updated sources to 0.3.6
- Updated spec to install the .desktop file.
- Removed the now obsolete patch lines

* Wed Jan 27 1999  JT Traub <jtraub@dragoncat.net>
- Upgraded to 0.3.5

* Sun Jan 24 1999  JT Traub <jtraub@dragoncat.net>
- First attempt at building this

%description
Irssi is a GTK based GUI IRC client by Timo Sirainen <cras@irccrew.org>.
More information can be found at http://xlife.dhs.org/irssi/.


%prep
%setup
#%patch0 -p1 -b .slang

%build
./configure --prefix=%{prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix} install
strip $RPM_BUILD_ROOT%{prefix}/bin/irssi
#strip $RPM_BUILD_ROOT%{prefix}/bin/irssi-text


%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-,root,root)
%doc AUTHORS COPYING INSTALL ChangeLog README TODO NEWS
%attr(755,root,root) %{prefix}/bin/irssi
#%attr(755,root,root) %{prefix}/bin/irssi-text
%attr(644,root,root) %config %{prefix}/etc/irssi.conf
%attr(644,root,root) %{prefix}/etc/CORBA/servers/irssi.gnorba
%attr(644,root,root) %{prefix}/share/applets/Network/irssi.desktop
%attr(644,root,root) %{prefix}/lib/irssi/plugins/*.so
#%attr(644,root,root) %{prefix}/lib/irssi/scripts/perl/test.pl
