Summary:	OpenPrinting CUPS filters and backends
Name:		cups-filters
Version:	1.0.41
Release:	8
# For a breakdown of the licensing, see COPYING file
# GPLv2:   filters: commandto*, imagetoraster, pdftops, rasterto*,
#                   imagetopdf, pstopdf, texttopdf
#         backends: parallel, serial
# GPLv2+:  filters: gstopxl, textonly, texttops, imagetops
# GPLv3:   filters: bannertopdf
# GPLv3+:  filters: urftopdf
# LGPLv2+:   utils: cups-browsed
# MIT:     filters: gstoraster, pdftoijs, pdftoopvp, pdftopdf, pdftoraster
License:	GPLv2 and GPLv2+ and GPLv3 and GPLv3+ and LGPLv2+ and MIT
Group:		Applications/Printing
Source0:	http://www.openprinting.org/download/cups-filters/%{name}-%{version}.tar.xz
# Source0-md5:	fe5a9a07b9a64b35975154068cbedef9
Patch1:		%{name}-pdf-landscape.patch
Patch2:		%{name}-dbus.patch
URL:		http://www.linuxfoundation.org/collaborate/workgroups/openprinting/cups-filters
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-devel
BuildRequires:	avahi-glib-devel
BuildRequires:	cups-devel >= 1:1.6.0
BuildRequires:	dbus-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	ghostscript-ijs-devel
BuildRequires:	lcms2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	poppler-cpp-devel
BuildRequires:	poppler-devel
BuildRequires:	poppler-progs
BuildRequires:	python-pycups
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	qpdf-devel
BuildRequires:	systemd
BuildRequires:	zlib-devel
# Testing font for test scripts.
#BuildRequires:	dejavu-sans-fonts
Requires:	cups-filters-libs = %{version}-%{release}
Requires:	fonts-TTF-freefont
Requires:	poppler-progs
# pstopdf
Requires:	bc
Requires:	grep
Requires:	sed
Provides:	ghostscript-cups = 9.08
Obsoletes:	ghostscript-cups < 9.08
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cups_serverbin		%(/usr/bin/cups-config --serverbin)

%package libs
Summary:	OpenPrinting CUPS filters and backends - cupsfilters and fontembed libraries
Group:		Libraries
# LGPLv2: libcupsfilters
# MIT:    libfontembed
License:	LGPLv2 and MIT

%package devel
Summary:	OpenPrinting CUPS filters and backends - development environment
License:	LGPLv2 and MIT
Group:		Development/Libraries
Requires:	cups-filters-libs = %{version}-%{release}

%description
Contains backends, filters, and other software that was once part of
the core CUPS distribution but is no longer maintained by Apple Inc.
In addition it contains additional filters developed independently of
Apple, especially filters for the PDF-centric printing workflow
introduced by OpenPrinting.

%description libs
This package provides cupsfilters and fontembed libraries.

%description devel
This is the development package for OpenPrinting CUPS filters and
backends.

%package -n cups-browsed
Summary:	A daemon for browsing the Bonjour broadcasts of shared, remote CUPS printers
Group:		Applications/Printing
Requires(post,preun,postun):	systemd-units
Requires:	cups-filters-libs = %{version}-%{release}
Requires:	systemd-units >= 38

%description -n cups-browsed
A daemon for browsing the Bonjour broadcasts of shared,
remote CUPS printers.

%package -n cups-backend-serial
Summary:	Serial port backend for CUPS
Summary(pl.UTF-8):	Backend obsługujący porty szeregowe dla CUPS-a
# must be larger than cups.spec
Epoch:		2
License:	GPL v2 + openssl exception
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}

%description -n cups-backend-serial
This package allow CUPS printing on printers connected by serial
ports.

%description -n cups-backend-serial -l pl.UTF-8
Ten pakiet umożliwia drukowanie z poziomu CUPS-a na drukarkach
podłączonych do portów szeregowych.

%package -n cups-backend-parallel
Summary:	Parallel port backend for CUPS
Summary(pl.UTF-8):	Backend obsługujący porty równoległe dla CUPS-a
# must be larger than cups.spec
Epoch:		2
License:	GPL v2 + openssl exception
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}

