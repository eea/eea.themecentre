import MySQLdb
import MySQLdb.cursors
from Acquisition import aq_base
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from eea.themecentre.browser.epaedia import *
from eea.themecentre.interfaces import IThemeTagging, IThemeCentreSchema
from eea.mediacentre.interfaces import IMediaType
from zope.app.event.objectevent import ObjectModifiedEvent
from zope.event import notify
from zope.component import getAdapter
from p4a.video.interfaces import IVideoDataAccessor

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

themes = { 200: 'climate',
           226: 'water',
           372: 'natural',
           373: 'human',
           526: 'households',
           534: 'transport',
           556: 'biodiversity',
           }

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
        for page_id, theme_id in themes.items():
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
        folder.invokeFactory('FlashFile', id=new_id, title=title)
        atfile = folder[new_id]
        file = open(path, 'rb')
        atfile.setFile(file)
        atfile.setWidth(530)
        atfile.setHeight(350)
        notify(ObjectModifiedEvent(atfile))
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

        filename = str(eid) + "_" + str(item) + ".flv"
        path = self.path + '/website/elements/video/' + filename
        folder.invokeFactory('File', id=new_id, title=title)
        atfile = folder[new_id]
        file = open(path, 'rb')
        atfile.setFile(file)
        atfile.setDescription(body)

        try:
            # p4a activates videos automatically by subscribing to modified events
            notify(ObjectModifiedEvent(atfile))
        except:
            # sometimes extracting metadata from file may fail and result in
            # error, but we can continue as we set metadata below instead
            pass

        video = getAdapter(atfile, IVideoDataAccessor,
                name="video/x-flv")
        video._video_data['width'] = METADATA[filename]['width']
        video._video_data['height'] = METADATA[filename]['height']
        video._video_data['duration'] = METADATA[filename]['duration']
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
        cursor.close()

        for db_row in files:
            folder = getattr(context, types[media_type]['path'])

            method = getattr(self, types[media_type]['method'])
            new_file = method(folder, db_row)

            try:
                media = IMediaType(new_file)
                media.types = [media_type]
            except:
                # links can't be adapted and shouldn't be
                pass

            themetag = IThemeTagging(new_file)
            themetag.tags = [theme_id]

            self.workflow.doActionFor(new_file, 'publish')
            self.catalog.indexObject(new_file)


