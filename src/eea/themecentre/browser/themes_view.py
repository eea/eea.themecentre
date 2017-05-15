""" Themes view logic
"""
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
import DateTime


class ThemesView(BrowserView):
    """ Themes view logic """


    def __call__(self):
        return self.template_view()

    def getCurrentLanguage(self):
        """ Getthe current user language """
        context = aq_inner(self.context)
        plt = getToolByName(context, 'portal_languages')
        return plt.getPreferredLanguage()

    def getPromotions(self):
        """ Get the 5 promotions to show on top """
        pl = self.getCurrentLanguage()
        ret_themes = []
        context = aq_inner(self.context)
        if pl != 'en':
            context = context.getCanonical()
        collections = context.restrictedTraverse('megatopics-collections', None)
        if not collections:
            return None
        topics = collections.getFolderContents(contentFilter={
            'portal_type': 'Topic', 'sort_on': 'getObjPositionInParent'})
        now = DateTime.DateTime()
        for topic in topics:
            ret_dict = {}
            tobj = topic.getObject()
            tobj_title = tobj.Title()
            ret_dict[tobj_title] = []
            ret_list = ret_dict[tobj_title]
            brains = tobj.queryCatalog()
            for brain in brains:
                url = brain.getURL()
                t = url, brain
                # do not show expired content
                if brain.expires <= now:
                    continue
                if 'eea.promotion.interfaces.IPromoted' in \
                    brain.object_provides:
                    can_url = brain.getObject().getCanonical().absolute_url()
                    ret_list.insert(0, can_url)
                ret_list.append(t)
            ret_themes.append(ret_dict)

        return ret_themes

    def getThemes(self):
        """ Get the themes translated
            The order of the themes was previously defined,
            we use a list of uid to keep the same order
        """
        themes = [["0d2e3d3da1d2f8f1cc4f029a27b931d0",
                   "cd6bef0c97b6c8ea3e216267af7f1605",
                   "619d5ebc70dbdf9895dda7c815c5364b",
                   "6723e6872d33d022a07eeae0e235ac48",
                   "25f41725a7916d7368797edf78f06cad",
                   "5412da76e31aedcea4ce1d520518604f",
                   "c64f9ed39bae175c77ee5fe3729472f6",
                   "5757e1ebd370ac9f0b9d9c4c41667304",
                   "e1129312d1ed476a3c54cf1c256e972f",
                   "912645e2479b571df739342b290cabbc",
                   "b6ef38c3f2e84948314b397d7668ea41",
                   "057759082066e8d4cc5ff7f3f8364442"],
                  ["47c19827e0f4e840c77ae6281f124f50",
                   "3cdc3686b331e7d580f9ade779c72ad9",
                   "61d1a9fbb975c5f3032dae362b3fff3b",
                   "5608e23801e3ac58668f8db1bdc0dc66",
                   "701da5f4fedf304c23433cba18a76fa2",
                   "e6a0723e37a75edc6a5387f8881eb183",
                   "29c22f68b31a59ba5e93f965ae506868",
                   "ca85d70438bcda31f0014606bced7455"],
                  ["c79b3492043943b66cffa48c47f4c3a2",
                   "515694fae21c1d760e5179a63291750b",
                   "e1a9f122c53c04739892f0e81a902989"],
                  ["0742501c1bd96c82e8bb993ee49f120c",
                   "f68e62dd80ecbc75f123197e48ef3ceb",
                   "bd4c672611920251e0ae681dfcbfd285"]]

        # We get the translation for each theme, otherwise we
        # return the theme in english
        pl = self.getCurrentLanguage()
        ret_themes = []
        context = aq_inner(self.context)

        for lthemes in themes:
            ret_list = []
            for theme in lthemes:
                o = context.reference_catalog.lookupObject(theme)
                if not o:
                    continue
                if o.hasTranslation(pl):
                    # Tuple containing the url, the object
                    t = o.absolute_url(), o.getTranslation(pl)
                    ret_list.append(t)
                else:
                    t = o.absolute_url(), o
                    ret_list.append(t)
            ret_themes.append(ret_list)

        return ret_themes
