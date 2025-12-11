from factory import Iterator, LazyFunction, PostGenerationMethodCall
from factory import LazyAttribute
from factory import SubFactory
from factory import Sequence
from factory.django import DjangoModelFactory
from faker import Faker
from supports.models import SupporTicket, TicketMessage
from users.models import User




faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    password = PostGenerationMethodCall('set_password', 'testpass123')
    login = Sequence(lambda n: f"user_{n}")
    name = Sequence(lambda n: f"user_{n}")
    email = LazyFunction(lambda: faker.email())
    message = Sequence(lambda n: "message_%03d" % n)

    is_superuser = Iterator([True, False])

    is_staff = Iterator([True, False])
    is_active = Iterator([True, False])

class SupporTicketFactory(DjangoModelFactory):
    class Meta:
        model = SupporTicket

    asker_id = SubFactory(UserFactory)
    responsible_id = SubFactory(UserFactory)

    def __str__(self):
        return f"Dialog between {self.user1}, {self.user2}"


class TicketMessageFactory(DjangoModelFactory):
    class Meta:
        model = TicketMessage

    # is_removed = Iterator([True, False])
    sender_id = SubFactory(UserFactory)
    recipient_id = SubFactory(UserFactory)
    text = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    file = LazyAttribute(lambda x: None)
    read = Iterator([True, False])