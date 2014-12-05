csc-cascading-config
====================

Cascading configuration


This is something i played with several times in the past.
The idea is to have a cascaded configuration mechanism to enable easy inheritance and maintenance of the actual content. To have ability to manage configuration and data model like we can with cascading stylesheets, but for general purpose, applicative configuration.

I updated my pick for a base syntax to be yaml, as it is readable and has some nice syntactic sugar to assist, but this could just as well be done with json, xml (and not as nicely with property files).

So yaml and python and then back to jvms.



for

```
---
basic_inst:
  packages: [ssh, rsync, openjdk-7-jre]
  mem: 12gb
  delme: a line to be deleted
  services: 
    active: [svc1, svc_cluster]
    standby: [svc2, svc5]
lXmp:
  based_on: basic_inst
  mem: 2gb
  overrides:
    - !Add{ packages: [mysql, php5-cli php5-fpm php5-mysql, libcurl3] }
    - !Del{ services/standby: [svc3, svc4, svc5] } # this will only remove svc5
  # alternate syntax
    - !Add{ path: packages, values: [mysql, php5-cli php5-fpm php5-mysql, libcurl3] } 
lamp:
  based_on: lXmp
  mem: 2gb
  overrides:
    - !Add{ packages: [apache] }
lnmp:
  based_on: lXmp
  mem: 2gb
  overrides:
    - !Add{ packages: [nginx] }

```