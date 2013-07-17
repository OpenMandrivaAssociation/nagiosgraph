Name:		nagiosgraph
Version:	1.4.3
Release:	4
Summary:	Visualization addon for nagios
License:	GPL
Group:		Networking/WWW
URL:		http://nagiosgraph.sourceforge.net
Source:     http://downloads.sourceforge.net/nagiosgraph/%{name}-%{version}.tar.gz
Patch:      nagiosgraph-1.4.3-fhs.patch
Requires:   nagios
BuildArch:	noarch

%description
Nagiosgraph is an add-on of Nagios. It collects service performance data into
rrd format, and displays the resulting graphs via cgi.

%prep
%setup -q -n %{name}-%{version}
%patch -p 1

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 etc/* %{buildroot}%{_sysconfdir}/%{name}
rm -f %{buildroot}%{_sysconfdir}/%{name}/*.pm

install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}/lib
install -m 644 etc/ngshared.pm %{buildroot}%{_datadir}/%{name}/lib

install -d -m 755 %{buildroot}%{_datadir}/%{name}/www
install -m 755 cgi/* %{buildroot}%{_datadir}/%{name}/www
install -m 644 share/*.css %{buildroot}%{_datadir}/%{name}/www

install -d -m 755 %{buildroot}%{_datadir}/%{name}/bin
install -m 755 lib/* %{buildroot}%{_datadir}/%{name}/bin

install -d -m 755 %{buildroot}%{_var}/lib/nagiosgraph

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
Alias /%{name} %{_datadir}/%{name}/www

<Directory %{_datadir}/%{name}/www>
    DirectoryIndex show.cgi
    Options ExecCGI

    Require all granted
</Directory>
EOF

cat > README.urpmi <<EOF
Mandriva RPM specific notes

setup
-----
This software has been modified to comply with FHS:
- all configurations files are located in %{_sysconfdir}/nagiosgraph
EOF

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif
%create_ghostfile /var/log/nagiosgraph.log nagios apache 664


%files
%defattr(-,root,root)
%doc AUTHORS CHANGELOG INSTALL README README.urpmi TODO
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/nagiosgraph
%{_datadir}/%{name}
%attr(-,nagios,nagios) %{_var}/lib/%{name}


%changelog
* Sat Jul 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.3-1mdv2011.0
+ Revision: 554504
- new version

* Thu Mar 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.2-1mdv2010.1
+ Revision: 525138
- new version
- rediff fhs patch

* Fri Feb 19 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.1-1mdv2010.1
+ Revision: 508002
- new version

* Wed Feb 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.0-2mdv2010.1
+ Revision: 507288
- fix dependencies

* Thu Jan 21 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.0-1mdv2010.1
+ Revision: 494750
- new version
- rely on filetrigger for reloading apache configuration begining with 2010.1,
  rpm-helper macros otherwise

* Thu Dec 17 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.3-1mdv2010.1
+ Revision: 479723
- new version

* Sun Nov 22 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.2-1mdv2010.1
+ Revision: 468634
- update to new version 1.3.2

* Sat Jul 18 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.1-1mdv2010.0
+ Revision: 397014
- new version

* Fri Jan 30 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.0-1mdv2009.1
+ Revision: 335581
- new version

* Sun Dec 28 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.3-1mdv2009.1
+ Revision: 320705
- import nagiosgraph


* Sun Dec 28 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.3-1mdv2009.1
- first mdv release 
