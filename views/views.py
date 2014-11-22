# Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# Haystack imports
from haystack.query import SearchQuerySet
from haystack.management.commands import update_index

# crispy_notes imports
from crispy_notes.models import *
from crispy_notes.forms import NotesSearchForm

# Other imports
import markdown
import html2text
import datetime
import calendar
from collections import Counter

def home(request):
    """Home page view for notes app.  Displays last 10 most viewed notes and Used tags.  """
    user    =   request.user
    if user.is_authenticated():
        nt              =   Note_Tags.objects.filter()
        nv              =   NoteViews.objects.filter().order_by('-views')[:10]
        nlu             =   NoteLastUpdated.objects.filter().order_by('-updated')[:10]
        c_nt            =   Counter([x.TAG_ID for x in nt])
        count_tags      =   sorted([(item,c_nt[item],) for item in c_nt],key=lambda x: x[0].tag)
        context         =   {   "nv":nv,
                                "count_tags":count_tags,
                                "nlu":nlu,
                            }
    else:
        user.username   =   'Guest'
        context         =   {"user":user,}
    return render(request,'home.html',context)

@login_required(login_url='/accounts/login/')
def view_tag(request,tag):
    """View all notes of a tag. """
    note_tags   =   Note_Tags.objects.filter(TAG_ID__tag=tag)
    notes       =   [note.NOTE_ID for note in note_tags.order_by("NOTE_ID__date","NOTE_ID__time")]
    tags        =   set([tag.TAG_ID for tag in Note_Tags.objects.filter(NOTE_ID__in=notes)])
    note_tags   =   Note_Tags.objects.filter(TAG_ID__in=tags)
    c_nt        =   Counter([x.TAG_ID for x in note_tags])
    count_tags  =   [(item,c_nt[item],) for item in c_nt]
    context     =   {   "notes":notes,
                        "tags":tags,
                        "count_tags":count_tags,
                        "view":"tag",
                    }
    return render(request,'home.html',context)

def tags(request,sortby=0):
    """ View all tags.

    sortby:
    0 view by Tags.tag
    1 view by Count descending order
    """
    nt          =   Note_Tags.objects.filter()
    c_nt        =   Counter([x.TAG_ID for x in nt])
    count_tags  =   [(item,c_nt[item],) for item in c_nt]
    tags        =   Tags.objects.filter().exclude(tag__in=[x.TAG_ID for x in nt])
    count_tags  +=   [(x,0,) for x in tags]
    sortby      = int(sortby)
    if sortby == 1:
        count_tags  = sorted(count_tags,key=lambda x: x[sortby],reverse=True)
    else:
        count_tags  = sorted(count_tags,key=lambda x: x[sortby].tag)
    context     =   { "count_tags":count_tags,}
    return render(request, "home.html", context)

@login_required(login_url='/accounts/login/')
def add(request):
    """Add new note. GET request blank form. POST request adds new note."""
    if request.method == 'POST':
        notes    =   NotesForm(request.POST)
        tags     =   TagsForm(request.POST)
        if notes.is_valid():
            #notes.instance.note = html2text.html2text(notes.instance.note)
            model_instance = notes.save(commit=True)
            NoteViews(NOTE_ID=model_instance).save()
            NoteLastUpdated(NOTE_ID=model_instance,updated=datetime.datetime.today()).save()
            if tags.is_valid():
                for x in tags.data.getlist('tag'):
                    Note_Tags(NOTE_ID=model_instance,TAG_ID=Tags.objects.get(id=x)).save()
            #update_index.Command().handle()
            return redirect('view', id=model_instance.id)
    else:
        notes   =   NotesForm()
        tags    =   TagsForm()
        context =   {"notes":notes,"tags":tags,"view":"Add","submit_value":"Add Note",}
        return render(request, 'add.html', context)

@login_required(login_url='/accounts/login/')
def edit_note(request,id):
    """ Edit a note. GET request retrieves note and POST request updated note in database. """
    if request.method == 'POST':
        notes    =   NotesForm(request.POST,instance=Notes.objects.get(id=id))
        tags     =   TagsForm(request.POST)
        if notes.is_valid():
            model_instance      =   notes.save(commit=False)
            #model_instance.note =   html2text.html2text(model_instance.note)
            note_updated        =   NoteLastUpdated.objects.get(NOTE_ID=model_instance)
            model_instance.save()
            note_updated.updated_note()
            if tags.is_valid():
                for x in tags.data.getlist('tag'):
                    Note_Tags(NOTE_ID=model_instance,TAG_ID=Tags.objects.get(id=x)).save()
            #update_index.Command().handle()
            return redirect('view', id=model_instance.id)
    else:
        data            =   Notes.objects.filter(id=id).values()[0]
        notes           =   NotesForm(data)
        tags            =   TagsForm()
        context         =   {"notes":notes,"tags":tags,"view":"Edit","submit_value":"Update Note",}
        return render(request, 'add.html', context)

