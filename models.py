from django.db import models
from django.forms import Form, ModelForm, TimeField, DateTimeField, ModelMultipleChoiceField
from django.contrib.admin import widgets

import datetime

class Owner(models.Model):
    first_name  = models.CharField(max_length=30)
    last_name   = models.CharField(max_length=30)
    email       = models.EmailField()

    def __str__(self):
        return "{}, {}".format(self.last_name,self.first_name)
    def __unicode__(self):
        return "{}, {}".format(self.last_name,self.first_name)

class Notes(models.Model):
    title   =   models.CharField(max_length=50)
    date    =   models.DateField()
    time    =   models.TimeField()
    note    =   models.TextField()

    def get_absolute_url(self):
        return "/%i/" % self.id
    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Notes"

class NoteViews(models.Model):
    NOTE_ID =   models.ForeignKey(Notes)
    views   =   models.IntegerField(default=0, editable=False)

    def increment_view_count(self):
        """
        Increase the view count of Note by 1.
        """
        self.views  +=   1
        self.save()

class NoteLastUpdated(models.Model):
    NOTE_ID =   models.OneToOneField(Notes)
    updated =   models.DateTimeField()

    def updated_note(self):
        self.updated =   datetime.datetime.today()
        self.save()

class Tags(models.Model):
    tag     =   models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.tag
    def __unicode__(self):
        return self.tag


class Note_Tags(models.Model):
    NOTE_ID =   models.ForeignKey(Notes)
    TAG_ID  =   models.ForeignKey(Tags)

    class Meta:
        verbose_name_plural = "Note Tags"

    def __str__(self):
        return "{} - {}".format(self.NOTE_ID.title,self.TAG_ID.tag)
    def __unicode__(self):
        return "{} - {}".format(self.NOTE_ID.title,self.TAG_ID.tag)

class NotesForm(ModelForm):
    class Meta:
        model   =   Notes
        fields  =   ['title','date','time','note']
    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        self.fields['time'].widget  =   widgets.AdminTimeWidget()
        self.fields['date'].widget  =   widgets.AdminDateWidget()
        self.fields['note'].widget.attrs['class']           =   "form-control"
        self.fields['note'].widget.attrs['id']              =   "pagedownMe"
        self.fields['note'].widget.attrs['style']           =   "height:300px;"

class TagsForm(Form):
    tag     =   ModelMultipleChoiceField(Tags.objects.filter().order_by('tag'))

class NewTagsForm(ModelForm):
    class Meta:
        model   =   Tags
        fields = ['tag']
