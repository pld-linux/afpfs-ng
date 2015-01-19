#
# Conditional build:
%bcond_without	fuse		# FUSE driver for AFP filesystem

Summary:	Apple Filing Protocol client
Name:		afpfs-ng
Version:	0.8.1
Release:	1
License:	GPL+
Group:		Base
Source0:	http://downloads.sourceforge.net/afpfs-ng/%{name}-%{version}.tar.bz2
# Source0-md5:	1bdd9f8a06e6085ea4cc38ce010ef60b
URL:		https://sites.google.com/site/alexthepuffin/
Patch0:		overflows.patch
Patch1:		pointer.patch
Patch2:		formatsec.patch
BuildRequires:	gmp-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	readline-devel
%if %{with fuse}
BuildRequires:	libfuse-devel
Suggests:	fuse-afp
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A command line client to access files exported from Mac OS system via
Apple Filing Protocol.

%package -n fuse-afp
Summary:	FUSE driver for AFP filesystem
Group:		Base

%description -n fuse-afp
A FUSE file system server to access files exported from Mac OS system
via AppleTalk or TCP using Apple Filing Protocol. The command line
client for AFP is in fuse-afp package

%package devel
Summary:	Development files for afpfs-ng
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Library for dynamic linking and header files of afpfs-ng.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# make would rebuild the autoconf infrastructure due to the following:
# Prerequisite `configure.ac' is newer than target `Makefile.in'.
# Prerequisite `aclocal.m4' is newer than target `Makefile.in'.
# Prerequisite `configure.ac' is newer than target `aclocal.m4'.
touch --reference aclocal.m4 configure.ac Makefile.in

%build
%configure \
	%{!?with_fuse:--disable-fuse} \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libafpclient.la

install -d $RPM_BUILD_ROOT%{_includedir}/afpfs-ng
cp -p include/* $RPM_BUILD_ROOT%{_includedir}/afpfs-ng

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING AUTHORS ChangeLog docs/README docs/performance docs/FEATURES.txt docs/REPORTING-BUGS.txt
%attr(755,root,root) %{_bindir}/afpcmd
%attr(755,root,root) %{_bindir}/afpgetstatus
%{_mandir}/man1/afpcmd.1*
%{_mandir}/man1/afpgetstatus.1*
%attr(755,root,root) %{_libdir}/libafpclient.so.0.0.0
%ghost %{_libdir}/libafpclient.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/afpfs-ng
%{_libdir}/libafpclient.so

%if %{with fuse}
%files -n fuse-afp
%defattr(644,root,root,755)
%doc COPYING AUTHORS ChangeLog
%attr(755,root,root) %{_bindir}/afp_client
%attr(755,root,root) %{_bindir}/afpfs
%attr(755,root,root) %{_bindir}/afpfsd
%attr(755,root,root) %{_bindir}/mount_afp
%{_mandir}/man1/afp_client.1*
%{_mandir}/man1/afpfsd.1*
%{_mandir}/man1/mount_afp.1*
%endif
