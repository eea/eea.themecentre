# monkey patch of Zope
from ZPublisher import HTTPRequest
from zope.publisher.base import DebugFlags

HTTPRequest.HTTPRequest.debug = DebugFlags()
