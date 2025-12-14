import factory

from factory import Iterator, LazyFunction, PostGenerationMethodCall
from factory import LazyAttribute
from factory import SubFactory
from factory import Sequence
from factory.django import DjangoModelFactory
from faker import Faker
from supports.models import SupporTicket, TicketMessage
from users.models import User, Companies, Contracts


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

class CompanyFactory(DjangoModelFactory):
    class Meta:
        model = Companies
    INN = Sequence(lambda n: 100000000 + n)
    OGRN = Sequence(lambda n: 100000000000 + n)
    name_company = Sequence(lambda n: f"company_{n}")
    status = Iterator([choice[0] for choice in Companies.STATUS_CHOICES])

    @factory.post_generation # Функция для адекватной работы ManyToMany
    def founder(self, creaete, extracted, **kwargs):
        if not creaete:
            return
        if extracted:
            self.founder = set(extracted)
        else:
            self.founder.add(UserFactory())

class ContractsFactory(DjangoModelFactory):
    class Meta:
        model = Contracts

    company = SubFactory(CompanyFactory)
    name_contract = Sequence(lambda n: f"company_{n}")
    status = Iterator([choice[0] for choice in Contracts.STATUS_CHOICES])

class SupporTicketFactory(DjangoModelFactory):
    class Meta:
        model = SupporTicket

    asker = SubFactory(UserFactory)
    responsible = SubFactory(UserFactory)
    contract = SubFactory(ContractsFactory)
    description = Sequence(lambda n: f"Support Ticket {n}")
    status = Iterator([choice[0] for choice in SupporTicket.STATUS_CHOICES])

    def __str__(self):
        return f"Dialog between {self.user1}, {self.user2}"


class TicketMessageFactory(DjangoModelFactory):
    class Meta:
        model = TicketMessage

    # is_removed = Iterator([True, False])
    ticket = SubFactory(SupporTicketFactory)
    sender = SubFactory(UserFactory)
    recipient = SubFactory(UserFactory)
    text = LazyAttribute(lambda x: faker.paragraph(nb_sentences=3, variable_nb_sentences=True))
    file = LazyAttribute(lambda x: None)
    read = Iterator([True, False])