%description -n cups-backend-parallel
This package allow CUPS printing on printers connected by parallel
ports.

%description -n cups-backend-parallel -l pl.UTF-8
Ten pakiet umożliwia drukowanie z poziomu CUPS-a na drukarkach
podłączonych do portów równoległych.

# CREATE ANY NEW PACKAGES BEFORE cups-backend-* (EPOCH)

%prep
%setup -q
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--disable-static \
	--disable-silent-rules \
	--with-pdftops=hybrid \
	--enable-dbus \
	--with-rcdir=no

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

# Not sure what is this good for.
%{__rm} $RPM_BUILD_ROOT%{_bindir}/ttfread

install -p utils/cups-browsed.service $RPM_BUILD_ROOT%{systemdunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n cups-browsed
if [ $1 -eq 1 ] ; then
	# We can remove this after few releases, it's just for the introduction of cups-browsed.
	if [ -f %{_sysconfdir}/cups/cups-browsed.conf ]; then
		echo -e "\n# NOTE: This file is not part of CUPS. You need to start & enable cups-browsed service." >>%{_sysconfdir}/cups/cups-browsed.conf
	fi

	# move BrowsePoll from cupsd.conf to cups-browsed.conf
	if [ -f %{_sysconfdir}/cups/cupsd.conf ] && grep -iq "^BrowsePoll" %{_sysconfdir}/cups/cupsd.conf; then
		if ! grep -iq "^BrowsePoll" %{_sysconfdir}/cups/cups-browsed.conf; then
			echo "# Settings automatically moved from cupsd.conf by RPM package:" >>%{_sysconfdir}/cups/cups-browsed.conf
			grep -i "^BrowsePoll" %{_sysconfdir}/cups/cupsd.conf >> %{_sysconfdir}/cups/cups-browsed.conf || :
		fi
		sed -i -e "s,^BrowsePoll,#BrowsePoll directive moved to cups-browsed.conf\n#BrowsePoll,i" %{_sysconfdir}/cups/cupsd.conf || :
	fi
fi
%systemd_post cups-browsed.service

%preun -n cups-browsed
%systemd_preun cups-browsed.service

%postun -n cups-browsed
%systemd_reload

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS NEWS
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fonts/conf.d/99pdftoopvp.conf
%attr(755,root,root) %{_cups_serverbin}/filter/*
%{_datadir}/cups/banners
%{_datadir}/cups/charsets
%{_datadir}/cups/data/*.pdf
%{_datadir}/cups/data/testprint
# this needs to be in the main package because of cupsfilters.drv
%{_datadir}/cups/ppdc/pcl.h
%{_datadir}/cups/drv/cupsfilters.drv
%{_datadir}/cups/mime/cupsfilters.types
%{_datadir}/cups/mime/cupsfilters.convs
%{_datadir}/ppd/cupsfilters

%files libs
%defattr(644,root,root,755)
%doc fontembed/README
%attr(755,root,root) %{_libdir}/libcupsfilters.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcupsfilters.so.1
%attr(755,root,root) %{_libdir}/libfontembed.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfontembed.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/cupsfilters
%{_includedir}/fontembed
%{_datadir}/cups/ppdc/escp.h
%{_pkgconfigdir}/libcupsfilters.pc
%{_pkgconfigdir}/libfontembed.pc
%attr(755,root,root) %{_libdir}/libcupsfilters.so
%attr(755,root,root) %{_libdir}/libfontembed.so

%files -n cups-browsed
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cups/cups-browsed.conf
%attr(755,root,root) %{_sbindir}/cups-browsed
%{systemdunitdir}/cups-browsed.service
%{_mandir}/man8/cups-browsed.8*
%{_mandir}/man5/cups-browsed.conf.5*

%files -n cups-backend-serial
%defattr(644,root,root,755)
%attr(755,root,root) %{_cups_serverbin}/backend/serial

%files -n cups-backend-parallel
%defattr(644,root,root,755)
%attr(755,root,root) %{_cups_serverbin}/backend/parallel
