from django.db import models

from edc_meta_data.models import CrfMetaDataMixin
from edc_visit_tracking.models import PreviousVisitMixin, VisitModelMixin
from edc_offstudy.models import OffStudyMixin
from edc_testing.models.test_consent import TestConsentWithMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_visit_tracking.models.crf_model_mixin import CrfModelMixin
from edc_visit_tracking.models.crf_inline_model_mixin import CrfInlineModelMixin


class TestVisitModel(CrfMetaDataMixin, OffStudyMixin, PreviousVisitMixin, VisitModelMixin, BaseUuidModel):

    REQUIRES_PREVIOUS_VISIT = True

    consent_model = TestConsentWithMixin

    off_study_model = ('edc_testing', 'TestOffStudy')

    death_report_model = ('edc_testing', 'TestDeathReport')

    def get_subject_identifier(self):
        return self.appointment.registered_subject.subject_identifier

    class Meta:
        app_label = 'edc_visit_tracking'


class TestVisitModel2(CrfMetaDataMixin, OffStudyMixin, PreviousVisitMixin, VisitModelMixin, BaseUuidModel):

    REQUIRES_PREVIOUS_VISIT = True

    off_study_model = ('edc_testing', 'TestOffStudy')

    death_report_model = ('edc_testing', 'TestDeathReport')

    class Meta:
        app_label = 'edc_visit_tracking'


class TestCrfModel(CrfModelMixin, BaseUuidModel):

    test_visit = models.OneToOneField(TestVisitModel)

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10)

    class Meta:
        app_label = 'edc_visit_tracking'


class TestCrfInlineModel(CrfInlineModelMixin, BaseUuidModel):

    fk_model_attr = 'test_crf_model'

    test_crf_model = models.OneToOneField(TestCrfModel)

    f1 = models.CharField(max_length=10)

    f2 = models.CharField(max_length=10)

    class Meta:
        app_label = 'edc_visit_tracking'
