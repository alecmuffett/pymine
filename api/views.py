#!/usr/bin/env python
##
## Copyright 2010 Adriana Lukas & Alec Muffett
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

"""docstring goes here""" # :-)

from django.conf import settings
from django.http import HttpResponse

from pymine.api.envelope import Envelope
from pymine.api.models import Comment, Item, Registry

import pymine.util.httpserve as httpserve

##################################################################

# this definition (create_comment) is auto-generated.
# ensure that any changes are made via the generator.
def create_comment(request, idz, **kwargs):
    """
    arguments: request, idz, **kwargs
    implements: POST /api/comment/item/(IDZ).(FMT)
    returns: an envelope containing the comment structure
    """
    m = Comment.create(request, commentUponItem=int(idz))
    return Envelope(request, result={ m.thing_prefix : m.to_structure(request) })

##################################################################

# this definition (create_thing) is auto-generated.
# ensure that any changes are made via the generator.
def create_thing(request, thyng, **kwargs):
    """
    arguments: request, thyng, **kwargs
    implements: POST /api/feed.(FMT)
    implements: POST /api/item.(FMT)
    implements: POST /api/tag.(FMT)
    implements: POST /api/vurl.(FMT)
    returns: an envelope containing the thing structure
    """
    m = thyng.create(request)

    convert = getattr(m, 'to_structure', None)

    if convert: # its a single Thing
	s = { m.thing_prefix : convert(request) }
    else: # is a list of Thing, or something that we assume to be sane
	s = m

    return Envelope(request, result=s)

##################################################################

# this definition (delete_registry_attr) is auto-generated.
# ensure that any changes are made via the generator.
def delete_registry_attr(request, rattr, **kwargs):
    """
    arguments: request, rattr, **kwargs
    implements: DELETE /api/registry/(RATTR).(FMT)
    returns: an empty envelope
    """
    m = Registry.get(key=rattr)
    m.delete()
    return Envelope(request, result=0)

##################################################################

# this definition (delete_thing) is auto-generated.
# ensure that any changes are made via the generator.
def delete_thing(request, thyng, id, **kwargs):
    """
    arguments: request, thyng, id, **kwargs
    implements: DELETE /api/comment/(ID).(FMT)
    implements: DELETE /api/feed/(ID).(FMT)
    implements: DELETE /api/item/(ID).(FMT)
    implements: DELETE /api/tag/(ID).(FMT)
    implements: DELETE /api/vurl/(ID).(FMT)
    returns: an empty envelope
    """

    m = thyng.get(id=int(id))
    m.delete()
    return Envelope(request, result=0)

##################################################################

# this definition (delete_thing_attr) is auto-generated.
# ensure that any changes are made via the generator.
def delete_thing_attr(request, thyng, id, attr, **kwargs):
    """
    arguments: request, thyng, id, attr, **kwargs
    implements: DELETE /api/comment/(ID)/(ATTR).(FMT)
    implements: DELETE /api/feed/(ID)/(ATTR).(FMT)
    implements: DELETE /api/item/(ID)/(ATTR).(FMT)
    implements: DELETE /api/tag/(ID)/(ATTR).(FMT)
    implements: DELETE /api/vurl/(ID)/(ATTR).(FMT)
    returns: ...
    """
    m = thyng.get(id=int(id))
    m.delete_attribute(attr)
    return Envelope(request, result={ m.thing_prefix : m.to_structure(request) })

##################################################################

# this definition (encode_minekey) is auto-generated.
# ensure that any changes are made via the generator.
def encode_minekey(request, **kwargs):
    """
    arguments: request, **kwargs
    implements: POST /api/encode.(FMT)
    returns: ...
    """
    s = {}
    return Envelope(request, result=s)

##################################################################

# this definition (get_registry_attr) is auto-generated.
# ensure that any changes are made via the generator.
def get_registry_attr(request, rattr, **kwargs):
    """
    arguments: request, rattr, **kwargs
    implements: GET /api/registry/(RATTR).(FMT)
    returns: ...
    """
    m = Registry.get(key=rattr)
    return Envelope(request, result=m.value)

##################################################################

# this definition (get_thing_attr) is auto-generated.
# ensure that any changes are made via the generator.
def get_thing_attr(request, thyng, id, attr, **kwargs):
    """
    arguments: request, thyng, id, attr, **kwargs
    implements: GET /api/comment/(ID)/(ATTR).(FMT)
    implements: GET /api/feed/(ID)/(ATTR).(FMT)
    implements: GET /api/item/(ID)/(ATTR).(FMT)
    implements: GET /api/tag/(ID)/(ATTR).(FMT)
    implements: GET /api/vurl/(ID)/(ATTR).(FMT)
    returns: ...
    """
    m = thyng.get(id=int(id))
    s = m.to_structure(request)
    return Envelope(request, result=s[attr]) # throw exception if not there

##################################################################

