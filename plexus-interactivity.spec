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

%global parent plexus
%global subname interactivity

Name:           plexus-interactivity
Version:        1.0
Release:        0.4.a6.9
Summary:        Plexus Interactivity Handler Component
License:        MIT
Group:          Development/Java
URL:            http://plexus.codehaus.org/
# svn export \
#   http://svn.codehaus.org/plexus/plexus-components/tags/plexus-interactivity-1.0-alpha-6/
# tar caf plexus-interactivity-1.0-alpha-6-src.tar.xz \
#   plexus-interactivity-1.0-alpha-6
Source0:        plexus-interactivity-1.0-alpha-6-src.tar.xz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-nodeps
BuildRequires:  maven2
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  jline
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils

Requires:  plexus-container-default
Requires:  plexus-utils
Requires:  jline

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n plexus-interactivity-1.0-alpha-6

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:aggregate

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}/plexus
install -pm 644 \
  plexus-interactivity-api/target/%{name}-api-%{version}-alpha-6.jar \
  %{buildroot}%{_javadir}/plexus/interactivity-api.jar
install -pm 644 \
  plexus-interactivity-jline/target/%{name}-jline-%{version}-alpha-6.jar \
  %{buildroot}%{_javadir}/plexus/interactivity-jline.jar

install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 \
pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{parent}-%{subname}.pom
install -pm 644 \
plexus-interactivity-api/pom.xml \
 	%{buildroot}%{_mavenpomdir}/JPP.%{parent}-interactivity-api.pom
install -pm 644 \
plexus-interactivity-jline/pom.xml \
 	%{buildroot}%{_mavenpomdir}/JPP.%{parent}-interactivity-jline.pom

%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}
%add_to_maven_depmap org.codehaus.plexus %{name}-api %{version} JPP/%{parent} interactivity-api
%add_to_maven_depmap org.codehaus.plexus %{name}-jline %{version} JPP/%{parent} interactivity-jline

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug #447156 (can be removed in F-17)
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*


