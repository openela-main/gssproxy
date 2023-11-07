Name:		gssproxy

Version:	0.8.4
Release:	6%{?dist}
Summary:	GSSAPI Proxy

License:	MIT
URL:		https://github.com/gssapi/gssproxy
Source0:	https://github.com/gssapi/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:	rwtab

%global servicename gssproxy
%global pubconfpath %{_sysconfdir}/gssproxy
%global gpstatedir %{_localstatedir}/lib/gssproxy

### Patches ###
Patch0001: 0001-Add-an-option-for-minimum-lifetime.patch

### Dependencies ###
Requires: krb5-libs >= 1.12.0
Requires: keyutils-libs
Requires: libverto-module-base
Requires: libini_config >= 1.2.0
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

# We use a Conflicts: here so as not to interfere with users who make
# their own policy.  The version is the last time someone has filed a
# bug about gssproxy being broken with selinux.
Conflicts: selinux-policy < 3.13.1-283.5

### Build Dependencies ###
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: docbook-style-xsl
BuildRequires: doxygen
BuildRequires: findutils
BuildRequires: gettext-devel
BuildRequires: git
BuildRequires: keyutils-libs-devel
BuildRequires: krb5-devel >= 1.12.0
BuildRequires: libini_config-devel >= 1.2.0
BuildRequires: libselinux-devel
BuildRequires: libtool
BuildRequires: libverto-devel
BuildRequires: libxml2
BuildRequires: libxslt
BuildRequires: make
BuildRequires: m4
BuildRequires: pkgconfig
BuildRequires: popt-devel
BuildRequires: systemd-units

%description
A proxy for GSSAPI credential handling

%prep
%autosetup -S git

%build
autoreconf -f -i
%configure \
    --with-pubconf-path=%{pubconfpath} \
    --with-initscript=systemd \
    --disable-static \
    --disable-rpath \
    --with-gpp-default-behavior=REMOTE_FIRST

make %{?_smp_mflags} all
make test_proxymech

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/gssproxy/proxymech.la
install -d -m755 %{buildroot}%{_sysconfdir}/gssproxy
install -m644 examples/gssproxy.conf %{buildroot}%{_sysconfdir}/gssproxy/gssproxy.conf
install -m644 examples/99-nfs-client.conf %{buildroot}%{_sysconfdir}/gssproxy/99-nfs-client.conf
mkdir -p %{buildroot}%{_sysconfdir}/gss/mech.d
install -m644 examples/mech %{buildroot}%{_sysconfdir}/gss/mech.d/gssproxy.conf
mkdir -p %{buildroot}%{gpstatedir}/rcache
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rwtab.d
install -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rwtab.d/gssproxy

%files
%license COPYING
%{_unitdir}/gssproxy.service
%{_sbindir}/gssproxy
%attr(755,root,root) %dir %{pubconfpath}
%attr(755,root,root) %dir %{gpstatedir}
%attr(700,root,root) %dir %{gpstatedir}/clients
%attr(700,root,root) %dir %{gpstatedir}/rcache
%attr(0600,root,root) %config(noreplace) /%{_sysconfdir}/gssproxy/gssproxy.conf
%attr(0600,root,root) %config(noreplace) /%{_sysconfdir}/gssproxy/99-nfs-client.conf
%attr(0644,root,root) %config(noreplace) /%{_sysconfdir}/gss/mech.d/gssproxy.conf
%dir %{_libdir}/gssproxy
%{_libdir}/gssproxy/proxymech.so
%{_mandir}/man5/gssproxy.conf.5*
%{_mandir}/man8/gssproxy.8*
%{_mandir}/man8/gssproxy-mech.8*
%config(noreplace) %{_sysconfdir}/rwtab.d/gssproxy

%post
%systemd_post gssproxy.service

%preun
%systemd_preun gssproxy.service

%postun
%systemd_postun_with_restart gssproxy.service

%changelog
* Wed Apr 05 2023 Julien Rische <jrische@redhat.com> - 0.8.4-6
- Use openldap-servers from EPEL repo for testing
- Resolves: rhbz#2187634

