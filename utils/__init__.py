from __future__ import unicode_literals
from django.utils.html import strip_tags
from haystack.utils import Highlighter

class WordHighlighter(Highlighter):

    def __init__(self,  query, **kwargs):
        super(WordHighlighter, self).__init__(query, **kwargs)
        self.title = True


    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if self.title == True:
            return self.render_html(highlight_locations, 0, len(self.text_block)+1)
        return self.render_html(highlight_locations, start_offset, end_offset)
