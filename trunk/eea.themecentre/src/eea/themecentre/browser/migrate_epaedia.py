# To run epaedia migration:
# First import mysql data
#
#  $ mysql -u root
#  mysql> create database epaedia;
#  mysql> quit
#
#  $ mysql -u root epaedia < epaedia.mysql
#
# Then run the migration, it's two views
# /www/SITE/multimedia/@@migrateEpaediaMultimedia?path=/home/tim/epaedia/E3-Encyclopedia
# /www/SITE/themes/@@migrateEpaediaArticles?multimedia_path=/www/SITE/multimedia
#
# Except path and multimedia_path four other parameters can be passed in the url
#  * host - defaults to 'localhost'
#  * db - defaults to 'epaedia'
#  * user - defaults to 'root'
#  * password - defaults to empty string

import MySQLdb
import MySQLdb.cursors
import os
from DateTime import DateTime
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
from Products.NavigationManager.sections import INavigationSectionPosition

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

eids_not_migrate = [607]

missing_title = {
    609: 'Fossil fuels in plants',
    621: 'Snow and mountains',
    623: 'Ice bears',
    625: 'EU coastline',
    633: 'Dandelions',
    635: 'Ox-eye daisy',
    641: 'Tree branches',
    649: 'Parking',
    653: 'People and umbrellas',
}

def load_pid_theme_mapping():
    path = os.path.dirname(__file__) + os.path.sep + 'epaedia-mapping.csv'
    mapping = {}

    for line in open(path, 'r'):
        pid, title, maintheme, theme2, theme3, theme4 = line.split('@')
        themes = filter(lambda x:len(x.strip())>0, [maintheme, theme2, theme3, theme4.strip()])
        mapping[int(pid)] = themes

    return mapping
            
DEFAULT_EFFECTIVE_DATE = DateTime('2006-02-02')

