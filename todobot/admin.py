from django.contrib import admin
from .models import *


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "is_active", "uid", "created_at", "updated_at"]
    list_display_links = ["id", "title"]    
    search_fields = ["title",]
    save_on_top = True
    save_as = True

admin.site.register(Uid)

admin.site.site_title = "ToDoBot 0.1"
admin.site.site_header = "ToDoBot 0.1"
