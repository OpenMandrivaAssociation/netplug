%define name netplug
%define version 1.2.9
%define release %mkrel 6

Summary: Hotplug-style support for network cables
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.red-bean.com/~bos/%{name}/%{name}-%{version}.tar.bz2
Patch0: netplug-1.2.9-execshield.patch.bz2
Patch1: netplug-1.2.9-bitkeeper.patch.bz2
Patch2: netplug-1.2.9-pinit.patch.bz2
License: GPL
Group: System/Configuration/Networking
Url: http://www.red-bean.com/~bos/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(post): rpm-helper
Requires(preun): rpm-helper
Conflicts: net-tools < 1.60-18mdk

%description
The netplug daemon listens for carrier detection and loss messages
from the kernel's netlink subsystem.  When a carrier signal is
detected on an interface, it runs a script to bring the interface up.
When carrier is lost, netplug runs a script to bring the interface
down.

NOTE: prefer ifplugd, since it's integrated in Mandriva network scripts
and is more configurable

%prep
%setup -q
%patch0 -p1 -b .execshield
%patch1 -p1 -b .bitkeeper
%patch2 -p1 -b .pinit

%build
%make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=%{buildroot} \
     initdir=%{buildroot}%{_initrddir} \
     mandir=%{buildroot}%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service netplugd

%preun
%_preun_service netplugd

%files
%defattr(-,root,root)
%doc README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/netplug/netplugd.conf
%dir %{_sysconfdir}/netplug.d
%attr(0755,root,root) %{_sysconfdir}/netplug.d/*
%attr(0755,root,root) %{_initrddir}/netplugd
/sbin/netplugd
%{_mandir}/man8/*

