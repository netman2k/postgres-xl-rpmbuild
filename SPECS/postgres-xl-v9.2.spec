# This spec file and ancilliary files are licensed in accordance with The 
# PostgreSQL license. 
# and others listed  
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:  
# rpm --define 'packagename 1' .... to force the package to build.
# rpm  --define 'packagename 0' .... to force the package NOT to build.
# The base package , the lib package, the devel package, and the server package always get built.

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?kerbdir:%define kerbdir "/usr"}

# This is a macro to be used with find_lang and other stuff
%define majorversion 9.2
%define pgmajorversion 9.2
%define packageversion 92 
%define oname postgres-xl
%define	pgxlbaseinstdir	/usr/postgres-xl-%{majorversion}

%{!?test:%define test 0}
%{!?plpython:%define plpython 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?ssl:%define ssl 1}
%{!?intdatetimes:%define intdatetimes 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?disablepgfts:%define disablepgfts 0}
%{!?runselftest:%define runselftest 0}
%{!?uuid:%define uuid 1}
%{!?ldap:%define ldap 1}
%{!?selinux:%define selinux 0}

Summary:	Postgres-XL client programs and libraries
Name:		%{oname}%{packageversion}
Version:	9.2
#Release:	1PGDG%{?dist}
Release:	34.1
License:	PostgreSQL
Group:		Applications/Databases
Url:		http://www.postgres-xl.org/ 

Source0:   	pgxl-v9.2.tar.gz	
Source4:	Makefile.regress
Source5:	pg_config.h
Source6:	README.rpm-dist
Source7:	ecpg_config.h
Source9:	pgxl-9.2-libs.conf
Source12:	postgresql-9.2-A4.pdf 
#http://www.postgres-xl.org/docs/pdf/%{oname}-%{majorversion}-A4.pdf
Source14:	pgxl.pam
Source16:	filter-requires-perl-Pg.sh
Source17:	pgxl%{packageversion}-setup
Source18:	pgxl-%{majorversion}.service

Patch1:		rpm-pgsql.patch
Patch3:		pgxl-logging.patch
Patch6:		pgxl-perl-rpath.patch

Buildrequires:	perl glibc-devel bison flex >= 2.5.31
Requires:	/sbin/ldconfig 

%if %plperl
BuildRequires:	perl-ExtUtils-Embed
BuildRequires:	perl(ExtUtils::MakeMaker) 
%endif

%if %plpython
BuildRequires:	python-devel
%endif

%if %pltcl
BuildRequires:	tcl-devel
%endif

BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4

%if %ssl
BuildRequires:	openssl-devel
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %uuid
BuildRequires:	uuid-devel
%endif

%if %ldap
BuildRequires:	openldap-devel
%endif

%if %selinux
BuildRequires: libselinux >= 2.0.93
BuildRequires: selinux-policy >= 3.9.13
%endif

Requires:	%{name}-libs = %{version}-%{release}
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

#BuildRequires:	systemd-units

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Postgres-XL is an advanced Object-Relational database management system (DBMS).
The base Postgres-XL package contains the client programs that you'll need to
access a Postgres-XL DBMS server, as well as HTML documentation for the whole
system.  These client programs can be located on the same machine as the
Postgres-XL server, or on a remote machine that accesses a Postgres-XL server
over a network connection.  The Postgres-XL server can be found in the
postgres-xl-server sub-package.

If you want to manipulate a Postgres-XL database on a local or remote Postgres-XL
server, you need this package. You also need to install this package
if you're installing the pgxl10-server package.

%package libs
Summary:	The shared libraries required for any Postgres-XL clients
Group:		Applications/Databases
Provides:	libpq.so

%description libs
The pgxl10-libs package provides the essential shared libraries for any
Postgres-XL client program or interface. You will need to install this package
to use any other Postgres-XL package or any clients that need to connect to a
Postgres-XL server.

%package server
Summary:	The programs needed to create and run a Postgres-XL server
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):	/usr/sbin/useradd
# pre/post stuff needs systemd too
##Requires(post):		systemd-units
##Requires(preun):	systemd-units
##Requires(postun):	systemd-units

Requires:	%{name} = %{version}-%{release}

%description server
Postgres-XL is an advanced Object-Relational database management system (DBMS).
The pgxl10-server package contains the programs needed to create
and run a Postgres-XL server, which will in turn allow you to create
and maintain Postgres-XL databases.

%package docs
Summary:	Extra documentation for Postgres-XL
Group:		Applications/Databases

