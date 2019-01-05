import coreapi
from rest_framework.schemas import ManualSchema, AutoSchema

registration_schema = ManualSchema(
    description='Registration',
    fields=[
        coreapi.Field('username', required=True, location='form', type='string', description='Username'),
        coreapi.Field('email', required=True, location='form', type='string', description='Email'),
        coreapi.Field('password', required=True, location='form', type='string', description='Password')
    ]
)