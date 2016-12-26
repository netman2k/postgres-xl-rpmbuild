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
%define majorversion 9.5
%define releaseversion r1.4
%define pgmajorversion 9.5
%define packageversion 95 
%define oname postgres-xl
%define pgbaseinstdir /usr/postgres-xl-%{majorversion}

%{!?disablepgfts:%global disablepgfts 0}
%{!?intdatetimes:%global intdatetimes 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?nls:%global nls 1}
%{!?pam:%global pam 1}
%{!?plpython:%global plpython 1}
%{!?pltcl:%global pltcl 1}
%{!?plperl:%global plperl 1}
%{!?ssl:%global ssl 1}
%{!?test:%global test 1}
%{!?runselftest:%global runselftest 0}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?systemd_enabled:%global systemd_enabled 0}
%{!?sdt:%global sdt 0}
%{!?selinux:%global selinux 0}
%else
%{!?systemd_enabled:%global systemd_enabled 1}
%{!?sdt:%global sdt 1}
%{!?selinux:%global selinux 1}
%endif
%if 0%{?fedora} > 23
%global _hardened_build 1
%endif

Summary:  Postgres-XL client programs and libraries
Name:   %{oname}%{packageversion}
Version:  9.5
#Release: 1PGDG%{?dist}
Release:  1.4%{?dist}
License:  PostgreSQL
Group:    Applications/Databases
Url:      http://www.postgres-xl.org/ 

Source0:  postgres-xl-9.5r1.4.tar.gz
Source4:  Makefile.regress
Source5:  pg_config.h
Source6:  README.rpm-dist
Source7:  ecpg_config.h
Source9:  pgxl-%{majorversion}-libs.conf
Source12: http://www.postgresql.org/files/documentation/pdf/%{majorversion}/postgresql-%{majorversion}-A4.pdf
Source14: pgxl.pam
Source16: filter-requires-perl-Pg.sh
Source17: pgxl%{packageversion}-setup
Source18: pgxl-%{majorversion}.service

Patch1:   rpm-pgsql.patch
Patch3:   pgxl-logging.patch
Patch6:   pgxl-perl-rpath.patch

Buildrequires:  perl glibc-devel bison flex >= 2.5.31
Requires: /sbin/ldconfig 

%if %plperl
BuildRequires:  perl-ExtUtils-Embed
BuildRequires:  perl(ExtUtils::MakeMaker) 
%endif

%if %plpython
BuildRequires:  python-devel
%endif

%if %pltcl
BuildRequires:  tcl-devel
%endif

BuildRequires:  readline-devel
BuildRequires:  zlib-devel >= 1.0.4

%if %ssl
BuildRequires:  openssl-devel
%endif

%if %kerberos
BuildRequires:  krb5-devel
BuildRequires:  e2fsprogs-devel
%endif

%if %nls
BuildRequires:  gettext >= 0.10.35
%endif

%if %xml
BuildRequires:  libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:  pam-devel
%endif

%if %uuid
BuildRequires:  libuuid-devel
%endif

%if %ldap
BuildRequires:  openldap-devel
%endif

%if %selinux
BuildRequires: libselinux >= 2.0.93
BuildRequires: selinux-policy >= 3.9.13
%endif

%if %{systemd_enabled}
BuildRequires:          systemd
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:               systemd
Requires(post):         systemd-sysv
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd
%else
Requires(post):         chkconfig
Requires(preun):        chkconfig
# This is for /sbin/service
Requires(preun):        initscripts
Requires(postun):       initscripts
%endif

Requires: %{name}-libs = %{version}-%{release}

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

#BuildRequires: systemd-units

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
if you're installing the pgxl%{packageversion}-server package.

%package libs
Summary:        The shared libraries required for any Postgres-XL clients
Group:          Applications/Databases
Provides:       postgres-xl-libs

%description libs
The pgxl%{packageversion}-libs package provides the essential shared libraries for any
Postgres-XL client program or interface. You will need to install this package
to use any other Postgres-XL package or any clients that need to connect to a
Postgres-XL server.

%package server
Summary:  The programs needed to create and run a Postgres-XL server
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires(pre):  /usr/sbin/useradd, /usr/sbin/groupadd
# for /sbin/ldconfig
Requires(post):         glibc
Requires(postun):       glibc
%if %{systemd_enabled}
# pre/post stuff needs systemd too
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%else
Requires: /usr/sbin/useradd /sbin/chkconfig
%endif
Requires: %{name} = %{version}-%{release}
Provides: postgres-xl-server