%description docs
The pgxl10-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the Postgres-XL documentation
project, or if you want to generate printed documentation. This package also 
includes HTML version of the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with Postgres-XL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description contrib
The postgres-xl-contrib package contains various extension modules that are
included in the Postgres-XL distribution.

%package devel
Summary:	Postgres-XL development header files and libraries
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The pgxl10-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a Postgres-XL database management server.  It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you want
to develop applications which will interact with a Postgres-XL server.

%package gtm
Summary:	Global Transaction Manager for Postgres-XL
Group:		Applications/Databases
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description gtm
The pgxl10-gtm package contains gtm binaries.

%if %plperl
%package plperl
Summary:	The Perl procedural language for Postgres-XL
Group:		Applications/Databases
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%ifarch ppc ppc64
BuildRequires:	perl-devel
%endif
Obsoletes:	pgxl10-pl

%description plperl
The pgxl10-plperl package contains the PL/Perl procedural language,
which is an extension to the Postgres-XL database server.
Install this if you want to write database functions in Perl.

%endif

%if %plpython
%package plpython
Summary:	The Python procedural language for Postgres-XL
Group:		Applications/Databases
Requires: 	%{name}%{?_isa} = %{version}-%{release}
Requires: 	%{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-pl

%description plpython
The pgxl10-plpython package contains the PL/Python procedural language,
which is an extension to the Postgres-XL database server.
Install this if you want to write database functions in Python.

%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for Postgres-XL
Group:		Applications/Databases
Requires:	%{name}-%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-pl

%description pltcl
Postgres-XL is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.
%endif

%if %test
%package test
Summary:	The test suite distributed with Postgres-XL
Group:		Applications/Databases
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description test
The Postgres-XL-test package contains files needed for various tests for the
Postgres-XL database management system, including regression tests and
benchmarks.
%endif

%define __perl_requires %{SOURCE16}

%prep
%setup -q -n postgres-xl
%patch1 -p1
%patch3 -p1
# patch5 is applied later
%patch6 -p1

cp -p %{SOURCE12} .

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
        if [ x"`id -u`" = x0 ]; then
               	echo "postgresql's regression tests fail if run as root."
                echo "If you really need to build the RPM as root, use"
                echo "--define='runselftest 0' to skip the regression tests."
                exit 1
        fi
%endif

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS

# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
# Add LINUX_OOM_ADJ=0 to ensure child processes reset postmaster's oom_adj
CFLAGS="$CFLAGS -DLINUX_OOM_ADJ=0"

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

# Use --as-needed to eliminate unnecessary link dependencies.
# Hopefully upstream will do this for itself in some future release.
LDFLAGS="-Wl,--as-needed"; export LDFLAGS

export LIBNAME=%{_lib}
./configure --enable-rpath \
	--prefix=%{pgxlbaseinstdir} \
	--includedir=%{pgxlbaseinstdir}/include \
	--mandir=%{pgxlbaseinstdir}/share/man \
	--datadir=%{pgxlbaseinstdir}/share \
	--libdir=%{pgxlbaseinstdir}/lib/ \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython
	--with-python \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5 \
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if !%intdatetimes
	--disable-integer-datetimes \
%endif
%if %disablepgfts
	--disable-thread-safety \
%endif
%if %uuid
	--with-ossp-uuid \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
%if %selinux
	--with-selinux
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgxl \
	--docdir=%{_docdir}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %uuid
make %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgxlbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

%if %runselftest
	pushd src/test/regress
	make all
	cp ../../../contrib/spi/refint.so .
	cp ../../../contrib/spi/autoinc.so .
	make MAX_CONNECTIONS=5 check
	make clean
	popd
	pushd src/pl
	make MAX_CONNECTIONS=5 check
	popd
	pushd contrib
	make MAX_CONNECTIONS=5 check
	popd
%endif

%if %test
	pushd src/test/regress
	make all
	popd
%endif

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{pgxlbaseinstdir}/share/extension/
make -C contrib DESTDIR=%{buildroot} install
%if %uuid
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		mv %{buildroot}%{pgxlbaseinstdir}/include/pg_config.h %{buildroot}%{pgxlbaseinstdir}/include/pg_config_`uname -i`.h
		install -m 644 %{SOURCE5} %{buildroot}%{pgxlbaseinstdir}/include/
		#mv %{buildroot}%{pgxlbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgxlbaseinstdir}/include/server/pg_config_`uname -i`.h
		#install -m 644 %{SOURCE5} %{buildroot}%{pgxlbaseinstdir}/include/server/
		mv %{buildroot}%{pgxlbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgxlbaseinstdir}/include/ecpg_config_`uname -i`.h
		install -m 644 %{SOURCE7} %{buildroot}%{pgxlbaseinstdir}/include/
		;;
	*)
	;;
