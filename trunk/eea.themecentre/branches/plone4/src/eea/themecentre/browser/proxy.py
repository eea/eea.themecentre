""" Proxy module
"""
from zope.component import getMultiAdapter
from Products.Five import BrowserView

class Proxy(BrowserView):
    """ Proxy
    """

    def real_view(self, view_name=None):
        """ Real view
        """
        if not view_name:
            view_name = self.request['view_name']

        context = self.context()
        view = getMultiAdapter((context, self.request),
                               name=view_name)
        view.view_name = view_name
        return view
