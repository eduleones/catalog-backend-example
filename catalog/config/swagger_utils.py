import yaml

from django.conf import settings
from urllib import parse
from rest_framework.compat import coreapi
from rest_framework.schemas import SchemaGenerator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_swagger import renderers


class CustomSchemaGenerator(SchemaGenerator):
    """
    Custom schema generator to support Swagger YAML docs.

    See:
        https://github.com/marcgibbons/django-rest-swagger/issues/549
        https://gist.github.com/gjain0/f536d3988eb61e693ea306305c441bb7
    """

    def get_link(self, path, method, view):
        """
        Parse YAML docs.

        __doc__ in yaml format, eg:
        description: the desc of this api.
        parameters:
        - name: mobile
          description: the mobile number
          type: string
          required: true
          location: query
        - name: promotion
          description: the activity id
          type: int
          required: true
          location: form
        """
        method_desc = ''
        fields = self.get_path_fields(path, method, view)

        func = getattr(view, method.lower(), None)

        yaml_doc = None
        if func and func.__doc__:
            try:
                method_desc, raw_yaml_doc = func.__doc__.split('---')
                yaml_doc = yaml.load(raw_yaml_doc)
            except Exception:
                yaml_doc = None

        if yaml_doc and 'parameters' in yaml_doc:
            for parameter in yaml_doc.get('parameters'):
                field = coreapi.Field(
                    name=parameter.get('name'),
                    description=parameter.get('description'),
                    required=parameter.get('required', True),
                    type=parameter.get('type', 'string'),
                    location=parameter.get('paramType', 'query')
                )
                fields.append(field)

        fields += self.get_serializer_fields(path, method, view)
        fields += self.get_pagination_fields(path, method, view)
        fields += self.get_filter_fields(path, method, view)

        if fields and any([f.location in ('form', 'body')
                           for f in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=parse.urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=method_desc
        )


class CustomOpenAPIRenderer(renderers.OpenAPIRenderer):

    def get_customizations(self):
        data = super(CustomOpenAPIRenderer, self).get_customizations()
        if settings.SWAGGER_USE_HTTPS:
            data['schemes'] = ['https']
        return data


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Return schema view which renders Swagger/OpenAPI.

    See:
        https://github.com/marcgibbons/django-rest-swagger/blob/master/
        rest_framework_swagger/views.py#L11
    """
    class SwaggerSchemaView(APIView):
        permission_classes = [AllowAny]
        renderer_classes = [
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            generator = SchemaGenerator()
            schema = generator.get_schema(request=request)

            return Response(schema)

    return SwaggerSchemaView.as_view()
