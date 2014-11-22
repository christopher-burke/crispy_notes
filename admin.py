from django.contrib import admin
from crispy_notes.models import *


class OwnerAdmin(admin.ModelAdmin):
    pass
class NotesAdmin(admin.ModelAdmin):
    class Media:
        js = (
            '/static/tinymce/tinymce.min.js',
            )
class TagsAdmin(admin.ModelAdmin):
    pass
class Note_TagsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Owner,OwnerAdmin)
admin.site.register(Notes,NotesAdmin)
admin.site.register(Tags,TagsAdmin)
admin.site.register(Note_Tags,Note_TagsAdmin)
