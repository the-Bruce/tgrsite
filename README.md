# tgrsite
Warwick Tabletop Games and Roleplaying Society website

## Environment configuration
The following environment varaibles are mandatory:
* `SECRET_KEY`: Site's own secret key, for encryption. See [Django's documentation of the `SECRET_KEY` setting](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECRET_KEY).

The following fields are optional:
* `DEBUG`: Determines whether to run the server in debug mode. See [Django's documentation of the `DEBUG` setting](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-DEBUG). DO NOT RUN A PRODUCTION SERVER WITH THIS ENABLED.
* `EMAIL_HOST`: Hostname of email API server. Email settings are required in order to properly send pasword reset emails and notifications.
* `EMAIL_HOST_USER`: Username to use to login to mail API.
* `EMAIL_HOST_PASSWORD`: Ditto, for password.
* `FROM_EMAIL`: Address to send emails from (eg "noreply@somesite.xyz").
* `HOST`: Hostname to add to allowed hosts. See [Django's documentation of the `ALLOWED_HOSTS` setting](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-ALLOWED_HOSTS).

## Advanced configuration
Create a `local_config.py` in the same directory as the `settings.py` file. This allows you to override any setting locally that you need to.

## Setup guide
* This app requires Python 3.6. Make sure you run these commands using the right version of Python. It is recommended that you [create a virtual environment](https://docs.djangoproject.com/en/2.0/topics/install/#installing-an-official-release-with-pip) for the app.
* Install required Python packages (eg `pip install -r requirements.txt`)
* Configure environment variables (see above).
* Ensure migrations are present: `python manage.py makemigrations`
    * You may need to list all the apps, like so `... makemigrations assets exec forum gallery inventory messaging minutes navbar newsletters notifications pages redirect rpgs templatetags timetable users website_settings`
* Run database migrations: `python manage.py migrate`
* Create a super user: `python manage.py createsuperuser`
* Run the server using `python manage.py runserver`
 * The server will be running on `localhost:8000`.
 * You should create a `Member` for your super user, since this is currently not automatically done.
  * Go to the admin site at `/admin`, log in, and add a Member object with `equiv_user` set to your superuser. IF you do not do this then your superuser will cause errors when viewing the site.

## Contributing
Contributions welcome, in the form of issue submissions, pull requests, and comments.
If you want to add a feature, fork and branch the repo, and create a pull request into `master`.
