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

def DISPATCH(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    put_view = kwargs.pop('PUT', None)
    delete_view = kwargs.pop('DELETE', None)

    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    elif request.method == 'PUT' and put_view is not None:
        return put_view(request, *args, **kwargs)
    elif request.method == 'DELETE' and delete_view is not None:
        return delete_view(request, *args, **kwargs)

    raise Http404

##################################################################

## url: /api/config.FMT
## method: read_config
## args: 
def read_config(request, *args, **kwargs):
    raise Http404('method read_config for url /api/config.FMT is not yet implemented')

## url: /api/config.FMT
## method: create_config
## args: 
def create_config(request, *args, **kwargs):
    raise Http404('method create_config for url /api/config.FMT is not yet implemented')

## url: /api/item.FMT
## method: read_item_list
## args: 
def read_item_list(request, *args, **kwargs):
    raise Http404('method read_item_list for url /api/item.FMT is not yet implemented')

## url: /api/item.FMT
## method: create_item
## args: 
def create_item(request, *args, **kwargs):
    raise Http404('method create_item for url /api/item.FMT is not yet implemented')

## url: /api/item/IID
## method: read_item_data
## args: iid
def read_item_data(request, iid, *args, **kwargs):
    raise Http404('method read_item_data for url /api/item/IID is not yet implemented')

## url: /api/item/IID
## method: create_item_data
## args: iid
def create_item_data(request, iid, *args, **kwargs):
    raise Http404('method create_item_data for url /api/item/IID is not yet implemented')

## url: /api/item/IID.FMT
## method: delete_item
## args: iid
def delete_item(request, iid, *args, **kwargs):
    raise Http404('method delete_item for url /api/item/IID.FMT is not yet implemented')

## url: /api/item/IID.FMT
## method: read_item
## args: iid
def read_item(request, iid, *args, **kwargs):
    raise Http404('method read_item for url /api/item/IID.FMT is not yet implemented')

## url: /api/item/IID/CID.FMT
## method: delete_comment
## args: iid cid
def delete_comment(request, iid, cid, *args, **kwargs):
    raise Http404('method delete_comment for url /api/item/IID/CID.FMT is not yet implemented')

## url: /api/item/IID/CID.FMT
## method: read_comment
## args: iid cid
def read_comment(request, iid, cid, *args, **kwargs):
    raise Http404('method read_comment for url /api/item/IID/CID.FMT is not yet implemented')

## url: /api/item/IID/CID/key.FMT
## method: create_comment_key
## args: iid cid
def create_comment_key(request, iid, cid, *args, **kwargs):
    raise Http404('method create_comment_key for url /api/item/IID/CID/key.FMT is not yet implemented')

## url: /api/item/IID/CID/key/KEY.FMT
## method: delete_comment_key
## args: iid cid key
def delete_comment_key(request, iid, cid, key, *args, **kwargs):
    raise Http404('method delete_comment_key for url /api/item/IID/CID/key/KEY.FMT is not yet implemented')

## url: /api/item/IID/CID/key/KEY.FMT
## method: read_comment_key
## args: iid cid key
def read_comment_key(request, iid, cid, key, *args, **kwargs):
    raise Http404('method read_comment_key for url /api/item/IID/CID/key/KEY.FMT is not yet implemented')

## url: /api/item/IID/CID/key/KEY.FMT
## method: create_comment_key
## args: iid cid key
def create_comment_key(request, iid, cid, key, *args, **kwargs):
    raise Http404('method create_comment_key for url /api/item/IID/CID/key/KEY.FMT is not yet implemented')

## url: /api/item/IID/clone.FMT
## method: read_clone_list
## args: iid
def read_clone_list(request, iid, *args, **kwargs):
    raise Http404('method read_clone_list for url /api/item/IID/clone.FMT is not yet implemented')

## url: /api/item/IID/clone.FMT
## method: create_clone
## args: iid
def create_clone(request, iid, *args, **kwargs):
    raise Http404('method create_clone for url /api/item/IID/clone.FMT is not yet implemented')

## url: /api/item/IID/comment.FMT
## method: read_comment_list
## args: iid
def read_comment_list(request, iid, *args, **kwargs):
    raise Http404('method read_comment_list for url /api/item/IID/comment.FMT is not yet implemented')

## url: /api/item/IID/comment.FMT
## method: create_comment
## args: iid
def create_comment(request, iid, *args, **kwargs):
    raise Http404('method create_comment for url /api/item/IID/comment.FMT is not yet implemented')

## url: /api/item/IID/key.FMT
## method: create_item_key
## args: iid
def create_item_key(request, iid, *args, **kwargs):
    raise Http404('method create_item_key for url /api/item/IID/key.FMT is not yet implemented')

## url: /api/item/IID/key/KEY.FMT
## method: delete_item_key
## args: iid key
def delete_item_key(request, iid, key, *args, **kwargs):
    raise Http404('method delete_item_key for url /api/item/IID/key/KEY.FMT is not yet implemented')

## url: /api/item/IID/key/KEY.FMT
## method: read_item_key
## args: iid key
def read_item_key(request, iid, key, *args, **kwargs):
    raise Http404('method read_item_key for url /api/item/IID/key/KEY.FMT is not yet implemented')

## url: /api/item/IID/key/KEY.FMT
## method: create_item_key
## args: iid key
def create_item_key(request, iid, key, *args, **kwargs):
    raise Http404('method create_item_key for url /api/item/IID/key/KEY.FMT is not yet implemented')

## url: /api/relation.FMT
## method: read_relation_list
## args: 
def read_relation_list(request, *args, **kwargs):
    raise Http404('method read_relation_list for url /api/relation.FMT is not yet implemented')

## url: /api/relation.FMT
## method: create_relation
## args: 
def create_relation(request, *args, **kwargs):
    raise Http404('method create_relation for url /api/relation.FMT is not yet implemented')

## url: /api/relation/RID.FMT
## method: delete_relation
## args: rid
def delete_relation(request, rid, *args, **kwargs):
    raise Http404('method delete_relation for url /api/relation/RID.FMT is not yet implemented')

## url: /api/relation/RID.FMT
## method: read_relation
## args: rid
def read_relation(request, rid, *args, **kwargs):
    raise Http404('method read_relation for url /api/relation/RID.FMT is not yet implemented')

## url: /api/relation/RID/key.FMT
## method: create_relation_key
## args: rid
def create_relation_key(request, rid, *args, **kwargs):
    raise Http404('method create_relation_key for url /api/relation/RID/key.FMT is not yet implemented')

## url: /api/relation/RID/key/KEY.FMT
## method: delete_relation_key
## args: rid key
def delete_relation_key(request, rid, key, *args, **kwargs):
    raise Http404('method delete_relation_key for url /api/relation/RID/key/KEY.FMT is not yet implemented')

## url: /api/relation/RID/key/KEY.FMT
## method: read_relation_key
## args: rid key
def read_relation_key(request, rid, key, *args, **kwargs):
    raise Http404('method read_relation_key for url /api/relation/RID/key/KEY.FMT is not yet implemented')

## url: /api/relation/RID/key/KEY.FMT
## method: create_relation_key
## args: rid key
def create_relation_key(request, rid, key, *args, **kwargs):
    raise Http404('method create_relation_key for url /api/relation/RID/key/KEY.FMT is not yet implemented')

## url: /api/select/item.FMT
## method: read_select_item
## args: 
def read_select_item(request, *args, **kwargs):
    raise Http404('method read_select_item for url /api/select/item.FMT is not yet implemented')

## url: /api/select/relation.FMT
## method: read_select_relation
## args: 
def read_select_relation(request, *args, **kwargs):
    raise Http404('method read_select_relation for url /api/select/relation.FMT is not yet implemented')

## url: /api/select/tag.FMT
## method: read_select_tag
## args: 
def read_select_tag(request, *args, **kwargs):
    raise Http404('method read_select_tag for url /api/select/tag.FMT is not yet implemented')

## url: /api/tag.FMT
## method: read_tag_list
## args: 
def read_tag_list(request, *args, **kwargs):
    raise Http404('method read_tag_list for url /api/tag.FMT is not yet implemented')

## url: /api/tag.FMT
## method: create_tag
## args: 
def create_tag(request, *args, **kwargs):
    raise Http404('method create_tag for url /api/tag.FMT is not yet implemented')

## url: /api/tag/TID.FMT
## method: delete_tag
## args: tid
def delete_tag(request, tid, *args, **kwargs):
    raise Http404('method delete_tag for url /api/tag/TID.FMT is not yet implemented')

## url: /api/tag/TID.FMT
## method: read_tag
## args: tid
def read_tag(request, tid, *args, **kwargs):
    raise Http404('method read_tag for url /api/tag/TID.FMT is not yet implemented')

## url: /api/tag/TID/key.FMT
## method: create_tag_key
## args: tid
def create_tag_key(request, tid, *args, **kwargs):
    raise Http404('method create_tag_key for url /api/tag/TID/key.FMT is not yet implemented')

## url: /api/tag/TID/key/KEY.FMT
## method: delete_tag_key
## args: tid key
def delete_tag_key(request, tid, key, *args, **kwargs):
    raise Http404('method delete_tag_key for url /api/tag/TID/key/KEY.FMT is not yet implemented')

## url: /api/tag/TID/key/KEY.FMT
## method: read_tag_key
## args: tid key
def read_tag_key(request, tid, key, *args, **kwargs):
    raise Http404('method read_tag_key for url /api/tag/TID/key/KEY.FMT is not yet implemented')

## url: /api/tag/TID/key/KEY.FMT
## method: create_tag_key
## args: tid key
def create_tag_key(request, tid, key, *args, **kwargs):
    raise Http404('method create_tag_key for url /api/tag/TID/key/KEY.FMT is not yet implemented')

## url: /api/url/RID.FMT
## method: read_encode_minekey
## args: rid
def read_encode_minekey1(request, rid, *args, **kwargs):
    raise Http404('method read_encode_minekey1 for url /api/url/RID.FMT is not yet implemented')

## url: /api/url/RID/IID.FMT
## method: read_encode_minekey
## args: rid iid
def read_encode_minekey2(request, rid, iid, *args, **kwargs):
    raise Http404('method read_encode_minekey2 for url /api/url/RID/IID.FMT is not yet implemented')

## url: /api/url/RID/RVSN/IID.FMT
## method: read_encode_minekey
## args: rid rvsn iid
def read_encode_minekey3(request, rid, rvsn, iid, *args, **kwargs):
    raise Http404('method read_encode_minekey3 for url /api/url/RID/RVSN/IID.FMT is not yet implemented')

## url: /api/version.FMT
## method: read_version
## args: 
def read_version(request, *args, **kwargs):
    raise Http404('method read_version for url /api/version.FMT is not yet implemented')