%description server
Postgres-XL is an advanced Object-Relational database management system (DBMS).
The pgxl%{majorversion}-server package contains the programs needed to create
and run a Postgres-XL server, which will in turn allow you to create
and maintain Postgres-XL databases.

%package docs
Summary:  Extra documentation for Postgres-XL
Group:    Applications/Databases
Provides: postgres-xl-docs

%description docs
The pgxl%{majorversion}-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the Postgres-XL documentation
project, or if you want to generate printed documentation. This package also 
includes HTML version of the documentation.

%package contrib
Summary:  Contributed source and binaries distributed with Postgres-XL
Group:    Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: postgres-xl-contrib

%description contrib
The postgres-xl-contrib package contains various extension modules that are
included in the Postgres-XL distribution.

%package devel
Summary:  Postgres-XL development header files and libraries
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: postgres-xl-devel

%description devel
The pgxl%{majorversion}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a Postgres-XL database management server.  It also contains the ecpg
Embedded C Postgres preprocessor. You need to install this package if you want
to develop applications which will interact with a Postgres-XL server.

%package gtm
Summary:  Global Transaction Manager for Postgres-XL
Group:    Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: postgres-xl-gtm

%description gtm
The pgxl%{majorversion}-gtm package contains gtm binaries.

%if %plperl
%package plperl
Summary:        The Perl procedural language for Postgres-XL
Group:          Applications/Databases
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%ifarch ppc ppc64
BuildRequires:  perl-devel
%endif
Obsoletes:      postgres-xl%{packageversion}-pl
Provides:       postgres-xl-plperl

%description plperl
The pgxl%{majorversion}-plperl package contains the PL/Perl procedural language,
which is an extension to the Postgres-XL database server.
Install this if you want to write database functions in Perl.

%endif

%if %plpython
%package plpython
Summary:    The Python procedural language for Postgres-XL
Group:      Applications/Databases
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:  %{name}-pl
Provides:   postgres-xl-plpython

%description plpython
The pgxl%{majorversion}-plpython package contains the PL/Python procedural language,
which is an extension to the Postgres-XL database server.
Install this if you want to write database functions in Python.

%endif

%if %pltcl
%package pltcl
Summary:    The Tcl procedural language for Postgres-XL
Group:      Applications/Databases
Requires:   %{name}-%{?_isa} = %{version}-%{release}
Requires:   %{name}-server%{?_isa} = %{version}-%{release}
Obsoletes:  %{name}-pl
Provides:   postgres-xl-pltcl

%description pltcl
Postgres-XL is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.
%endif

%if %test
%package test
Summary:    The test suite distributed with Postgres-XL
Group:      Applications/Databases
Requires:   %{name}-server%{?_isa} = %{version}-%{release}
Requires:   %{name}-devel%{?_isa} = %{version}-%{release}
Provides:   postgres-xl-test

%description test
The Postgres-XL-test package contains files needed for various tests for the
Postgres-XL database management system, including regression tests and
benchmarks.
%endif

%define __perl_requires %{SOURCE16}

%prep
#%setup -q -n postgres-xl
#%setup -q -n postgres-xl-%{majorversion}%{releaseversion}
%setup -q -n %{oname}-%{majorversion}%{releaseversion}
#%patch1 -p1
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
  --prefix=%{pgbaseinstdir} \
  --includedir=%{pgbaseinstdir}/include \
  --mandir=%{pgbaseinstdir}/share/man \
  --datadir=%{pgbaseinstdir}/share \
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
  --with-gssapi \
  --with-includes=%{kerbdir}/include \
  --with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
  --enable-nls \
%endif
%if %sdt
        --enable-dtrace \
%endif
%if !%intdatetimes
  --disable-integer-datetimes \
%endif
%if %disablepgfts
  --disable-thread-safety \
%endif
%if %uuid
  --with-uuid=e2fs \
%endif
%if %xml
  --with-libxml \
  --with-libxslt \
%endif
%if %ldap
  --with-ldap \
%endif
%if %selinux
  --with-selinux \
%endif
  --with-system-tzdata=%{_datadir}/zoneinfo \
  --sysconfdir=/etc/sysconfig/pgsql \
  --docdir=%{pgbaseinstdir}/doc \
  --htmldir=%{pgbaseinstdir}/doc/html

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %uuid
make %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
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

mkdir -p %{buildroot}%{pgbaseinstdir}/share/extension/
make -C contrib DESTDIR=%{buildroot} install

#mv %{buildroot}%{pgbaseinstdir}/doc/extension/*.example %{buildroot}%{pgbaseinstdir}/share/extension/

