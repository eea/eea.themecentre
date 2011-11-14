""" EEA Theme Centre import steps
"""
from Products.CMFCore.utils import getToolByName

def setupMergedThemesVocabulary(context):
    """ Setup Merged Themes Vocabulary
    """
    site = context.getSite()
    vocab = getToolByName(site, 'portal_vocabularies')

    if not getattr(vocab, 'themesmerged', None):
        vocab.invokeFactory('TreeVocabulary', id='themesmerged')
    mergedthemes = vocab.getVocabularyByName('themesmerged')

    themes = {'acidification': 'air',
              'air_quality': 'air',
              'health': 'human',
              'information': 'reporting',
              'management': 'policy',
              'nature': 'biodiversity',
              'ozone': 'climate',
              'population': 'economy',
              'reporting': 'policy'}

    for theme, mergedwith in themes.items():
        if not hasattr(mergedthemes, theme):
            tId = theme
            tId = mergedthemes.invokeFactory('TreeVocabularyTerm',
                                             id=tId)
            t = mergedthemes[tId]
            t.setTitle(theme)
            mId = mergedwith
            mId = mergedthemes[tId].invokeFactory('TreeVocabularyTerm',
                                                  id=mId)
            t[mId].setTitle(mergedwith)

def setupVarious(context):
    """ Setup various
    """
    if context.readDataFile('eea.themecentre.txt') is None:
        return

    logger = context.getLogger('eea.themecentre')

    setupMergedThemesVocabulary(context)
    logger.info("EEA Theme Centre: merged themes vocabulary added")

    logger.info("EEA Theme Centre: done setting import steps")
    return
