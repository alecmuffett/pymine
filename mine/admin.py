##
## Copyright 2009 Adriana Lukas & Alec Muffett
##
## Licensed under the Apache License, Version 2.0 (the "License"); you
## may not use this file except in compliance with the License. You
## may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
## implied. See the License for the specific language governing
## permissions and limitations under the License.
##

from pymine.mine.models import Tag, Relation, Item, Comment, VanityURL
from django.contrib import admin

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_modified', 'created')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['name']}), 
        ('Advanced', {'fields': ['description', 'implies']}), 
        ('Debugging', {'fields': ['cached_implications'], 'classes': ['collapse']}), 
        ]

class RelationAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'last_modified', 'created')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['name', 'version', 'description', 'tags']}), 
        ('Advanced Tags', {'fields': ['tags_required', 'tags_excluded'], 'classes': ['collapse']}), 
        ('Contact Information', {'fields': ['email_address', 'url_homepage', 'url_image', 'url_callback']}), 
        ('Access Control', {'fields': ['embargo_before', 'embargo_after', 'network_pattern'], 'classes': ['collapse']}), 
        ]

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'content_type', 'last_modified', 'created')
    search_fields = ['name', 'description']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['name', 'status', 'content_type', 'description', 'tags']}), 
        ('Advanced Tags', {'fields': ['item_for_relations', 'item_not_relations'], 'classes': ['collapse']}), 
        ('Access Control', {'fields': ['hide_before', 'hide_after'], 'classes': ['collapse']}), 
        ]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'relation', 'item', 'likes', 'last_modified', 'created')
    search_fields = ['title', 'body']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['title', 'body', 'likes']}), 
        ('Advanced', {'fields': ['item', 'relation']}), 
        ]

class VanityURLAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'last_modified', 'created')
    search_fields = ['name']
    list_filter = ['created']
    date_hierarchy = 'created'
    fieldsets = [
        (None, {'fields': ['name', 'link']}), 
        ]

admin.site.register(Tag, TagAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(VanityURL, VanityURLAdmin)