%if %uuid
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
  i386 | x86_64 | ppc | ppc64 | s390 | s390x)
    %{__mv} %{buildroot}%{pgbaseinstdir}/include/pg_config.h %{buildroot}%{pgbaseinstdir}/include/pg_config_`uname -i`.h
    install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/
    %{__mv}  %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgbaseinstdir}/include/server/pg_config_`uname -i`.h
    install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/server/
    %{__mv} %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgbaseinstdir}/include/ecpg_config_`uname -i`.h
    install -m 644 %{SOURCE7} %{buildroot}%{pgbaseinstdir}/include/
    ;;
  *)
  ;;
esac

# prep the setup script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{version}|' \
        -e 's|^PGENGINE=.*$|PGENGINE=/usr/pgxl-%{majorversion}/bin|' \
        <%{SOURCE17} >pgxl%{packageversion}-setup
install -m 755 pgxl%{packageversion}-setup %{buildroot}%{pgbaseinstdir}/bin/pgxl%{packageversion}-setup

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
  mkdir -p %{buildroot}%{pgbaseinstdir}/lib/test
  cp -a src/test/regress %{buildroot}%{pgbaseinstdir}/lib/test
  install -m 0755 contrib/spi/refint.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
  install -m 0755 contrib/spi/autoinc.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
  pushd  %{buildroot}%{pgbaseinstdir}/lib/test/regress
  strip *.so
  rm -f GNUmakefile Makefile *.o
  chmod 0755 pg_regress regress.so
  popd
  # clean up binary
  rm src/test/regress/pg_regress

  cp %{SOURCE4} %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
  chmod 0644 %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mkdir -p %{buildroot}%{pgbaseinstdir}/share/doc/html
mv doc/src/sgml/html doc
mkdir -p %{buildroot}%{pgbaseinstdir}/share/man/
mv doc/src/sgml/man{1,3,7}  %{buildroot}%{pgbaseinstdir}/share/man/
rm -rf %{buildroot}%{_docdir}/pgxl

# Temp measure for some lib files. This needs to be fixed upstream: 
#mv %{buildroot}%{pgbaseinstdir}/lib/pgxl/* %{buildroot}%{pgbaseinstdir}/lib/
###mv %{buildroot}%{pgbaseinstdir}/lib/pgxl/* %{buildroot}%{pgbaseinstdir}/lib/

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
%find_lang pg_rewind-%{majorversion}
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

#%post libs -p /sbin/ldconfig 
#%postun libs -p /sbin/ldconfig 

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgxl -s /bin/bash \
        -c "Postgres-XL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %systemd_post pgxl-%{majorversion}.service
   %tmpfiles_create
fi
# pgxl' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgxl/%{majorversion}/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgxl/.pgxl_profile ] && source /var/lib/pgxl/.pgxl_profile" >  /var/lib/pgxl/.bash_profile
chown postgres: /var/lib/pgxl/.bash_profile
chmod 700 /var/lib/pgxl/.bash_profile

##%preun server
if [ $1 -eq 0 ] ; then
  # Package removal, not upgrade
  /bin/systemctl --no-reload disable pgxl-%{majorversion}.service >/dev/null 2>&1 || :
  /bin/systemctl stop pgxl-%{majorversion}.service >/dev/null 2>&1 || :
fi

%postun server
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
  # Package upgrade, not uninstall
  /bin/systemctl try-restart pgxl-%{majorversion}.service >/dev/null 2>&1 || :
fi

%if %plperl
%post   -p /sbin/ldconfig   plperl
%postun -p /sbin/ldconfig   plperl
%endif

%if %plpython
%post   -p /sbin/ldconfig   plpython
%postun -p /sbin/ldconfig   plpython
%endif

%if %pltcl
%post   -p /sbin/ldconfig   pltcl
%postun -p /sbin/ldconfig   pltcl
%endif


# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install /usr/bin/psql pgxl-psql %{pgbaseinstdir}/bin/psql 100
%{_sbindir}/update-alternatives --install /usr/bin/clusterdb  pgxl-clusterdb  %{pgbaseinstdir}/bin/clusterdb 100
%{_sbindir}/update-alternatives --install /usr/bin/createdb   pgxl-createdb   %{pgbaseinstdir}/bin/createdb 100
%{_sbindir}/update-alternatives --install /usr/bin/createlang pgxl-createlang %{pgbaseinstdir}/bin/createlang 100
%{_sbindir}/update-alternatives --install /usr/bin/createuser pgxl-createuser %{pgbaseinstdir}/bin/createuser 100
%{_sbindir}/update-alternatives --install /usr/bin/dropdb     pgxl-dropdb     %{pgbaseinstdir}/bin/dropdb 100
%{_sbindir}/update-alternatives --install /usr/bin/droplang   pgxl-droplang   %{pgbaseinstdir}/bin/droplang 100
%{_sbindir}/update-alternatives --install /usr/bin/dropuser   pgxl-dropuser   %{pgbaseinstdir}/bin/dropuser 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_basebackup pgxl_basebackup  %{pgbaseinstdir}/bin/pg_basebackup 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_basebackupman pgxl_basebackupman  %{pgbaseinstdir}/share/man/man1/pg_basebackup.1 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_dump    pgxl-pg_dump    %{pgbaseinstdir}/bin/pg_dump 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_dumpall pgxl-pg_dumpall %{pgbaseinstdir}/bin/pg_dumpall 100
%{_sbindir}/update-alternatives --install /usr/bin/pg_restore pgxl-pg_restore %{pgbaseinstdir}/bin/pg_restore 100
%{_sbindir}/update-alternatives --install /usr/bin/reindexdb  pgxl-reindexdb  %{pgbaseinstdir}/bin/reindexdb 100
%{_sbindir}/update-alternatives --install /usr/bin/vacuumdb   pgxl-vacuumdb   %{pgbaseinstdir}/bin/vacuumdb 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/clusterdb.1  pgxl-clusterdbman     %{pgbaseinstdir}/share/man/man1/clusterdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createdb.1   pgxl-createdbman   %{pgbaseinstdir}/share/man/man1/createdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createlang.1 pgxl-createlangman    %{pgbaseinstdir}/share/man/man1/createlang.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createuser.1 pgxl-createuserman    %{pgbaseinstdir}/share/man/man1/createuser.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropdb.1     pgxl-dropdbman        %{pgbaseinstdir}/share/man/man1/dropdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/droplang.1   pgxl-droplangman   %{pgbaseinstdir}/share/man/man1/droplang.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropuser.1   pgxl-dropuserman   %{pgbaseinstdir}/share/man/man1/dropuser.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dump.1    pgxl-pg_dumpman    %{pgbaseinstdir}/share/man/man1/pg_dump.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dumpall.1 pgxl-pg_dumpallman    %{pgbaseinstdir}/share/man/man1/pg_dumpall.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_restore.1 pgxl-pg_restoreman    %{pgbaseinstdir}/share/man/man1/pg_restore.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/psql.1     pgxl-psqlman          %{pgbaseinstdir}/share/man/man1/psql.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/reindexdb.1  pgxl-reindexdbman     %{pgbaseinstdir}/share/man/man1/reindexdb.1 100
%{_sbindir}/update-alternatives --install /usr/share/man/man1/vacuumdb.1   pgxl-vacuumdbman   %{pgbaseinstdir}/share/man/man1/vacuumdb.1 100

