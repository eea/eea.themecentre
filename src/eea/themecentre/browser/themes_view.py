""" Themes view logic
"""
from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.themecentre import eeaMessageFactory as _

class ThemesView(BrowserView):
    """ Themes view logic """
    
    template_view = ViewPageTemplateFile('templates/themes_view.pt')

    def __call__(self):
        return self.template_view()
    
    def getCurrentLanguage(self):
        # Get user current language
        context = aq_inner(self.context)
        plt = getToolByName(context, 'portal_languages')
        return plt.getPreferredLanguage()        
    
    def getPromotions(self):
        """ Get the 5 promotions """
        
        pl = self.getCurrentLanguage()
        
        # define promotions
        ret_promotions = [] 
        promotions = [("0d2e3d3da1d2f8f1cc4f029a27b931d0",
                       "not-just-hot-air",
                       _(u"visit-pollution-website", default = u"Visit our air pollution website")),
                      ("cd6bef0c97b6c8ea3e216267af7f1605",
                       "assessing-biodiversity",
                       _(u"visit-biodiversity-website", default = u"Visit our biodiversity website")),
                      ("6723e6872d33d022a07eeae0e235ac48",
                       "new-estimates-confirm-the-declining-trend-in-eu-greenhouse-gas-emissions",
                       _(u"visit-climate-website", default = u"Visit our climate change website")),
                      ("5412da76e31aedcea4ce1d520518604f",
                       "discover-europe2019s-landscape-through-satellite-and-ground-level-pictures-1",
                       _(u"visit-land-use-website", default = u"Visit our land use website")),
                      ("b6ef38c3f2e84948314b397d7668ea41",
                       "heading-for-your-favourite-beach-is-the-bathing-water-clean",
                       _(u"visit-water-website", default = u"Visit our water website"))]
        
        # get promotion attributes and title in current language
        context = aq_inner(self.context)
        tr_tool = getToolByName(context, 'translation_service')
        
        for promo in promotions:
            o = context.reference_catalog.lookupObject(promo[0])
            if o.hasTranslation(pl):
                t = o.getTranslation(pl), promo[1], tr_tool.translate(promo[2], domain = "eea", target_language = pl), o.absolute_url()
                ret_promotions.append(t)
            else:
                t = o, promo[1], promo[2], o.absolute_url()
                ret_promotions.append(t)
                            
        return ret_promotions
    
    def getThemes(self):
        
        # The order of the themes was previously defined, we use a list of uid to keep the same order 
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
        
        # We get the translation for each theme
        pl = self.getCurrentLanguage()        
        ret_themes = []
        context = aq_inner(self.context)
        
        for lthemes in themes:
            ret_list = []
            for theme in lthemes:
                o = context.reference_catalog.lookupObject(theme)
                t = o.absolute_url(), o.getTranslation(pl)
                ret_list.append(t)
            ret_themes.append(ret_list)
            
        return ret_themes
    
        
    