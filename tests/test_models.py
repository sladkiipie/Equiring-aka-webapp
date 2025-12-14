#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django_private_chat2
------------

Tests for `django_private_chat2` models module.
"""

from django.test import TestCase

from supports.models import SupporTicket, TicketMessage, UploadedFile
from django.forms.models import model_to_dict

from django.db import IntegrityError
from .factories import SupporTicketFactory, TicketMessageFactory, UserFactory, faker


class UploadedFileModelTests(TestCase):
    def setUp(self) -> None:
        self.file = UploadedFile.objects.create(uploaded_by=UserFactory.create(), file="LICENSE")

    def test_str(self):
        self.assertEqual(str(self.file), "LICENSE")


class MessageAndDialogModelTests(TestCase):

    def setUp(self):
        UserFactory.create_batch(10)
        self.msg1 = TicketMessageFactory.create()

    def test_str_message(self):
        self.assertEqual(str(self.msg1), str(self.msg1.pk))

    def test_str_dialog(self):
        u1, u2 = UserFactory.create(), UserFactory.create()
        dialog = SupporTicketFactory.create(asker=u1, responsible=u2)
        self.assertEqual(str(dialog), f"Dialogs beetwen {u1.login} {u2.login}")

    def test_dialog_unique(self):
        u1, u2 = UserFactory.create(), UserFactory.create()
        SupporTicketFactory.create(asker=u1, responsible=u2)
        SupporTicketFactory.create(asker=u2, responsible=u1)
        self.assertRaises(IntegrityError, SupporTicketFactory.create, responsible=u1, asker=u2)

    def test_get_dialogs_for_user(self):
        u1, u2 = UserFactory.create(), UserFactory.create()
        SupporTicketFactory.create(asker=u1, responsible=u2)
        d = SupporTicket.get_dialogs_for_user(user=u1).first()
        d2 = SupporTicket.get_dialogs_for_user(user=u2).first()
        self.assertEqual(d, d2)

    def test_get_unread_count_for_dialog_with_user(self):
        sender_id, recipient_id = UserFactory.create(), UserFactory.create()
        num_unread = faker.random.randint(1, 20)
        _ = TicketMessageFactory.create_batch(num_unread, read=False, sender=sender_id, recipient=recipient_id)

        self.assertEqual(TicketMessage.get_unread_count_for_dialog_with_user(sender_id, recipient_id), num_unread)

    def test_get_last_message_for_dialog(self):
        sender_id, recipient_id = UserFactory.create(), UserFactory.create()
        last_message = TicketMessageFactory.create(sender=sender_id, recipient=recipient_id)

        last_message1 = TicketMessage.get_last_message_for_dialog(sender_id, recipient_id)
        last_message2 = TicketMessage.get_last_message_for_dialog(recipient_id, sender_id)

        self.assertEqual(last_message, last_message1)
        self.assertEqual(last_message, last_message2)

    def test_save_creates_dialog_if_not_exists(self):
        before = SupporTicket.objects.count()
        sender_id, recipient_id = UserFactory.create(), UserFactory.create()
        TicketMessageFactory.create(sender=sender_id, recipient=recipient_id)
        after = SupporTicket.objects.count()
        self.assertEqual(after, before + 1)

    def tearDown(self):
        pass


class TestCaseSupporTicketGenerated(TestCase):

    def test_create(self):
        """
        Test the creation of a SupporTicket model using a factory
        """
        dialogs_model = SupporTicketFactory.create()
        self.assertEqual(SupporTicket.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 SupporTicket models using a factory
        """
        dialogs_models = SupporTicketFactory.create_batch(5)
        self.assertEqual(SupporTicket.objects.count(), 5)
        self.assertEqual(len(dialogs_models), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of SupporTicket server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        dialogs_model = SupporTicketFactory.create()
        dialogs_model_dict = model_to_dict(dialogs_model)
        self.assertEqual(len(dialogs_model_dict.keys()), 6)

    def test_attribute_content(self):
        """
        Test that all attributes of SupporTicket server have content. This test will break if an attributes name is changed.
        """
        dialogs_model = SupporTicketFactory.create()
        self.assertIsNotNone(dialogs_model.created)
        self.assertIsNotNone(dialogs_model.modified)
        self.assertIsNotNone(dialogs_model.id)
        self.assertIsNotNone(dialogs_model.asker)
        self.assertIsNotNone(dialogs_model.responsible)


class TestCaseTicketMessageGenerated(TestCase):
    def setUp(self):
        UserFactory.create_batch(15)

    def test_create(self):
        """
        Test the creation of a TicketMessage model using a factory
        """

        message_model = TicketMessageFactory.create()

        self.assertEqual(TicketMessage.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 TicketMessage models using a factory
        """
        message_models = TicketMessageFactory.create_batch(5)
        self.assertEqual(TicketMessage.objects.count(), 5)
        self.assertEqual(len(message_models), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of TicketMessage server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        message_model = TicketMessageFactory.create()
        message_model_dict = model_to_dict(message_model)
        self.assertEqual(len(message_model_dict.keys()), 8 )

    def test_attribute_content(self):
        """
        Test that all attributes of TicketMessage server have content. This test will break if an attributes name is changed.
        """
        message_model = TicketMessageFactory.create()
        self.assertIsNotNone(message_model.created)
        self.assertIsNotNone(message_model.modified)
        self.assertIsNotNone(message_model.is_removed)
        self.assertIsNotNone(message_model.id)
        self.assertIsNotNone(message_model.sender_id)
        self.assertIsNotNone(message_model.recipient_id)
        self.assertIsNotNone(message_model.text)
        self.assertIsNone(message_model.file)
        self.assertIsNotNone(message_model.read)