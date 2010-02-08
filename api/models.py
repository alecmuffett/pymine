#!/usr/bin/python
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

#from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
#from django.template.loader import render_to_string
#from django.utils import feedgenerator
from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.db import models, transaction
from django.db.models import Q
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote

import base64
import os
import string

import util.base58 as base58

# TODO:
# phrase tags
# xattrs are represented as $thingAttribute
# envelope for creation can deal with single and multiple returns for create()
# envelope removes status and exit
# multiple file uploads for create
# status flag becomes a bitfield / typed coersce field
# garbage collection for delete

##################################################################
##################################################################
##################################################################

item_fss = FileSystemStorage(location = settings.MINE_DBDIR_FILES)
icon_fss = FileSystemStorage(location = settings.MINE_DBDIR_ICONS)
comment_fss = FileSystemStorage(location = settings.MINE_DBDIR_COMMENTS)
fss_yyyymmdd = '%Y-%m/%d'

##################################################################

item_status_choices = (
    ( '0', 'locked' ),
    ( '2', 'linkable-by-items-in-feeds' ),
    ( '4', 'to-explicitly-cited-feeds' ),
    ( '6', 'to-private-feeds-via-tags' ),
    ( '8', 'to-public-feeds-via-tags' ),
    # In all instances, additional per-item "not:feedname" explicit tagging will be honoured.
    # In all instances, additional per-feed "exclude:tag" explicit tagging will be honoured.
    )

# create a status-lookup table, long->short and short->long
# short->long is covered by m.get_status_display()

status_lookup = {}
for short, long in item_status_choices:
    status_lookup[long] = short

##################################################################

