from Products.Five.formlib.formbase import EditForm
from zope.formlib.form import Fields
from eea.themecentre.interfaces import IThemeTagging

class ThemeEditForm(EditForm):
    """ Form for editing themes. """

    form_fields = Fields(IThemeTagging)
    label = u'Edit themes'