%post libs
#%{_sbindir}/update-alternatives --install /etc/ld.so.conf.d/pgxl-libs.conf   pgxl-ld-conf   %{pgbaseinstdir}/share/pgxl-%{majorversion}-libs.conf %{packageversion}0
/sbin/ldconfig

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
    # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
    %{_sbindir}/update-alternatives --remove pgxl-psql              %{pgbaseinstdir}/bin/psql
    %{_sbindir}/update-alternatives --remove pgxl-clusterdb         %{pgbaseinstdir}/bin/clusterdb
    %{_sbindir}/update-alternatives --remove pgxl-clusterdbman      %{pgbaseinstdir}/share/man/man1/clusterdb.1
    %{_sbindir}/update-alternatives --remove pgxl-createdb          %{pgbaseinstdir}/bin/createdb
    %{_sbindir}/update-alternatives --remove pgxl-createdbman       %{pgbaseinstdir}/share/man/man1/createdb.1
    %{_sbindir}/update-alternatives --remove pgxl-createlang        %{pgbaseinstdir}/bin/createlang
    %{_sbindir}/update-alternatives --remove pgxl-createlangman     %{pgbaseinstdir}/share/man/man1/createlang.1
    %{_sbindir}/update-alternatives --remove pgxl-createuser        %{pgbaseinstdir}/bin/createuser
    %{_sbindir}/update-alternatives --remove pgxl-createuserman     %{pgbaseinstdir}/share/man/man1/createuser.1
    %{_sbindir}/update-alternatives --remove pgxl-dropdb            %{pgbaseinstdir}/bin/dropdb
    %{_sbindir}/update-alternatives --remove pgxl-dropdbman         %{pgbaseinstdir}/share/man/man1/dropdb.1
    %{_sbindir}/update-alternatives --remove pgxl-droplang          %{pgbaseinstdir}/bin/droplang
    %{_sbindir}/update-alternatives --remove pgxl-droplangman       %{pgbaseinstdir}/share/man/man1/droplang.1
    %{_sbindir}/update-alternatives --remove pgxl-dropuser          %{pgbaseinstdir}/bin/dropuser
    %{_sbindir}/update-alternatives --remove pgxl-dropuserman       %{pgbaseinstdir}/share/man/man1/dropuser.1
    %{_sbindir}/update-alternatives --remove pgxl-pg_basebackup     %{pgbaseinstdir}/bin/pg_basebackup
    %{_sbindir}/update-alternatives --remove pgxl-pg_basebackupman  %{pgbaseinstdir}/bin/pg_basebackupman
    %{_sbindir}/update-alternatives --remove pgxl-pg_dump           %{pgbaseinstdir}/bin/pg_dump
    %{_sbindir}/update-alternatives --remove pgxl-pg_dumpall        %{pgbaseinstdir}/bin/pg_dumpall
    %{_sbindir}/update-alternatives --remove pgxl-pg_dumpallman     %{pgbaseinstdir}/share/man/man1/pg_dumpall.1
    %{_sbindir}/update-alternatives --remove pgxl-pg_dumpman        %{pgbaseinstdir}/share/man/man1/pg_dump.1
    %{_sbindir}/update-alternatives --remove pgxl-pg_restore        %{pgbaseinstdir}/bin/pg_restore
    %{_sbindir}/update-alternatives --remove pgxl-pg_restoreman     %{pgbaseinstdir}/share/man/man1/pg_restore.1
    %{_sbindir}/update-alternatives --remove pgxl-psqlman           %{pgbaseinstdir}/share/man/man1/psql.1
    %{_sbindir}/update-alternatives --remove pgxl-reindexdb         %{pgbaseinstdir}/bin/reindexdb
    %{_sbindir}/update-alternatives --remove pgxl-reindexdbman      %{pgbaseinstdir}/share/man/man1/reindexdb.1
    %{_sbindir}/update-alternatives --remove pgxl-vacuumdb          %{pgbaseinstdir}/bin/vacuumdb
    %{_sbindir}/update-alternatives --remove pgxl-vacuumdbman       %{pgbaseinstdir}/share/man/man1/vacuumdb.1
fi

#if [ "$1" -eq 0 ];then
  rm -f /etc/ld.so.conf.d/pgxl-%{majorversion}-libs.conf
  /sbin/ldconfig
fi


%clean
rm -rf %{buildroot}

# FILES section.

