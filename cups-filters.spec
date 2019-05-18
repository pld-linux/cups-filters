#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	braille		# Braille embossers support
%bcond_without	perl		# Perl module
%bcond_without	php		# PHP extension

%if 0%{!?php_name:1}
%define		php_name	php55
%endif
Summary:	OpenPrinting CUPS filters and backends
Summary(pl.UTF-8):	Filtry i backendy CUPS-a z projektu OpenPrinting
Name:		cups-filters
Version:	1.23.0
Release:	1
# For a breakdown of the licensing, see COPYING file
# GPLv2:   filters: commandto*, imagetoraster, pdftops, rasterto*,
#                   imagetopdf, pstopdf, texttopdf
#         backends: parallel, serial
# GPLv2+:  filters: gstopxl, textonly, texttops, imagetops
# GPLv3:   filters: bannertopdf
# GPLv3+:  filters: urftopdf
# LGPLv2+:   utils: cups-browsed
# MIT:     filters: gstoraster, pdftoijs, pdftoopvp, pdftopdf, pdftoraster
License:	GPL v2, GPL v2+, GPL v3, GPL v3+, LGPL v2+, MIT
Group:		Applications/Printing
Source0:	http://www.openprinting.org/download/cups-filters/%{name}-%{version}.tar.xz
# Source0-md5:	45a0ccc742d50e51c90e4b8ec1e8be5c
Patch0:		%{name}-dbus.patch
Patch1:		%{name}-php.patch
Patch2:		%{name}-php7.patch
Patch3:		%{name}-php73.patch
Patch4:		%{name}-poppler.patch
URL:		http://www.linuxfoundation.org/collaborate/workgroups/openprinting/cups-filters
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	avahi-devel
BuildRequires:	avahi-glib-devel
BuildRequires:	cups-devel >= 1:1.6.0
BuildRequires:	dbus-devel
BuildRequires:	fontconfig-devel >= 2.0.0
BuildRequires:	freetype-devel >= 2
# /usr/bin/gs, for features detection
%{?with_php:BuildRequires:	%{php_name}-devel}
BuildRequires:	ghostscript
BuildRequires:	ghostscript-ijs-devel
BuildRequires:	glib2-devel >= 1:2.30.2
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libjpeg-devel
%{?with_braille:BuildRequires:	liblouis-devel}
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	openldap-devel
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	pkgconfig >= 1:0.20
# just for cpp/poppler-version.h
BuildRequires:	poppler-cpp-devel >= 0.19
BuildRequires:	poppler-devel >= 0.19
# /usr/bin/pdftops, for features detection
BuildRequires:	poppler-progs >= 0.19
BuildRequires:	qpdf-devel >= 8.3.0
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	zlib-devel
# DejaVuSans.ttf (testing font for test scripts)
#BuildRequires:	fonts-TTF-DejaVu
Requires:	%{name}-libs = %{version}-%{release}
# pstopdf
Requires:	bc
Requires:	cups >= 1:1.6.0
Requires:	fontconfig >= 2.0.0
Requires:	ghostscript
Requires:	grep
Requires:	mupdf
Requires:	poppler >= 0.19
Requires:	poppler-progs >= 0.19
Requires:	qpdf-libs >= 8.3.0
Requires:	sed
Suggests:	fonts-TTF-freefont
Provides:	cups-filter-foomatic
Provides:	ghostscript-cups = 9.08
Obsoletes:	cups-filter-foomatic
Obsoletes:	foomatic-filters
Obsoletes:	ghostscript-cups < 9.08
Conflicts:	cups-backend-hp < 3.13.11-2
Conflicts:	hplip-ppd < 3.13.11-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cups_serverbin		%(/usr/bin/cups-config --serverbin)

%description
Contains backends, filters, and other software that was once part of
the core CUPS distribution but is no longer maintained by Apple Inc.
In addition it contains additional filters developed independently of
Apple, especially filters for the PDF-centric printing workflow
introduced by OpenPrinting.

