%define name	nagiosgraph
%define version 1.4.3
%define release %mkrel 1

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Visualization addon for nagios
License:	GPL
Group:		Networking/WWW
URL:		http://nagiosgraph.sourceforge.net
Source:     http://downloads.sourceforge.net/nagiosgraph/%{name}-%{version}.tar.gz
Patch:      nagiosgraph-1.4.3-fhs.patch
Requires:   nagios
Requires(post):   rpm-helper
%if %mdkversion < 201010
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

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

    Order allow,deny
    Allow from all
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

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc AUTHORS CHANGELOG INSTALL README README.urpmi TODO
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/nagiosgraph
%{_datadir}/%{name}
%attr(-,nagios,nagios) %{_var}/lib/%{name}
