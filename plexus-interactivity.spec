# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# We just want to use ant
%define _without_maven 1

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define with_maven %{!?_without_maven:1}%{?_without_maven:0}
%define without_maven %{?_without_maven:1}%{!?_without_maven:0}
%define gcj_support 0

Summary:	Plexus Interactivity Handler Component
Name:		plexus-interactivity
Version:	1.0
Release:	0.1.a5.2.2.8
License:	Apache License
Group:		Development/Java
Url:		http://plexus.codehaus.org/
# svn export \
#   svn://svn.plexus.codehaus.org/plexus/tags/plexus-interactivity-1.0-alpha-5/
# tar cjf plexus-interactivity-1.0-alpha-5-src.tar.bz2 \
#   plexus-interactivity-1.0-alpha-5
# md5sum 7b2a814da29fc1118bc5b4e4bc6225eb
Source0:	plexus-interactivity-1.0-alpha-5-src.tar.bz2
Source1:	plexus-interactivity-1.0-api-build.xml
Source2:	plexus-interactivity-1.0-jline-build.xml
%if %{with_maven}
Source3:	plexus-interactivity-1.0-api-project.xml
Source4:	plexus-interactivity-1.0-jline-project.xml
%endif
%if !%{gcj_support}
BuildArch:	noarch
BuildRequires:	java-devel
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	ant >= 0:1.6
BuildRequires:	ant-nodeps 
%if %{with_maven}
BuildRequires:	maven
%endif
BuildRequires:	jline
BuildRequires:	plexus-container-default
BuildRequires:	plexus-utils
Requires:	plexus-container-default
Requires:	plexus-utils
Requires:	jline

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -qn plexus-interactivity-1.0-alpha-5
cp %{SOURCE1} plexus-interactivity-api/build.xml
cp %{SOURCE2} plexus-interactivity-jline/build.xml
%if %{with_maven}
cp %{SOURCE3} plexus-interactivity-api/project.xml
cp %{SOURCE4} plexus-interactivity-jline/project.xml
%endif

%build
%if %{with_maven}
mkdir -p .maven/repository/maven/jars
build-jar-repository .maven/repository/maven/jars \
maven-jelly-tags

mkdir -p .maven/repository/JPP/jars
build-jar-repository -s -p .maven/repository/JPP/jars \
jline plexus/container-default plexus/utils
export MAVEN_HOME_LOCAL=$(pwd)/.maven
%endif

pushd plexus-interactivity-api
%if %{with_maven}
maven \
        -Dmaven.repo.remote=file:/usr/share/maven/repository \
        -Dmaven.home.local=$MAVEN_HOME_LOCAL \
        jar:install javadoc

%else

mkdir -p target/lib
build-jar-repository -s -p target/lib plexus/container-default plexus/utils
%{ant} jar javadoc
%endif
popd

pushd plexus-interactivity-jline
%if %{with_maven}
maven \
        -Dmaven.repo.remote=file:/usr/share/maven/repository \
        -Dmaven.home.local=$MAVEN_HOME_LOCAL \
        jar:install javadoc

%else
mkdir -p target/lib
cp \
  ../plexus-interactivity-api/target/plexus-interactivity-api-1.0-alpha-5.jar \
  target/lib
build-jar-repository -s -p target/lib jline plexus/container-default
ant jar javadoc
%endif
popd

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}/plexus
install -pm 644 \
  plexus-interactivity-api/target/%{name}-api-%{version}-alpha-5.jar \
  %{buildroot}%{_javadir}/plexus/interactivity-api-%{version}.jar
install -pm 644 \
  plexus-interactivity-jline/target/%{name}-jline-%{version}-alpha-5.jar \
  %{buildroot}%{_javadir}/plexus/interactivity-jline-%{version}.jar
(cd %{buildroot}%{_javadir}/plexus && \
 for jar in *-%{version}*; do \
     ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; \
 done \
)

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}/api
cp -pr plexus-interactivity-api/target/docs/apidocs/* \
  %{buildroot}%{_javadocdir}/%{name}-%{version}/api
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}/jline
cp -pr plexus-interactivity-jline/target/docs/apidocs/* \
  %{buildroot}%{_javadocdir}/%{name}-%{version}/jline
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%doc %{_javadocdir}/*

