Summary:	OpenPrinting CUPS filters and backends
Summary(pl.UTF-8):	Filtry i backendy CUPS-a z projektu OpenPrinting
Name:		cups-filters
Version:	2.0.1
Release:	2
License:	Apache v2.0
Group:		Applications/Printing
#Source0:	https://www.openprinting.org/download/cups-filters/%{name}-%{version}.tar.xz
Source0:	https://github.com/OpenPrinting/cups-filters/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	b40d0f135af414666e1c3917983a1bb3
URL:		http://www.linuxfoundation.org/collaborate/workgroups/openprinting/cups-filters
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	cups-devel >= 1:1.6.0
BuildRequires:	gettext-tools >= 0.18.3
BuildRequires:	libcupsfilters-devel
BuildRequires:	libppd-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	cups >= 1:1.6.0
Requires:	ghostscript
Requires:	mupdf
Suggests:	fonts-TTF-freefont
Provides:	cups-filter-foomatic
Provides:	ghostscript-cups = 9.08
Obsoletes:	cups-filter-foomatic
Obsoletes:	foomatic-filters
Obsoletes:	ghostscript-cups < 9.08
Obsoletes:	cups-filters-braille < 2.0.1
Obsoletes:	perl-cups < 2.0.1
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

%package -n cups-backend-parallel
Summary:	Parallel port backend for CUPS
Summary(pl.UTF-8):	Backend CUPS-a obsługujący porty równoległe
# must be larger than cups.spec before 1.6.0
Epoch:		2
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
Group:		Applications/Printing
Requires:	cups >= 1:1.6.0

%description -n cups-backend-serial
This package allow CUPS printing on printers connected by serial
ports.

%description -n cups-backend-serial -l pl.UTF-8
Ten pakiet umożliwia drukowanie z poziomu CUPS-a na drukarkach
podłączonych do portów szeregowych.

# CREATE ANY NEW PACKAGES BEFORE cups-backend-* (EPOCH)

%prep
%setup -q

%build

%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-gs-path=/usr/bin/gs \
	--with-ippfind-path=/usr/bin/ippfind \
	--with-mutool-path=/usr/bin/mutool

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/cups-filters

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md
%attr(755,root,root) %{_bindir}/driverless
%attr(755,root,root) %{_bindir}/driverless-fax
%attr(755,root,root) %{_bindir}/foomatic-rip
%attr(700,root,root) %{_cups_serverbin}/backend/beh
%attr(700,root,root) %{_cups_serverbin}/backend/driverless
%attr(700,root,root) %{_cups_serverbin}/backend/driverless-fax
%attr(755,root,root) %{_cups_serverbin}/driver/driverless
%attr(755,root,root) %{_cups_serverbin}/driver/driverless-fax
%attr(755,root,root) %{_cups_serverbin}/filter/bannertopdf
%attr(755,root,root) %{_cups_serverbin}/filter/commandtoescpx
%attr(755,root,root) %{_cups_serverbin}/filter/commandtopclx
%attr(755,root,root) %{_cups_serverbin}/filter/foomatic-rip
%attr(755,root,root) %{_cups_serverbin}/filter/gstopdf
%attr(755,root,root) %{_cups_serverbin}/filter/gstopxl
%attr(755,root,root) %{_cups_serverbin}/filter/gstoraster
%attr(755,root,root) %{_cups_serverbin}/filter/imagetopdf
%attr(755,root,root) %{_cups_serverbin}/filter/imagetops
%attr(755,root,root) %{_cups_serverbin}/filter/imagetoraster
%attr(755,root,root) %{_cups_serverbin}/filter/mupdftopwg
%attr(755,root,root) %{_cups_serverbin}/filter/pclmtoraster
%attr(755,root,root) %{_cups_serverbin}/filter/pdftopdf
%attr(755,root,root) %{_cups_serverbin}/filter/pdftops
%attr(755,root,root) %{_cups_serverbin}/filter/pdftoraster
%attr(755,root,root) %{_cups_serverbin}/filter/pwgtopclm
%attr(755,root,root) %{_cups_serverbin}/filter/pwgtopdf
%attr(755,root,root) %{_cups_serverbin}/filter/pwgtoraster
%attr(755,root,root) %{_cups_serverbin}/filter/rastertoescpx
%attr(755,root,root) %{_cups_serverbin}/filter/rastertopclx
%attr(755,root,root) %{_cups_serverbin}/filter/rastertops
%attr(755,root,root) %{_cups_serverbin}/filter/texttopdf
%attr(755,root,root) %{_cups_serverbin}/filter/texttops
%attr(755,root,root) %{_cups_serverbin}/filter/texttotext
%attr(755,root,root) %{_cups_serverbin}/filter/universal
%{_datadir}/cups/drv/cupsfilters.drv
%{_datadir}/cups/mime/cupsfilters.convs
%{_datadir}/cups/mime/cupsfilters.types
%{_datadir}/cups/mime/cupsfilters-universal.convs
%{_datadir}/cups/mime/cupsfilters-universal-postscript.convs
%{_datadir}/ppdc/escp.h
%{_datadir}/ppdc/pcl.h
%{_datadir}/ppd/cupsfilters
%{_mandir}/man1/driverless.1*
%{_mandir}/man1/foomatic-rip.1*

%files -n cups-backend-parallel
%defattr(644,root,root,755)
%attr(700,root,root) %{_cups_serverbin}/backend/parallel

%files -n cups-backend-serial
%defattr(644,root,root,755)
%attr(700,root,root) %{_cups_serverbin}/backend/serial
