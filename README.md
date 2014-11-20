dndtools
==========

An open source Django-based wiki-like web application for DnD.

Status
------
This github repository is currently a clone of a private repository. It contains ONLY source codes of the application, not its data. 

Also, this readme file is just an early preview to be updated as soon as someone have the time. 

If you find anything wrong, just start an issue.

Installation info
-----------------
(Windows 7 steps, for linux/mac something will probably have to be change. Also, referring binaries that are now NOT part of the repository!)

1. python 2.7
2. Django-1.2.7.tar.gz
3. etianen-django-reversion-release-1.3.3-0-g3c9a873.zip (setup.py install), https://nodeload.github.com/etianen/django-reversion/zipball/release-1.3.3
4. appserv-win32-2.5.10.exe (MySQL), MySQL-python-1.2.3.win32-py2.7.exe (or 64b)
4x. probably missing easy_install here
5. ez_setup.py
6. easy_install pip
7. easy_install South
8. easy_install django-pagination
9. easy_install django-debug-toolbar
10. easy_install textile
11. PIL-1.1.7.win32-py2.7.exe
12. alex-django-filter-0.5.3-2-g51b39fc.zip (setup.py install), https://nodeload.github.com/alex/django-filter/zipball/master
13. easy_install recaptcha-client

Linux
-----

For newer branch (will publish soon flush from my drive), use those packages:

pip freeze
Django==1.5.5
MySQL-python==1.2.4
Pillow==2.2.2
South==0.8.4
argparse==1.2.1
django-debug-toolbar==0.11.0
django-filter==0.5.3
django-pagination==1.0.7
django-reversion==1.8.0
recaptcha-client==1.0.6
sqlparse==0.1.10
textile==2.1.5
wsgiref==0.1.2