%description -l pl.UTF-8
Ten pakiet zawiera backendy, filtry i inne oprogramowanie, będące
kiedyś częścią CUPS-a, ale nie utrzymywane już przez firmę Apple Inc.
Dodatkowo pakiet zawiera dodatkowe filtry stworzone niezależnie od
Apple'a, w szczególności filtry dla PDF-ocentrycznego obiegu
drukowania wprowadzonego przez OpenPrinting.

%package braille
Summary:	OpenPrinting CUPS filters for Braille embossers
Summary(pl.UTF-8):	Filtry CUPS-a z projektu OpenPrinting dla drukarek Braille'a
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}

%description braille
OpenPrinting CUPS filters for Braille embossers.

%description braille -l pl.UTF-8
Filtry CUPS-a z projektu OpenPrinting dla drukarek Braille'a.

%package libs
Summary:	OpenPrinting CUPS filters and backends - cupsfilters and fontembed libraries
Summary(pl.UTF-8):	Filtry i backendy CUPS-a z projektu OpenPrinting - biblioteki cupsfilters i fontembed
# LGPLv2: libcupsfilters
# MIT:    libfontembed
License:	LGPL v2, MIT
Group:		Libraries
Requires:	cups-lib >= 1:1.6.0

%description libs
This package provides cupsfilters and fontembed libraries.

%description libs -l pl.UTF-8
Ten pakiet udostępnia biblioteki cupsfilters i fontembed.

%package devel
Summary:	OpenPrinting CUPS filters and backends - development environment
Summary(pl.UTF-8):	Filtry i backendy CUPS-a z projektu OpenPrinting - środowisko programistyczne
License:	LGPL v2, MIT
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	cups-devel >= 1:1.6.0
Requires:	libjpeg-devel
Requires:	libpng-devel
Requires:	libtiff-devel

%description devel
This is the development package for OpenPrinting CUPS filters and
backends.

%description devel -l pl.UTF-8
To jest pakiet programistyczny dla filtrów i backendów CUPS-a z
projektu OpenPrinting.

%package static
Summary:	OpenPrinting CUPS filters and backends - static cupsfilters and fontembed libraries
Summary(pl.UTF-8):	Filtry i backendy CUPS-a z projektu OpenPrinting - statyczne biblioteki cupsfilters i fontembed
License:	LGPL v2, MIT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package provides static cupsfilters and fontembed libraries.

%description static -l pl.UTF-8
Ten pakiet udostępnia statyczne biblioteki cupsfilters i fontembed.

%package -n cups-browsed
Summary:	A daemon for browsing the Bonjour broadcasts of shared, remote CUPS printers
Summary(pl.UTF-8):	Demon do przeglądania broadcastów Bonjour współdzielonych, zdalnych drukarek CUPS
Group:		Applications/Printing
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units
Requires:	glib2 >= 1:2.30.2
Requires:	systemd-units >= 38

%description -n cups-browsed
A daemon for browsing the Bonjour broadcasts of shared, remote CUPS
printers.

%description -n cups-browsed -l pl.UTF-8
Demon do przeglądania broadcastów Bonjour współdzielonych, zdalnych
drukarek CUPS.

%package -n cups-backend-parallel
Summary:	Parallel port backend for CUPS
Summary(pl.UTF-8):	Backend CUPS-a obsługujący porty równoległe
# must be larger than cups.spec before 1.6.0
Epoch:		2
License:	GPL v2 + OpenSSL exception
Group:		Applications/Printing
Requires:	cups >= 1:1.6.0

%description -n cups-backend-parallel
This package allow CUPS printing on printers connected by parallel
ports.

%description -n cups-backend-parallel -l pl.UTF-8
Ten pakiet umożliwia drukowanie z poziomu CUPS-a na drukarkach
podłączonych do portów równoległych.

%package -n cups-backend-serial
Summary:	Serial port backend for CUPS
Summary(pl.UTF-8):	Backend CUPS-a obsługujący porty szeregowe
# must be larger than cups.spec before 1.6.0
Epoch:		2
License:	GPL v2 + OpenSSL exception
Group:		Applications/Printing
Requires:	cups >= 1:1.6.0