%files -f pg_main.lst
#%defattr(-,pgxl,pgxl)
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT doc/bug.template
%doc README.rpm-dist
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createlang
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/droplang
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/pg_archivecleanup
%{pgbaseinstdir}/bin/pg_basebackup
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
%{pgbaseinstdir}/bin/pg_isready
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/pg_rewind
%{pgbaseinstdir}/bin/pg_test_fsync
%{pgbaseinstdir}/bin/pg_test_timing
%{pgbaseinstdir}/bin/pg_receivexlog
%{pgbaseinstdir}/bin/pg_upgrade
%{pgbaseinstdir}/bin/pg_xlogdump
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/share/man/man1/clusterdb.*
%{pgbaseinstdir}/share/man/man1/createdb.*
%{pgbaseinstdir}/share/man/man1/createlang.*
%{pgbaseinstdir}/share/man/man1/createuser.*
%{pgbaseinstdir}/share/man/man1/dropdb.*
%{pgbaseinstdir}/share/man/man1/droplang.*
%{pgbaseinstdir}/share/man/man1/dropuser.*
%{pgbaseinstdir}/share/man/man1/pgbench.1
%{pgbaseinstdir}/share/man/man1/pg_archivecleanup.1
%{pgbaseinstdir}/share/man/man1/pg_basebackup.*
%{pgbaseinstdir}/share/man/man1/pg_config.*
%{pgbaseinstdir}/share/man/man1/pg_dump.*
%{pgbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgbaseinstdir}/share/man/man1/pg_isready.1
%{pgbaseinstdir}/share/man/man1/pg_receivexlog.1
%{pgbaseinstdir}/share/man/man1/pg_restore.*
%{pgbaseinstdir}/share/man/man1/pg_rewind.1
%{pgbaseinstdir}/share/man/man1/pg_test_fsync.1
%{pgbaseinstdir}/share/man/man1/pg_test_timing.1
%{pgbaseinstdir}/share/man/man1/pg_upgrade.1
%{pgbaseinstdir}/share/man/man1/pg_xlogdump.1
%{pgbaseinstdir}/share/man/man1/psql.*
%{pgbaseinstdir}/share/man/man1/reindexdb.*
%{pgbaseinstdir}/share/man/man1/vacuumdb.*
%{pgbaseinstdir}/share/man/man3/*
%{pgbaseinstdir}/share/man/man7/*
%{pgbaseinstdir}/share/locale/de/LC_MESSAGES/pg_rewind-9.5.mo
%{pgbaseinstdir}/share/locale/es/LC_MESSAGES/pg_rewind-9.5.mo
%{pgbaseinstdir}/share/locale/fr/LC_MESSAGES/pg_rewind-9.5.mo
%{pgbaseinstdir}/share/locale/it/LC_MESSAGES/pg_rewind-9.5.mo
%{pgbaseinstdir}/share/locale/ko/LC_MESSAGES/pg_rewind-9.5.mo
%{pgbaseinstdir}/share/locale/pl/LC_MESSAGES/pg_rewind-9.5.mo
%{pgbaseinstdir}/share/locale/pt_BR/LC_MESSAGES/pg_rewind-9.5.mo
%{pgbaseinstdir}/share/locale/ru/LC_MESSAGES/pg_rewind-9.5.mo
%{pgbaseinstdir}/share/locale/zh_CN/LC_MESSAGES/pg_rewind-9.5.mo

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
%defattr(-,root,root)
%doc %{pgbaseinstdir}/doc/extension/*.example
%{pgbaseinstdir}/lib/_int.so
%{pgbaseinstdir}/lib/adminpack.so
%{pgbaseinstdir}/lib/auth_delay.so
%{pgbaseinstdir}/lib/autoinc.so
%{pgbaseinstdir}/lib/auto_explain.so
%{pgbaseinstdir}/lib/btree_gin.so
%{pgbaseinstdir}/lib/btree_gist.so
%{pgbaseinstdir}/lib/chkpass.so
%{pgbaseinstdir}/lib/citext.so
%{pgbaseinstdir}/lib/cube.so
%{pgbaseinstdir}/lib/dblink.so
%{pgbaseinstdir}/lib/earthdistance.so
%{pgbaseinstdir}/lib/file_fdw.so*
%{pgbaseinstdir}/lib/fuzzystrmatch.so
%{pgbaseinstdir}/lib/insert_username.so
%{pgbaseinstdir}/lib/isn.so
%{pgbaseinstdir}/lib/hstore.so
%if %plperl
%{pgbaseinstdir}/lib/hstore_plperl.so
%endif
%if %plpython
%{pgbaseinstdir}/lib/hstore_plpython2.so
%endif
%{pgbaseinstdir}/lib/lo.so
%{pgbaseinstdir}/lib/ltree.so
%if %plpython
%{pgbaseinstdir}/lib/ltree_plpython2.so
%endif
%{pgbaseinstdir}/lib/moddatetime.so
%{pgbaseinstdir}/lib/pageinspect.so
%{pgbaseinstdir}/lib/passwordcheck.so
%{pgbaseinstdir}/lib/pgcrypto.so
%{pgbaseinstdir}/lib/pgrowlocks.so
%{pgbaseinstdir}/lib/pgstattuple.so
%{pgbaseinstdir}/lib/pg_buffercache.so
%{pgbaseinstdir}/lib/pg_freespacemap.so
%{pgbaseinstdir}/lib/pg_prewarm.so
%{pgbaseinstdir}/lib/pg_stat_statements.so
%{pgbaseinstdir}/lib/pg_trgm.so
%{pgbaseinstdir}/lib/postgres_fdw.so
%{pgbaseinstdir}/lib/refint.so
%{pgbaseinstdir}/lib/seg.so
%{pgbaseinstdir}/lib/sslinfo.so
%if %selinux
%{pgbaseinstdir}/lib/sepgsql.so
%{pgbaseinstdir}/share/contrib/sepgsql.sql
%endif
%{pgbaseinstdir}/lib/tablefunc.so
%{pgbaseinstdir}/lib/tcn.so
%{pgbaseinstdir}/lib/test_decoding.so
%{pgbaseinstdir}/lib/timetravel.so
%{pgbaseinstdir}/lib/tsm_system_rows.so
%{pgbaseinstdir}/lib/tsm_system_time.so
%{pgbaseinstdir}/lib/unaccent.so
%if %xml
%{pgbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgbaseinstdir}/lib/uuid-ossp.so
%endif
%{pgbaseinstdir}/share/extension/adminpack*
%{pgbaseinstdir}/share/extension/autoinc*
%{pgbaseinstdir}/share/extension/btree_gin*
%{pgbaseinstdir}/share/extension/btree_gist*
%{pgbaseinstdir}/share/extension/chkpass*
%{pgbaseinstdir}/share/extension/citext*
%{pgbaseinstdir}/share/extension/cube*
%{pgbaseinstdir}/share/extension/dblink*
%{pgbaseinstdir}/share/extension/dict_int*
%{pgbaseinstdir}/share/extension/dict_xsyn*
%{pgbaseinstdir}/share/extension/earthdistance*
%{pgbaseinstdir}/share/extension/file_fdw*
%{pgbaseinstdir}/share/extension/fuzzystrmatch*
%{pgbaseinstdir}/share/extension/hstore*
%{pgbaseinstdir}/share/extension/insert_username*
%{pgbaseinstdir}/share/extension/intagg*
%{pgbaseinstdir}/share/extension/intarray*
%{pgbaseinstdir}/share/extension/isn*
%{pgbaseinstdir}/share/extension/lo*
%{pgbaseinstdir}/share/extension/ltree*
%{pgbaseinstdir}/share/extension/moddatetime*
%{pgbaseinstdir}/share/extension/pageinspect*
%{pgbaseinstdir}/share/extension/pg_buffercache*
%{pgbaseinstdir}/share/extension/pg_freespacemap*
%{pgbaseinstdir}/share/extension/pg_prewarm*
%{pgbaseinstdir}/share/extension/pg_stat_statements*
%{pgbaseinstdir}/share/extension/pg_trgm*
%{pgbaseinstdir}/share/extension/pgcrypto*
%{pgbaseinstdir}/share/extension/pgrowlocks*
%{pgbaseinstdir}/share/extension/pgstattuple*
%{pgbaseinstdir}/share/extension/postgres_fdw*
%{pgbaseinstdir}/share/extension/refint*
%{pgbaseinstdir}/share/extension/seg*
%{pgbaseinstdir}/share/extension/sslinfo*
%{pgbaseinstdir}/share/extension/tablefunc*
%{pgbaseinstdir}/share/extension/tcn*
%{pgbaseinstdir}/share/extension/timetravel*
%{pgbaseinstdir}/share/extension/tsearch2*
%{pgbaseinstdir}/share/extension/tsm_system_rows*
%{pgbaseinstdir}/share/extension/tsm_system_time*
%{pgbaseinstdir}/share/extension/unaccent*
%if %uuid
%{pgbaseinstdir}/share/extension/uuid-ossp*
%endif
%{pgbaseinstdir}/share/extension/xml2*
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/bin/pg_recvlogical
%{pgbaseinstdir}/bin/pg_standby
%{pgbaseinstdir}/share/man/man1/oid2name.1
%{pgbaseinstdir}/share/man/man1/pg_recvlogical.1
%{pgbaseinstdir}/share/man/man1/pg_standby.1
%{pgbaseinstdir}/share/man/man1/vacuumlo.1

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so.*
%{pgbaseinstdir}/lib/libecpg.so*
%{pgbaseinstdir}/lib/libpgtypes.so.*
%{pgbaseinstdir}/lib/libecpg_compat.so.*
%{pgbaseinstdir}/lib/libpqwalreceiver.so
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/pgxl-%{majorversion}-libs.conf

%files server -f pg_server.lst
%defattr(-,root,root)
%{pgbaseinstdir}/bin/pgxl%{packageversion}-setup
%{_unitdir}/pgxl-%{majorversion}.service
%if %pam
%config(noreplace) /etc/pam.d/pgxl%{packageversion}
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgxl
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_resetxlog
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/bin/postmaster
%{pgbaseinstdir}/bin/pgxc_ctl
%{pgbaseinstdir}/bin/pgxc_clean
%{pgbaseinstdir}/bin/pgxc_monitor
%{pgbaseinstdir}/share/man/man1/initdb.*
%{pgbaseinstdir}/share/man/man1/pg_controldata.*
%{pgbaseinstdir}/share/man/man1/pg_ctl.*
%{pgbaseinstdir}/share/man/man1/pg_resetxlog.*
%{pgbaseinstdir}/share/man/man1/postgres.*
%{pgbaseinstdir}/share/man/man1/postmaster.*
%{pgbaseinstdir}/share/postgres.bki
%{pgbaseinstdir}/share/postgres.description
%{pgbaseinstdir}/share/postgres.shdescription
%{pgbaseinstdir}/share/system_views.sql
%{pgbaseinstdir}/share/*.sample
%{pgbaseinstdir}/share/extension/stormstats*
%{pgbaseinstdir}/share/storm_catalog.sql
%{pgbaseinstdir}/share/timezonesets/*
%{pgbaseinstdir}/share/tsearch_data/*.affix
%{pgbaseinstdir}/share/tsearch_data/*.dict
%{pgbaseinstdir}/share/tsearch_data/*.ths
%{pgbaseinstdir}/share/tsearch_data/*.rules
%{pgbaseinstdir}/share/tsearch_data/*.stop
%{pgbaseinstdir}/share/tsearch_data/*.syn
%{pgbaseinstdir}/lib/dict_int.so
%{pgbaseinstdir}/lib/dict_snowball.so
%{pgbaseinstdir}/lib/dict_xsyn.so
%{pgbaseinstdir}/lib/euc2004_sjis2004.so
%{pgbaseinstdir}/lib/plpgsql.so
%dir %{pgbaseinstdir}/share/extension
%{pgbaseinstdir}/share/extension/plpgsql*
#%{pgbaseinstdir}/lib/test_parser.so
%{pgbaseinstdir}/lib/tsearch2.so
%{pgbaseinstdir}/lib/stormstats.so


%dir %{pgbaseinstdir}/lib
%dir %{pgbaseinstdir}/share
%attr(700,postgres,postgres) %dir /var/lib/pgxl
%attr(700,postgres,postgres) %dir /var/lib/pgxl/%{majorversion}
%attr(700,postgres,postgres) %dir /var/lib/pgxl/%{majorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/pgxl/%{majorversion}/backups
#%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgxl/.bash_profile
%{pgbaseinstdir}/lib/*_and_*.so
%{pgbaseinstdir}/share/conversion_create.sql
%{pgbaseinstdir}/share/information_schema.sql
%{pgbaseinstdir}/share/snowball_create.sql
%{pgbaseinstdir}/share/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pgbaseinstdir}/include/*
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/lib/libpq.so
%{pgbaseinstdir}/lib/libecpg.so
%{pgbaseinstdir}/lib/libpq.a
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.so
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgport.a
%{pgbaseinstdir}/lib/libpgtypes.so
%{pgbaseinstdir}/lib/libpgtypes.a
%{pgbaseinstdir}/lib/libpgcommon.a
%{pgbaseinstdir}/lib/pgxs/*
%{pgbaseinstdir}/lib/pkgconfig/*
%{pgbaseinstdir}/share/man/man1/ecpg.*

%files gtm -f pg_devel.lst
%defattr(-,root,root)
%{pgbaseinstdir}/bin/gtm
%{pgbaseinstdir}/bin/gtm_ctl
%{pgbaseinstdir}/bin/gtm_proxy
%{pgbaseinstdir}/bin/initgtm
%{pgbaseinstdir}/share/man/man1/gtm.1
%{pgbaseinstdir}/share/man/man1/gtm_ctl.1
%{pgbaseinstdir}/share/man/man1/gtm_proxy.1
%{pgbaseinstdir}/share/man/man1/initgtm.1

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plperl.so
%{pgbaseinstdir}/share/extension/plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/pltcl.so
%{pgbaseinstdir}/bin/pltcl_delmod
%{pgbaseinstdir}/bin/pltcl_listmod
%{pgbaseinstdir}/bin/pltcl_loadmod
%{pgbaseinstdir}/share/unknown.pltcl
%{pgbaseinstdir}/share/extension/pltcl*
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plpython2.so
%{pgbaseinstdir}/share/extension/plpython2u*
%{pgbaseinstdir}/share/extension/plpythonu*
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{pgbaseinstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{pgbaseinstdir}/lib/test
%endif

%changelog
* Thu Dec 26 2016 Daehyung Lee <daehyung@gmail.com> - 9.5.1.4
- Create for Postgres-XL 9.5 R1.4

* Fri May 19 2013 ViVek Raghuwanshi <vivek.r@stormdb.com> - 1.0.2-1PGDG
- Updated to 1.0.2

* Wed Sep 5 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.1-1PGDG
- Update to 1.0.1

* Mon Sep 03 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-2PGDG
- Remove useless ldconfig call from -server subpackage.

* Mon Aug 13 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial cut for 1.0.0
