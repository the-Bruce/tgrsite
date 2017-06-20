# tgrsite
Current website for Warwick Univeristy's Tabletop, Games and Roleplaying Society.

## Setup guide
* Install requirements (`pip install -r requirements.txt`)
* Note the `DEBUG` option in tgrsite/settings.py - this must be `False` in production!
* Before running, make sure that the database migrations are present by running: ` python manage.py makemigrations bugreports rpgs users forum messaging` (i.e. all directories that have models in), followed by `python manage.py migrate`
 * When you change any models make sure to do this to the changed app!
* Run the server with `python manage.py runserver`
* To set up an admin superuser, make sure to:
  * Run `python manage.py createsuperuser`, of course.
  * Start the server, go into /admin, log in, and add a Member with "equivalent user" as that account.
  * This is because createsuperuser circumvents the site's signups system which creates both a User (Django auth) and a Member (site stuff).

## Contributing
Repo branches for features and tags on releases. Take a look at the issue tracker if you want to contribute. PRs and discussion of issues welcome.

(to reiterate: please **don't push directly to master**: work in a branch or fork and PR to merge.
