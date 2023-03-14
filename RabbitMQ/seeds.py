from faker import Faker

from src.models import Contact
from MongoDB import connect

fake = Faker('uk-UA')


def seed_contact():
    contacts = []
    for i in range(15):
        contact = Contact(fullname=fake.name(),
                          phone=fake.phone_number(),
                          email=fake.email(),
                          send=False).save()
        contacts.append(contact.id)
    return contacts


if __name__ == '__main__':
    seed_contact()
