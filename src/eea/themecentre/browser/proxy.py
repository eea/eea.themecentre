from Products.CMFPlone import utils
from zope.component import getMultiAdapter
from zope.publisher.interfaces.browser import  IBrowserRequest

class Proxy(utils.BrowserView):

    def real_view(self, view_name=None):
        if not view_name:
            view_name = self.request['view_name']

        context = utils.context(self)
        view = getMultiAdapter((context, self.request),
                               name=view_name)
        view.view_name = view_name
        return view