* Mon Apr 03 2023 Julien Rische <jrische@redhat.com> - 0.8.4-5
- Add an option for minimum lifetime
- Resolves: rhbz#2184333
- Remove unused patch files
- Fix date typographical error in changelog

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com>
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com>
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Robbie Harwood <rharwood@redhat.com> - 0.8.4-1
- New upstream release (0.8.4)

* Thu Oct 29 2020 Robbie Harwood <rharwood@redhat.com> - 0.8.3-6
- Leak fix pullup

* Mon Oct 12 2020 Robbie Harwood <rharwood@redhat.com> - 0.8.3-5
- Document config file non-merging

* Wed Aug 26 2020 Robbie Harwood <rharwood@redhat.com> - 0.8.3-4
- Fix leak of mech OID in gssi_inquire_context()

* Fri Jul 31 2020 Robbie Harwood <rharwood@redhat.com> - 0.8.3-3
- Avoid leak of special mechs in gss_mech_interposer()

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Apr 17 2020 Robbie Harwood <rharwood@redhat.com> - 0.8.3-1
- New upstream release (0.8.3)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Robbie Harwood <rharwood@redhat.com> - 0.8.2-7
- Delay gssproxy start until after network.target

* Thu Oct 31 2019 Robbie Harwood <rharwood@redhat.com> - 0.8.2-6
- Make syslog of call status configurable

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Robbie Harwood <rharwood@redhat.com> - 0.8.2-4
- Replace /var/run -> /run in gssproxy.service
- Resolves: #1729739

* Fri May 03 2019 Robbie Harwood <rharwood@redhat.com> - 0.8.2-3
- Update NFS service name in systemd unit
- Resolves: #1702443

* Wed May 01 2019 Robbie Harwood <rharwood@redhat.com> - 0.8.2-2
- Avoid uninitialized free when allocating buffers

* Thu Apr 18 2019 Robbie Harwood <rharwood@redhat.com> - 0.8.2-1
- New usptream version (0.8.2)

* Tue Apr 16 2019 Robbie Harwood <rharwood@redhat.com> - 0.8.1-11
- New upstream version (0.8.1)
- Resolves: #1700541

* Mon Mar 18 2019 Robbie Harwood <rharwood@redhat.com> - 0.8.0-11
- Fix gssproxy blocking inside epoll_wait() due to kernel race

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Robbie Harwood <rharwood@redhat.com> - 0.8.0-9
- Add hack to support read-only root

* Tue Oct 02 2018 Robbie Harwood <rharwood@redhat.com> - 0.8.0-8
- Update docs to reflect actual behavior of krb5_principal

* Thu Sep 20 2018 Robbie Harwood <rharwood@redhat.com> - 0.8.0-7
- Use pthread keys for thread local storage

* Fri Aug 03 2018 Robbie Harwood <rharwood@redhat.com> - 0.8.0-6
- Don't leak sock_ctx if verto_add_io() fails

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 12 2018 Robbie Harwood <rharwood@redhat.com> - 0.8.0-4
- Drop patch level by one (woo!)

* Thu Apr 12 2018 Robbie Harwood <rharwood@redhat.com> - 0.8.0-3
- Always choose highest requested debug level
- Update man pages about debugging

* Tue Feb 27 2018 Robbie Harwood <rharwood@redhat.com> - 0.8.0-2
- Always use the encype we selected

* Fri Feb 09 2018 Robbie Harwood <rharwood@redhat.com> - 0.8.0-1
- Release version 0.8.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 13 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-29
- Conditionally reload kernel interface on SIGHUP

* Tue Dec 12 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-28
- Fixup previous

* Tue Dec 12 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-27
- More code hygeine fixes from upstream
- Reorder patches to match el7

* Tue Dec 05 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-26
- Properly initialize ccaches before storing into them

* Fri Dec 01 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-25
- Properly locate credentials in collection caches in mechglue

* Tue Oct 31 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-24
- Only empty FILE ccaches when storing remote creds

* Mon Oct 30 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-23
- Fix error message handling in gp_config_from_dir()

* Fri Oct 27 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-22
- Fix concurrency issue in server socket handling

* Mon Oct 02 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-21
- Off-by-one error fix in selinux-policy version

* Mon Oct 02 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-20
- Change selinux-policy versioning to Conflicts

