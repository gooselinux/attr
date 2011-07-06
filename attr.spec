Summary: Utilities for managing filesystem extended attributes
Name: attr
Version: 2.4.44
Release: 4%{?dist}
Conflicts: xfsdump < 2.0.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: http://download.savannah.gnu.org/releases-noredirect/attr/attr-%{version}.src.tar.gz
Source2: sort-getfattr-output
Patch1: attr-2.2.0-multilib.patch
Patch2: attr-2.4.32-build.patch
Patch3: attr-2.4.43-leak.patch
Patch4: attr-2.4.44-tests.patch
Patch5: attr-bz599562.patch
License: GPLv2+
URL: http://oss.sgi.com/projects/xfs/
Group: System Environment/Base
BuildRequires: gettext
BuildRequires: libtool
Requires: libattr = %{version}-%{release}

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n libattr
Summary: Dynamic library for extended attribute support
Group: System Environment/Libraries
License: LGPLv2+

%description -n libattr
This package contains the libattr.so dynamic library which contains
the extended attribute system calls and library functions.

%package -n libattr-devel
Summary: Extended attribute static libraries and headers
Group: Development/Libraries
License: LGPLv2+
Requires: libattr = %{version}-%{release}

%description -n libattr-devel
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

Currently only ext2, ext3 and XFS support extended attributes.
The SGI IRIX compatibility API built above the Linux system calls is
used by programs such as xfsdump(8), xfsrestore(8) and xfs_fsr(8).

You should install libattr-devel if you want to develop programs
which make use of extended attributes.  If you install libattr-devel,
you'll also want to install attr.

%prep
%setup -q
# We need to turn off executable permissions on the script in %doc
# because we don't want to drag perl into the base.  Users advanced
# enough to have used ACLs before they were added to the distro can
# figure out how to chmod and how to install perl.  :-)
%patch1 -p1
%patch2 -p1

# applied upstream
%patch3 -p1

# make the test-suite ready for SELinux
%patch4 -p1

# bz #599562
%patch5 -p1

# test-suite helper script
install -m0755 %{SOURCE2} test/

autoconf

%build
# attr abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}
make LIBTOOL="libtool --tag=CC"

%check
if ./setfattr/setfattr -n user.name -v value .; then
    make tests || exit $?
else
    echo '*** xattrs are probably not supported by the file system,' \
         'the test-suite will NOT run ***'
fi

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-dev DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

# get rid of libattr.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libattr.la

# fix links to shared libs and permissions
rm -f $RPM_BUILD_ROOT/%{_libdir}/libattr.so
ln -sf ../../%{_lib}/libattr.so $RPM_BUILD_ROOT/%{_libdir}/libattr.so
chmod 0755 $RPM_BUILD_ROOT/%{_lib}/libattr.so.*.*.*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libattr -p /sbin/ldconfig

%postun -n libattr -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc doc
%{_bindir}/attr
%{_bindir}/getfattr
%{_bindir}/setfattr
%{_mandir}/man1/attr.1*
%{_mandir}/man1/getfattr.1*
%{_mandir}/man1/setfattr.1*
%{_mandir}/man5/attr.5*