# this definition (list_comments) is auto-generated.
# ensure that any changes are made via the generator.
def list_comments(request, idz, **kwargs):
    """
    arguments: request, idz, **kwargs
    implements: GET /api/comment/item/(IDZ).(FMT)
    returns: ...
    """

    iid = int(idz)

    if iid == 0:
	qs = Comment.list()
    else:
	item = Item.get(id=iid)
	qs = item.comment_set.filter(is_deleted=False)

    if 'query' in request.REQUEST:
	qs = Comment.execute_search_query(request.REQUEST['query'], qs)

    result = [ { m.thing_prefix : m.to_structure(request) } for m in qs ]
    return Envelope(request, result=result)

##################################################################

# this definition (list_registry) is auto-generated.
# ensure that any changes are made via the generator.
def list_registry(request, **kwargs):
    """
    arguments: request, **kwargs
    implements: GET /api/registry.(FMT)
    returns: ...
    """
    qs = Registry.objects.all()
    result = [ m.to_structure(request) for m in qs ]
    return Envelope(request, result=result)

##################################################################

# this definition (list_things) is auto-generated.
# ensure that any changes are made via the generator.
def list_things(request, thyng, **kwargs):
    """
    arguments: request, thyng, **kwargs
    implements: GET /api/feed.(FMT)
    implements: GET /api/item.(FMT)
    implements: GET /api/tag.(FMT)
    implements: GET /api/vurl.(FMT)
    returns: ...
    """
    qs = thyng.list()

    if 'query' in request.REQUEST:
	qs = thyng.execute_search_query(request.REQUEST['query'], qs)

    result = [ { m.thing_prefix : m.to_structure(request) } for m in qs ]
    return Envelope(request, result=result)

##################################################################

# this definition (read_item_data) is auto-generated.
# ensure that any changes are made via the generator.
def read_item_data(request, id, token, **kwargs):
    """
    arguments: request, id, token, **kwargs
    implements: GET /api/data/(ID)(/TOKEN)
    returns: ...
    """

    m = Item.get(id=int(id))
    ct = m.data_type

    if m.data:
	f = m.data.chunks()
	response = HttpResponse(f, content_type=ct)
	response['Content-Length'] = m.data.size
    else:
        d = m.feed_description()
	response = HttpResponse(d)
	response['Content-Length'] = len(d)

    return response

##################################################################

# this definition (read_item_icon) is auto-generated.
# ensure that any changes are made via the generator.
def read_item_icon(request, id, token, **kwargs):
    """
    arguments: request, id, token, **kwargs
    implements: GET /api/icon/(ID)(/TOKEN)
    returns: ...
    """
    return httpserve.httpserve_path(request, 'images/icon.png')

##################################################################

# this definition (read_thing) is auto-generated.
# ensure that any changes are made via the generator.
def read_thing(request, thyng, id, **kwargs):
    """
    arguments: request, thyng, id, **kwargs
    implements: GET /api/comment/(ID).(FMT)
    implements: GET /api/feed/(ID).(FMT)
    implements: GET /api/item/(ID).(FMT)
    implements: GET /api/tag/(ID).(FMT)
    implements: GET /api/vurl/(ID).(FMT)
    returns: ...
    """
    m = thyng.get(id=int(id))
    return Envelope(request, result={ m.thing_prefix : m.to_structure(request) })

##################################################################

# this definition (read_version) is auto-generated.
# ensure that any changes are made via the generator.
def read_version(request, **kwargs):
    """
    arguments: request, **kwargs
    implements: GET /api/version.(FMT)
    returns: ...
    """
    vinfo = {
	'mineApiVersion': settings.MINE_API_VERSION,
	'softwareName': settings.MINE_SW_NAME,
	'softwareMajorVersion': settings.MINE_SW_MAJOR_VERSION,
	'softwareMinorVersion': settings.MINE_SW_MINOR_VERSION,
	'softwareStatus': settings.MINE_SW_STATUS,
	}
    return Envelope(request, result=dict(version=vinfo))

##################################################################

# this definition (update_registry_attr) is auto-generated.
# ensure that any changes are made via the generator.
def update_registry_attr(request, rattr, **kwargs):
    """
    arguments: request, rattr, **kwargs
    implements: POST /api/registry/(RATTR).(FMT)
    returns: ...
    """
    v = request.POST[rattr]
    m, created = Registry.objects.get_or_create(key=rattr, defaults={ 'value': v })
    if not created: # then it will need updating
	m.value = v
	m.save();
    return Envelope(request, result=m.to_structure(request))

##################################################################

# this definition (update_thing) is auto-generated.
# ensure that any changes are made via the generator.
def update_thing(request, thyng, id, **kwargs):
    """
    arguments: request, thyng, id, **kwargs
    implements: POST /api/comment/(ID).(FMT)
    implements: POST /api/feed/(ID).(FMT)
    implements: POST /api/item/(ID).(FMT)
    implements: POST /api/tag/(ID).(FMT)
    implements: POST /api/vurl/(ID).(FMT)
    returns: ...
    """
    m = thyng.get(id=int(id))
    m = m.update(request)
    return Envelope(request, result={ m.thing_prefix : m.to_structure(request) })

##################################################################
