""" ThemeTaggable """
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent
from Products.LinguaPlone.public import InAndOutWidget, BaseContent
from Products.LinguaPlone.public import Schema, StringField
from Products.validation.config import validation
from Products.validation.interfaces.IValidator import IValidator
from eea.themecentre.interfaces import IThemeTagging, IThemeTaggable
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zope.interface import implements

class ThemesField(StringField):
    """ Save themes as annotation """

    def set(self, instance, value, **kwargs):
        """ Save as annotation
        """
        IThemeTagging(instance).tags = [val for val in value if val]

    def get(self, instance, **kwargs):
        """ Get from annotation
        """
        return IThemeTagging(instance).tags

class MaxValuesValidator(object):
    """ Validator
    """
    implements(IValidator)

    def __init__( self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, instance, *args, **kwargs):
        maxValues = getattr(kwargs['field'].widget, 'maxValues', None)
        value = [ val for val in value
                      if val ]
        if maxValues is not None and len(value)>maxValues:
            return "To many values, please choose max %s." % maxValues
        return 1

validation.register(MaxValuesValidator('maxValues'))

schema = Schema((

    ThemesField(
        name='themes',
        schemata='categorization',
        validators=('maxValues',),
        widget=InAndOutWidget
        (
            maxValues=3,
            label="Themes",
            description="Choose max 3 themes",
            label_msgid='EEAContentTypes_label_themes',
            description_msgid='EEAContentTypes_help_themes',
            i18n_domain='EEAContentTypes',
        ),
        languageIndependent=True,
        vocabulary='_getMergedThemes',
        index="KeywordIndex:brains",
        enforceVocabulary=1,
        default=[],
        accessor='getThemes',
        mutator='setThemes',
    ),

),
)


ThemeTaggable_schema = schema.copy()

class ThemeTaggable(BaseContent):
    """ Theme Taggable Content-Type
    """
    implements(IThemeTaggable)
    security = ClassSecurityInfo()

    allowed_content_types = []
    _at_rename_after_creation = True

    schema = ThemeTaggable_schema

    # Methods
    def getThemes(self):
        """ Getter
        """
        tagging = IThemeTagging(self)
        return tagging.tags

    security.declareProtected(ModifyPortalContent, 'setThemes')
    def setThemes(self, value, **kw):
        """ Use the tagging adapter to set the themes. """
        #value = filter(None, value)
        value = [val for val in value if val]
        tagging = IThemeTagging(self)
        tagging.tags = value

    def _getMergedThemes(self):
        """ Merged themes
        """
        vocab = getUtility(IVocabularyFactory,
                           name="Allowed themes for edit")(self)
        return [(term.value, term.title) for term in vocab]
