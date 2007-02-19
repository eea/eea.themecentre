Theme Centre is a folder that contains content on a certain theme.

To get it working
=================
You need Five 1.4+ and plone.app.form

There's a bug in Zope 2.9 (and probably in later versions as well)
that raises AttributeError: debug when using plone.app.form. The
fix is to add two lines of code to ZPublisher/HTTPRequest.

from zope.publisher.base import DebugFlags
self.debug = DebugFlags   # inside __init__
