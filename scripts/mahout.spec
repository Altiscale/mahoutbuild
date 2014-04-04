%define major_ver %(echo ${MAHOUT_VERSION})
%define service_name vcc-mahout
%define company_prefix altiscale
%define pkg_name %{service_name}-%{major_ver}
%define install_mahout_dest /opt/%{pkg_name}
%define packager %(echo ${PKGER})
#%define mahout_user %(echo ${MAHOUT_USER})
#%define mahout_gid %(echo ${MAHOUT_GID})
#%define mahout_uid %(echo ${MAHOUT_UID})

Name: %{service_name}
Summary: %{pkg_name} RPM Installer
Version: %{major_ver}
Release: 4%{?dist}
License: Copyright (C) 2014 Altiscale. All rights reserved.
# Packager: %{packager}
Source: %{_sourcedir}/%{service_name}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%{service_name}
# Requires: scala-2.10.3 >= 2.10.3
# Apply all patches to fix CLASSPATH and java lib issues
Patch1: %{_sourcedir}/patch.mahout

Url: http://www.altiscale.com/

%description
%{pkg_name} is a repackaged mahout distro that is compiled against Hadoop 2.2.x. 
This package should work with Altiscale Hadoop.

%prep
# copying files into BUILD/mahout/ e.g. BUILD/mahout/* 
echo "ok - copying files from %{_sourcedir} to folder  %{_builddir}/%{service_name}"
cp -r %{_sourcedir}/%{service_name} %{_builddir}/

%patch1 -p0

%build
echo "ANT_HOME=$ANT_HOME"
echo "JAVA_HOME=$JAVA_HOME"
echo "MAVEN_HOME=$MAVEN_HOME"
echo "MAVEN_OPTS=$MAVEN_OPTS"
echo "M2_HOME=$M2_HOME"

echo "build - mahout core in %{_builddir}"
pushd `pwd`
cd %{_builddir}/%{service_name}/
export HADOOP_VERSION=2.2.0

mvn clean install -DskipTests -Dhadoop2 -Dhadoop2.version=${HADOOP_VERSION}
# mvn test -Dhadoop2 -Dhadoop2.version=${HADOOP_VERSION}

popd
echo "Build Completed successfully!"

%install
# manual cleanup for compatibility, and to be safe if the %clean isn't implemented
rm -rf %{buildroot}%{install_mahout_dest}
# re-create installed dest folders
mkdir -p %{buildroot}%{install_mahout_dest}
echo "compiled/built folder is (not the same as buildroot) RPM_BUILD_DIR = %{_builddir}"
echo "test installtion folder (aka buildroot) is RPM_BUILD_ROOT = %{buildroot}"
echo "test install mahout dest = %{buildroot}/%{install_mahout_dest}"
echo "test install mahout label pkg_name = %{pkg_name}"
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/examples/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/core/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/math/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/math-scala/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/buildtools/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/spark/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/integration/target/
# work folder is for runtime, this is a dummy placeholder here to set the right permission within RPMs
cp -rp %{_builddir}/%{service_name}/bin %{buildroot}%{install_mahout_dest}/
cp -rp %{_builddir}/%{service_name}/examples/target/*.jar %{buildroot}%{install_mahout_dest}/examples/target/
cp -rp %{_builddir}/%{service_name}/core/target/*.jar %{buildroot}%{install_mahout_dest}/core/target/
cp -rp %{_builddir}/%{service_name}/math/target/*.jar %{buildroot}%{install_mahout_dest}/math/target/
cp -rp %{_builddir}/%{service_name}/math-scala/target/*.jar %{buildroot}%{install_mahout_dest}/math-scala/target/
cp -rp %{_builddir}/%{service_name}/buildtools/target/*.jar %{buildroot}%{install_mahout_dest}/buildtools/target/
cp -rp %{_builddir}/%{service_name}/spark/target/*.jar %{buildroot}%{install_mahout_dest}/spark/target/
cp -rp %{_builddir}/%{service_name}/integration/target/*.jar %{buildroot}%{install_mahout_dest}/integration/target/

%clean
echo "ok - cleaning up temporary files, deleting %{buildroot}%{install_mahout_dest}"
rm -rf %{buildroot}%{install_mahout_dest}

%files
%defattr(0755,root,root,0755)
%{install_mahout_dest}

%changelog
* Wed Apr 2 2014 Andrew Lee 20140402
- Rename package name with prefix vcc- so we can search for Altiscale RPMs
* Sat Mar 30 2014 Andrew Lee 20140330
- Initial Creation of spec file for Mahout-1.0-trunk-20140328