%files -n libattr-devel
%defattr(-,root,root,-)
/%{_lib}/libattr.so
%{_includedir}/attr
%{_libdir}/libattr.*
%{_mandir}/man2/*attr.2*
%{_mandir}/man3/attr_*.3.*

%files -n libattr
%defattr(-,root,root,-)
/%{_lib}/libattr.so.*

%changelog
* Thu Jun 03 2010 Kamil Dudka <kdudka@redhat.com> 2.2.44-4
- fix memory leak and possible double free (#599562)

* Tue May 25 2010 Kamil Dudka <kdudka@redhat.com> 2.2.44-3
- let attr depend on the same version of libattr (#595689)

* Wed Mar 24 2010 Kamil Dudka <kdudka@redhat.com> 2.2.44-2
- run the test-suite if possible

* Thu Jan 07 2010 Kamil Dudka <kdudka@redhat.com> 2.4.44-1
- update to the latest bugfix release
- cleanup in BuildRequires

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.4.43-4.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Zdenek Prikryl <zprikryl@redhat.com> 2.4.43-2
- Fixed memory leaks (#485473)

* Wed Jul 16 2008 Zdenek Prikryl <zprikryl@redhat.com> 2.4.43-1
- New version 2.4.43

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.41-2
- fix license tags

* Tue Feb 13 2008 Zdenek Prikryl <zprikryl@redhat.com> 2.4.41-1
- New version 2.4.41
- Removed useless attr-2.0.8-docperms.patch

* Wed Oct 31 2007 Zdenek Prikryl <zprikryl@redhat.com> 2.4.39-1
- New version 2.4.39
- Resolves #284121

* Tue Oct 30 2007 Zdenek Prikryl <zprikryl@redhat.com> 2.4.38-2
- Removed explicit Requires(post + postun)
- Resolves #225290

* Tue Jul 31 2007 Zdenek Prikryl <zprikryl@redhat.com> 2.4.38-1
- New version 2.4.38
- Resolves #245415

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 2.4.32-2
- add disttag
- remove trailing dot from summary
- fix buildroot
- -devel package requires same libattr version
- change prereq to Requires(post)
- escape macro in changelog
- replace absolute link with relative link (libattr.so)
- use %%doc macro

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.4.32-1.1
- rebuild

* Wed Jul  5 2006 Thomas Woerner <twoerne@redhat.com> 2.4.32-1
- new version 2.4.32
- fixes segmentation fault in attr, which affects #189106

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 2.4.28-2
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.28-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.28-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Thomas Woerner <twoerner@redhat.com> 2.4.28-1
- new version 2.4.28

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Thomas Woerner <twoerner@redhat.com> 2.4.24-2
- spec file cleanup
- mark po files as lang specific

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 2.4.24

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.4.23-1
- update to 2.4.23

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.4.16-6
- get rid of *.la files
- remove duplicate doc files

* Wed Feb  9 2005 Stephen C. Tweedie <sct@redhat.com> 2.4.16-4
- Rebuild

* Fri Sep 10 2004 Stephen C. Tweedie <sct@redhat.com> 2.4.16-3
- Build requires libtool >= 1.5

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.16-2
- Make libattr.so.* executable.

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.4.16-1
- Update to latest upstream version.

* Sun Aug  8 2004 Alan Cox <alan@redhat.com> 2.4.1-6
- Fix bug #125304 (Steve Grubb: build requires gettext)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 31 2004 Stephen C. Tweedie <sct@redhat.com> 2.4.1-4
- Add missing %%defattr

* Tue Mar 30 2004 Stephen C. Tweedie <sct@redhat.com> 2.4.1-3
- Add /usr/include/attr to files manifest
- Fix location of doc files, add main doc dir to files manifest

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Aug  5 2003 Elliot Lee <sopwith@redhat.com> 2.4.1-2
- Fix libtool

* Tue Jun  3 2003 Stephen C. Tweedie <sct@redhat.com> 2.4.1-1
- update to attr-2.4.1

* Tue Jan 28 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.0-1
- update/rebuild

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.0.8-6
- set execute bits on library so that requires are generated.

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 2.0.8-5
- Redo multilib patch to work everywhere

* Wed Sep 11 2002 Than Ngo <than@redhat.com> 2.0.8-4
- Added fix to install libs in correct directory on 64bit machine 

* Thu Aug 08 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-3
- Made the package only own the one directory that is unique to it:
  /usr/include/attr

* Wed Jun 26 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-2
- get perl out of base with attr-2.0.8-docperms.patch

* Mon Jun 24 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.8-1
- Initial Red Hat package
  Made as few changes as possible relative to upstream packaging to
  make it easier to maintain long-term.  This means that some of
  the techniques used here are definitely not standard Red Hat
  techniques.  If you are looking for an example package to fit
  into Red Hat Linux transparently, this would not be the one to
  pick.
- attr-devel -> libattr-devel
