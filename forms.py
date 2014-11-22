from crispy_notes.models import Notes
from django import forms
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

class NotesSearchForm(SearchForm):

    def search(self):
        # First, store the SearchQuerySet received from other processing. (the main work is run internally by Haystack here).
        sqs = super(NotesSearchForm, self).search()
        # if something goes wrong
        if not self.is_valid():
            return self.no_query_found()

        # you can then adjust the search results and ask for instance to order the results by title

        #sqs = SearchQuerySet().filter(content__startswith=self.cleaned_data['q'])
        return sqs
