import grok


grok.definelayer('my')
grok.defineskin('my')  # Picks up the layer 'my' if it exists

# If there is only a single layer defined in a module, it will be the default
grok.layer('my')


class Painting(grok.View):
    pass


fireplace = grok.PageTemplate("""\
<html><body></body></html>
""")
