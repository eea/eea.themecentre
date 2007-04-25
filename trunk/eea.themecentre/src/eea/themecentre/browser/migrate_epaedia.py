import MySQLdb
from Acquisition import aq_base
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from eea.themecentre.browser.epaedia import *
from eea.themecentre.interfaces import IThemeTagging
from eea.mediacentre.interfaces import IMediaType
from zope.app.event.objectevent import ObjectModifiedEvent
from zope.event import notify

types = { 'image':
            { 'sql': sql_images,
              'method': 'images',
              'path': 'images' },
          'animation':
            { 'sql': sql_animations,
              'method': 'animations',
              'path': 'animations' },
          'mindstretcher':
            { 'sql': sql_mindstretchers,
              'method': 'mindstretchers',
              'path': 'mindstretchers' },
          'video':
            { 'sql': sql_videos,
              'method': 'videos',
              'path': 'videos' },
          'link':
            { 'sql': sql_links,
              'method': 'links',
              'path': 'links' },
        }

themes = { 'climate': 200 }

class MigrateMedia(utils.BrowserView):

    def __init__(self, context, request):
        super(MigrateMedia, self).__init__(context, request)
        self.db = MySQLdb.connect(host="localhost", user="root", db="epaedia")
        self.path = request.get('path')
        self.workflow = getToolByName(context, 'portal_workflow')
        self.catalog = getToolByName(context, 'portal_catalog')

    def migrate(self):
        context = utils.context(self)

        # create the media folders that need to be there
        for media_type in types:
            path = types[media_type]['path']
            folder = getattr(aq_base(context), path, None)
            if not folder:
                context.invokeFactory('Folder', id=path,
                        title=media_type)

        # copy all files from filesystem to the eea site
        for theme_id, page_id in themes.items():
            for media_type in types:
                self.migrate_files(theme_id, page_id, media_type)

        self.request.RESPONSE.redirect(context.absolute_url())

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

    def animations(self, folder, db_row):
        eid, title = db_row
        new_id = utils.normalizeString(title, encoding='latin1')
        path = self.path + '/website/elements/animations/' + str(eid) + '.swf'
        folder.invokeFactory('File', id=new_id, title=title)
        atfile = folder[new_id]
        file = open(path, 'rb')
        atfile.setFile(file)
        return atfile

    def mindstretchers(self, folder, db_row):
        return self.animations(folder, db_row)

    def videos(self, folder, db_row):
        eid, title, body, item = db_row

        new_id = utils.normalizeString(title, encoding='latin1')
        taken_ids = folder.objectIds()
        if new_id in taken_ids:
            extra = 1
            while new_id + str(extra) in taken_ids:
                extra += 1
            new_id = new_id + str(extra)

        path = self.path + '/website/elements/video/' + str(eid) + "_" + \
               str(item) + '.flv'
        folder.invokeFactory('File', id=new_id, title=title)
        atfile = folder[new_id]
        file = open(path, 'rb')
        atfile.setFile(file)
        atfile.setDescription(body)

        # p4a activates videos automatically by subscribing to modified events
        notify(ObjectModifiedEvent(atfile))

        return atfile

    def links(self, folder, db_row):
        eid, link, title, body = db_row
        new_id = utils.normalizeString(title, encoding='latin1')
        folder.invokeFactory('Link', id=new_id, title=title)
        linkobj = folder[new_id]
        linkobj.setDescription(body)
        linkobj.setRemoteUrl(link)
        return linkobj

    def migrate_files(self, theme_id, page_id, media_type):
        context = utils.context(self)
        cursor = self.db.cursor()
        cursor.execute(types[media_type]['sql'] % page_id)
        files = cursor.fetchall()

        for db_row in files:
            folder = getattr(context, types[media_type]['path'])

            method = getattr(self, types[media_type]['method'])
            new_file = method(folder, db_row)

            try:
                media = IMediaType(new_file)
                media.media_type = media_type
            except:
                # links can't be adapted and shouldn't be
                pass

            themetag = IThemeTagging(new_file)
            themetag.tags = [theme_id]

            self.workflow.doActionFor(new_file, 'publish')
            self.catalog.indexObject(new_file)