* Fri Sep 29 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-19
- Add explicit selinux-policy dependency after some fixes

* Fri Sep 29 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-18
- Fix silent death if config file has duplicate sections

* Thu Sep 21 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-17
- Handle outdated encrypted ccaches

* Fri Sep 15 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-16
- Backport updates to epoll logic

* Tue Sep 12 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-15
- Backport two security fixes

* Tue Aug 22 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-14
- Non-blocking IO + Extended request debug logging

* Sun Aug 20 2017 Ville Skyttä <ville.skytta@iki.fi> - 0.7.0-13
- Own the %%{_libdir}/gssproxy dir
- Mark COPYING as %%license

* Mon Jul 31 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-12
- Add client ID to debug messages
- Move packaging to autosetup

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-10
 - Fix potential explicit NULL deref of program name

* Thu May 25 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-9
- Make proc failure loud but nonfatal

* Wed May 24 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-8
- Remove (buggy?) logic around NFS snippet.

* Wed May 17 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-7
- Remove NFS server stanza if nfs-utils not present
- Also update gcc7 patch to match upstream

* Tue May 16 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-6
- Fix segfault when no configuration files are found
- Various build fixes for gcc7

* Mon May 01 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-5
- Update systemd unit file (nfs removal, reload capability)

* Mon Apr 03 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-4
- Backport fix for double unlock

* Tue Mar 28 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-3
- Drop NFS server snippet (removes dependency on nfs kernel component)

* Tue Mar 14 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-2
- Fix credential renewal and impersonator checking for m_a_g

* Tue Mar 07 2017 Robbie Harwood <rharwood@redhat.com> - 0.7.0-1
- New upstream release - 0.7.0

* Mon Mar 06 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.2-4
- Actually apply the patches I just added
- Also include a Coverity fix.

* Tue Feb 28 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.2-2
- Include other non-null fix and various things from master

* Thu Feb 23 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.2-1
- Fix incorrect use of non-null string in xdr
- Also move version number to better reflect what is inside

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.1-2
- Fix allocation issue of cred store
- Resolves: #1415400

* Fri Jan 20 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.1-1
- New upstream release v0.6.1
- Resolves: #1415090

* Wed Jan 18 2017 Robbie Harwood <rharwood@redhat.com> - 0.6.0-1
- New upstream release v0.6.0

* Tue Sep 27 2016 Robbie Harwood <rharwood@redhat.com> - 0.5.1-3
- Adjust libverto dependency to not use a specific backend
- Resolves: #1379812

* Tue Jun 14 2016 Robbie Harwood <rharwood@redhat.com> - 0.5.1-2
- Own /var/lib/gssproxy/rcache

* Mon Jun 13 2016 Robbie Harwood <rharwood@redhat.com> - 0.5.1-1
- Update to upstream release v0.5.1
- Resolves: #1345871

* Tue Jun 07 2016 Robbie Harwood <rharwood@redhat.com> - 0.5.0-5
- Acquire new socket for fork/permission drops on clients

* Mon May 09 2016 Robbie Harwood <rharwood@redhat.com> - 0.5.0-4
- Do not package mod_auth_gssapi conf file
  - This ensures gssproxy works even when the apache user does not exist

* Thu May 05 2016 Robbie Harwood <rharwood@redhat.com> - 0.5.0-3
- Ensure we actually package the config files

* Thu May 05 2016 Simo Sorce <simo@redhat.com> - 0.5.0-2
- Fix typo in requires

* Wed May 04 2016 Robbie Harwood <rharwood@redhat.com> - 0.5.0-1
- Release new upstream version
- Bump ini_config version for `ini_config_augment()`

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 16 2015 Robbie Harwood <rharwood@redhat.com> - 0.4.1-4
- Fix issues with 1.14
- Fix bogus date in changelog (March 30 2015 was a Monday)

* Wed Oct 21 2015 Robbie Harwood <rharwood@redhat.com> - 0.4.1-3
- Clear message buffer to fix segfault on arm
- resolves: #1235902

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Simo Sorce <simo@redhat.com> 0.4.1-1
- New upstream release
- Fix issues with paths in config files

