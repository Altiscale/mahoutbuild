mahoutbuild
===========

Repo wrapper to build Mahout on VCC-Hadoop2.2.

In order to support hadoop 2.2 according to the patches in MAHOUT-1329
(see https://issues.apache.org/jira/browse/MAHOUT-1329), we decided to apply 
the following approach.

- We clone mahout-0.8, and patched it to the current trunk (20140328) that 
supports hadoop 2.2.0 integration. The patch is created base on the current 
trunk (as of today).

,,,
diff -uNar -x .git mahout mahout.trunk > patch.mahout
,,,

Keep this patch with mahout-0.8 to get the current build. If a new branch comes out,
you could upgrade the branch to the later one. Otherwise, 0.8 is the latest release 
that does NOT support Hadoop 2.2, and we use this patch to fast forward to the latest
trunk that contains the support for Hadoop 2.2.





