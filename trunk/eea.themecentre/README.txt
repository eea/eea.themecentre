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

Install Five 1.4.2 and our Plone4ArtistVideo tar ( we have a tar since svn checkout isn't allowed from pelican)
Configure zope to use Plone-2.5.2-1 and Plone-2.5.2-1/CacheFu
Reinstall CacheSetup (2-10min)

Make sure you don't have Archetypes, PortalTransforms and PloneLanguageTool in your bundle. They are not removed automically.
Remove portal_types/NavigationPage to avoid Composite pack errors
Then migrate old objects to new theme tagging funcionallity SITE/@@migrateThemeTaggable ( 1-5min)

Migrate Plone and ATCT (15-30min)
Reinstall older products (not necessary) (2-10min)
Install FiveSite 
Install ThemeCentre (this takes time because we add a new index and reindex the catalog) (10-20 min)
If you don't have anything in portal_skins/custom you 
  Go to portal_setup -> properties, select EEA WWW and import skins tool 
otherwise
  manually add themecentre_* layers to the skins.

Make sure portal_fiveactions is in portal_actions -> action providers

Create folder themes in SITE/
Create folder rdf-repository in SITE/themes
In actions menu click 'make as rdfrepository'
run SITE/themes/rdf-repository/@@migrateRDF (2-10min)
Rename the Dataset and map+graphs feeds
run SITE/themes/rdf-repository/@@migrateIndicatorRDF (2-5min)


run SITE/themes/@@initiateThemes?migrate=True (15-50min)
if you want to do a test with only 3 themes run  SITE/themes/@@initiateThemes?migrate=True&noThemes=3


How to migrate themes for the LAZY one :)
=========================================

Configure zope to use Plone-2.5.2-1 and Plone-2.5.2-1/CacheFu
update bundle
If you are using eeadesign2006-bundle (not devel)
  Install Five 1.4.2 and our Plone4ArtistVideo tar ( we have a tar since svn checkout isn't allowed from pelican)

Make sure you don't have Archetypes, PortalTransforms and PloneLanguageTool in your bundle. They are not removed automically.
copy data.fs from production site
restart your zope