%description -n cups-backend-serial
This package allow CUPS printing on printers connected by serial
ports.

%description -n cups-backend-serial -l pl.UTF-8
Ten pakiet umożliwia drukowanie z poziomu CUPS-a na drukarkach
podłączonych do portów szeregowych.

%package -n perl-cups
Summary:	Perl module for CUPS
Summary(pl.UTF-8):	Moduł Perla CUPS
# must be larger than cups.spec before 1.6.0
Epoch:		2
License:	GPL v2 + OpenSSL exception
Group:		Development/Languages/Perl
Requires:	cups-lib >= 1:1.6.0

%description -n perl-cups
Perl module for Common Unix Printing System.

%description -n perl-cups -l pl.UTF-8
Moduł Perla do ogólnego systemu druku dla Uniksa.

%package -n %{php_name}-cups
Summary:	PHP module for CUPS
Summary(pl.UTF-8):	Moduł PHP CUPS
# must be larger than cups.spec before 1.6.0
Epoch:		2
License:	GPL v2 + OpenSSL exception
Group:		Development/Languages/PHP
Requires:	cups-lib >= 1:1.6.0
%{?requires_php_extension}

%description -n %{php_name}-cups
PHP module for Common Unix Printing System.

%description -n %{php_name}-cups -l pl.UTF-8
Moduł PHP do ogólnego systemu druku dla Uniksa.

# CREATE ANY NEW PACKAGES BEFORE cups-backend-* (EPOCH)

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	%{!?with_braille:--disable-braille} \
	--enable-dbus \
	--enable-ijs \
	--enable-opvp \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{?with_php:--with-php} \
	--with-pdftops=hybrid \
	--with-rcdir=/etc/rc.d/init.d \
	--with-rclevels= \
	--with-mutool-path=/usr/bin/mutool \
	--with-test-font-path=/usr/share/fonts/TTF/DejaVuSans.ttf

%{__make}

%if %{with perl}
cd scripting/perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor \
	OPTIMIZE="%{rpmcflags}"

%{__make}
cd ../..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with php}
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/phpcups.ini << 'EOF'
; Enable phpcups extension module
extension=libphpcups.so
EOF
# dlopened module
%{__rm} $RPM_BUILD_ROOT%{php_extensiondir}/libphpcups.la
%endif

%if %{with perl}
%{__make} -C scripting/perl install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

install -p utils/cups-browsed.service $RPM_BUILD_ROOT%{systemdunitdir}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/cups-filters
# Not sure what is this good for.
%{__rm} $RPM_BUILD_ROOT%{_bindir}/ttfread

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post -n cups-browsed
if [ "$1" = "1" ]; then
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
/sbin/chkconfig --add cups-browsed
%service cups-browsed restart
%systemd_post cups-browsed.service

%preun -n cups-browsed
if [ "$1" = "0" ]; then
	%service cups-browsed stop
	/sbin/chkconfig --del cups-browsed
fi
%systemd_preun cups-browsed.service

