import MySQLdb
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from eea.themecentre.browser.epaedia import *
from eea.themecentre.interfaces import IThemeTagging
from eea.mediacentre.interfaces import IMediaType

types = { 'image': { 'sql': sql_images, 'tid': 5, 'path': '/www/SITE/images',
    'method': 'images' } }

themes = { 'climate': 200 }

class MigrateMedia(utils.BrowserView):

    def __init__(self, context, request):
        super(MigrateMedia, self).__init__(context, request)
        self.db = MySQLdb.connect(host="localhost", user="root", db="epaedia")
        self.path = request.get('path')
        self.workflow = getToolByName(context, 'portal_workflow')
        self.catalog = getToolByName(context, 'portal_catalog')

    def migrate(self):
        for theme_id, page_id in themes.items():
            self.migrate_files(theme_id, page_id, 'image')

    def images(self, folder, db_row):
        eid, title, extension = db_row
        new_id = utils.normalizeString(title, encoding='latin1')
        path = self.path + '/website/elements/images/' + str(eid) + \
            '_large.' + extension
        folder.invokeFactory('Image', id=new_id, title=title)
        atimage = folder[new_id]
        image = open(path, 'rb')
        atimage.setImage(image)
        return atimage

    def migrate_files(self, theme_id, page_id, media_type):
        context = utils.context(self)
        cursor = self.db.cursor()
        cursor.execute(sql_images % page_id)
        images = cursor.fetchall()

        for db_row in images:
            path = types[media_type]['path']
            folder = context.unrestrictedTraverse(path)

            method = getattr(self, types[media_type]['method'])
            new_file = method(folder, db_row)

            media = IMediaType(new_file)
            media.media_type = media_type

            themetag = IThemeTagging(new_file)
            themetag.tags = [theme_id]

            #self.workflow.doActionFor(atfile, 'publish')
            self.catalog.indexObject(new_file)
