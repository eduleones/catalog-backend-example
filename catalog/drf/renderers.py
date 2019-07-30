from collections import OrderedDict

from rest_framework.renderers import JSONRenderer

from config import __version__


class CustomJSONRenderer(JSONRenderer):

    charset = 'utf-8'

    def render(self, data, *args, **kwargs):
        meta = {
            'version': __version__,
        }

        if data and all(
            [key in data for key in ('count', 'next', 'previous')]
        ):
            modified_data = data.pop('results', [])
            meta.update(data)
        else:
            modified_data = data

        response = OrderedDict([
            ('meta', meta),
            ('data', modified_data)
        ])

        return super(CustomJSONRenderer, self).render(
            response,
            *args, **kwargs
        )
