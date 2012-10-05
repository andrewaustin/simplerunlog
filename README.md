Simple Run Log
==============

A multi-user run tracker.

Features
--------
* Computes various run length metrics
* Ajax interface for monthly and weekly runs
* Ajax interface to add new runs
* Public profile to share run progress
* PEP8 compliant code
* Uses class based generic views when appropriate

Installation
------------
* pip install -r requirements.txt
* python manage.py syncdb
* python manage.py migrate
* python manage.py runserver

Known Bugs
----------
* Timezone disparity between local time and server time.
    * https://docs.djangoproject.com/en/dev/topics/i18n/timezones/
* Days run this week looks at past 7 days not current week.

Things To Do
-------------
* Finish full conversion to tastypie vs. own /run/ view
* Use JS templating vs. inline html for week calendar widget
* Use flot charts to make some nice graphs
* Run types from jack daniels
* Calendar
    * Add Planned Runs
    * Add Races
    * Goals
* integrate with facebook when posting runs
* autogenerate image signature that links to user profile (PIL)
    * http://docs.python.org/library/stringio.html
    * http://www.pythonware.com/library/pil/handbook/image.htm#Image.save
* user registration
* 30 day trial
* better unit tests
* better design
    * dashboard buttons
    * http://developer.garmin.com/
    * http://fpcomplete.com/services/
    * http://www.456bereastreet.com/