esac

# prep the setup script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{version}|' \
        -e 's|^PGENGINE=.*$|PGENGINE=/usr/pgxl-%{majorversion}/bin|' \
        <%{SOURCE17} >pgxl%{packageversion}-setup
install -m 755 pgxl%{packageversion}-setup %{buildroot}%{pgxlbaseinstdir}/bin/pgxl%{packageversion}-setup

install -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/pgxl-%{majorversion}.service

%if %pam
install -d %{buildroot}/etc/pam.d
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/pgxl%{packageversion}
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgxl/%{majorversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgxl/%{majorversion}/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgxl/%{majorversion}

# Install a file under /etc/ld.so.conf.d, so libs can be detected easily.
install -d -m 755 %{buildroot}/etc/ld.so.conf.d/
install -m 700 %{SOURCE9} %{buildroot}/etc/ld.so.conf.d/

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness.  We replace the original
	# Makefiles, however.
	mkdir -p %{buildroot}%{pgxlbaseinstdir}/lib/test
	cp -a src/test/regress %{buildroot}%{pgxlbaseinstdir}/lib/test
	install -m 0755 contrib/spi/refint.so %{buildroot}%{pgxlbaseinstdir}/lib/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}%{pgxlbaseinstdir}/lib/test/regress
	pushd  %{buildroot}%{pgxlbaseinstdir}/lib/test/regress
	strip *.so
	rm -f GNUmakefile Makefile *.o
	chmod 0755 pg_regress regress.so
	popd
	cp %{SOURCE4} %{buildroot}%{pgxlbaseinstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{pgxlbaseinstdir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mkdir -p %{buildroot}%{pgxlbaseinstdir}/share/doc/html
mv doc-xc/src/sgml/html doc
mkdir -p %{buildroot}%{pgxlbaseinstdir}/share/man/
mv doc-xc/src/sgml/man1 doc-xc/src/sgml/man3 doc-xc/src/sgml/man7  %{buildroot}%{pgxlbaseinstdir}/share/man/
rm -rf %{buildroot}%{_docdir}/pgxl

# Temp measure for some lib files. This needs to be fixed upstream: 
#mv %{buildroot}%{pgxlbaseinstdir}/lib/pgxl/* %{buildroot}%{pgxlbaseinstdir}/lib/
###mv %{buildroot}%{pgxlbaseinstdir}/lib/pgxl/* %{buildroot}%{pgxlbaseinstdir}/lib/

# initialize file lists
cp /dev/null main.lst
cp /dev/null libs.lst
cp /dev/null server.lst
cp /dev/null devel.lst
cp /dev/null plperl.lst
cp /dev/null pltcl.lst
cp /dev/null plpython.lst

# initialize file lists
cp /dev/null main.lst
cp /dev/null libs.lst
cp /dev/null server.lst
cp /dev/null devel.lst
cp /dev/null plperl.lst
cp /dev/null pltcl.lst
cp /dev/null plpython.lst

%if %nls
%find_lang ecpg-%{pgmajorversion}
%find_lang ecpglib6-%{pgmajorversion}
%find_lang initdb-%{pgmajorversion}
%find_lang libpq5-%{pgmajorversion}
%find_lang pg_basebackup-%{pgmajorversion}
%find_lang pg_config-%{pgmajorversion}
%find_lang pg_controldata-%{pgmajorversion}
%find_lang pg_ctl-%{pgmajorversion}
%find_lang pg_dump-%{pgmajorversion}
%find_lang pg_resetxlog-%{pgmajorversion}
%find_lang pgscripts-%{pgmajorversion}
%if %plperl
%find_lang plperl-%{pgmajorversion}
cat plperl-%{pgmajorversion}.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%{pgmajorversion}
%if %plpython
%find_lang plpython-%{pgmajorversion}
cat plpython-%{pgmajorversion}.lang > pg_plpython.lst
%endif
%if %pltcl
%find_lang pltcl-%{pgmajorversion}
cat pltcl-%{pgmajorversion}.lang > pg_pltcl.lst
%endif
%find_lang postgres-%{pgmajorversion}
%find_lang psql-%{pgmajorversion}
%endif

cat libpq5-%{pgmajorversion}.lang > pg_libpq5.lst
cat pg_config-%{pgmajorversion}.lang ecpg-%{pgmajorversion}.lang ecpglib6-%{pgmajorversion}.lang > pg_devel.lst
cat initdb-%{pgmajorversion}.lang pg_ctl-%{pgmajorversion}.lang psql-%{pgmajorversion}.lang pg_dump-%{pgmajorversion}.lang pg_basebackup-%{pgmajorversion}.lang pgscripts-%{pgmajorversion}.lang > pg_main.lst
cat postgres-%{pgmajorversion}.lang pg_resetxlog-%{pgmajorversion}.lang pg_controldata-%{pgmajorversion}.lang plpgsql-%{pgmajorversion}.lang > pg_server.lst

%post libs -p /sbin/ldconfig 
%postun libs -p /sbin/ldconfig 

%pre server
groupadd -r pgxl >/dev/null 2>&1 || :
useradd -m -g pgxl -r -s /bin/bash \
        -c "pgxl Server" pgxl >/dev/null 2>&1 || :

%post server
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
# pgxl' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgxl/1.0/data
export PGDATA" >  /var/lib/pgxl/.bash_profile
chown pgxl: /var/lib/pgxl/.bash_profile

##%preun server
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable pgxl-1.0.service >/dev/null 2>&1 || :
	/bin/systemctl stop pgxl-1.0.service >/dev/null 2>&1 || :
fi

%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart pgxl-1.0.service >/dev/null 2>&1 || :
fi
###########################################################################################################
##%preun server
##if [ $1 = 0 ] ; then
##	/sbin/service postgresql-xl condstop >/dev/null 2>&1
##	chkconfig --del postgresql-xl
##fi

##%postun server
##/sbin/ldconfig 
##if [ $1 -ge 1 ]; then
##  /sbin/service postgresql-xl condrestart >/dev/null 2>&1
##fi
##############################################################################################
%if %plperl
%post 	-p /sbin/ldconfig	plperl
%postun	-p /sbin/ldconfig 	plperl
%endif

%if %plpython
%post 	-p /sbin/ldconfig	plpython
%postun	-p /sbin/ldconfig 	plpython
%endif

%if %pltcl
%post 	-p /sbin/ldconfig	pltcl
%postun	-p /sbin/ldconfig 	pltcl
%endif

%if %test
%post test
chown -R pgxl:pgxl /usr/share/pgxl/test >/dev/null 2>&1 || :
%endif

# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install /usr/bin/psql pgxl-psql %{pgxlbaseinstdir}/bin/psql 100
%{_sbindir}/update-alternatives --install /usr/bin/clusterdb  pgxl-clusterdb  %{pgxlbaseinstdir}/bin/clusterdb 100
%{_sbindir}/update-alternatives --install /usr/bin/createdb   pgxl-createdb   %{pgxlbaseinstdir}/bin/createdb 100
%{_sbindir}/update-alternatives --install /usr/bin/createlang pgxl-createlang %{pgxlbaseinstdir}/bin/createlang 100
%{_sbindir}/update-alternatives --install /usr/bin/createuser pgxl-createuser %{pgxlbaseinstdir}/bin/createuser 100
%{_sbindir}/update-alternatives --install /usr/bin/dropdb     pgxl-dropdb     %{pgxlbaseinstdir}/bin/dropdb 100
%{_sbindir}/update-alternatives --install /usr/bin/droplang   pgxl-droplang   %{pgxlbaseinstdir}/bin/droplang 100
%{_sbindir}/update-alternatives --install /usr/bin/dropuser   pgxl-dropuser   %{pgxlbaseinstdir}/bin/dropuser 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_dump    pgxl-pg_dump    %{pgxlbaseinstdir}/bin/pg_dump 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_dumpall pgxl-pg_dumpall %{pgxlbaseinstdir}/bin/pg_dumpall 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_restore pgxl-pg_restore %{pgxlbaseinstdir}/bin/pg_restore 100
%{_sbindir}/update-alternatives --install /usr/bin/reindexdb  pgxl-reindexdb  %{pgxlbaseinstdir}/bin/reindexdb 100
%{_sbindir}/update-alternatives --install /usr/bin/vacuumdb   pgxl-vacuumdb   %{pgxlbaseinstdir}/bin/vacuumdb 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/clusterdb.1  pgxl-clusterdbman     %{pgxlbaseinstdir}/share/man/man1/clusterdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createdb.1   pgxl-createdbman	  %{pgxlbaseinstdir}/share/man/man1/createdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createlang.1 pgxl-createlangman    %{pgxlbaseinstdir}/share/man/man1/createlang.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createuser.1 pgxl-createuserman    %{pgxlbaseinstdir}/share/man/man1/createuser.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropdb.1     pgxl-dropdbman        %{pgxlbaseinstdir}/share/man/man1/dropdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/droplang.1   pgxl-droplangman	  %{pgxlbaseinstdir}/share/man/man1/droplang.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropuser.1   pgxl-dropuserman	  %{pgxlbaseinstdir}/share/man/man1/dropuser.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dump.1    pgxl-pg_dumpman	  %{pgxlbaseinstdir}/share/man/man1/pg_dump.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dumpall.1 pgxl-pg_dumpallman    %{pgxlbaseinstdir}/share/man/man1/pg_dumpall.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_restore.1 pgxl-pg_restoreman    %{pgxlbaseinstdir}/share/man/man1/pg_restore.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/psql.1	   pgxl-psqlman          %{pgxlbaseinstdir}/share/man/man1/psql.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/reindexdb.1  pgxl-reindexdbman     %{pgxlbaseinstdir}/share/man/man1/reindexdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/vacuumdb.1   pgxl-vacuumdbman	  %{pgxlbaseinstdir}/share/man/man1/vacuumdb.1 100

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
        # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pgxl-psql		%{pgxlbaseinstdir}/bin/psql
	%{_sbindir}/update-alternatives --remove pgxl-clusterdb	%{pgxlbaseinstdir}/bin/clusterdb
	%{_sbindir}/update-alternatives --remove pgxl-clusterdbman	%{pgxlbaseinstdir}/share/man/man1/clusterdb.1
	%{_sbindir}/update-alternatives --remove pgxl-createdb		%{pgxlbaseinstdir}/bin/createdb
	%{_sbindir}/update-alternatives --remove pgxl-createdbman	%{pgxlbaseinstdir}/share/man/man1/createdb.1
	%{_sbindir}/update-alternatives --remove pgxl-createlang	%{pgxlbaseinstdir}/bin/createlang
	%{_sbindir}/update-alternatives --remove pgxl-createlangman	%{pgxlbaseinstdir}/share/man/man1/createlang.1
	%{_sbindir}/update-alternatives --remove pgxl-createuser	%{pgxlbaseinstdir}/bin/createuser
	%{_sbindir}/update-alternatives --remove pgxl-createuserman	%{pgxlbaseinstdir}/share/man/man1/createuser.1
	%{_sbindir}/update-alternatives --remove pgxl-dropdb		%{pgxlbaseinstdir}/bin/dropdb
	%{_sbindir}/update-alternatives --remove pgxl-dropdbman	%{pgxlbaseinstdir}/share/man/man1/dropdb.1
	%{_sbindir}/update-alternatives --remove pgxl-droplang		%{pgxlbaseinstdir}/bin/droplang
	%{_sbindir}/update-alternatives --remove pgxl-droplangman	%{pgxlbaseinstdir}/share/man/man1/droplang.1
	%{_sbindir}/update-alternatives --remove pgxl-dropuser		%{pgxlbaseinstdir}/bin/dropuser
	%{_sbindir}/update-alternatives --remove pgxl-dropuserman	%{pgxlbaseinstdir}/share/man/man1/dropuser.1
	%{_sbindir}/update-alternatives --remove pgxl-pg_dump		%{pgxlbaseinstdir}/bin/pg_dump
	%{_sbindir}/update-alternatives --remove pgxl-pg_dumpall	%{pgxlbaseinstdir}/bin/pg_dumpall
	%{_sbindir}/update-alternatives --remove pgxl-pg_dumpallman	%{pgxlbaseinstdir}/share/man/man1/pg_dumpall.1
	%{_sbindir}/update-alternatives --remove pgxl-pg_dumpman	%{pgxlbaseinstdir}/share/man/man1/pg_dump.1
	%{_sbindir}/update-alternatives --remove pgxl-pg_restore	%{pgxlbaseinstdir}/bin/pg_restore
	%{_sbindir}/update-alternatives --remove pgxl-pg_restoreman	%{pgxlbaseinstdir}/share/man/man1/pg_restore.1
	%{_sbindir}/update-alternatives --remove pgxl-psqlman		%{pgxlbaseinstdir}/share/man/man1/psql.1
	%{_sbindir}/update-alternatives --remove pgxl-reindexdb	%{pgxlbaseinstdir}/bin/reindexdb
	%{_sbindir}/update-alternatives --remove pgxl-reindexdbman	%{pgxlbaseinstdir}/share/man/man1/reindexdb.1
	%{_sbindir}/update-alternatives --remove pgxl-vacuumdb		%{pgxlbaseinstdir}/bin/vacuumdb
	%{_sbindir}/update-alternatives --remove pgxl-vacuumdbman	%{pgxlbaseinstdir}/share/man/man1/vacuumdb.1
fi

%clean
rm -rf %{buildroot}

# FILES section.

%files -f pg_main.lst
%defattr(-,pgxl,pgxl)
#%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT doc/bug.template
%doc README.rpm-dist
%{pgxlbaseinstdir}/bin/clusterdb
%{pgxlbaseinstdir}/bin/createdb
%{pgxlbaseinstdir}/bin/createlang
%{pgxlbaseinstdir}/bin/createuser
%{pgxlbaseinstdir}/bin/dropdb
%{pgxlbaseinstdir}/bin/droplang
%{pgxlbaseinstdir}/bin/dropuser
%{pgxlbaseinstdir}/bin/makesgml
%{pgxlbaseinstdir}/bin/pg_basebackup
%{pgxlbaseinstdir}/bin/pg_config
%{pgxlbaseinstdir}/bin/pg_dump
%{pgxlbaseinstdir}/bin/pg_dumpall
%{pgxlbaseinstdir}/bin/pg_restore
%{pgxlbaseinstdir}/bin/pg_test_fsync
%{pgxlbaseinstdir}/bin/psql
%{pgxlbaseinstdir}/bin/reindexdb
%{pgxlbaseinstdir}/bin/vacuumdb
%{pgxlbaseinstdir}/share/man/man1/clusterdb.*
%{pgxlbaseinstdir}/share/man/man1/createdb.*
%{pgxlbaseinstdir}/share/man/man1/createlang.*
%{pgxlbaseinstdir}/share/man/man1/createuser.*
%{pgxlbaseinstdir}/share/man/man1/dropdb.*
%{pgxlbaseinstdir}/share/man/man1/droplang.*
%{pgxlbaseinstdir}/share/man/man1/dropuser.*
%{pgxlbaseinstdir}/share/man/man1/pg_basebackup.*
%{pgxlbaseinstdir}/share/man/man1/pg_config.*
%{pgxlbaseinstdir}/share/man/man1/pg_dump.*
%{pgxlbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgxlbaseinstdir}/share/man/man1/pg_restore.*
%{pgxlbaseinstdir}/share/man/man1/psql.*
%{pgxlbaseinstdir}/share/man/man1/reindexdb.*
%{pgxlbaseinstdir}/share/man/man1/vacuumdb.*
%{pgxlbaseinstdir}/share/man/man3/*
%{pgxlbaseinstdir}/share/man/man7/*

%files docs
#%defattr(-,root,root)
%defattr(-,pgxl,pgxl)
%doc doc-xc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
#%defattr(-,root,root)
%defattr(-,pgxl,pgxl)
%{pgxlbaseinstdir}/lib/_int.so
%{pgxlbaseinstdir}/lib/adminpack.so
%{pgxlbaseinstdir}/lib/auth_delay.so
%{pgxlbaseinstdir}/lib/autoinc.so
%{pgxlbaseinstdir}/lib/auto_explain.so
%{pgxlbaseinstdir}/lib/btree_gin.so
%{pgxlbaseinstdir}/lib/btree_gist.so
%{pgxlbaseinstdir}/lib/chkpass.so
%{pgxlbaseinstdir}/lib/citext.so
%{pgxlbaseinstdir}/lib/cube.so
%{pgxlbaseinstdir}/lib/dblink.so
%{pgxlbaseinstdir}/lib/dummy_seclabel.so
%{pgxlbaseinstdir}/lib/earthdistance.so
%{pgxlbaseinstdir}/lib/file_fdw.so*
%{pgxlbaseinstdir}/lib/fuzzystrmatch.so
%{pgxlbaseinstdir}/lib/insert_username.so
%{pgxlbaseinstdir}/lib/isn.so
%{pgxlbaseinstdir}/lib/hstore.so
%{pgxlbaseinstdir}/lib/passwordcheck.so
%{pgxlbaseinstdir}/lib/pg_freespacemap.so
%{pgxlbaseinstdir}/lib/pg_stat_statements.so
%{pgxlbaseinstdir}/lib/pgrowlocks.so
%{pgxlbaseinstdir}/lib/sslinfo.so
%{pgxlbaseinstdir}/lib/lo.so
%{pgxlbaseinstdir}/lib/ltree.so
%{pgxlbaseinstdir}/lib/moddatetime.so
%{pgxlbaseinstdir}/lib/pageinspect.so
%{pgxlbaseinstdir}/lib/pgcrypto.so
%{pgxlbaseinstdir}/lib/pgstattuple.so
%{pgxlbaseinstdir}/lib/pg_buffercache.so
%{pgxlbaseinstdir}/lib/pg_trgm.so
%{pgxlbaseinstdir}/lib/pg_upgrade_support.so
%{pgxlbaseinstdir}/lib/refint.so
%{pgxlbaseinstdir}/lib/seg.so
%{pgxlbaseinstdir}/lib/tablefunc.so
%{pgxlbaseinstdir}/lib/timetravel.so
%{pgxlbaseinstdir}/lib/unaccent.so
%if %xml
%{pgxlbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgxlbaseinstdir}/lib/uuid-ossp.so
%endif
#%{pgxlbaseinstdir}/share/pgxc/extension/
%{pgxlbaseinstdir}/share/extension/
%{pgxlbaseinstdir}/bin/oid2name
%{pgxlbaseinstdir}/bin/pgbench
%{pgxlbaseinstdir}/bin/pgxc_clean
%{pgxlbaseinstdir}/bin/vacuumlo
%{pgxlbaseinstdir}/bin/pg_archivecleanup
%{pgxlbaseinstdir}/bin/pg_standby
%{pgxlbaseinstdir}/bin/pg_upgrade

%files libs -f pg_libpq5.lst
#%defattr(-,root,root)
%defattr(-,pgxl,pgxl)
%{pgxlbaseinstdir}/lib/libpq.so.*
%{pgxlbaseinstdir}/lib/libecpg.so*
%{pgxlbaseinstdir}/lib/libpgtypes.so.*
%{pgxlbaseinstdir}/lib/libecpg_compat.so.*
%{pgxlbaseinstdir}/lib/libpqwalreceiver.so

%config(noreplace) %{_sysconfdir}/ld.so.conf.d/pgxl-%{majorversion}-libs.conf

%files server -f pg_server.lst
%defattr(-,pgxl,pgxl)
#%defattr(-,root,root)
#%{_unitdir}/pgxl-%{majorversion}.service
%{pgxlbaseinstdir}/bin/pgxl%{packageversion}-setup
%if %pam
%config(noreplace) /etc/pam.d/pgxl%{packageversion}
%endif
#%attr (755,root,root) %dir /etc/sysconfig/pgxl
%attr (755,pgxl,pgxl) %dir /etc/sysconfig/pgxl
%{pgxlbaseinstdir}/bin/initdb
%{pgxlbaseinstdir}/bin/pg_controldata
%{pgxlbaseinstdir}/bin/pg_ctl
%{pgxlbaseinstdir}/bin/pg_resetxlog
%{pgxlbaseinstdir}/bin/postgres
%{pgxlbaseinstdir}/bin/postmaster
%{pgxlbaseinstdir}/bin/pgxc_ctl
%{pgxlbaseinstdir}/bin/pg_receivexlog
%{pgxlbaseinstdir}/bin/pg_test_timing
%{pgxlbaseinstdir}/share/storm_catalog.sql
%{pgxlbaseinstdir}/share/man/man1/initdb.*
%{pgxlbaseinstdir}/share/man/man1/pg_controldata.*
%{pgxlbaseinstdir}/share/man/man1/pg_ctl.*
%{pgxlbaseinstdir}/share/man/man1/pg_resetxlog.*
%{pgxlbaseinstdir}/share/man/man1/postgres.*
%{pgxlbaseinstdir}/share/man/man1/postmaster.*
%{pgxlbaseinstdir}/share/postgres.bki
%{pgxlbaseinstdir}/share/postgres.description
%{pgxlbaseinstdir}/share/postgres.shdescription
%{pgxlbaseinstdir}/share/system_views.sql
%{pgxlbaseinstdir}/share/*.sample
%{pgxlbaseinstdir}/share/timezonesets/*
%{pgxlbaseinstdir}/share/tsearch_data/*.affix
%{pgxlbaseinstdir}/share/tsearch_data/*.dict
%{pgxlbaseinstdir}/share/tsearch_data/*.ths
%{pgxlbaseinstdir}/share/tsearch_data/*.rules
%{pgxlbaseinstdir}/share/tsearch_data/*.stop
%{pgxlbaseinstdir}/share/tsearch_data/*.syn
%{pgxlbaseinstdir}/lib/dict_int.so
%{pgxlbaseinstdir}/lib/dict_snowball.so
%{pgxlbaseinstdir}/lib/dict_xsyn.so
%{pgxlbaseinstdir}/lib/euc2004_sjis2004.so
%{pgxlbaseinstdir}/lib/plpgsql.so
%dir %{pgxlbaseinstdir}/share/extension
%{pgxlbaseinstdir}/share/extension/plpgsql*
%{pgxlbaseinstdir}/lib/test_parser.so
%{pgxlbaseinstdir}/lib/tsearch2.so

%dir %{pgxlbaseinstdir}/lib
%dir %{pgxlbaseinstdir}/share
%attr(700,pgxl,pgxl) %dir /var/lib/pgxl
%attr(700,pgxl,pgxl) %dir /var/lib/pgxl/%{majorversion}
%attr(700,pgxl,pgxl) %dir /var/lib/pgxl/%{majorversion}/data
%attr(700,pgxl,pgxl) %dir /var/lib/pgxl/%{majorversion}/backups
#%attr(644,pgxl,pgxl) %config(noreplace) /var/lib/pgxl/.bash_profile
%{pgxlbaseinstdir}/lib/*_and_*.so
%{pgxlbaseinstdir}/share/conversion_create.sql
%{pgxlbaseinstdir}/share/information_schema.sql
%{pgxlbaseinstdir}/share/snowball_create.sql
%{pgxlbaseinstdir}/share/sql_features.txt

%files devel -f pg_devel.lst
#%defattr(-,root,root)
%defattr(-,pgxl,pgxl)
%{pgxlbaseinstdir}/include/*
%{pgxlbaseinstdir}/bin/ecpg
###%{pgxlbaseinstdir}/lib/libpq.so
###%{pgxlbaseinstdir}/lib/libecpg.so
###%{pgxlbaseinstdir}/lib/libpq.a
###%{pgxlbaseinstdir}/lib/libecpg.a
###%{pgxlbaseinstdir}/lib/libecpg_compat.so
###%{pgxlbaseinstdir}/lib/libecpg_compat.a
###%{pgxlbaseinstdir}/lib/libpgport.a
###%{pgxlbaseinstdir}/lib/libpgtypes.so
###%{pgxlbaseinstdir}/lib/libpgtypes.a
################################################################%{pgxlbaseinstdir}/lib/pgxl/*
%{pgxlbaseinstdir}/lib/*
%{pgxlbaseinstdir}/share/man/man1/ecpg.*

%files gtm -f pg_devel.lst
#%defattr(-,root,root)
%defattr(-,pgxl,pgxl)
%{pgxlbaseinstdir}/bin/gtm
%{pgxlbaseinstdir}/bin/gtm_ctl
%{pgxlbaseinstdir}/bin/gtm_proxy
%{pgxlbaseinstdir}/bin/initgtm
%{pgxlbaseinstdir}/share/man/man1/gtm.1
%{pgxlbaseinstdir}/share/man/man1/gtm_ctl.1
%{pgxlbaseinstdir}/share/man/man1/gtm_proxy.1
%{pgxlbaseinstdir}/share/man/man1/initgtm.1

%if %plperl
%files plperl -f pg_plperl.lst
#%defattr(-,root,root)
%defattr(-,pgxl,pgxl)
%{pgxlbaseinstdir}/lib/plperl.so
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst

%defattr(-,pgxl,pgxl)
#%defattr(-,root,root)
%{pgxlbaseinstdir}/lib/pltcl.so
%{pgxlbaseinstdir}/bin/pltcl_delmod
%{pgxlbaseinstdir}/bin/pltcl_listmod
%{pgxlbaseinstdir}/bin/pltcl_loadmod
%{pgxlbaseinstdir}/share/unknown.pltcl
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,pgxl,pgxl)
#%defattr(-,root,root)
%{pgxlbaseinstdir}/lib/plpython*.so
%endif

%if %test
%files test
%defattr(-,pgxl,pgxl)
#%defattr(-,pgxl,pgxl)
%attr(-,pgxl,pgxl) %{pgxlbaseinstdir}/lib/test/*
%attr(-,pgxl,pgxl) %dir %{pgxlbaseinstdir}/lib/test
%endif

%changelog
* Fri May 19 2013 ViVek Raghuwanshi <vivek.r@stormdb.com> - 1.0.2-1PGDG
- Updated to 1.0.2

* Wed Sep 5 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.1-1PGDG
- Update to 1.0.1

* Mon Sep 03 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-2PGDG
- Remove useless ldconfig call from -server subpackage.

* Mon Aug 13 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial cut for 1.0.0
