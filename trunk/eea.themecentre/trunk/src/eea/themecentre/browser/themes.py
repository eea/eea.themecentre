""" Themes
"""
from Products.CMFCore.utils import getToolByName
from five.formlib.formbase import EditForm
from zope.app.form.browser.itemswidgets import OrderedMultiSelectWidget
from zope.formlib.form import Fields
from eea.themecentre.interfaces import IThemeTagging
from eea.themecentre.vocabulary import ThemesEditVocabularyFactory
from eea.themecentre.vocabulary import ThemesVocabularyFactory

class ThemesOrderedWidget(OrderedMultiSelectWidget):
    """ Widget showing the themes that are selected and available.
    """

    def __init__(self, field, request):
        vocabulary = ThemesVocabularyFactory(field)
        super(ThemesOrderedWidget, self).__init__(field, vocabulary, request)

    def choices(self):
        """ Return a set of tuples (text, value) that are available.
        """
        # Not all content objects must necessarily support the attributes
        if hasattr(self.context.context, self.context.__name__):
            available_values = self.context.get(self.context.context)
        else:
            available_values = []
        vocab = ThemesEditVocabularyFactory(self.vocabulary)
        return [{'text': self.textForValue(term), 'value': term.token}
                for term in vocab
                if term.value not in available_values]

    def selected(self):
        """ Return a list of tuples (text, value) that are selected.
        """
        # Get form values
        values = self._getFormValue()
        # Not all content objects must necessarily support the attributes
        if hasattr(self.context.context, self.context.__name__):
            # merge in values from content
            for value in self.context.get(self.context.context):
                if value not in values and value is not None:
                    values.append(value)

        terms = [self.vocabulary.getTerm(val)
                     for val in values if val not in [None, '']]
        nondeprecated = ThemesEditVocabularyFactory(self.context)
        result = []
        for term in terms:
            if term.value in nondeprecated:
                result.append({'text': self.textForValue(term),
                              'value': term.token})
            else:
                result.append({
                        'text': self.textForValue(term) + ' (deprecated)',
                        'value': term.token})
        return result

    def required(self):
        """ Required
        """
        return False

class ThemeEditForm(EditForm):
    """ Form for editing themes.
    """

    label = u'Edit themes'
    form_fields = Fields(IThemeTagging)
    form_fields['tags'].custom_widget = ThemesOrderedWidget

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')

        # by default max_length is decided by the IThemeTagging interface
        # but managers want to be able to add any number of themes
        if mtool.checkPermission('Manage portal', self.context):
            self.form_fields['tags'].field.max_length = None

        return super(ThemeEditForm, self).__call__()
