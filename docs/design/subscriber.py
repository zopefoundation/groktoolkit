import grok
from calc import Calculator
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


@grok.subscriber(Calculator, IObjectModifiedEvent)
def calculatorChanged(calc, event):
    pass


# perhaps alias zope.event.notify to grok.notify???