class MigrateArticles(object):
    """ Migrates articles from epaedia website. """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.db = MySQLdb.connect(host="localhost", user="root", db="epaedia",
                                  cursorclass=MySQLdb.cursors.SSDictCursor)
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.workflow = getToolByName(context, 'portal_workflow')
        self.multimedia_path = request.get('multimedia')

    def migrate(self):
        """ Some docstring. """

        epaedia_themes = self._epaedia_themes()
        for theme in epaedia_themes:
            page_id = theme['pid']
            themecentre = self._themecentre(themes[page_id])
            if page_id == 200:
                self._migrate_articles(themecentre, theme)
        return 'migration of epaedia articles is successfully finished'

    def _create_article_from_sections(self, folder, page_id, id_suffix='', title=None):
        cursor = self.db.cursor()
        cursor.execute(sql_title % page_id)
        row = cursor.fetchone()
        cursor.close()

        doc_id = utils.normalizeString(row['title'], encoding='latin1') + \
                id_suffix
        new_id = folder.invokeFactory('Document', id=doc_id,
                                      title=title or row['title'])
        article = getattr(folder, new_id)
        article.setDescription(row['title'])
        self.workflow.doActionFor(article, 'publish')
        article.reindexObject()

        cursor = self.db.cursor()
        cursor.execute(sql_sections % page_id)
        sections = cursor.fetchall()
        cursor.close()

        total_body = ""

        for section in sections:
            section_no = section['section']
            content = self._section_content(page_id, section_no)
            title = unicode(content['title'], 'latin1').encode('utf8')
            body = unicode(content['body'], 'latin1').encode('utf8')
            quote = unicode(content['quote'], 'latin1').encode('utf8')
            tag = unicode(content['tag'], 'latin1').encode('utf8')
            align = unicode(section['align'], 'latin1').encode('utf8')
            section_type = section['type']
            body_html = self._nl_to_p(body)

            # title and body
            if section_type == 1 and section_no > 1:
                if len(title.strip()) > 0:
                    total_body += "<h2>%s</h2>\n" % title
                if len(body) > 0:
                    total_body += body_html + '\n'
            # title, body and image
            if section_type == 2 and section_no > 1:
                if len(title.strip()) > 0:
                    total_body += '<h2>%s</h2>\n' % title
                image_url = self._image_url(section['eid']) + '/image_mini'
                #image_url = "/multimedia/images/"
                image_html = '<img src="%s" alt="%s" />' % \
                              (image_url, title)
                if align == 'l':
                    left = image_html
                    right = body_html
                else:
                    left = body_html
                    right = image_html
                total_body += '<table><td>%s</td><td>%s</td></table>\n' % \
                              (left, right)
            # title, quote, body
            if section_type == 3 and section_no > 1:
                if len(title.strip()) > 0:
                    total_body += '<h2>%s</h2>\n' % title
                total_body += '<blockquote class="quote-left">\n' + \
                              '<p>%s</p>\n' % quote + \
                              '<p class="source">%s</p>\n' % tag + \
                              '</blockquote>\n' + \
                              '<div class="visualClear"><!-- --></div>\n'
                if len(body) > 0:
                    total_body += "<p>%s</p>\n" % body_html
            # title, body, link
            if section_type == 4 and section_no > 1:
                cursor = self.db.cursor()
                cursor.execute(sql_article_links % section['eid'])
                link = cursor.fetchone()
                cursor.close()

                link_id = utils.normalizeString(title, encoding='latin1')
                path = '/'.join((self.multimedia_path, types['link']['path'],
                         link_id))

                if len(title.strip()) > 0:
                    total_body += '<h2>%s</h2>\n' % title
                total_body += '<table><tr><td><a href="%s" alt="%s">%s</a>' % \
                              (path, link['title'], link['title']) + \
                              '</td></tr><tr><td>%s</td></tr></table>\n' % \
                              link['body']
            if section_type == 5 and section_no > 1:
                if len(title.strip()) > 0:
                    total_body += '<h2>%s</h2>\n' % title
                if quote:
                    total_body += '<ul>\n'
                    for listitem in quote.split('|'):
                        total_body += '<li>%s</li>\n' % listitem.strip()
                    total_body += '</ul>\n'


        article.setText(total_body)
        article.reindexObject()
        return article.getId()

    def _create_intro(self, folder, page_id):
        return self._create_article_from_sections(folder, page_id,
                                                  id_suffix='-intro')

    def _create_snapshot(self, folder, page_id):
        cursor = self.db.cursor()
        cursor.execute(sql_cid_with_onetier_pid % page_id)
        cid = cursor.fetchone()['cid']
        cursor.close()

        cursor = self.db.cursor()
        cursor.execute(sql_snapshot_pid % cid)
        result = cursor.fetchone()
        cursor.close()
        if result:
            pid = result['pid']
            return self._create_article_from_sections(folder, pid,
                                                      id_suffix='-snapshot',
                                                      title='Snapshot')
        else:
            return None

    def _create_fullarticle(self, folder, page_id):
        cursor = self.db.cursor()
        cursor.execute(sql_cid_with_onetier_pid % page_id)
        cid = cursor.fetchone()['cid']
        cursor.close()

        cursor = self.db.cursor()
        cursor.execute(sql_fullarticle_pid % cid)
        result = cursor.fetchone()
        cursor.close()
        if result:
            pid = result['pid']
            return self._create_article_from_sections(folder, pid,
                                                      id_suffix='-fullarticle',
                                                      title='Full article')
        else:
            return None

    def _epaedia_themes(self):
        cursor = self.db.cursor()
        cursor.execute(sql_level_one)
        level_one = cursor.fetchall()
        cursor.close()
        return level_one

    def _image_url(self, eid):
        cursor = self.db.cursor()
        cursor.execute(sql_image_by_eid % eid)
        image = cursor.fetchone()
        cursor.close()

        title = image['title']
        image_id = utils.normalizeString(title, encoding='latin1')
        path = '/'.join((self.multimedia_path, types['image']['path'],
                         image_id))
        return path

    def _migrate_articles(self, folder, theme):
        """ migrates every article in mysql which belongs to the main
            theme 'theme'. 'folder' is where the content will be added. """

        page_id = theme['pid']
        theme_id = themes[page_id]
        cid = theme['cid']
        
        doc_id = self._create_intro(folder, page_id)
        intro = getattr(folder, doc_id)
        doc_id = self._create_snapshot(folder, page_id)
        snapshot = getattr(folder, doc_id)
        doc_id = self._create_fullarticle(folder, page_id)
        fullarticle = getattr(folder, doc_id)
        return
        self._relate(intro, snapshot, fullarticle)

        cursor = self.db.cursor()
        cursor.execute(sql_level_two % cid)
        level_two = cursor.fetchall()
        cursor.close()

        for menu_item in level_two:
            title = menu_item['title']
            folder_id = utils.normalizeString(title, encoding='latin1')
            new_id = folder.invokeFactory('Folder', id=folder_id,
                                                    title=title)
            level_two_folder = getattr(folder, new_id)
            self.workflow.doActionFor(level_two_folder, 'publish')
            level_two_folder.reindexObject()

            pid = menu_item['pid']

            new_id = self._create_intro(level_two_folder, pid)
            if new_id:
                level_two_folder.manage_addProperty('default_page', new_id,
                                                    'string')

            ciid = menu_item['ciid']
            cursor = self.db.cursor()
            cursor.execute(sql_level_three % ciid)
            level_three = cursor.fetchall()
            cursor.close()

            for menu_item in level_three:
                title = menu_item['title']
                folder_id = utils.normalizeString(title, encoding='latin1')
                level_two_folder.invokeFactory('Folder',
                        id=folder_id, title=title)
                level_three_folder = getattr(level_two_folder, folder_id)
                self.workflow.doActionFor(level_three_folder, 'publish')
                level_three_folder.reindexObject()

                pid = menu_item['pid']

                new_id = self._create_intro(level_three_folder, pid)
                if new_id:
                    level_three_folder.manage_addProperty('default_page',
                                                          new_id, 'string')

    def _nl_to_p(self, text):
        result = ''
        for para in text.split('\n'):
            result += '<p>%s</p>' % para
        return result

    def _relate(self, intro, snapshot, fullarticle):
        intro.setRelatedItems([snapshot, fullarticle])
        snapshot.setRelatedItems([intro, fullarticle])
        fullarticle.setRelatedItems([intro, snapshot])

        intro.reindexObject()
        snapshot.reindexObject()
        fullarticle.reindexObject()

    def _section_content(self, page_id, section_no):
        cursor = self.db.cursor()
        cursor.execute(sql_section_content % (page_id, section_no))
        result = cursor.fetchone()
        cursor.close()
        return result

    def _themecentre(self, theme_id):
        iface = 'eea.themecentre.interfaces.IThemeCentre'
        themes = self.catalog.searchResults(object_provides=iface)
        # there should be exactly one themecentre for each theme
        for theme in themes:
            obj = theme.getObject()
            if IThemeCentreSchema(obj).tags == theme_id:
                return obj
        raise 'No theme exists with id ' + theme_id
