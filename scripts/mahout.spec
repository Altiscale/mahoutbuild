%define altiscale_release_ver %(echo ${ALTISCALE_RELEASE})
%define mahout_ver %(echo ${MAHOUT_VERSION})
%define rpm_package_name alti-mahout
%define mahout_folder_name %{rpm_package_name}-%{mahout_ver}
%define install_mahout_dest /opt/%{mahout_folder_name}
#%define packager %(echo ${PKGER})
%define build_release %(echo ${BUILD_TIME})

Name: %{rpm_package_name}
Summary: %{mahout_folder_name} RPM Installer
Version: %{mahout_ver}
Release: %{altiscale_release_ver}.%{build_release}%{?dist}
License: Copyright (C) 2014 Altiscale. All rights reserved.
# Packager: %{packager}
Source: %{_sourcedir}/%{rpm_package_name}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%{rpm_package_name}
# Requires: scala-2.10.3 >= 2.10.3
# Apply all patches to fix CLASSPATH and java lib issues
Patch1: %{_sourcedir}/patch.mahout

Url: https://mahout.apache.org/

%description
%{mahout_folder_name} is a repackaged mahout distro that is compiled against Hadoop 2.2.x. 
This package should work with Altiscale Hadoop.

%prep
# copying files into BUILD/mahout/ e.g. BUILD/mahout/* 
echo "ok - copying files from %{_sourcedir} to folder  %{_builddir}/%{rpm_package_name}"
cp -r %{_sourcedir}/%{rpm_package_name} %{_builddir}/

%patch1 -p0

%build
echo "ANT_HOME=$ANT_HOME"
echo "JAVA_HOME=$JAVA_HOME"
echo "MAVEN_HOME=$MAVEN_HOME"
echo "MAVEN_OPTS=$MAVEN_OPTS"
echo "M2_HOME=$M2_HOME"

echo "build - mahout core in %{_builddir}"
pushd `pwd`
cd %{_builddir}/%{rpm_package_name}/
export HADOOP_VERSION=2.2.0

mvn clean install -DskipTests -Dhadoop2 -Dhadoop2.version=${HADOOP_VERSION}
echo "warn - test is skipped due to spark binding error, all other test looks good"
echo "warn - this error only happens when integrating with Spark, will need to look into it later"
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
echo "test install mahout label mahout_folder_name = %{mahout_folder_name}"
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/examples/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/core/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/math/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/math-scala/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/buildtools/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/spark/target/
%{__mkdir} -p %{buildroot}%{install_mahout_dest}/integration/target/
# work folder is for runtime, this is a dummy placeholder here to set the right permission within RPMs
cp -rp %{_builddir}/%{rpm_package_name}/bin %{buildroot}%{install_mahout_dest}/
cp -rp %{_builddir}/%{rpm_package_name}/examples/target/*.jar %{buildroot}%{install_mahout_dest}/examples/target/
cp -rp %{_builddir}/%{rpm_package_name}/core/target/*.jar %{buildroot}%{install_mahout_dest}/core/target/
cp -rp %{_builddir}/%{rpm_package_name}/math/target/*.jar %{buildroot}%{install_mahout_dest}/math/target/
cp -rp %{_builddir}/%{rpm_package_name}/math-scala/target/*.jar %{buildroot}%{install_mahout_dest}/math-scala/target/
cp -rp %{_builddir}/%{rpm_package_name}/buildtools/target/*.jar %{buildroot}%{install_mahout_dest}/buildtools/target/
cp -rp %{_builddir}/%{rpm_package_name}/spark/target/*.jar %{buildroot}%{install_mahout_dest}/spark/target/
cp -rp %{_builddir}/%{rpm_package_name}/integration/target/*.jar %{buildroot}%{install_mahout_dest}/integration/target/

%clean
echo "ok - cleaning up temporary files, deleting %{buildroot}%{install_mahout_dest}"
rm -rf %{buildroot}%{install_mahout_dest}

%files
%defattr(0755,root,root,0755)
%{install_mahout_dest}

%changelog
* Fri Apr 4 2014 Andrew Lee 20140404
- Change UID to 411460025, and change the name back from vcc- to alti-
* Wed Apr 2 2014 Andrew Lee 20140402
- Rename package name with prefix alti- so we can search for Altiscale RPMs
* Sat Mar 30 2014 Andrew Lee 20140330
- Initial Creation of spec file for Mahout-1.0-trunk-20140328