class MigrateMedia(object):
    """ Migrates media from epaedia database."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dbname = request.get('db', 'epaedia')
        self.user = request.get('user', 'root')
        self.password = request.get('password', '')
        self.host = request.get('host', 'localhost')
        self.db = MySQLdb.connect(host=self.host, user=self.user, db=self.dbname,
                                  passwd=self.password)
        self.path = request.get('path')
        self.workflow = getToolByName(context, 'portal_workflow')
        self.catalog = getToolByName(context, 'portal_catalog')
        self.themes = {}

    def migrate(self):
        self.file = open('media_files.txt', 'w')
        self.eids = {}

        self.themes = load_pid_theme_mapping()

        # create the media folders that need to be there
        #for media_type in types:
        #    path = types[media_type]['path']
        #    folder = getattr(aq_base(context), path, None)
        #    if not folder:
        #        context.invokeFactory('Folder', id=path,
        #                title=media_type)

        # copy all files from filesystem to the eea site
        #for page_id, theme_id in themes.items():
        #    for media_type in types:
        #        self.migrate_files(theme_id, page_id, media_type)

        cursor = self.db.cursor()
        cursor.execute(sql_level_one)
        level_one = cursor.fetchall()
        cursor.close()
        media_types = types.keys()
        media_types.remove('image')

        for levelone in level_one:
            page_id = levelone[1]
            if self.themes[page_id]:
                theme_id = self.themes[page_id][0]
            else:
                continue
            cid = levelone[2]
            snapshot_pid = self._snapshot_pid(int(page_id))
            fullarticle_pid = self._fullarticle_pid((page_id))
            for media_type in media_types:
                for pid in filter(None, (page_id, snapshot_pid, \
                        fullarticle_pid)):
                    self.migrate_files(theme_id, pid, media_type)
                    #self.migrate_section_files(theme_id, pid, media_type)

            cursor = self.db.cursor()
            cursor.execute(sql_level_two % cid)
            level_two = cursor.fetchall()
            cursor.close()

            for leveltwo in level_two:
                page_id = leveltwo[0]
                ciid = leveltwo[1]
                for media_type in media_types:
                    self.migrate_files(theme_id, page_id, media_type)
                    #self.migrate_section_files(theme_id, pid, media_type)

                cursor = self.db.cursor()
                cursor.execute(sql_level_three % ciid)
                level_three = cursor.fetchall()
                cursor.close()

                for levelthree in level_three:
                    page_id = levelthree[0]
                    for media_type in media_types:
                        self.migrate_files(theme_id, page_id, media_type)
                        #self.migrate_section_files(theme_id, pid, media_type)


        self._migrate_images()

        self.file.close()
        #import pdb; pdb.set_trace()
        self.request.RESPONSE.redirect(self.context.absolute_url())

    def images(self, folder, db_row, theme_id):
        eid, title, extension = db_row
        if not title:
            title = missing_title[eid]
        new_id = utils.normalizeString(title, encoding='latin1')
        path = self.path + '/website/elements/images/' + str(eid) + \
            '_large.' + extension
        if not os.path.exists(path):
            path = self.path + '/website/elements/images/' + str(eid) + \
                '.' + extension
        if not os.path.exists(path):
            return None

        title = unicode(title, 'latin1').encode('utf-8')

        # if there already is an object with this id, use a counter
        count = 1
        while getattr(folder, new_id, None):
            count += 1
            new_id = new_id + str(count)

        folder.invokeFactory('Image', id=new_id, title=title)
        atimage = folder[new_id]
        atimage.processForm()
        image = open(path, 'rb')
        atimage.setImage(image)
        atimage.setEffectiveDate(DEFAULT_EFFECTIVE_DATE)
        atimage.setModificationDate(DEFAULT_EFFECTIVE_DATE)
        return atimage

    def animations(self, folder, db_row, theme_id):
        eid, title = db_row
        if not title:
            title = missing_title[eid]
        new_id = utils.normalizeString(title, encoding='latin1')
        path = self.path + '/website/elements/animations/' + str(eid) + '.swf'
        folder.invokeFactory('FlashFile', id=new_id, title=title)
        atfile = folder[new_id]
        file = open(path, 'rb')
        atfile.setFile(file)
        atfile.setWidth(530)
        atfile.setHeight(350)
        atfile.setEffectiveDate(DEFAULT_EFFECTIVE_DATE)
        atfile.processForm()
        #notify(ObjectModifiedEvent(atfile))
        atfile.setModificationDate(DEFAULT_EFFECTIVE_DATE)
        return atfile

    def mindstretchers(self, folder, db_row, theme_id):
        return self.animations(folder, db_row, theme_id)

    def videos(self, folder, db_row, theme_id):
        eid, title, body, item = db_row

        if not title:
            title = missing_title[eid]
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
        atfile.setEffectiveDate(DEFAULT_EFFECTIVE_DATE)
        atfile.processForm()

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
        atfile.setModificationDate(DEFAULT_EFFECTIVE_DATE)
        return atfile

    def links(self, folder, db_row, theme_id):
        eid, link, title, body, pid = db_row

        # if pid is not 0, then this is an internal link which
        # we are not interested in
        if pid > 0:
            return None

        if not title:
            title = missing_title[eid]
        new_id = utils.normalizeString(title, encoding='latin1')
        query = { 'object_provides': 'eea.themecentre.interfaces.IThemeCentre',
                  'getId': theme_id }
        brains = self.catalog.searchResults(query)
        themecentre = brains[0].getObject()
        linksfolder = getattr(themecentre, 'links')
        linksfolder.invokeFactory('Link', id=new_id, title=title)
        linkobj = linksfolder[new_id]
        linkobj.setDescription(body)
        linkobj.setRemoteUrl(link)
        linkobj.processForm()
        linkobj.setEffectiveDate(DEFAULT_EFFECTIVE_DATE)
        linkobj.setModificationDate(DEFAULT_EFFECTIVE_DATE)
        return linkobj

    def migrate_files(self, theme_id, page_id, media_type):
        cursor = self.db.cursor()
        cursor.execute(types[media_type]['sql'] % page_id)
        files = cursor.fetchall()
        cursor.close()

        for db_row in files:
            if self.eids.has_key(db_row[0]):
                continue

            #folder = getattr(context, types[media_type]['path'])
            folder = self.context

            method = getattr(self, types[media_type]['method'])
            new_file = method(folder, db_row, theme_id)

            try:
                media = IMediaType(new_file)
                media.types = [media_type]
            except:
                # links can't be adapted and shouldn't be
                pass

            if media_type != 'link':
                self._apply_themes(theme_id, new_file, page_id)

            self.catalog.indexObject(new_file)
            self._save_to_file(db_row[0],
                               '/'.join(new_file.getPhysicalPath()))


    #def _migrate_section_files(self, theme_id, page_id, media_type):
    #    if media_type not in ('image', 'link'):
    #        return
#
#        cursor = self.db.cursor()
#        cursor.execute(sql_sections % page_id)
#        files2 = cursor.fetchall()
#        cursor.close()
#
#        for db_row in files2:
#            if self.eids.has_key(db_row[0]):
#                continue
#
#            eid = db_row[3]
#            if media_type == 'image':
#                cursor = self.db.cursor()
#                cursor.execute(sql_image_by_eid % eid)
#                db_row = cursor.fetchone()
#                cursor.close()
#
#                self.images(self.multimedia_folder, db_row, page_id)


    def _apply_themes(self, theme_id, new_file, page_id):
        themetag = IThemeTagging(new_file)
        tags = self.themes[page_id]
        if theme_id == tags[0]:
            themetag.tags = tags
        else:
            1/0

    def _change_workflow(self, obj):
        pass

    def _fullarticle_pid(self, page_id):
        cursor = self.db.cursor()
        cursor.execute(sql_cid_with_onetier_pid % page_id)
        cid = cursor.fetchone()[0]
        cursor.close()

        cursor = self.db.cursor()
        cursor.execute(sql_fullarticle_pid % cid)
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return None

    def _migrate_images(self):
        """ Migrate all images that migrate_files didn't migrate.
            When migrate_files runs it will tag the images with theme
            tags. In this method those are not tagged.
        """
        cursor = self.db.cursor()
        cursor.execute(sql_all_images)
        result = cursor.fetchall()
        cursor.close()

        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        folder = portal.SITE.images

        for db_row in result:
            if self.eids.has_key(db_row[0]):
                continue
            if db_row[0] in eids_not_migrate:
                continue
            image = self.images(folder, db_row, None)
            if not image:
                continue

            try:
                media = IMediaType(image)
                media.types = ['image']
            except:
                # links can't be adapted and shouldn't be
                pass

            #self._apply_themes(theme_id, image, page_id)

            self._change_workflow(image)
            self.catalog.indexObject(image)
            self._save_to_file(db_row[0],
                               '/'.join(image.getPhysicalPath()))

    def _save_to_file(self, eid, path):
        self.file.write(str(eid) + '|' + path + '\n')
        self.eids[eid] = True

    def _snapshot_pid(self, page_id):
        # media belonging to snapshot article
        cursor = self.db.cursor()
        cursor.execute(sql_cid_with_onetier_pid % page_id)
        cid = cursor.fetchone()[0]
        cursor.close()

        cursor = self.db.cursor()
        cursor.execute(sql_snapshot_pid % cid)
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return None


class MigrateArticles(object):
    """ Migrates articles from epaedia website. """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.dbname = request.get('db', 'epaedia')
        self.user = request.get('user', 'root')
        self.password = request.get('password', '')
        self.host = request.get('host', 'localhost')
        self.db = MySQLdb.connect(host=self.host, user=self.user, db=self.dbname,
                                  passwd=self.password,
                                  cursorclass=MySQLdb.cursors.SSDictCursor)
        self._article_file = open('articles.txt', 'w')
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.workflow = getToolByName(context, 'portal_workflow')
        self._read_file()
        self.pidpaths = {}
        self.themes = {}
        multimedia_path = request.get('multimedia_path')
        self.multimedia_folder = context.unrestrictedTraverse(multimedia_path)
        self.objects_with_links = {}

        portal_url = getToolByName(context, 'portal_url')
        portal = portal_url.getPortalObject()
        self.image_folder = portal.SITE.images

    def migrate(self):
        """ Some docstring. """

        self.themes = load_pid_theme_mapping()
        self._image_sizes = self._load_images()

        themes_folder = self.context
        if not themes_folder.hasProperty('navigation_sections_left'):
            themes_folder.manage_addProperty('navigation_sections_left',
                                             'subpages,Topics', 'lines')
        portlet = 'here/@@leftNavigationSections'
        portlets = themes_folder.getProperty('left_slots')
        if not portlet in portlets:
            new_portlets = portlets + (portlet,)
            themes_folder.manage_changeProperties(left_slots=new_portlets)

        themes_folder.getProperty('left_slots')
        epaedia_themes = self._epaedia_themes()
        for theme in epaedia_themes:
            page_id = theme['pid']
            # if the page has a theme migrate, not everyone has a theme
            # for instance 'Sustainable resources'
            if self.themes[page_id]:
                themecentre = self._themecentre(self.themes[page_id][0])
                self._migrate_articles(themecentre, theme)
        self._fix_internal_links()
        #self._fix_external_links()
        self._article_file.close()
        return 'migration of epaedia articles is successfully finished'

    def _apply_media_relations(self, folder, doc_id, page_id):
        doc = getattr(folder, doc_id)
        cursor = self.db.cursor()
        cursor.execute(sql_eids_by_pid % page_id)
        rows = cursor.fetchall()
        cursor.close()

        related = doc.getRelatedItems()
        for row in rows:
            eid = row['eid']
            # only apply relations to those media files that are migrated
            if not self.file_paths.has_key(eid):
                continue
            path = self.file_paths[eid].strip()
            file_obj = self.context.unrestrictedTraverse(path)
            related.append(file_obj)
        doc.setRelatedItems(related)

    def _apply_themes(self, article, page_id):
        themetag = IThemeTagging(article)
        tags = self.themes[page_id]
        themetag.tags = tags

    def _assign_subpages_section(self, obj):
        navContext = INavigationSectionPosition(obj)
        navContext.section = 'subpages'

    def _change_workflow(self, obj):
        pass

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
        article.processForm()
        article.setEffectiveDate(DEFAULT_EFFECTIVE_DATE)
        article.setModificationDate(DEFAULT_EFFECTIVE_DATE)
        self._change_workflow(article)
        article.reindexObject()
        self._save_pid_path(page_id, article)

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
                image = self._image_info(section['eid'])
                image_width = self._image_sizes[section['eid']]
                image_html = ('<div class="figure-plus-container figure-plus" style="width:%dpx">\n' % image_width) + \
                             '<div>\n' + \
                             ('<a href="%s"><img src="%s" alt="%s" /></a>' % \
                                 (image['path']+'/image_view_fullscreen', image['path']+'/image_mini', image['title'])) + \
                             '</div>\n' + \
                             ('<div class="figure-title">%s</div>\n' % image['title']) + \
                             (len(image['copyright'])>0 and ('<div class="figure-source-copyright">%s</div>\n' %
                                 image['copyright']) or '') + \
                              '</div>\n'

                if align == 'l':
                    left = image_html
                    right = body_html
                else:
                    left = body_html
                    right = image_html
                #total_body += '<table><td>%s</td><td>%s</td></table>\n' % \
                              #(left, right)
                total_body += '<div class="figure-left">\n' + \
                                image_html + '\n' + body_html + \
                              '</div>\n'

            # title, quote, body
            if section_type == 3 and section_no > 1:
                if len(title.strip()) > 0:
                    total_body += '<h2>%s</h2>\n' % title
                total_body += '<blockquote>\n' + \
                              '<p>%s</p>\n' % quote + \
                              '<p class="source">%s</p>\n' % tag + \
                              '</blockquote>\n'
                if len(body) > 0:
                    total_body += "<p>%s</p>\n" % body_html
            # title, body, link
            if section_type == 4 and section_no > 1:
                cursor = self.db.cursor()
                cursor.execute(sql_article_links % section['eid'])
                link = cursor.fetchone()
                cursor.close()

                #link_id = utils.normalizeString(title, encoding='latin1')
                #path = '/'.join(self.multimedia_path, link_id)

                if len(title.strip()) > 0:
                    total_body += '<h2>%s</h2>\n' % title

                if link['pid'] > 0:
                    # internal link, pid>0
                    link_str = 'PID' + str(link['pid']) + 'PID'

                    if not self.objects_with_links.has_key(page_id):
                        self.objects_with_links[page_id] = []
                    self.objects_with_links[page_id].append(link['pid'])
                else:
                    # external links, pid=0
                    link_str = link['link']
                    #if not self.external_links.has_key(page_id):
                    #    self.external_links[page_id] = []
                    #self.external_links[page_id].append(link['pid'])

                total_body += '<div class="linkbox"><div class="linkhref"><a href="%s" alt="%s">%s</a></div>' % \
                              (link_str, link['title'], link['title']) + \
                              '<div class="linkdesc">%s</div></div>\n' % \
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
        self._apply_themes(article, page_id)
        self._save_article(article, page_id)
        return article

    def _create_intro(self, folder, page_id):
        article = self._create_article_from_sections(folder, page_id,
                                                  id_suffix='-intro')
        self._apply_media_relations(folder, article.getId(), page_id)
        self._assign_subpages_section(article)
        return article.getId()

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
            article = self._create_article_from_sections(folder, pid,
                                                      id_suffix='-snapshot',
                                                      title='Snapshot')
            self._apply_media_relations(folder, article.getId(), page_id)
            self._assign_subpages_section(article)
            article.setExcludeFromNav(True)

            return article.getId()
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
            article = self._create_article_from_sections(folder, pid,
                                                      id_suffix='-fullarticle',
                                                      title='Full article')
            self._apply_media_relations(folder, article.getId(), page_id)
            self._assign_subpages_section(article)
            article.setExcludeFromNav(True)
            return article.getId()
        else:
            return None

    def _epaedia_themes(self):
        cursor = self.db.cursor()
        cursor.execute(sql_level_one)
        level_one = cursor.fetchall()
        cursor.close()
        return level_one

    def _fix_internal_links(self):
        for obj_pid, link_pids in self.objects_with_links.items():
            obj = self.pidpaths[obj_pid]
            text = obj.getText()
            
            for pid in link_pids:
                to_replace = 'PID' + str(pid) + 'PID'
                link_to = self.pidpaths[pid]
                link = "resolveuid/" + link_to.UID()
                new_text = text.replace(to_replace, link)
                # add object to "related pages"
                relations = obj.getRelatedItems()
                obj.setRelatedItems(relations + [link_to])

                obj.setText(new_text)
                obj.reindexObject()

    #def _fix_external_links(self):
    #    for obj_pid, link_pids in self.external_links.items():
    #        obj = self.pidpaths[obj_pid]
    #        link_obj = 

    def _image_info(self, eid):
        cursor = self.db.cursor()
        cursor.execute(sql_image_by_eid % eid)
        image = cursor.fetchone()
        cursor.close()

        if eid in missing_title:
            title = missing_title[eid]
        else:
            title = image['title']
        image_id = utils.normalizeString(title, encoding='latin1')
        try:
            imageobj = getattr(self.image_folder, image_id)
        except:
            1/0
        path = 'resolveuid/' + imageobj.UID()
        return { 'path': path, 'title': image['title'],
                'copyright': image['source'] }

    def _load_images(self):
        path = os.path.dirname(__file__) + os.path.sep + 'epaedia-images.csv'
        mapping = {}

        for line in open(path, 'r'):
            eid, orig_size, new_size = line.split(',')
            mapping[int(eid)] = int(new_size.split('x')[0])

        return mapping

    def _migrate_articles(self, folder, theme):
        """ migrates every article in mysql which belongs to the main
            theme 'theme'. 'folder' is where the content will be added. """

        page_id = theme['pid']
        theme_id = self.themes[page_id][0]
        cid = theme['cid']

        doc_id = self._create_intro(folder, page_id)
        intro = getattr(folder, doc_id)
        doc_id = self._create_snapshot(folder, page_id)
        snapshot = getattr(folder, doc_id)
        doc_id = self._create_fullarticle(folder, page_id)
        fullarticle = getattr(folder, doc_id)

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
            level_two_folder.processForm()
            level_two_folder.setEffectiveDate(DEFAULT_EFFECTIVE_DATE)
            level_two_folder.setModificationDate(DEFAULT_EFFECTIVE_DATE)
            self._assign_subpages_section(level_two_folder)
            self._change_workflow(level_two_folder)
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
                level_three_folder.processForm()
                level_three_folder.setEffectiveDate(DEFAULT_EFFECTIVE_DATE)
                level_three_folder.setModificationDate(DEFAULT_EFFECTIVE_DATE)
                self._assign_subpages_section(level_two_folder)
                self._change_workflow(level_three_folder)
                level_three_folder.reindexObject()

                pid = menu_item['pid']

                new_id = self._create_intro(level_three_folder, pid)
                if new_id:
                    level_three_folder.manage_addProperty('default_page',
                                                          new_id, 'string')
    def _nl_to_p(self, text):
        result = ''
        for para in text.split('\n'):
            if para.strip():
                result += '<p>%s</p>' % para
        return result

    def _read_file(self):
        self.file_paths = {}
        file = open('media_files.txt', 'r')
        for line in file:
            eid, file_path = line.split('|')
            self.file_paths[int(eid)] = file_path
        file.close()

    def _relate(self, intro, snapshot, fullarticle):
        current_intro = intro.getRelatedItems()
        current_snap = intro.getRelatedItems()
        current_full = intro.getRelatedItems()

        intro.setRelatedItems([snapshot, fullarticle] + current_intro)
        snapshot.setRelatedItems([intro, fullarticle] + current_snap)
        fullarticle.setRelatedItems([intro, snapshot] + current_full)

        intro.reindexObject()
        snapshot.reindexObject()
        fullarticle.reindexObject()

    def _relate_link(self, article1, linked_article):
        current_relations = article1.getRelatedItems()
        #current_article2 = linked_article.getRelatedItems()

        article1.setRelatedItems([linked_article] + current_relations)
        #linked_article.setRelatedItems([article1] + current_article2)

    def _save_article(self, article, page_id):
        self._article_file.write(str(page_id) + '|' + '/'.join(article.getPhysicalPath()) + '\n')

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
        themes = self.catalog.searchResults(object_provides=iface)
        # there should be exactly one themecentre for each theme
        for theme in themes:
            obj = theme.getObject()
            if IThemeCentreSchema(obj).tags == theme_id:
                return obj
        raise 'No theme exists with id ' + theme_id

    def _save_pid_path(self, pid, obj):
        self.pidpaths[pid] = obj