def random_bits(nbits):
    return base64.urlsafe_b64encode(os.urandom(nbits//8)).rstrip('=')

##################################################################

class Space:
    """library of conversion routines for passing stuff between s-space and m-space"""

    class r2s_lib:
	@staticmethod
	def bool(r, s, sattr):
	    """copy a field from a request, to a bool in a structure"""
	    s[sattr] = True if int(r.POST[sattr]) else False

	@staticmethod
	def integer(r, s, sattr):
	    """copy a field from a request, to an int in a structure"""
	    s[sattr] = int(r.POST[sattr])

	@staticmethod # THIS IS THE DEFAULT HARDCODED R2S_LIB METHOD
	def strip(r, s, sattr):
	    """copy a string from a request, to a string in a structure, stripping leading and trailing spaces"""
	    s[sattr] = str(r.POST[sattr]).strip()

	@staticmethod
	def verbatim(r, s, sattr):
	    """copy a string from a request, to a string in a structure, verbatim"""
	    s[sattr] = str(r.POST[sattr])

    class s2m_lib:
	@staticmethod
	def comment_from_feed(r, s, sattr, m, mattr):
	    """insert reference from a comment to the feed from which it was sourced"""
	    src = s[sattr]
	    dst = Feed.get(name=src)
	    setattr(m, mattr, dst)

	@staticmethod
	def comment_upon_item(r, s, sattr, m, mattr):
	    """insert reference from a comment to the item to which it refers"""
	    src = s[sattr]
	    dst = Item.get(id=src)
	    setattr(m, mattr, dst)

	@staticmethod
	def feed_interests(r, s, sattr, m, mattr):
	    """insert tags regarding which the feed is interested"""
	    dst = m.interests
	    dst.clear()
	    for x in s[sattr].split():
		dst.add(Tag.get_or_auto_tag(r, x))

	@staticmethod
	def feed_interests_exclude(r, s, sattr, m, mattr):
	    """insert tags regarding which the feed is not interested"""
	    dst = m.interests_exclude
	    dst.clear()
	    for x in s[sattr].split():
		dst.add(Tag.get_or_auto_tag(r, x))

	@staticmethod
	def feed_interests_require(r, s, sattr, m, mattr):
	    """insert tags regarding which the feed mandates requirement"""
	    dst = m.interests_require
	    dst.clear()
	    for x in s[sattr].split():
		dst.add(Tag.get_or_auto_tag(r, x))

	@staticmethod
	def item_for_feeds(r, s, sattr, m, mattr):
	    """insert feeds to which the item is explicitly to be fed"""
	    dst = m.for_feeds
	    dst.clear()
	    for x in s[sattr].split():
		dst.add(Feed.get(name=x))

	@staticmethod
	def item_links_to_items(r, s, sattr, m, mattr):
	    """insert the list of items which this item encloses"""
	    dst = m.links_to_items
	    dst.clear()
	    for x in s[sattr].split():
		dst.add(Item.get(id=int(x)))

	@staticmethod
	def item_not_feeds(r, s, sattr, m, mattr):
	    """insert feeds for which the item is explicitly banned"""
	    dst = m.for_feeds
	    dst.clear()
	    for x in s[sattr].split():
		dst.add(Feed.get(name=x))

	@staticmethod
	def item_tags(r, s, sattr, m, mattr):
	    """ """
	    dst = m.tags
	    dst.clear()
	    for x in s[sattr].split():
		dst.add(Tag.get_or_auto_tag(r, x))

	@staticmethod
	def item_status(r, s, sattr, m, mattr):
	    """set the item statius"""
	    src = s[sattr]
	    setattr(m, mattr, status_lookup[src])

	@staticmethod
	def tag_implies(r, s, sattr, m, mattr):
	    """what tags does this tag imply"""
	    dst = m.implies
	    dst.clear()
	    for x in s[sattr].split():
		dst.add(Tag.get_or_auto_tag(r, x))

	@staticmethod
	def bool(r, s, sattr, m, mattr):
	    """copy a bool in a structure, to a bool in a model"""
	    if s[sattr]:
		setattr(m, mattr, True)
	    else:
		setattr(m, mattr, False)

	@staticmethod
	def copy(r, s, sattr, m, mattr):
	    """copy a field in a structure, to a field in a model, preserving type"""
	    setattr(m, mattr, s[sattr])

	@staticmethod
	def date(r, s, sattr, m, mattr):
	    """copy a date in a structure, to a date in a model"""
	    raise RuntimeError, "not yet integrated the Date parser"

	@staticmethod
	def strip(r, s, sattr, m, mattr):
	    """copy a field (assume type string) in a structure, to a string in a model, stripping leading and trailing spaces"""
	    setattr(m, mattr, s[sattr].strip())

    # m2s must currently check for null before copy/set
    class m2s_lib:
	@staticmethod
	def comment_from_feed(r, m, mattr, s, sattr):
	    """what feed is the comment from?"""
            s[sattr] = getattr(m, mattr).name

	@staticmethod
	def comment_upon_item(r, m, mattr, s, sattr):
	    """what item is the comment upon"""
            s[sattr] = getattr(m, mattr).id

	@staticmethod
	def feed_interests(r, m, mattr, s, sattr):
	    """these tags are relevant to my interests"""
            src = m.interests
            x = " ".join([ x.name for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def feed_interests_exclude(r, m, mattr, s, sattr):
	    """these tags are not relevant to my interests"""
            src = m.interests_exclude
            x = " ".join([ x.name for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def feed_interests_require(r, m, mattr, s, sattr):
	    """these tags are required for my interest"""
            src = m.interests_require
            x = " ".join([ x.name for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def item_for_feeds(r, m, mattr, s, sattr):
	    """this item is destined for..."""
            src = m.for_feeds
            x = " ".join([ x.name for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def item_links_to_items(r, m, mattr, s, sattr):
            """this item contains..."""
            src = m.links_to_items
            x = " ".join([ str(x.id) for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def item_not_feeds(r, m, mattr, s, sattr):
	    """this item is banned from being seen by..."""
            src = m.not_feeds
            x = " ".join([ x.name for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def item_tags(r, m, mattr, s, sattr):
            """this item is tagged..."""
            src = m.tags
            x = " ".join([ x.name for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def item_status(r, m, mattr, s, sattr):
	    """ """
	    pass

	@staticmethod
	def tag_cloud(r, m, mattr, s, sattr):
            """this tag has the following cloud of indirect implications..."""
            src = m.cloud
            x = ' '.join([ x.name for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def tag_implies(r, m, mattr, s, sattr):
            """this tag has the following implications..."""
            src = m.implies
            x = ' '.join([ x.name for x in src.all() ])
            if x: s[sattr] = x

	@staticmethod
	def bool(r, m, mattr, s, sattr):
	    """copy a field in a model, to a field in a structure"""
	    x = getattr(m, mattr)
	    if x:
		s[sattr] = 1
	    else:
		s[sattr] = 0

	@staticmethod
	def copy(r, m, mattr, s, sattr):
	    """copy a field in a model, to a field in a structure, preserving type"""
	    x = getattr(m, mattr)
	    if x: s[sattr] = x

	@staticmethod
	def date(r, m, mattr, s, sattr):
	    """copy a date in a model, to a date in a structure"""
	    x = getattr(m, mattr)
	    if x: s[sattr] = x.isoformat()

    class gc_lib:
	@staticmethod
	def skip(m, mattr):
	    """do not trash a field"""
	    pass

	@staticmethod
	def nullify(m, mattr):
	    """trash a field in a model, by nulling it (not secure delete). requires save()"""
	    setattr(m, matter, None)

	@staticmethod
	def blankify(m, mattr):
	    """trash a field in a model by blanking it (not secure delete). requires save()"""
	    setattr(m, matter, "")

	@staticmethod
	def zeroify(m, mattr):
	    """trash a field in a model by setting it to 0 (not secure delete). requires save()"""
	    setattr(m, matter, 0)

	@staticmethod
	def falsify(m, mattr):
	    """trash a field in a model by setting it to False (not secure delete). requires save()"""
	    setattr(m, matter, False)

	@staticmethod
	def munge(m, mattr):
	    """trash a field in a model by filling it with hopefully unique garbage (not secure delete). requires save()"""
	    setattr(m, mattr, "__%s_%d_%s__" % (mattr, m.id, random_bits(128)))

	@staticmethod
	def reflist(m, mattr):
	    """trash a field in a model, by unreferencing the contents (not secure delete). requires save()"""
	    pass

	@staticmethod
	def file(m, mattr):
	    """trash a file in a model by deleting it (not likely to be secure delete).  requires save()"""
	    pass

	@staticmethod
	def item_status(m, mattr):
	    """trash item.status_choice.  requires save()"""
	    m.status = item_status_choices[0][0]

    @staticmethod
    def compile(attr_map):
	"""
	return the three compiled conversion tables for moving/updating a thing between
	r- to s- space
	s- to m- space
	m- to s- space
	"""

	r2s = {}
	s2m = {}
	m2s = {}
	gc = {}

	defer_table = {
	    'commentFromFeed': True,
	    'commentUponItem': True,
	    'feedInterests': True,
	    'feedInterestsExclude': True,
	    'feedInterestsRequire': True,
	    'itemData': True,
	    'itemForFeeds': True,
	    'itemIcon': True,
	    'itemLinksToItems': True,
	    'itemNotFeeds': True,
	    'itemTags': True,
	    'tagCloud': True,
	    'tagImplies': True,
	    }

	def barf(direction, mattr, sattr):
	    """to be called when methud exists but is empty"""
	    raise RuntimeError, 'blank methud for %s, %s, %s' % (direction, mattr, sattr)

	prefix = attr_map.pop('__prefix__')

	# for an explanation of the weird closure default arguments, see:
	# http://code.activestate.com/recipes/502271/ regarding test2()

	for mattr in attr_map.keys():
	    table = attr_map[mattr]
	    sattr = prefix + "".join([ string.capitalize(x) for x in mattr.split("_") ])

	    # print prefix + "." + mattr, "->", sattr
	    # print table

	    if 'm2s' in table:
		methud = getattr(Space.m2s_lib, table['m2s'])
		if not methud:
		    barf('m2s', mattr, sattr)

		def m2s_closure(r, m, s, mattr=mattr, sattr=sattr, methud=methud):
		    if getattr(m, mattr):
			methud(r, m, mattr, s, sattr)

		m2s[mattr] = m2s_closure

	    if 's2m' in table:
		methud = getattr(Space.s2m_lib, table['s2m'])
		if not methud:
		    barf('s2m', mattr, sattr)

		def s2m_closure(r, s, m, sattr=sattr, mattr=mattr, methud=methud):
		    if sattr in s:
			methud(r, s, sattr, m, mattr)

		def r2s_closure(r, s, sattr=sattr):
		    if sattr in r.POST:
			Space.r2s_lib.strip(r, s, sattr)

		s2m[sattr] = ( defer_table.get(sattr, False), s2m_closure )
		r2s[sattr] = r2s_closure

	    if 'r2s' in table: # override default provided in s2m
		methud = getattr(Space.r2s_lib, table['r2s'])
		if not methud:
		    barf('r2s', mattr, sattr)

		def r2s_closure(r, s, sattr=sattr, methud=methud):
		    if sattr in r.POST:
			methud(r, s, sattr)

		r2s[sattr] = r2s_closure

	    if mattr == 'id':
		pass # id fields do not get gc'ed
	    elif 'gc' in table:
		methud = getattr(Space.gc_lib, table['gc'])
		gc[mattr] = lambda m: methud(m, mattr)
	    else:
		gc[mattr] = lambda m: gc_lib.nullify(m, mattr) # default nullify()

	return (r2s, s2m, m2s, gc)

##################################################################
##################################################################
##################################################################

class AbstractField:
    """superclass to frontend model fields and ease porting between GAE and Django"""

    STRING_SHORT = 256 # bytes

    class Meta:
	abstract = True

    @staticmethod
    def parse(input):
	"""
	Argument parser/translater for AbstractField.

	One dict comes in, another goes out.

	implements unique, symmetrical, storage, upload_to, pivot
	"""

	if input.get('required', True):
	    output = dict(null=False, blank=False)
	else:
	    output = dict(null=True, blank=True)

	for iname, oname in (('unique', 'unique'),
			     ('symmetrical', 'symmetrical'),
			     ('storage', 'storage'),
			     ('upload_to', 'upload_to'),
			     ('pivot', 'related_name'),
			     ):
	    if iname in input:
		output[oname] = input[iname]

	return output

    @staticmethod
    def bool(default):
	"""implements a bool (true/false)"""
	return models.BooleanField(default=default)

    @staticmethod
    def choice(choices):
	"""implements a choices-field (max length of an encoded choice is 1 character)"""
	return models.CharField(max_length=1, choices=choices)

    @staticmethod
    def created():
	"""implements created date"""
	return models.DateTimeField(auto_now_add=True)

    @staticmethod
    def datetime(**kwargs):
	"""implements date/time field"""
	x = AbstractField.parse(kwargs)
	return models.DateTimeField(**x)

    @staticmethod
    def file(**kwargs):
	"""implements a file"""
	x = AbstractField.parse(kwargs)
	return models.FileField(**x)

    @staticmethod
    def integer(default):
	"""implements an integer"""
	return models.PositiveIntegerField(default=default)

    @staticmethod
    def last_modified():
	"""implements last_modified date"""
	return models.DateTimeField(auto_now=True)

    @staticmethod
    def reference(what, **kwargs):
	"""implements foreign-keys"""
	x = AbstractField.parse(kwargs)
	return models.ForeignKey(what, **x)

    @staticmethod
    def reflist(what, **kwargs):
	"""implements list-of-foreign-keys; AbstractField.parses out 'pivot' argument"""
	x = AbstractField.parse(kwargs)
	return models.ManyToManyField(what, **x)

    @staticmethod
    def slug(**kwargs):
	"""implements a slug (alphanumeric string, no spaces)"""
	x = AbstractField.parse(kwargs)
	return models.SlugField(max_length=AbstractField.STRING_SHORT, **x)

    @staticmethod
    def string(**kwargs):
	"""implements string"""
	x = AbstractField.parse(kwargs)
	return models.CharField(max_length=AbstractField.STRING_SHORT, **x)

    @staticmethod
    def text(**kwargs):
	"""implements a text area / text of arbitrary size"""
	x = AbstractField.parse(kwargs)
	return models.TextField(**x)

    @staticmethod
    def url(**kwargs):
	"""implements a URL string"""
	x = AbstractField.parse(kwargs)
	return models.URLField(max_length=AbstractField.STRING_SHORT, **x)

##################################################################
##################################################################
##################################################################

class AbstractModel(models.Model):
    """superclass to frontend models and ease porting between GAE and Django"""

    class Meta:
	abstract = True

    created = AbstractField.created()
    last_modified = AbstractField.last_modified()

##################################################################
##################################################################
##################################################################

class AbstractXattr(AbstractModel):
    """superclass to frontend extended attributes"""

    class Meta:
	abstract = True

    key = AbstractField.slug()
    value = AbstractField.text()

    def __unicode__(self):
	"""return the name of this xattr"""
	return self.key

##################################################################

class TagXattr(AbstractXattr):
    """tag extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('tag', 'key')
	verbose_name = 'TagXattr'

    tag = AbstractField.reference('Tag')

##################################################################

class VurlXattr(AbstractXattr):
    """vurl extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('vurl', 'key')
	verbose_name = 'VurlXattr'

    vurl = AbstractField.reference('Vurl')

##################################################################

class FeedXattr(AbstractXattr):
    """feed extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('feed', 'key')
	verbose_name = 'FeedXattr'

    feed = AbstractField.reference('Feed')

##################################################################

class ItemXattr(AbstractXattr):
    """item extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('item', 'key')
	verbose_name = 'ItemXattr'

    item = AbstractField.reference('Item')

##################################################################

class CommentXattr(AbstractXattr):
    """comment extended attributes"""

    class Meta:
	ordering = ['key']
	unique_together = ('comment', 'key')
	verbose_name = 'CommentXattr'

    comment = AbstractField.reference('Comment')

##################################################################
##################################################################
##################################################################

class AbstractThing(AbstractModel):
    """superclass for all the major mine types"""

    class Meta:
	abstract = True

    attr_map = {
	'__prefix__': "thing",
	}

    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    id = 0
    name = 'thing'
    is_deleted = AbstractField.bool(False)

    @classmethod
    def create(klass, request=None, **kwargs):
	"""
	create a new Thing from a HTTPRequest, overriding with values from kwargs.

	NB: for Item() ONLY: create one or more new Items() from a
	HTTPRequest, overriding with values from kwargs; assuming
	nothing goes wrong, one Item() will be created per "data" file
	submitted in the multipart POST request.  If no "data" file is
	submitted, only a single non-data Item will result.  The
	result for a single Item() creation will be a single Item().
	The result for multiple Item() creation will be a list of
	multiple Items().  For Item() creation via the API, all this
	will be made plain via the envelope metadata.
	"""
	margs = {}
	m = klass(**margs)
	return m.update(request, **kwargs)

    @classmethod
    def get(klass, **kwargs):
	"""return a single model matching kwargs; expunge virtually-deleted ones; if none return None; if multiple, throw exception"""
	return klass.objects.filter(is_deleted=False).get(**kwargs)

    @classmethod
    def list(klass):
	"""return a queryset of models matching kwargs; expunge virtually-deleted ones"""
	return klass.objects.filter(is_deleted=False)

    @classmethod
    def execute_search_query(klass, search_string, qs):
	"""take one queryset and return another, filtered by the content of search_string; this version is a no-op"""
	return qs

    @classmethod
    def search(klass, search_string, **kwargs):
	"""return a queryset of models matching **kwargs and search_string; expunge virtually-deleted ones"""
	return klass.execute_search_query(search_string, klass.list(**kwargs))

    def update(self, request=None, **kwargs):
	"""
	update a single Thing from a HTTPRequest, overriding with values from kwargs

	kwargs override is needed so that commenters cannot cite commentFromFeed in request.POST
	"""

	# build a shadow structure: useful for debug/clarity
	s = {}

	# update shadow structure from request and kwargs
	for sattr in self.r2s.keys():

	    if sattr in kwargs:
		s[sattr] = kwargs[sattr]
	    elif request and sattr in request.POST:
		self.r2s[sattr](request, s)
	    else:
		continue # kinda redundant but clearer

	# update self from shadow structure

	# stage 1: undeferred
	i_changed_something = False

	for sattr in self.s2m.keys():

	    defer, methud = self.s2m[sattr]
	    if not defer:
		methud(request, s, self)
		i_changed_something = True

	# the point of deferral is to save a record so there is an Id,
	# so that foreign keys can work and files can be saved; so
	# it's only really relevant if there is no Id

	if i_changed_something and not self.id:
	    self.save() # generate an id

	# stage 2: deferred
	i_changed_something = False

	for sattr in self.s2m.keys():

	    defer, methud = self.s2m[sattr]
	    if defer:
		methud(request, s, self)
		i_changed_something = True

	if i_changed_something:
	    self.save()

	# stage 3: file saving
	# do this by subclassing

	# done
	return self

    def delete(self): # this is the primary consumer of gc
	"""gc all the fields and mark this Thing as deleted"""
	for mattr in self.gc.keys():
	    self.gc[mattr](self)
	self.is_deleted = True
	self.save()

    def to_structure(self, request=None): # this is the primary consumer of m2s
	"""convert this model m to a dictionary structure s (ie: s-space)"""
	s = {}
	for mattr in self.m2s.keys():
	    self.m2s[mattr](request, self, s)
	return s

    def get_absolute_url(self):
	"""return a url for this object for administrative purposes"""
	url = u''
	return iri_to_uri(url)

    def delete_attribute(self, key):
	"""
	erase the value of attribute 'key' (or delete extended attribute '$key')

	get_, set_, update_, and list_attributes are performed via views()
	"""
	pass

    def __unicode__(self):
	"""return the canonical name of this object"""
	return self.name

##################################################################

class Tag(AbstractThing):
    attr_map = {
	'__prefix__': "tag",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'name': dict(gc='munge', s2m='copy', m2s='copy'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'implies': dict(gc='reflist', s2m='tag_implies', m2s='tag_implies'),
	'cloud': dict(gc='reflist', m2s='tag_cloud'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.slug(unique=True)
    description = AbstractField.text(required=False)
    implies = AbstractField.reflist('self', symmetrical=False, pivot='implied_by', required=False)
    cloud = AbstractField.reflist('self', symmetrical=False, pivot='clouded_by', required=False)

    def __update_cloud_field(self):
	""" """
	# wipe our cloud cache
	self.cloud.clear()
	# get us into the processing loop
	tgraph = { self: False }
	loop = True
	# until we make a pass thru tgraph where nothing happens
	while loop:
	    # default: we won't go round again
	    loop = False
	    # for each tag in tgraph
	    for tag, visited in tgraph.items():
		# if we've already exploded it, skip to next
		if visited:
		    continue
		# register all the unvisited parents into tgraph
		for parent in tag.implies.all():
		    if not tgraph.get(parent, False):
			tgraph[parent] = False
			loop = True # mark more work to be done
		# add this tag to the cloud
		self.cloud.add(tag)
		# mark current tag as 'visited'
		tgraph[tag] = True
	self.save() # needed?

    def __update_cloud_graph(self, tgraph):
	"""
	I could try ripping out the list of tags just once (avoiding
	~n! database hits) and reconstructing the graph from that, but
	if they change on disk underneath me then something nasty can
	happen; better to let caching at a lower level take the hit...
	"""
	# update all the tags with this data
	for tag in tgraph.keys():
	    tag = Tag.objects.get(id=tag.id) # potentially dirty, reload
	    tag.__update_cloud_field()

    def __expand_cloud_graph(self):
	"""
	This is brute-force and ignorance code but it is proof against loops.
	"""
	tgraph = { self: False }
	if not self.id:
	    return tgraph # we are not yet in the database
	loop = True # get us into the processing loop
	while loop:
	    loop = False
	    for tag, visited in tgraph.items():
		if visited:
		    continue
		for parent in tag.implies.all():
		    if not tgraph.get(parent, False):
			tgraph[parent] = False
			loop = True
		for child in tag.implied_by.all():
		    if not tgraph.get(child, False):
			tgraph[child] = False
			loop = True
		tgraph[tag] = True
	return tgraph

    @transaction.commit_on_success # <- rollback if it raises an exception
    def delete_attribute(self, sattr):
	"""
	This method overrides AbstractThing.delete_attribute() and acts as
	a hook to detect changes in the Tag implications that might
	trigger a recalculation of the Tag cloud.
	"""
	if sattr == 'tagImplies':
	    tgraph = self.__expand_cloud_graph()
	else:
	    tgraph = None
	super(Tag, self).delete_attribute(sattr)
	if tgraph:
	    self.__update_cloud_graph(tgraph)

    @transaction.commit_on_success # <- rollback if it raises an exception
    def update_from_request(self, r, **kwargs):
	"""
	This method overrides AbstractThing.update_from_request() and
	acts as a hook to detect changes in the Tag implications that
	might trigger a recalculation of the Tag cloud.

	There is a performance impact here which needs to be
	considered; we *ought* to determine whether something has
	changed that would require the cloud to be recomputed; but
	maybe slightly overzealous refreshing will be good for a
	while... having flushed out a bug where an Item with no
	implications was not clouding itself, the simplicity of just
	recomputing every time is attractive, especially with the
	likely shallow hierarchies of implication, if any at all...
	"""

	tgraph = self.__expand_cloud_graph()
	retval = super(Tag, self).update_from_request(r, **kwargs)
	self.__update_cloud_graph(tgraph)
	retval = Tag.objects.get(id=retval.id) # reload, possibly dirty
	return retval

    @classmethod
    def get_or_auto_tag(klass, request, name):
	if 'auto_tag' in request.POST and request.POST['auto_tag']:
	    t, created = Tag.objects.get_or_create(name=name, defaults={})  # TBD: MAY HAVE ISSUES WITH PREVIOUSLY DELETED TAGS?
	    if created:
		tgraph = t.__expand_cloud_graph()
		t.__update_cloud_graph(tgraph)
		t.save()
	else:
	    t = Tag.objects.get(name=name)
	return t

##################################################################

class Vurl(AbstractThing):
    attr_map = {
	'__prefix__': "vurl",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'name': dict(gc='munge', s2m='copy', m2s='copy'),
	'link': dict(gc='munge', s2m='copy', m2s='copy'),
	'invalid_before': dict(s2m='date', m2s='date'),
	'invalid_after': dict(s2m='date', m2s='date'),
	'use_temporary_redirect': dict(gc='falsify', r2s='bool', s2m='bool', m2s='bool'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.slug(unique=True)
    link = AbstractField.text(unique=True)
    invalid_before = AbstractField.datetime(required=False)
    invalid_after = AbstractField.datetime(required=False)
    use_temporary_redirect = AbstractField.bool(False)

    @staticmethod
    def get_with_vurlkey(encoded):
	""" """
	return Vurl.get(id=base58.b58decode(encoded))

    def vurlkey(self):
	""" """
	return base58.b58encode(self.id)

    def save(self):
	"""override save method to install a name if necessary"""

	if not self.name:
	    self.name = '__tmp_vurl_%s__' % random_bits(128)
	    s = super(Vurl, self).save()
	    self.name = '__%s__' % self.vurlkey()

	s = super(Vurl, self).save()

    def to_structure(self):
	"""
	Splices the virtual vurlKey/vurlPath sattrs into the Vurl
	structure; since m2s_foo above only allows for a single mattr
	to map to a single sattr, and since vurl.id is bound to
	vurlId, and since vurlKey is a restatement of vurl.id in
	base58, and since the vurlId is permanent and readonly, we
	have no real option but to kludge this right here as duplicate
	information.
	"""

	vk = self.vurlkey()
	s = super(Vurl, self).to_structure()
	s['vurlKey'] = vk
	s['vurlPathShort'] = "/get/k/%s" % vk
	s['vurlPathLong'] =  "/get/n/%s" % self.name
	return s

    def http_response(self):
	if self.use_temporary_redirect:
	    return HttpResponseRedirect(self.link)
	else:
	    return HttpResponsePermanentRedirect(self.link)

##################################################################

class Feed(AbstractThing):
    attr_map = {
	'__prefix__': "feed",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'name': dict(gc='munge', s2m='copy', m2s='copy'),
	'version': dict(gc='zeroify', r2s='integer', s2m='copy', m2s='copy'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'embargo_after': dict(s2m='date', m2s='date'),
	'embargo_before': dict(s2m='date', m2s='date'),
	'interests': dict(gc='reflist', s2m='feed_interests', m2s='feed_interests'),
	'interests_exclude': dict(gc='reflist', s2m='feed_interests_exclude', m2s='feed_interests_exclude'),
	'interests_require': dict(gc='reflist', s2m='feed_interests_require', m2s='feed_interests_require'),
	'permitted_networks': dict(s2m='copy', m2s='copy'),
	'content_constraints': dict(s2m='copy', m2s='copy'),
	'is_private': dict(gc='falsify', r2s='bool', s2m='bool', m2s='bool'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.slug(unique=True)
    version = AbstractField.integer(1)
    description = AbstractField.text(required=False)
    embargo_after = AbstractField.datetime(required=False)
    embargo_before = AbstractField.datetime(required=False)
    interests = AbstractField.reflist(Tag, pivot='feeds_with_tag', required=False)
    interests_exclude = AbstractField.reflist(Tag, pivot='feeds_excluding', required=False)
    interests_require = AbstractField.reflist(Tag, pivot='feeds_requiring', required=False)
    permitted_networks = AbstractField.string(required=False)
    content_constraints = AbstractField.string(required=False)
    is_private = AbstractField.bool(True)

##################################################################

class Item(AbstractThing):
    attr_map = {
	'__prefix__': "item",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'name': dict(gc='munge', s2m='copy', m2s='copy'),
	'status': dict(gc='item_status', s2m='item_status', m2s='item_status'),
	'description': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'hide_after': dict(s2m='date', m2s='date'),
	'hide_before': dict(s2m='date', m2s='date'),
	'tags': dict(gc='reflist', s2m='item_tags', m2s='item_tags'),
	'for_feeds': dict(gc='reflist', s2m='item_for_feeds', m2s='item_for_feeds'),
	'not_feeds': dict(gc='reflist', s2m='item_not_feeds', m2s='item_not_feeds'),
	'data_type': dict(s2m='copy', m2s='copy'),
	'data_remote_url': dict(s2m='copy', m2s='copy'),
	'links_to_items': dict(gc='reflist', s2m='item_links_to_items', m2s='item_links_to_items'),
	'encryption_method': dict(s2m='copy', m2s='copy'),
	'digest_method': dict(s2m='copy', m2s='copy'),
	'encryption_key': dict(s2m='copy', m2s='copy'),
	'ciphertext_digest': dict(s2m='copy', m2s='copy'),
	'icon_type': dict(s2m='copy', m2s='copy'),
	'icon_ciphertext_digest': dict(s2m='copy', m2s='copy'),

	'data': dict(gc='file'),
	'icon': dict(gc='file'),
	}
    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    name = AbstractField.string()
    status = AbstractField.choice(item_status_choices)
    description = AbstractField.text(required=False)
    hide_after = AbstractField.datetime(required=False)
    hide_before = AbstractField.datetime(required=False)
    tags = AbstractField.reflist(Tag, pivot='items_tagged', required=False)
    for_feeds = AbstractField.reflist(Feed, pivot='items_explicitly_for', required=False)
    not_feeds = AbstractField.reflist(Feed, pivot='items_explicitly_not', required=False)

    data = AbstractField.file(storage=item_fss, upload_to=fss_yyyymmdd, required=False) # not translated
    data_type = AbstractField.string(required=False)
    data_remote_url = AbstractField.url(required=False)

    links_to_items = AbstractField.reflist('Item', pivot='item_linked_from', required=False)

    encryption_method = AbstractField.text(required=False)
    digest_method = AbstractField.text(required=False)
    encryption_key = AbstractField.text(required=False)
    ciphertext_digest = AbstractField.text(required=False)

    icon = AbstractField.file(storage=icon_fss, upload_to=fss_yyyymmdd, required=False) # not translated
    icon_type = AbstractField.string(required=False)
    icon_ciphertext_digest = AbstractField.text(required=False)

##################################################################

class Comment(AbstractThing):
    attr_map = {
	'__prefix__': "comment",
	'id': dict(r2s='integer', s2m='copy', m2s='copy'),
	'created': dict(gc='skip', s2m='date', m2s='date'),
	'last_modified': dict(gc='skip', s2m='date', m2s='date'),

	'title': dict(gc='munge', s2m='copy', m2s='copy'),
	'body': dict(r2s='verbatim', s2m='copy', m2s='copy'),
	'from_feed': dict(s2m='comment_from_feed', m2s='comment_from_feed'), # r2s=string, not integer!
	'upon_item': dict(r2s='integer', s2m='comment_upon_item', m2s='comment_upon_item'),
	'encryption_method': dict(s2m='copy', m2s='copy'),
	'digest_method': dict(s2m='copy', m2s='copy'),
	'encryption_key': dict(s2m='copy', m2s='copy'),
	'ciphertext_digest': dict(s2m='copy', m2s='copy'),

	'data': dict(gc='file'),
	}

    (r2s, s2m, m2s, gc) = Space.compile(attr_map)

    title = AbstractField.string()
    body = AbstractField.text(required=False)
    from_feed = AbstractField.reference(Feed, required=False)
    upon_item = AbstractField.reference(Item, required=False)

    data = AbstractField.file(storage=comment_fss, upload_to=fss_yyyymmdd, required=False) # not translated

    encryption_method = AbstractField.text(required=False)
    digest_method = AbstractField.text(required=False)
    encryption_key = AbstractField.text(required=False)
    ciphertext_digest = AbstractField.text(required=False)

    def __unicode__(self):
	"""return the title of this comment; comments lack a "name" field"""
	return self.title

##################################################################

class Registry(AbstractModel): # not a Thing
    """key/value pairs for Mine configuration"""

    key = AbstractField.slug(unique=True)
    value = AbstractField.text()

    @classmethod
    def get(klass, key):
	""" """
	return Registry.objects.get(key=key).value

    @classmethod
    def get_decoded(klass, key):
	""" """
	return base64.urlsafe_b64decode(klass.get(key))

    @classmethod
    def set(klass, key, value, overwrite_ok):
	""" """
	r, created = Registry.objects.get_or_create(key=key, defaults={ 'value': value })
	if not created and not int(overwrite_ok):
	    raise RuntimeError, 'not allowed to overwrite existing Registry key: %s' % key
	r.save()
	return r

    @classmethod
    def set_encoded(klass, key, value, overwrite_ok):
	""" """
	return klass.set(key, base64.urlsafe_b64encode(value), overwrite_ok)

    def to_structure(self):
	""" """
	s = {}
	s[self.key] = self.value # this is why it is not a Thing
	s['keyCreated'] = self.created.isoformat()
	s['keyLastModified'] = self.last_modified.isoformat()
	return s

    class Meta:
	ordering = ['key']
	verbose_name = 'Register'
	verbose_name_plural = 'Registry'

    def __unicode__(self):
	return self.key

##################################################################

class Event(AbstractModel): # not a Thing
    """audit trail for Mine"""

    message = AbstractField.string()
    alert = AbstractField.bool(False)

    feed = AbstractField.reference(Feed, required=False)
    item = AbstractField.reference(Item, required=False)
    ip_address = AbstractField.string(required=False)
    method = AbstractField.string(required=False)
    url = AbstractField.string(required=False)
