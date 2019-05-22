""" Upgrade scripts for 9.7 version of this package
"""
import logging
import transaction
from Products.Archetypes.utils import shasattr
from eea.themecentre.vocabulary import vocabs
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger("eea.themecentre upgrades 9.7")


def setupATVocabularies(portal):
    """ Installs all AT-based Vocabularies """

    vkeys = vocabs.keys()
    atvm = getToolByName(portal, 'portal_vocabularies', None)
    if atvm is None:
        logger.info("Products.ATVocabularyManager is NOT installed")
        return

    for vkey in vkeys:

        if shasattr(atvm, vkey):
            continue

        logger.info("adding vocabulary %s", vkey)

        try:
            atvm.invokeFactory('SimpleVocabulary', id=vkey,
                               title='Popular Searches')
        except Exception:
            logger.info("Error adding vocabulary %s", vkey)

        vocab = atvm[vkey]
        # enable once we have actual data
        # workflow = getToolByName(portal, 'portal_workflow')
        # workflow.doActionFor(vocab, 'publish')
        for (ikey, value) in vocabs[vkey]:
            vocab.invokeFactory('SimpleVocabularyTerm', ikey)
            vocab[ikey].setTitle(value)

    transaction.savepoint(optimistic=True)
    logger.info("Adding eea.themecentre popular search catalog ... DONE")