* Tue Mar 24 2015 Simo Sorce <simo@redhat.com> 0.4.0-2
- Workaround rawhide bug (bz1204646) with krb5-config by switching to
  pkg-config (patch from upstream)

* Tue Mar 24 2015 Simo Sorce <simo@redhat.com> 0.4.0-1
- New upstream realease
  Added optional support for running GSS-Proxy as an unprivileged user
  Uses new /etc/gss/mech.d configuration directory for gss mechanisms
  Kernel related fixes
  General bug fixing, many minor errors or incorrect behaviours have been corrected
- drop all patches, they are all included upstream

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Simo Sorce <simo@redhat.com> 0.3.1-2
- Rebuild as new ding-libs brings in soname bump

* Thu Mar 13 2014 Guenther Deschner <gdeschner@redhat.com> 0.3.1-1
- Fix flags handling in gss_init_sec_context()
- resolves: https://fedorahosted.org/gss-proxy/ticket/112
- Fix nfsd startup
- resolves: https://fedorahosted.org/gss-proxy/ticket/114
- Fix potential mutex deadlock
- resolves: https://fedorahosted.org/gss-proxy/ticket/120
- Fix segfault in gssi_inquire_context
- resolves: https://fedorahosted.org/gss-proxy/ticket/117
- resolves: #1061133

* Tue Nov 26 2013 Guenther Deschner <gdeschner@redhat.com> 0.3.1-0
- New upstream release 0.3.1:
  * Fix use of gssproxy for client initiation
  * Add new enforcing and filtering options for context initialization
  * Fix potential thread safety issues
- resolves: https://fedorahosted.org/gss-proxy/ticket/110
- resolves: https://fedorahosted.org/gss-proxy/ticket/111

* Tue Nov 19 2013 Guenther Deschner <gdeschner@redhat.com> 0.3.0-3
- Fix flags handling in gss_init_sec_context()
- resolves: https://fedorahosted.org/gss-proxy/ticket/106
- Fix OID handling in gss_inquire_cred_by_mech()
- resolves: https://fedorahosted.org/gss-proxy/ticket/107
- Fix continuation processing for not yet fully established contexts.
- resolves: https://fedorahosted.org/gss-proxy/ticket/108
- Add flags filtering and flags enforcing.
- resolves: https://fedorahosted.org/gss-proxy/ticket/109

* Wed Oct 23 2013 Guenther Deschner <gdeschner@redhat.com> 0.3.0-0
- New upstream release 0.3.0:
  * Add support for impersonation (depends on s4u2self/s4u2proxy on the KDC)
  * Add support for new rpc.gssd mode of operation that forks and changes uid
  * Add 2 new options allow_any_uid and cred_usage

* Fri Oct 18 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.3-8
- Fix default proxymech documentation and fix LOCAL_FIRST implementation
- resolves: https://fedorahosted.org/gss-proxy/ticket/105

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.3-6
- Add better default gssproxy.conf file for nfs client and server usage

* Thu Jun 06 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.3-5
- New upstream release

* Fri May 31 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.2-5
- Require libverto-tevent to make sure libverto initialization succeeds

* Wed May 29 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.2-4
- Modify systemd unit files for nfs-secure services

* Wed May 22 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.2-3
- Fix cred_store handling w/o client keytab

* Thu May 16 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.2-2
- New upstream release

* Tue May 07 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.1-2
- New upstream release

* Wed Apr 24 2013 Guenther Deschner <gdeschner@redhat.com> 0.2.0-1
- New upstream release

* Mon Apr 01 2013 Simo Sorce <simo@redhat.com> - 0.1.0-0
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.3-7
- Update to 0.0.3

* Wed Aug 22 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.2-6
- Use new systemd-rpm macros
- resolves: #850139

* Wed Jul 18 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.2-5
- More spec file fixes

* Mon Jul 16 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.2-4
- Fix systemd service file

* Fri Jul 13 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.2-3
- Fix various packaging issues

* Mon Jul 02 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.1-2
- Add systemd packaging

* Wed Mar 28 2012 Guenther Deschner <gdeschner@redhat.com> 0.0.1-1
- Various fixes

* Mon Dec 12 2011 Simo Sorce <simo@redhat.com> - 0.0.2-0
- Automated build of the gssproxy daemon
