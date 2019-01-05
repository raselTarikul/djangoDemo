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

login_schema = ManualSchema(
    description='Login Device',
    fields=[
        coreapi.Field('username', required=True, location='form', type='string', description='Username'),
        coreapi.Field('password', required=True, location='form', type='string', description='Password')
    ]
)

change_pass_schema = ManualSchema(
    description='Change Password',
    fields=[
        coreapi.Field('username', required=True, location='form', type='string', description='Username'),
        coreapi.Field('password', required=True, location='form', type='string', description='Password'),
        coreapi.Field('new_password', required=True, location='form', type='string', description='New Password')
    ]
)