@login_required(login_url='/accounts/login/')
def view(request,id):
    """ View note. Using the request.id = Notes.ID """
    note                =   Notes.objects.get(id=id)
    tags                =   Note_Tags.objects.filter(NOTE_ID=id)
    tags                =   [x.TAG_ID for x in tags]
    note.note           =   markdown.markdown(note.note)
    note_views          =   NoteViews.objects.get(NOTE_ID=note)
    note_views.increment_view_count()
    context =   {"note":note,"tags":tags,}
    return render(request, 'note.html', context)

def new_tag(request):
    """Add new tag to Tags."""
    messages = {    "ADD"       :   "Add new Tag.",
                    "INVALID"   :   "Invalid Tag, please try again.",
                    "VALID"     :   "Tag Added. Add another?",
    }
    message =   "ADD"
    if request.method == 'POST':
        new_tag    =   NewTagsForm(request.POST)
        if new_tag.is_valid():
            model_instance = new_tag.save(commit=True)
            message = "VALID"
        else:
            message = "INVALID"
    new_tag =   NewTagsForm()
    context =   {"notes":new_tag,"view":"Tag","tag_message":messages[message],"submit_value":"Add Tag",}
    return render(request, 'add.html', context)

def remove_tags(request,id):
    """Remove selected tags from a note."""
    if request.method == 'POST':
        remove_tags    =    request.POST.getlist('remove-tags')
        for x in remove_tags:
            note_tag    =   Note_Tags.objects.get(NOTE_ID=id,TAG_ID=int(x))
            note_tag.delete()
    note   =   Notes.objects.get(id=id)
    tags   =   Note_Tags.objects.filter(NOTE_ID=id)
    tags   =    [x.TAG_ID for x in tags]
    note.note   =   markdown.markdown(note.note)
    context =   {"note":note,"tags":tags,}
    return render(request, "remove.html", context)

def action(request):
    """Actions on Notes. The action matches a named url."""
    action              =   request.GET['action']
    view_action,note_id =   action.split("+")
    return HttpResponseRedirect(reverse(view_action,args=[note_id]))

def report_year(request,year):
    """Show reports for the provided year."""
    user    =   request.user
    if user.is_authenticated():
        notes   =   Notes.objects.filter(date__year=year)
        context         =   {   "notes" :notes,
                                "report":"{} Notes".format(year),
                            }
    else:
        user.username   =   'Guest'
        context         =   {"user":user,}
    return render(request,'report.html',context)

def report_month(request,year,month):
    """Show reports for the provided year and month."""
    user    =   request.user
    if user.is_authenticated():
        notes   =   Notes.objects.filter(date__year=year,date__month=month)
        context =   {   "notes" :notes,
                        "report":"{} {} Notes".format(calendar.month_name[int(month)],year),
                    }
    else:
        user.username   =   'Guest'
        context         =   {"user":user,}
    return render(request,'report.html',context)

def report_day(request,year,month,day):
    """Show reports for the provided year, month and date."""
    user    =   request.user
    if user.is_authenticated():
        notes   =   Notes.objects.filter(date__year=year,date__month=month,date__day=day)
        context =   {   "notes" :notes,
                        "report":"{} {}, {} Notes".format(calendar.month_name[int(month)],day,year),
                    }
    else:
        user.username   =   'Guest'
        context         =   {"user":user,}
    return render(request,'report.html',context)

def login_user(request):
    state = "Please log in below..."
    if request.POST:
        username    = request.POST['username']
        password    = request.POST['password']
        user        = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST['next']:
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect('/')
            else:
                state = 'Your account is not active, please contact the site admin.'
        else:
            state = 'Your username and/or password were incorrect.'
    else:
        username = ''
    if request.GET:
        initialData = {'state':state, 'username': username, 'next':request.GET['next'],}
    else:
        user = request.user
        if user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            user.username = 'Guest'
        initialData = {'state':state, 'username': username,'user':user}
    csrfContext = RequestContext(request, initialData)
    return render(request,'auth.html',initialData)

def logout_user(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

###################################################################
# Haystack search views
###################################################################

def root(request):
    """
    Search > Root
    """
    search_query = request.GET.get('q')

    # we retrieve the query to display it in the template
    form = NotesSearchForm(request.GET)
    # we call the search method from the NotesSearchForm. Haystack do the work!
    results = form.search()

    return render(request, 'search/search_root.html', {
        'search_query' : search_query,
        'notes' : results,
    })
