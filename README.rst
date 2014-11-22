=====
Crispy Notes
=====


Crispy Notes is a Django app to take notes.


Quick start
-----------

1. Add "crispy_notes" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'crispy_notes',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^crispy/', include('crispy_notes.urls')),

3. Run `python manage.py migrate` to create the crispy_notes models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/crispy/.
