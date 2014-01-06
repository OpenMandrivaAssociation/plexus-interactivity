
%undefine _compress
%undefine _extension
%global _duplicate_files_terminate_build 0
%global _files_listed_twice_terminate_build 0
%global _unpackaged_files_terminate_build 0
%global _nonzero_exit_pkgcheck_terminate_build 0
%global _use_internal_dependency_generator 0
%global __find_requires /bin/sed -e 's/.*//'
%global __find_provides /bin/sed -e 's/.*//'

Name:		plexus-interactivity
Version:	1.0
Release:	0.11.alpha6.1
License:	GPLv3+
Source0:	plexus-interactivity-1.0-0.11.alpha6.1-omv2014.0.noarch.rpm

URL:		https://abf.rosalinux.ru/openmandriva/plexus-interactivity
BuildArch:	noarch
Summary:	plexus-interactivity bootstrap version
Requires:	javapackages-bootstrap
Requires:	jline
Requires:	jpackage-utils
Requires:	plexus-component-api
Requires:	plexus-utils
Provides:	mvn(org.codehaus.plexus:plexus-interactivity) = 1.0.alpha.6
Provides:	mvn(org.codehaus.plexus:plexus-interactivity-api) = 1.0.alpha.6
Provides:	mvn(org.codehaus.plexus:plexus-interactivity-jline) = 1.0.alpha.6
Provides:	mvn(org.codehaus.plexus:plexus-interactivity:pom:) = 1.0.alpha.6
Provides:	plexus-interactivity = 0:1.0-0.11.alpha6.1:2014.0

%description
plexus-interactivity bootstrap version.

%files
/usr/share/java/plexus
/usr/share/java/plexus/interactivity-api.jar
/usr/share/java/plexus/interactivity-jline.jar
/usr/share/maven-fragments/plexus-interactivity
/usr/share/maven-poms/JPP.plexus-interactivity-api.pom
/usr/share/maven-poms/JPP.plexus-interactivity-jline.pom
/usr/share/maven-poms/JPP.plexus-interactivity.pom

#------------------------------------------------------------------------
%prep

%build

%install
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -id
