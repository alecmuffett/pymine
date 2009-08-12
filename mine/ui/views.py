#!/usr/bin/python
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

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

##################################################################

## rest: GET /ui
## function: read_ui_root
## declared args: 
def read_ui_root(request, *args, **kwargs):
    raise Http404('backend read_ui_root for GET /ui is not yet implemented') # TO BE DONE
    return render_to_response('read-ui-root.html')

## rest: GET /ui/create-comment/IID.html
## function: create_comment
## declared args: iid
def create_comment(request, iid, *args, **kwargs):
    raise Http404('backend create_comment for GET /ui/create-comment/IID.html is not yet implemented') # TO BE DONE
    return render_to_response('create-comment.html')

## rest: GET /ui/create-item.html
## function: create_item
## declared args: 
def create_item(request, *args, **kwargs):
    raise Http404('backend create_item for GET /ui/create-item.html is not yet implemented') # TO BE DONE
    return render_to_response('create-item.html')

## rest: GET /ui/create-relation.html
## function: create_relation
## declared args: 
def create_relation(request, *args, **kwargs):
    raise Http404('backend create_relation for GET /ui/create-relation.html is not yet implemented') # TO BE DONE
    return render_to_response('create-relation.html')

## rest: GET /ui/create-tag.html
## function: create_tag
## declared args: 
def create_tag(request, *args, **kwargs):
    raise Http404('backend create_tag for GET /ui/create-tag.html is not yet implemented') # TO BE DONE
    return render_to_response('create-tag.html')

## rest: GET /ui/delete-comment/IID/CID.html
## function: delete_comment
## declared args: iid cid
def delete_comment(request, iid, cid, *args, **kwargs):
    raise Http404('backend delete_comment for GET /ui/delete-comment/IID/CID.html is not yet implemented') # TO BE DONE
    return render_to_response('delete-comment.html')

## rest: GET /ui/delete-item/IID.html
## function: delete_item
## declared args: iid
def delete_item(request, iid, *args, **kwargs):
    raise Http404('backend delete_item for GET /ui/delete-item/IID.html is not yet implemented') # TO BE DONE
    return render_to_response('delete-item.html')

## rest: GET /ui/delete-relation/RID.html
## function: delete_relation
## declared args: rid
def delete_relation(request, rid, *args, **kwargs):
    raise Http404('backend delete_relation for GET /ui/delete-relation/RID.html is not yet implemented') # TO BE DONE
    return render_to_response('delete-relation.html')

## rest: GET /ui/delete-tag/TID.html
## function: delete_tag
## declared args: tid
def delete_tag(request, tid, *args, **kwargs):
    raise Http404('backend delete_tag for GET /ui/delete-tag/TID.html is not yet implemented') # TO BE DONE
    return render_to_response('delete-tag.html')

## rest: GET /ui/list-comments/IID.html
## function: list_comments
## declared args: iid
def list_comments(request, iid, *args, **kwargs):
    raise Http404('backend list_comments for GET /ui/list-comments/IID.html is not yet implemented') # TO BE DONE
    return render_to_response('list-comments.html')

## rest: GET /ui/list-items.html
## function: list_items
## declared args: 
def list_items(request, *args, **kwargs):
    raise Http404('backend list_items for GET /ui/list-items.html is not yet implemented') # TO BE DONE
    return render_to_response('list-items.html')

## rest: GET /ui/list-relations.html
## function: list_relations
## declared args: 
def list_relations(request, *args, **kwargs):
    raise Http404('backend list_relations for GET /ui/list-relations.html is not yet implemented') # TO BE DONE
    return render_to_response('list-relations.html')

## rest: GET /ui/list-tags.html
## function: list_tags
## declared args: 
def list_tags(request, *args, **kwargs):
    raise Http404('backend list_tags for GET /ui/list-tags.html is not yet implemented') # TO BE DONE
    return render_to_response('list-tags.html')

## rest: GET /ui/read-comment/IID/CID.html
## function: read_comment
## declared args: iid cid
def read_comment(request, iid, cid, *args, **kwargs):
    raise Http404('backend read_comment for GET /ui/read-comment/IID/CID.html is not yet implemented') # TO BE DONE
    return render_to_response('read-comment.html')

## rest: GET /ui/read-item/IID.html
## function: read_item
## declared args: iid
def read_item(request, iid, *args, **kwargs):
    raise Http404('backend read_item for GET /ui/read-item/IID.html is not yet implemented') # TO BE DONE
    return render_to_response('read-item.html')

## rest: GET /ui/read-registry.html
## function: read_registry
## declared args: 
def read_registry(request, *args, **kwargs):
    raise Http404('backend read_registry for GET /ui/read-registry.html is not yet implemented') # TO BE DONE
    return render_to_response('read-registry.html')

## rest: GET /ui/read-relation/RID.html
## function: read_relation
## declared args: rid
def read_relation(request, rid, *args, **kwargs):
    raise Http404('backend read_relation for GET /ui/read-relation/RID.html is not yet implemented') # TO BE DONE
    return render_to_response('read-relation.html')

## rest: GET /ui/read-tag/TID.html
## function: read_tag
## declared args: tid
def read_tag(request, tid, *args, **kwargs):
    raise Http404('backend read_tag for GET /ui/read-tag/TID.html is not yet implemented') # TO BE DONE
    return render_to_response('read-tag.html')

## rest: GET /ui/update-comment/IID/CID.html
## function: update_comment
## declared args: iid cid
def update_comment(request, iid, cid, *args, **kwargs):
    raise Http404('backend update_comment for GET /ui/update-comment/IID/CID.html is not yet implemented') # TO BE DONE
    return render_to_response('update-comment.html')

## rest: GET /ui/update-item/IID.html
## function: update_item
## declared args: iid
def update_item(request, iid, *args, **kwargs):
    raise Http404('backend update_item for GET /ui/update-item/IID.html is not yet implemented') # TO BE DONE
    return render_to_response('update-item.html')

## rest: GET /ui/update-registry.html
## function: update_registry
## declared args: 
def update_registry(request, *args, **kwargs):
    raise Http404('backend update_registry for GET /ui/update-registry.html is not yet implemented') # TO BE DONE
    return render_to_response('update-registry.html')

## rest: GET /ui/update-relation/RID.html
## function: update_relation
## declared args: rid
def update_relation(request, rid, *args, **kwargs):
    raise Http404('backend update_relation for GET /ui/update-relation/RID.html is not yet implemented') # TO BE DONE
    return render_to_response('update-relation.html')

## rest: GET /ui/update-tag/TID.html
## function: update_tag
## declared args: tid
def update_tag(request, tid, *args, **kwargs):
    raise Http404('backend update_tag for GET /ui/update-tag/TID.html is not yet implemented') # TO BE DONE
    return render_to_response('update-tag.html')

## rest: GET /ui/version.html
## function: version
## declared args: 
def version(request, *args, **kwargs):
    raise Http404('backend version for GET /ui/version.html is not yet implemented') # TO BE DONE
    return render_to_response('version.html')

