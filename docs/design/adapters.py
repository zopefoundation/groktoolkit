import grok
from calc import Calculator
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserView


class ISomething(Interface):
    pass


class SingleAdapter(grok.Adapter):
    grok.context(Calculator)
    # generally allowed, but not in this case, because there's already
    # grok.context:
    grok.adapts(Calculator)
    grok.implements(ISomething)  # if this is not specified, app breaks
    grok.provides(ISomething)  # if adapter implements more than one interface
    grok.name('')  # this is actually the default

    def something(self):
        """self.context is automatically provided"""
        return self.context.foo


class CalculatorContentProvider(grok.MultiAdapter):
    grok.adapts(Calculator, IBrowserRequest, IBrowserView)
    grok.implements(IContentProvider)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    # ...
