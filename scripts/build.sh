#!/bin/bash

curr_dir=`dirname $0`
curr_dir=`cd $curr_dir; pwd`

setup_host="$curr_dir/setup_host.sh"
mahout_spec="$curr_dir/mahout.spec"

if [ -f "$curr_dir/setup_env.sh" ]; then
  source "$curr_dir/setup_env.sh"
fi

if [ "x${WORKSPACE}" = "x" ] ; then
  WORKSPACE="$curr_dir/../"
fi

if [ ! -f "$curr_dir/setup_host.sh" ]; then
  echo "warn - $setup_host does not exist, we may not need this if all the libs and RPMs are pre-installed"
fi

if [ ! -e "$mahout_spec" ] ; then
  echo "fail - missing $mahout_spec file, can't continue, exiting"
  exit -9
fi

env | sort

echo "checking if scala is installed on the system"
# this chk can be smarter, however, the build script will re-download the scala libs again during build process
# we can save some build time if we can just re-use the pre-installed scala
chk_scala_rpm=$(rpm -qa *scala*)
if [ "x${chk_scala_rpm}" = "x" -o ! -d "${SCALA_HOME}" ] ; then
  echo "warn - SCALA_HOME may or may not be defined, however, $SCALA_HOME folder doesn't exist, re-downloading scala and install scala temporarily"
  wget --quiet --output-document=scala.tgz  "http://www.scala-lang.org/files/archive/scala-2.10.3.tgz"
  tar xvf scala.tgz
  if [ -d $WORKSPACE/scala ] ; then
    echo "deleting prev installed scala"
    rm -rf $WORKSPACE/scala
  fi
  mv scala-* $WORKSPACE/scala
  export SCALA_HOME=$WORKSPACE/scala
  echo "scala downloaded completed, and put to $SCALA_HOME"
fi

#if [ ! -f "/usr/bin/rpmdev-setuptree" -o ! -f "/usr/bin/rpmbuild" ] ; then
#  echo "fail - rpmdev-setuptree and rpmbuild in /usr/bin/ are both required to build RPMs"
#  exit -8
#fi

# should switch to WORKSPACE, current folder will be in WORKSPACE/mahout due to 
# hadoop_ecosystem_component_build.rb => this script will change directory into your submodule dir
# WORKSPACE is the default path when jenkin launches e.g. /mnt/ebs1/jenkins/workspace/mahout_build_test-alee
# If not, you will be in the $WORKSPACE/mahout folder already, just go ahead and work on the submodule
# The path in the following is all relative, if the parent jenkin config is changed, things may break here.
pushd `pwd`
cd $WORKSPACE/mahout

# Manual fix Git URL issue in submodule, safety net, just in case the git scheme doesn't work
# sed -i 's/git\@github.com:Altiscale\/mahout.git/https:\/\/github.com\/Altiscale\/mahout.git/g' .gitmodules
# sed -i 's/git\@github.com:Altiscale\/mahout.git/https:\/\/github.com\/Altiscale\/mahout.git/g' .git/config
echo "ok - switching to mahout-0.8 and refetch the files"
git checkout mahout-0.8
git fetch --all
popd

echo "ok - tar zip source file, preparing for build/compile by rpmbuild"
pushd `pwd`
# mahout is located at $WORKSPACE/mahout
cd $WORKSPACE
# tar cvzf $WORKSPACE/mahout.tar.gz mahout
popd

# Looks like this is not installed on all machines
# rpmdev-setuptree
mkdir -p $WORKSPACE/rpmbuild/{BUILD,BUILDROOT,RPMS,SPECS,SOURCES,SRPMS}/
cp "$mahout_spec" $WORKSPACE/rpmbuild/SPECS/mahout.spec
cp -r $WORKSPACE/mahout $WORKSPACE/rpmbuild/SOURCES/vcc-mahout
cp $WORKSPACE/patches/* $WORKSPACE/rpmbuild/SOURCES/
# SCALA_HOME=$SCALA_HOME rpmbuild -vv -ba $WORKSPACE/rpmbuild/SPECS/mahout.spec --define "_topdir $WORKSPACE/rpmbuild" --rcfile=$mahout_rc_macros --buildroot $WORKSPACE/rpmbuild/BUILDROOT/
rpmbuild -vv -ba $WORKSPACE/rpmbuild/SPECS/mahout.spec --define "_topdir $WORKSPACE/rpmbuild" --buildroot $WORKSPACE/rpmbuild/BUILDROOT/


if [ $? -ne "0" ] ; then
  echo "fail - RPM build failed"
fi
  
echo "ok - build Completed successfully!"

exit 0












