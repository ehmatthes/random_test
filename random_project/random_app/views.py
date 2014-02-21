from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page, patch_cache_control

from django.utils.cache import get_cache_key
from django.core.cache import cache
from django.http import HttpRequest
from django.core.urlresolvers import reverse

from random import randint


@cache_page(60 * 10)
def index(request):
    numbers = [randint(1,9) for x in range(0,10)]

    response = render_to_response('random_app/index.html',
                              {'numbers': numbers,
                               },
                              context_instance=RequestContext(request))

    #response['Cache-Control'] = 'no-cache'
    patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True, max_age=60)
    return response


def refreshing_page(request):
    # Invalidated the index page.
    invalidate_cache('index')
    return render_to_response('random_app/refreshing_page.html',
                              {},
                              context_instance=RequestContext(request))


def non_refreshing_page(request):
    return render_to_response('random_app/non_refreshing_page.html',
                              {},
                              context_instance=RequestContext(request))


def invalidate_cache(view_path, args=[], namespace=None, key_prefix=None):
    """Function to allow invalidating a view-level cache.
    Adapted from: http://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django
    """
    # Usage: invalidate_cache('index', namespace='ed_news', key_prefix=':1:')

    # Create a fake request.
    request = HttpRequest()
    # Get the request path.
    if namespace:
        view_path = namespace + ":" + view_path

    request.path = reverse(view_path, args=args)
    #print 'request:', request

    # Get cache key, expire if the cached item exists.
    # Using the key_prefix did not work on first testing.
    #key = get_cache_key(request, key_prefix=key_prefix)
    page_key = get_cache_key(request)
    header_key = ''

    if page_key:
        # Need to clear page and header cache. Get the header key
        #  from the page key.
        # Typical page key: :1:views.decorators.cache.cache_page..GET.6666cd76f96956469e7be39d750cc7d9.d41d8cd98f00b204e9800998ecf8427e.en-us.UTC
        # Typical header key: :1:views.decorators.cache.cache_header..6666cd76f96956469e7be39d750cc7d9.en-us.UTC
        #  Change _page..GET. to _header..
        #  then lose the second hash.
        import re
        p = re.compile("(.*)_page\.\.GET\.([a-z0-9]*)\.[a-z0-9]*(.*en-us.UTC)")
        m = p.search(page_key)
        header_key = m.groups()[0] + '_header..' + m.groups()[1] + m.groups()[2]

        print '\n\nviews.invalidate_cache'
        print 'page_key:', page_key
        print 'header_key:', header_key
    
        # If the page/ header have been cached, destroy them.
        if cache.get(page_key):
            # Delete the page and header caches.
            cache.delete(page_key)
            #cache.delete(header_key)

            print 'invalidated cache'
            return True

    print "couldn't invalidate cache"
    return False
