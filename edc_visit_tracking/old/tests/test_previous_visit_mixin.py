from django.utils import timezone

# from edc_testing.models import TestVisitModel2
from edc_appointment.models.appointment import Appointment
from edc_constants.constants import SCHEDULED
from edc_visit_schedule.models.visit_definition import VisitDefinition
from edc_visit_tracking.models import PreviousVisitError

from .base_test_case import BaseTestCase
from .test_models import TestVisitModel, TestVisitModel2


class TestPreviousVisitMixin(BaseTestCase):

    def test_previous_visit_definition(self):
        """Asserts visit definitions exist in sequence."""
        TestVisitModel.requires_previous_visit = False
        visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        TestVisitModel.requires_previous_visit = False
        test_visit = TestVisitModel.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(test_visit.previous_visit_definition(visit_definition).code, '1000')

    def test_previous_visit_doesnotexist(self):
        """Asserts the first scheduled visit has no previous visit."""
        TestVisitModel.requires_previous_visit = False
        self.visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=self.visit_definition)
        test_visit = TestVisitModel.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertIsNone(test_visit.previous_visit())

    def test_previous_visit_exists(self):
        """Asserts that if two visits created in sequence, 1000 and 2000,
        an error is not raised when requires_previous_visit is False."""
        TestVisitModel.requires_previous_visit = False
        visit_definition = VisitDefinition.objects.get(code='1000')
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        test_visit = TestVisitModel.objects.create(
            appointment=appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        next_test_visit = TestVisitModel.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(next_test_visit.previous_visit(), test_visit)

    def test_previous_visit(self):
        """Asserts that if two visits created in sequence, 1000 and 2000,
        an error is not raised when requires_previous_visit is True."""
        TestVisitModel.requires_previous_visit = True
        visit_definition = VisitDefinition.objects.get(code='1000')
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        test_visit = TestVisitModel.objects.create(
            appointment=appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        next_test_visit = TestVisitModel.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(next_test_visit.previous_visit(), test_visit)

    def test_visit_raises_if_no_previous(self):
        """Asserts that the second of two visits is created first,
        an error is raised."""
        TestVisitModel.requires_previous_visit = True
        visit_definition = VisitDefinition.objects.get(code='2000')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        self.assertRaises(
            PreviousVisitError,
            TestVisitModel.objects.create,
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)

    def test_visit_not_raised_for_first_visit(self):
        """Asserts that if the first of two visits is created first,
        an error is not raised (this a repeat of a previous test)."""
        TestVisitModel.requires_previous_visit = True
        visit_definition = VisitDefinition.objects.get(code='1000')
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        with self.assertRaises(PreviousVisitError):
            try:
                TestVisitModel.objects.create(
                    appointment=appointment,
                    report_datetime=timezone.now(),
                    reason=SCHEDULED)
            except:
                pass
            else:
                raise PreviousVisitError

    def test_visit_not_raised_for_first_visit2(self):
        TestVisitModel2.requires_previous_visit = True
        visit_definition = VisitDefinition.objects.get(code='2000A')
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        with self.assertRaises(PreviousVisitError):
            try:
                TestVisitModel2.objects.create(
                    appointment=appointment,
                    report_datetime=timezone.now(),
                    reason=SCHEDULED)
            except Exception as e:
                raise Exception(e)
                pass
            else:
                raise PreviousVisitError

    def test_visit_raises_if_no_previous2(self):
        TestVisitModel2.requires_previous_visit = True
        visit_definition = VisitDefinition.objects.get(code='2010A')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        self.assertRaises(
            PreviousVisitError,
            TestVisitModel2.objects.create,
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)

    def test_previous_visit_definition2(self):
        TestVisitModel2.requires_previous_visit = False
        visit_definition = VisitDefinition.objects.get(code='2010A')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        TestVisitModel2.requires_previous_visit = False
        test_visit = TestVisitModel2.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(test_visit.previous_visit_definition(visit_definition).code, '2000A')

    def test_previous_visit_definition2A(self):
        TestVisitModel2.requires_previous_visit = False
        visit_definition = VisitDefinition.objects.get(code='2020A')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        TestVisitModel2.requires_previous_visit = False
        test_visit = TestVisitModel2.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(test_visit.previous_visit_definition(visit_definition).code, '2010A')

    def test_previous_visit_definition2B(self):
        TestVisitModel.requires_previous_visit = False
        visit_definition = VisitDefinition.objects.get(code='2030A')
        next_appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition=visit_definition)
        TestVisitModel2.requires_previous_visit = False
        test_visit = TestVisitModel2.objects.create(
            appointment=next_appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(test_visit.previous_visit_definition(visit_definition).code, '2020A')