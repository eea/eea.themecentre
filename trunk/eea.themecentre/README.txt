Theme Centre is a folder that contains content on a certain theme.

To get it working
=================
You need
 * Five 1.4+  (http://svn.zope.org/Products.Five/tags/1.4.2/)
 * plone.app.form  (https://svn.plone.org/svn/plone/plone.app.form/trunk)
 * FiveSite   (http://svn.eionet.europa.eu/repositories/Zope/trunk/FiveSite)

There's a bug in Zope 2.9 (and probably in later versions as well)
that raises AttributeError: debug when using plone.app.form. The
fix is to add two lines of code to ZPublisher/HTTPRequest.

from zope.publisher.base import DebugFlags
self.debug = DebugFlags   # inside __init__


How to migrate themes
=====================

Then migrate old objects to new theme tagging funcionallity SITE/@@migrateThemeTaggable

Install FiveSite and then ThemeCentre (this takes time because we add a new index and reindex the catalog)

Create folder themes in SITE/

run SITE/themes/@@initiateThemes?migrate=True
if you want to do a test with only 3 themes run  SITE/themes/@@initiateThemes?migrate=True&noThemes=3

Create folder rdf-repository in SITE/themes
In actions menu click 'make as rdfrepository'

run SITE/themes/rdf-repository/@@migrateRDF
run SITE/themes/rdf-repository/@@migrateIndicatorRDF

Rename the Dataset and map+graphs feeds


