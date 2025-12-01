from zoneinfo import ZoneInfo

from django.conf import settings

from factory import Iterator
from factory import LazyAttribute
from factory import SubFactory
from factory import Sequence
from factory.django import DjangoModelFactory
from faker import Faker
from supports.models import DialogsModel, MessageModel
from users.models import User




faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    password = LazyAttribute(lambda x: faker.text(max_nb_chars=128))
    login = LazyAttribute(lambda x: faker.text(max_nb_chars=255))
    name = Sequence(lambda n: "user_%03d" % n)
    email = faker.email()

    is_superuser = Iterator([True, False])

    is_staff = Iterator([True, False])
    is_active = Iterator([True, False])

class DialogsModelFactory(DjangoModelFactory):
    class Meta:
        model = DialogsModel

    user1 = SubFactory(UserFactory)
    user2 = SubFactory(UserFactory)


class MessageModelFactory(DjangoModelFactory):
    class Meta:
        model = MessageModel

    # is_removed = Iterator([True, False])
    sender = Iterator(User.objects.all())
    recipient = Iterator(User.objects.all())
    text = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    file = LazyAttribute(lambda x: None)
    read = Iterator([True, False])