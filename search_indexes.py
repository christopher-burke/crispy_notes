import datetime
from haystack import indexes
from crispy_notes.models import Notes


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text            =   indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Notes

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
