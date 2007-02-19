from zope.formlib.form import Fields, EditForm
from eea.themecentre.interfaces import IThemeTagging

class ThemeEditForm(EditForm):
    """ Form for editing themes. """

    form_fields = Fields(IThemeTagging)
    label = u'Edit themes'
