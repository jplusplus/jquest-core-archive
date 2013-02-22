# jQuest Core
## Installation
### Software dependencies
To make jQuest Core up and running, you need:

* **Python** 2.7.3
* **PostGreSQL** 9.*
* A database connector/interface for python (Ex: *python-mysqldb*)
* **Pip** (package manager)
* **Virtualenv** 1.8.4

The following installation builds jQuest Core at the top of SQLite:

    $ sudo apt-get install python-pip python python-imaging virtualenvwrapper postgresql-9.1 

### Load virtualenv
From the top-level directory, create a virtual environment :

    $ virtualenv venv --distribute

And load it :
    
    $ source venv/bin/activate

### Dependencies
To download and set up the whole dependancies three and the active virtualenv, simply run from the project's root directory:

    $ pip install -r requirements.text

### Environment variables
The following environment variables should be use 

* **PORT** defines the port to listen to when using foreman (ex: *80*).
* **DATABASE_URL** defines the Universal Resource Locator (ex: *sqlite:///:jquest.db*) 
    
*Tips: you can also use [autoenv](https://github.com/kennethreitz/autoenv) to load virtual environment and variables automatically when you `cd` your server directory.*

### Prepare your database
Postgresql must support the [hstore](http://www.postgresql.org/docs/9.0/interactive/hstore.html) extention. To activate this extention on your jQuest database, connect you using psql on your jquest database and enter:

```sql
CREATE EXTENSION hstore;
```

For more information about hstore on Django, see also:
* The [Django Hstore](https://github.com/jordanm/django-hstore) module;
* The [documentation from Django](http://django-orm.readthedocs.org/en/latest/orm-pg-hstore.html) about this extention.

### Synchronize the database
Once you saved the settings file, run this command to synchronize your database with the jQuest's models:

    $ python jquest_core/mange.py syncdb

You must see this result:  
    
    Creating tables ...
    Creating table tastypie_apiaccess
    Creating table tastypie_apikey
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table django_content_type
    Creating table django_session
    Creating table django_site
    Creating table django_admin_log
    Creating table jquest_instance
    Creating table jquest_mission
    Creating table jquest_missionrelationship
    Creating table jquest_language
    Creating table jquest_post
    Creating table jquest_useroauth
    Creating table jquest_userprogression

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): 

Say **yes** to the prompt and enter your superuser credidentials. 


### Launching
To wake up jQuest Core, run the following command from the server directory:

    $ python jquest_core/manage.py runserver

You must see this result:

    Validating models...

    0 errors found
    Django version 1.4.3, using settings 'settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Your server is now available at [http://127.0.0.1:8000](http://127.0.0.1:8000) !

## Licence
Copryright © [Journalism++](http://jplusplus.org) - All rights reserved