%postun -n cups-browsed
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fonts/conf.d/99pdftoopvp.conf
%attr(755,root,root) %{_bindir}/driverless
%attr(755,root,root) %{_bindir}/foomatic-rip
%attr(755,root,root) %{_cups_serverbin}/backend/beh
%attr(755,root,root) %{_cups_serverbin}/backend/cups-brf
%attr(755,root,root) %{_cups_serverbin}/backend/driverless
%attr(755,root,root) %{_cups_serverbin}/driver/driverless
%attr(755,root,root) %{_cups_serverbin}/filter/bannertopdf
%attr(755,root,root) %{_cups_serverbin}/filter/brftopagedbrf
%attr(755,root,root) %{_cups_serverbin}/filter/cgmtopdf
%attr(755,root,root) %{_cups_serverbin}/filter/cmxtopdf
%attr(755,root,root) %{_cups_serverbin}/filter/commandtoescpx
%attr(755,root,root) %{_cups_serverbin}/filter/commandtopclx
%attr(755,root,root) %{_cups_serverbin}/filter/emftopdf
%attr(755,root,root) %{_cups_serverbin}/filter/foomatic-rip
%attr(755,root,root) %{_cups_serverbin}/filter/gstopdf
%attr(755,root,root) %{_cups_serverbin}/filter/gstopxl
%attr(755,root,root) %{_cups_serverbin}/filter/gstoraster
%attr(755,root,root) %{_cups_serverbin}/filter/imagetopdf
%attr(755,root,root) %{_cups_serverbin}/filter/imagetops
%attr(755,root,root) %{_cups_serverbin}/filter/imagetoraster
%attr(755,root,root) %{_cups_serverbin}/filter/mupdftoraster
%attr(755,root,root) %{_cups_serverbin}/filter/musicxmltobrf
%attr(755,root,root) %{_cups_serverbin}/filter/pdftoijs
%attr(755,root,root) %{_cups_serverbin}/filter/pdftoopvp
%attr(755,root,root) %{_cups_serverbin}/filter/pdftopdf
%attr(755,root,root) %{_cups_serverbin}/filter/pdftops
%attr(755,root,root) %{_cups_serverbin}/filter/pdftoraster
%attr(755,root,root) %{_cups_serverbin}/filter/rastertoescpx
%attr(755,root,root) %{_cups_serverbin}/filter/rastertopclm
%attr(755,root,root) %{_cups_serverbin}/filter/rastertopclx
%attr(755,root,root) %{_cups_serverbin}/filter/rastertopdf
%attr(755,root,root) %{_cups_serverbin}/filter/rastertops
%attr(755,root,root) %{_cups_serverbin}/filter/svgtopdf
%attr(755,root,root) %{_cups_serverbin}/filter/sys5ippprinter
%attr(755,root,root) %{_cups_serverbin}/filter/texttopdf
%attr(755,root,root) %{_cups_serverbin}/filter/texttops
%attr(755,root,root) %{_cups_serverbin}/filter/texttotext
%attr(755,root,root) %{_cups_serverbin}/filter/vectortobrf
%attr(755,root,root) %{_cups_serverbin}/filter/vectortopdf
%attr(755,root,root) %{_cups_serverbin}/filter/vectortoubrl
%attr(755,root,root) %{_cups_serverbin}/filter/wmftopdf
%attr(755,root,root) %{_cups_serverbin}/filter/xfigtopdf
%{_datadir}/cups/banners/*
%{_datadir}/cups/charsets
%{_datadir}/cups/data/classified.pdf
%{_datadir}/cups/data/confidential.pdf
%{_datadir}/cups/data/default.pdf
%{_datadir}/cups/data/default-testpage.pdf
%{_datadir}/cups/data/form_english.pdf
%{_datadir}/cups/data/form_english_in.odt
%{_datadir}/cups/data/form_russian.pdf
%{_datadir}/cups/data/form_russian_in.odt
%{_datadir}/cups/data/secret.pdf
%{_datadir}/cups/data/standard.pdf
%{_datadir}/cups/data/topsecret.pdf
%{_datadir}/cups/data/unclassified.pdf
%{_datadir}/cups/data/testprint
%{_datadir}/cups/drv/cupsfilters.drv
%{_datadir}/cups/drv/generic-ubrl.drv
%{_datadir}/cups/mime/cupsfilters.types
%{_datadir}/cups/mime/cupsfilters.convs
%{_datadir}/cups/mime/cupsfilters-ghostscript.convs
%{_datadir}/cups/mime/cupsfilters-mupdf.convs
%{_datadir}/cups/mime/cupsfilters-poppler.convs
# definitions for drivers; pcl.h is used by cupsfilters.drv
%{_datadir}/cups/ppdc/escp.h
%{_datadir}/cups/ppdc/pcl.h
%{_datadir}/ppd/cupsfilters
%{_mandir}/man1/driverless.1*
%{_mandir}/man1/foomatic-rip.1*

%if %{with braille}
%files braille
%defattr(644,root,root,755)
%attr(755,root,root) %{_cups_serverbin}/filter/brftoembosser
%attr(755,root,root) %{_cups_serverbin}/filter/imagetobrf
%attr(755,root,root) %{_cups_serverbin}/filter/imagetoubrl
%attr(755,root,root) %{_cups_serverbin}/filter/imageubrltoindexv3
%attr(755,root,root) %{_cups_serverbin}/filter/imageubrltoindexv4
%attr(755,root,root) %{_cups_serverbin}/filter/textbrftoindexv3
%attr(755,root,root) %{_cups_serverbin}/filter/textbrftoindexv4
%attr(755,root,root) %{_cups_serverbin}/filter/texttobrf
%dir %{_datadir}/cups/braille
%attr(755,root,root) %{_datadir}/cups/braille/cups-braille.sh
%attr(755,root,root) %{_datadir}/cups/braille/index.sh
%attr(755,root,root) %{_datadir}/cups/braille/indexv3.sh
%attr(755,root,root) %{_datadir}/cups/braille/indexv4.sh
%{_datadir}/cups/drv/generic-brf.drv
%{_datadir}/cups/drv/indexv3.drv
%{_datadir}/cups/drv/indexv4.drv
%{_datadir}/cups/mime/braille.convs
%{_datadir}/cups/mime/braille.types
%{_datadir}/cups/ppdc/braille.defs
%{_datadir}/cups/ppdc/fr-braille.po
%{_datadir}/cups/ppdc/imagemagick.defs
%{_datadir}/cups/ppdc/index.defs
%{_datadir}/cups/ppdc/liblouis.defs
%{_datadir}/cups/ppdc/liblouis1.defs
%{_datadir}/cups/ppdc/liblouis2.defs
%{_datadir}/cups/ppdc/liblouis3.defs
%{_datadir}/cups/ppdc/liblouis4.defs
%{_datadir}/cups/ppdc/media-braille.defs
%endif

%files libs
%defattr(644,root,root,755)
%doc fontembed/README
%attr(755,root,root) %{_libdir}/libcupsfilters.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcupsfilters.so.1
%attr(755,root,root) %{_libdir}/libfontembed.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfontembed.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcupsfilters.so
%attr(755,root,root) %{_libdir}/libfontembed.so
%{_includedir}/cupsfilters
%{_includedir}/fontembed
%{_pkgconfigdir}/libcupsfilters.pc
%{_pkgconfigdir}/libfontembed.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcupsfilters.a
%{_libdir}/libfontembed.a

%files -n cups-browsed
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cups/cups-browsed.conf
%attr(755,root,root) %{_sbindir}/cups-browsed
%attr(755,root,root) %{_cups_serverbin}/backend/implicitclass
%attr(754,root,root) /etc/rc.d/init.d/cups-browsed
%{systemdunitdir}/cups-browsed.service
%{_mandir}/man5/cups-browsed.conf.5*
%{_mandir}/man8/cups-browsed.8*

%files -n cups-backend-parallel
%defattr(644,root,root,755)
%attr(755,root,root) %{_cups_serverbin}/backend/parallel

%files -n cups-backend-serial
%defattr(644,root,root,755)
%attr(755,root,root) %{_cups_serverbin}/backend/serial

%if %{with perl}
%files -n perl-cups
%defattr(644,root,root,755)
%doc scripting/perl/README
%{perl_vendorarch}/CUPS.pm
%dir %{perl_vendorarch}/auto/CUPS
%{perl_vendorarch}/auto/CUPS/autosplit.ix
%attr(755,root,root) %{perl_vendorarch}/auto/CUPS/CUPS.so
%{_mandir}/man3/CUPS.3pm*
%endif

%if %{with php}
%files -n %{php_name}-cups
%defattr(644,root,root,755)
%doc scripting/php/README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/phpcups.ini
%attr(755,root,root) %{php_extensiondir}/libphpcups.so
%endif
