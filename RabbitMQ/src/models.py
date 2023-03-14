from mongoengine import Document
from mongoengine.fields import StringField, EmailField, BooleanField


class Contact(Document):
    fullname = StringField(required=True)
    phone = StringField()
    email = EmailField()
    send = BooleanField(default=False)
