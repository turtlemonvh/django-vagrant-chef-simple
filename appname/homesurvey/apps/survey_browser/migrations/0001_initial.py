# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AppSettings'
        db.create_table('survey_browser_appsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('setting_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('setting', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('survey_browser', ['AppSettings'])

        # Adding model 'Participant'
        db.create_table('survey_browser_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pid', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('survey_browser', ['Participant'])

        # Adding model 'ParticipantFilterGroup'
        db.create_table('survey_browser_participantfiltergroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('survey_browser', ['ParticipantFilterGroup'])

        # Adding model 'ParticipantFilter'
        db.create_table('survey_browser_participantfilter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filter_field', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('argument', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('survey_browser', ['ParticipantFilter'])

        # Adding M2M table for field groups on 'ParticipantFilter'
        db.create_table('survey_browser_participantfilter_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantfilter', models.ForeignKey(orm['survey_browser.participantfilter'], null=False)),
            ('participantfiltergroup', models.ForeignKey(orm['survey_browser.participantfiltergroup'], null=False))
        ))
        db.create_unique('survey_browser_participantfilter_groups', ['participantfilter_id', 'participantfiltergroup_id'])

        # Adding model 'ParticipantMetaFilter'
        db.create_table('survey_browser_participantmetafilter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('survey_browser', ['ParticipantMetaFilter'])

        # Adding M2M table for field groups on 'ParticipantMetaFilter'
        db.create_table('survey_browser_participantmetafilter_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantmetafilter', models.ForeignKey(orm['survey_browser.participantmetafilter'], null=False)),
            ('participantfiltergroup', models.ForeignKey(orm['survey_browser.participantfiltergroup'], null=False))
        ))
        db.create_unique('survey_browser_participantmetafilter_groups', ['participantmetafilter_id', 'participantfiltergroup_id'])

        # Adding M2M table for field filters on 'ParticipantMetaFilter'
        db.create_table('survey_browser_participantmetafilter_filters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantmetafilter', models.ForeignKey(orm['survey_browser.participantmetafilter'], null=False)),
            ('participantfilter', models.ForeignKey(orm['survey_browser.participantfilter'], null=False))
        ))
        db.create_unique('survey_browser_participantmetafilter_filters', ['participantmetafilter_id', 'participantfilter_id'])

        # Adding model 'LimeToken'
        db.create_table('survey_browser_limetoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey_id', self.gf('django.db.models.fields.IntegerField')()),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.Participant'])),
            ('date_imported', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('survey_browser', ['LimeToken'])

        # Adding unique constraint on 'LimeToken', fields ['survey_id', 'token', 'participant']
        db.create_unique('survey_browser_limetoken', ['survey_id', 'token', 'participant_id'])

        # Adding model 'AnswerOption'
        db.create_table('survey_browser_answeroption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('table', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('unique_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('survey_browser', ['AnswerOption'])

        # Adding model 'QuestionOption'
        db.create_table('survey_browser_questionoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.TextField')()),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('table', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('unique_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('short_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('survey_browser', ['QuestionOption'])

        # Adding model 'ParticipantContactInstance'
        db.create_table('survey_browser_participantcontactinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.Participant'])),
            ('date_of_test', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('survey_browser', ['ParticipantContactInstance'])

        # Adding model 'SPMSQ_question'
        db.create_table('survey_browser_spmsq_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.QuestionOption'])),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('survey_browser', ['SPMSQ_question'])

        # Adding model 'SPMSQ'
        db.create_table('survey_browser_spmsq', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.ParticipantContactInstance'])),
            ('nerrors', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('survey_browser', ['SPMSQ'])

        # Adding M2M table for field questions on 'SPMSQ'
        db.create_table('survey_browser_spmsq_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('spmsq', models.ForeignKey(orm['survey_browser.spmsq'], null=False)),
            ('spmsq_question', models.ForeignKey(orm['survey_browser.spmsq_question'], null=False))
        ))
        db.create_unique('survey_browser_spmsq_questions', ['spmsq_id', 'spmsq_question_id'])

        # Adding model 'IADL_option'
        db.create_table('survey_browser_iadl_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.AnswerOption'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.QuestionOption'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('survey_browser', ['IADL_option'])

        # Adding model 'IADL'
        db.create_table('survey_browser_iadl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.ParticipantContactInstance'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['IADL'])

        # Adding M2M table for field questions on 'IADL'
        db.create_table('survey_browser_iadl_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('iadl', models.ForeignKey(orm['survey_browser.iadl'], null=False)),
            ('iadl_option', models.ForeignKey(orm['survey_browser.iadl_option'], null=False))
        ))
        db.create_unique('survey_browser_iadl_questions', ['iadl_id', 'iadl_option_id'])

        # Adding model 'TUGTrail'
        db.create_table('survey_browser_tugtrail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('time', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['TUGTrail'])

        # Adding model 'TUG'
        db.create_table('survey_browser_tug', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.ParticipantContactInstance'])),
            ('average', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('mobility_rating', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mobility_rating', null=True, to=orm['survey_browser.AnswerOption'])),
            ('fall_risk', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fall_risk', null=True, to=orm['survey_browser.AnswerOption'])),
        ))
        db.send_create_signal('survey_browser', ['TUG'])

        # Adding M2M table for field times on 'TUG'
        db.create_table('survey_browser_tug_times', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tug', models.ForeignKey(orm['survey_browser.tug'], null=False)),
            ('tugtrail', models.ForeignKey(orm['survey_browser.tugtrail'], null=False))
        ))
        db.create_unique('survey_browser_tug_times', ['tug_id', 'tugtrail_id'])

        # Adding model 'ParticipantInductionStatic'
        db.create_table('survey_browser_participantinductionstatic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.Participant'])),
            ('us_citizen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hisp_latino', self.gf('django.db.models.fields.related.ForeignKey')(related_name='hisp_latino', to=orm['survey_browser.AnswerOption'])),
            ('racial_origin_comments', self.gf('django.db.models.fields.TextField')()),
            ('retirement_year', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('gender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.AnswerOption'])),
        ))
        db.send_create_signal('survey_browser', ['ParticipantInductionStatic'])

        # Adding M2M table for field racial_origin on 'ParticipantInductionStatic'
        db.create_table('survey_browser_participantinductionstatic_racial_origin', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantinductionstatic', models.ForeignKey(orm['survey_browser.participantinductionstatic'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_participantinductionstatic_racial_origin', ['participantinductionstatic_id', 'answeroption_id'])

        # Adding model 'ParticipantInductionVolatile'
        db.create_table('survey_browser_participantinductionvolatile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.ParticipantContactInstance'])),
            ('education_level', self.gf('django.db.models.fields.related.ForeignKey')(related_name='education_level', to=orm['survey_browser.AnswerOption'])),
            ('marital_status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='marital_status', to=orm['survey_browser.AnswerOption'])),
            ('n_perm_residents', self.gf('django.db.models.fields.IntegerField')()),
            ('housing_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='housing_type', to=orm['survey_browser.AnswerOption'])),
            ('household_income', self.gf('django.db.models.fields.related.ForeignKey')(related_name='household_income', to=orm['survey_browser.AnswerOption'])),
            ('leave_home_freq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='leave_home_freq', to=orm['survey_browser.AnswerOption'])),
            ('limited_tranport', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_home_internet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_wireless_internet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type_of_internet', self.gf('django.db.models.fields.related.ForeignKey')(related_name='type_of_internet', to=orm['survey_browser.AnswerOption'])),
        ))
        db.send_create_signal('survey_browser', ['ParticipantInductionVolatile'])

        # Adding M2M table for field perm_residents on 'ParticipantInductionVolatile'
        db.create_table('survey_browser_participantinductionvolatile_perm_residents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantinductionvolatile', models.ForeignKey(orm['survey_browser.participantinductionvolatile'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_participantinductionvolatile_perm_residents', ['participantinductionvolatile_id', 'answeroption_id'])

        # Adding M2M table for field occupation_status on 'ParticipantInductionVolatile'
        db.create_table('survey_browser_participantinductionvolatile_occupation_status', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantinductionvolatile', models.ForeignKey(orm['survey_browser.participantinductionvolatile'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_participantinductionvolatile_occupation_status', ['participantinductionvolatile_id', 'answeroption_id'])

        # Adding M2M table for field current_occupation on 'ParticipantInductionVolatile'
        db.create_table('survey_browser_participantinductionvolatile_current_occupation', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantinductionvolatile', models.ForeignKey(orm['survey_browser.participantinductionvolatile'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_participantinductionvolatile_current_occupation', ['participantinductionvolatile_id', 'answeroption_id'])

        # Adding M2M table for field leave_home_reasons on 'ParticipantInductionVolatile'
        db.create_table('survey_browser_participantinductionvolatile_leave_home_reasons', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantinductionvolatile', models.ForeignKey(orm['survey_browser.participantinductionvolatile'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_participantinductionvolatile_leave_home_reasons', ['participantinductionvolatile_id', 'answeroption_id'])

        # Adding model 'ParticipantSurgeries'
        db.create_table('survey_browser_participantsurgeries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('t_surgery', self.gf('django.db.models.fields.TextField')()),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('survey_browser', ['ParticipantSurgeries'])

        # Adding model 'ParticipantMedicalCondition'
        db.create_table('survey_browser_participantmedicalcondition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('condition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.QuestionOption'])),
            ('condition_onset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.AnswerOption'])),
            ('year_of_onset', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['ParticipantMedicalCondition'])

        # Adding model 'ParticipantMedication'
        db.create_table('survey_browser_participantmedication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('medication_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dose_amt', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('dose_units', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('dose_frequency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.AnswerOption'], null=True)),
            ('med_reason', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('med_duration', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('side_effects', self.gf('django.db.models.fields.TextField')(null=True)),
            ('is_prescription', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['ParticipantMedication'])

        # Adding model 'ParticipantMobilityHealth'
        db.create_table('survey_browser_participantmobilityhealth', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.ParticipantContactInstance'])),
            ('ht_in', self.gf('django.db.models.fields.FloatField')()),
            ('wt_lbs', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('physical_activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='physical_activity', to=orm['survey_browser.AnswerOption'])),
        ))
        db.send_create_signal('survey_browser', ['ParticipantMobilityHealth'])

        # Adding M2M table for field assistive_devices on 'ParticipantMobilityHealth'
        db.create_table('survey_browser_participantmobilityhealth_assistive_devices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantmobilityhealth', models.ForeignKey(orm['survey_browser.participantmobilityhealth'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_participantmobilityhealth_assistive_devices', ['participantmobilityhealth_id', 'answeroption_id'])

        # Adding M2M table for field mobility_aids on 'ParticipantMobilityHealth'
        db.create_table('survey_browser_participantmobilityhealth_mobility_aids', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantmobilityhealth', models.ForeignKey(orm['survey_browser.participantmobilityhealth'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_participantmobilityhealth_mobility_aids', ['participantmobilityhealth_id', 'answeroption_id'])

        # Adding M2M table for field surgeries on 'ParticipantMobilityHealth'
        db.create_table('survey_browser_participantmobilityhealth_surgeries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantmobilityhealth', models.ForeignKey(orm['survey_browser.participantmobilityhealth'], null=False)),
            ('participantsurgeries', models.ForeignKey(orm['survey_browser.participantsurgeries'], null=False))
        ))
        db.create_unique('survey_browser_participantmobilityhealth_surgeries', ['participantmobilityhealth_id', 'participantsurgeries_id'])

        # Adding M2M table for field medical_conditions on 'ParticipantMobilityHealth'
        db.create_table('survey_browser_participantmobilityhealth_medical_conditions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantmobilityhealth', models.ForeignKey(orm['survey_browser.participantmobilityhealth'], null=False)),
            ('participantmedicalcondition', models.ForeignKey(orm['survey_browser.participantmedicalcondition'], null=False))
        ))
        db.create_unique('survey_browser_participantmobilityhealth_medical_conditions', ['participantmobilityhealth_id', 'participantmedicalcondition_id'])

        # Adding M2M table for field medications on 'ParticipantMobilityHealth'
        db.create_table('survey_browser_participantmobilityhealth_medications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantmobilityhealth', models.ForeignKey(orm['survey_browser.participantmobilityhealth'], null=False)),
            ('participantmedication', models.ForeignKey(orm['survey_browser.participantmedication'], null=False))
        ))
        db.create_unique('survey_browser_participantmobilityhealth_medications', ['participantmobilityhealth_id', 'participantmedication_id'])

        # Adding model 'ScaleQuestionAndOption'
        db.create_table('survey_browser_scalequestionandoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.QuestionOption'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.AnswerOption'], null=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
        ))
        db.send_create_signal('survey_browser', ['ScaleQuestionAndOption'])

        # Adding model 'ParticipantScaleRatingScores'
        db.create_table('survey_browser_participantscaleratingscores', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fma_std_fn_index', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('fma_raw_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('fma_std_daily_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('fma_std_emot_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('fma_std_armh_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('fma_std_mobi_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('fma_std_bother_index', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('fma_bother_raw_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('promis_raw_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('promis_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('whoqol_bref_health', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('whoqol_bref_psych', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('whoqol_bref_social', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('whoqol_bref_envir', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('whoqol_old_sense', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('whoqol_old_aut', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('tech_confidence_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
            ('tech_attitude_score', self.gf('django.db.models.fields.FloatField')(default=None, null=True)),
        ))
        db.send_create_signal('survey_browser', ['ParticipantScaleRatingScores'])

        # Adding model 'ParticipantScaleRatings'
        db.create_table('survey_browser_participantscaleratings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.ParticipantContactInstance'])),
            ('rating_scores', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.ParticipantScaleRatingScores'])),
            ('research_notes', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['ParticipantScaleRatings'])

        # Adding M2M table for field survey_selections on 'ParticipantScaleRatings'
        db.create_table('survey_browser_participantscaleratings_survey_selections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('participantscaleratings', models.ForeignKey(orm['survey_browser.participantscaleratings'], null=False)),
            ('scalequestionandoption', models.ForeignKey(orm['survey_browser.scalequestionandoption'], null=False))
        ))
        db.create_unique('survey_browser_participantscaleratings_survey_selections', ['participantscaleratings_id', 'scalequestionandoption_id'])

        # Adding model 'ResidenceEntrance'
        db.create_table('survey_browser_residenceentrance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter_id', self.gf('django.db.models.fields.CharField')(default='A', max_length=1)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entrance_location', to=orm['survey_browser.AnswerOption'])),
            ('floor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='floor', to=orm['survey_browser.AnswerOption'])),
            ('n_steps', self.gf('django.db.models.fields.IntegerField')()),
            ('t_stairs', self.gf('django.db.models.fields.related.ForeignKey')(related_name='t_stairs', to=orm['survey_browser.AnswerOption'])),
            ('w_door', self.gf('django.db.models.fields.FloatField')()),
            ('h_thresh', self.gf('django.db.models.fields.FloatField')()),
            ('wheelchair_access', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_freq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entrance_use_freq', to=orm['survey_browser.AnswerOption'])),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['ResidenceEntrance'])

        # Adding model 'ResidenceRoom'
        db.create_table('survey_browser_residenceroom', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room_id', self.gf('django.db.models.fields.IntegerField')()),
            ('room_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='room_type', to=orm['survey_browser.AnswerOption'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='room_location', to=orm['survey_browser.AnswerOption'])),
            ('floor_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='floor_type', to=orm['survey_browser.AnswerOption'])),
            ('use_freq', self.gf('django.db.models.fields.related.ForeignKey')(related_name='room_use_freq', to=orm['survey_browser.AnswerOption'])),
            ('w_room', self.gf('django.db.models.fields.FloatField')()),
            ('l_room', self.gf('django.db.models.fields.FloatField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['ResidenceRoom'])

        # Adding M2M table for field entrances on 'ResidenceRoom'
        db.create_table('survey_browser_residenceroom_entrances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('residenceroom', models.ForeignKey(orm['survey_browser.residenceroom'], null=False)),
            ('residenceentrance', models.ForeignKey(orm['survey_browser.residenceentrance'], null=False))
        ))
        db.create_unique('survey_browser_residenceroom_entrances', ['residenceroom_id', 'residenceentrance_id'])

        # Adding M2M table for field connections on 'ResidenceRoom'
        db.create_table('survey_browser_residenceroom_connections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('residenceroom', models.ForeignKey(orm['survey_browser.residenceroom'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_residenceroom_connections', ['residenceroom_id', 'answeroption_id'])

        # Adding model 'ResidenceInteriorDoor'
        db.create_table('survey_browser_residenceinteriordoor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='doorroom1', null=True, to=orm['survey_browser.ResidenceRoom'])),
            ('room2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='doorroom2', null=True, to=orm['survey_browser.ResidenceRoom'])),
            ('w_door', self.gf('django.db.models.fields.FloatField')()),
            ('h_thresh', self.gf('django.db.models.fields.FloatField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['ResidenceInteriorDoor'])

        # Adding model 'ResidenceInteriorStair'
        db.create_table('survey_browser_residenceinteriorstair', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stairroom1', to=orm['survey_browser.ResidenceRoom'])),
            ('room2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stairroom2', to=orm['survey_browser.ResidenceRoom'])),
            ('location_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('n_steps', self.gf('django.db.models.fields.IntegerField')()),
            ('t_stairs', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.AnswerOption'])),
            ('narrowest_width', self.gf('django.db.models.fields.FloatField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['ResidenceInteriorStair'])

        # Adding model 'ResidencePhotograph'
        db.create_table('survey_browser_residencephotograph', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey_browser.ResidenceRoom'])),
            ('photo_path', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['ResidencePhotograph'])

        # Adding model 'HomeInventory'
        db.create_table('survey_browser_homeinventory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nstories', self.gf('django.db.models.fields.IntegerField')()),
            ('bed_ht', self.gf('django.db.models.fields.FloatField')()),
            ('bed_size', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bed_size', to=orm['survey_browser.AnswerOption'])),
            ('bed_adjustable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('home_notes', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('survey_browser', ['HomeInventory'])

        # Adding M2M table for field contact_instance on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_contact_instance', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('participantcontactinstance', models.ForeignKey(orm['survey_browser.participantcontactinstance'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_contact_instance', ['homeinventory_id', 'participantcontactinstance_id'])

        # Adding M2M table for field home_features on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_home_features', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_home_features', ['homeinventory_id', 'answeroption_id'])

        # Adding M2M table for field home_cooling on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_home_cooling', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_home_cooling', ['homeinventory_id', 'answeroption_id'])

        # Adding M2M table for field home_heating on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_home_heating', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('answeroption', models.ForeignKey(orm['survey_browser.answeroption'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_home_heating', ['homeinventory_id', 'answeroption_id'])

        # Adding M2M table for field entrances on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_entrances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('residenceentrance', models.ForeignKey(orm['survey_browser.residenceentrance'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_entrances', ['homeinventory_id', 'residenceentrance_id'])

        # Adding M2M table for field rooms on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_rooms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('residenceroom', models.ForeignKey(orm['survey_browser.residenceroom'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_rooms', ['homeinventory_id', 'residenceroom_id'])

        # Adding M2M table for field interior_doors on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_interior_doors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('residenceinteriordoor', models.ForeignKey(orm['survey_browser.residenceinteriordoor'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_interior_doors', ['homeinventory_id', 'residenceinteriordoor_id'])

        # Adding M2M table for field interior_stairs on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_interior_stairs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('residenceinteriorstair', models.ForeignKey(orm['survey_browser.residenceinteriorstair'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_interior_stairs', ['homeinventory_id', 'residenceinteriorstair_id'])

        # Adding M2M table for field photographs on 'HomeInventory'
        db.create_table('survey_browser_homeinventory_photographs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('homeinventory', models.ForeignKey(orm['survey_browser.homeinventory'], null=False)),
            ('residencephotograph', models.ForeignKey(orm['survey_browser.residencephotograph'], null=False))
        ))
        db.create_unique('survey_browser_homeinventory_photographs', ['homeinventory_id', 'residencephotograph_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'LimeToken', fields ['survey_id', 'token', 'participant']
        db.delete_unique('survey_browser_limetoken', ['survey_id', 'token', 'participant_id'])

        # Deleting model 'AppSettings'
        db.delete_table('survey_browser_appsettings')

        # Deleting model 'Participant'
        db.delete_table('survey_browser_participant')

        # Deleting model 'ParticipantFilterGroup'
        db.delete_table('survey_browser_participantfiltergroup')

        # Deleting model 'ParticipantFilter'
        db.delete_table('survey_browser_participantfilter')

        # Removing M2M table for field groups on 'ParticipantFilter'
        db.delete_table('survey_browser_participantfilter_groups')

        # Deleting model 'ParticipantMetaFilter'
        db.delete_table('survey_browser_participantmetafilter')

        # Removing M2M table for field groups on 'ParticipantMetaFilter'
        db.delete_table('survey_browser_participantmetafilter_groups')

        # Removing M2M table for field filters on 'ParticipantMetaFilter'
        db.delete_table('survey_browser_participantmetafilter_filters')

        # Deleting model 'LimeToken'
        db.delete_table('survey_browser_limetoken')

        # Deleting model 'AnswerOption'
        db.delete_table('survey_browser_answeroption')

        # Deleting model 'QuestionOption'
        db.delete_table('survey_browser_questionoption')

        # Deleting model 'ParticipantContactInstance'
        db.delete_table('survey_browser_participantcontactinstance')

        # Deleting model 'SPMSQ_question'
        db.delete_table('survey_browser_spmsq_question')

        # Deleting model 'SPMSQ'
        db.delete_table('survey_browser_spmsq')

        # Removing M2M table for field questions on 'SPMSQ'
        db.delete_table('survey_browser_spmsq_questions')

        # Deleting model 'IADL_option'
        db.delete_table('survey_browser_iadl_option')

        # Deleting model 'IADL'
        db.delete_table('survey_browser_iadl')

        # Removing M2M table for field questions on 'IADL'
        db.delete_table('survey_browser_iadl_questions')

        # Deleting model 'TUGTrail'
        db.delete_table('survey_browser_tugtrail')

        # Deleting model 'TUG'
        db.delete_table('survey_browser_tug')

        # Removing M2M table for field times on 'TUG'
        db.delete_table('survey_browser_tug_times')

        # Deleting model 'ParticipantInductionStatic'
        db.delete_table('survey_browser_participantinductionstatic')

        # Removing M2M table for field racial_origin on 'ParticipantInductionStatic'
        db.delete_table('survey_browser_participantinductionstatic_racial_origin')

        # Deleting model 'ParticipantInductionVolatile'
        db.delete_table('survey_browser_participantinductionvolatile')

        # Removing M2M table for field perm_residents on 'ParticipantInductionVolatile'
        db.delete_table('survey_browser_participantinductionvolatile_perm_residents')

        # Removing M2M table for field occupation_status on 'ParticipantInductionVolatile'
        db.delete_table('survey_browser_participantinductionvolatile_occupation_status')

        # Removing M2M table for field current_occupation on 'ParticipantInductionVolatile'
        db.delete_table('survey_browser_participantinductionvolatile_current_occupation')

        # Removing M2M table for field leave_home_reasons on 'ParticipantInductionVolatile'
        db.delete_table('survey_browser_participantinductionvolatile_leave_home_reasons')

        # Deleting model 'ParticipantSurgeries'
        db.delete_table('survey_browser_participantsurgeries')

        # Deleting model 'ParticipantMedicalCondition'
        db.delete_table('survey_browser_participantmedicalcondition')

        # Deleting model 'ParticipantMedication'
        db.delete_table('survey_browser_participantmedication')

        # Deleting model 'ParticipantMobilityHealth'
        db.delete_table('survey_browser_participantmobilityhealth')

        # Removing M2M table for field assistive_devices on 'ParticipantMobilityHealth'
        db.delete_table('survey_browser_participantmobilityhealth_assistive_devices')

        # Removing M2M table for field mobility_aids on 'ParticipantMobilityHealth'
        db.delete_table('survey_browser_participantmobilityhealth_mobility_aids')

        # Removing M2M table for field surgeries on 'ParticipantMobilityHealth'
        db.delete_table('survey_browser_participantmobilityhealth_surgeries')

        # Removing M2M table for field medical_conditions on 'ParticipantMobilityHealth'
        db.delete_table('survey_browser_participantmobilityhealth_medical_conditions')

        # Removing M2M table for field medications on 'ParticipantMobilityHealth'
        db.delete_table('survey_browser_participantmobilityhealth_medications')

        # Deleting model 'ScaleQuestionAndOption'
        db.delete_table('survey_browser_scalequestionandoption')

        # Deleting model 'ParticipantScaleRatingScores'
        db.delete_table('survey_browser_participantscaleratingscores')

        # Deleting model 'ParticipantScaleRatings'
        db.delete_table('survey_browser_participantscaleratings')

        # Removing M2M table for field survey_selections on 'ParticipantScaleRatings'
        db.delete_table('survey_browser_participantscaleratings_survey_selections')

        # Deleting model 'ResidenceEntrance'
        db.delete_table('survey_browser_residenceentrance')

        # Deleting model 'ResidenceRoom'
        db.delete_table('survey_browser_residenceroom')

        # Removing M2M table for field entrances on 'ResidenceRoom'
        db.delete_table('survey_browser_residenceroom_entrances')

        # Removing M2M table for field connections on 'ResidenceRoom'
        db.delete_table('survey_browser_residenceroom_connections')

        # Deleting model 'ResidenceInteriorDoor'
        db.delete_table('survey_browser_residenceinteriordoor')

        # Deleting model 'ResidenceInteriorStair'
        db.delete_table('survey_browser_residenceinteriorstair')

        # Deleting model 'ResidencePhotograph'
        db.delete_table('survey_browser_residencephotograph')

        # Deleting model 'HomeInventory'
        db.delete_table('survey_browser_homeinventory')

        # Removing M2M table for field contact_instance on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_contact_instance')

        # Removing M2M table for field home_features on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_home_features')

        # Removing M2M table for field home_cooling on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_home_cooling')

        # Removing M2M table for field home_heating on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_home_heating')

        # Removing M2M table for field entrances on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_entrances')

        # Removing M2M table for field rooms on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_rooms')

        # Removing M2M table for field interior_doors on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_interior_doors')

        # Removing M2M table for field interior_stairs on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_interior_stairs')

        # Removing M2M table for field photographs on 'HomeInventory'
        db.delete_table('survey_browser_homeinventory_photographs')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'survey_browser.answeroption': {
            'Meta': {'object_name': 'AnswerOption'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'option': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'table': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unique_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'survey_browser.appsettings': {
            'Meta': {'object_name': 'AppSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'setting': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'setting_key': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'survey_browser.homeinventory': {
            'Meta': {'object_name': 'HomeInventory'},
            'bed_adjustable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bed_ht': ('django.db.models.fields.FloatField', [], {}),
            'bed_size': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bed_size'", 'to': "orm['survey_browser.AnswerOption']"}),
            'contact_instance': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ParticipantContactInstance']", 'symmetrical': 'False'}),
            'entrances': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ResidenceEntrance']", 'symmetrical': 'False'}),
            'home_cooling': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'home_cooling'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'home_features': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'home_features'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'home_heating': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'home_heating'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'home_notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interior_doors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ResidenceInteriorDoor']", 'symmetrical': 'False'}),
            'interior_stairs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ResidenceInteriorStair']", 'symmetrical': 'False'}),
            'nstories': ('django.db.models.fields.IntegerField', [], {}),
            'photographs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ResidencePhotograph']", 'symmetrical': 'False'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ResidenceRoom']", 'symmetrical': 'False'})
        },
        'survey_browser.iadl': {
            'Meta': {'object_name': 'IADL'},
            'contact_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.ParticipantContactInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.IADL_option']", 'symmetrical': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'survey_browser.iadl_option': {
            'Meta': {'object_name': 'IADL_option'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.AnswerOption']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.QuestionOption']"}),
            'score': ('django.db.models.fields.IntegerField', [], {})
        },
        'survey_browser.limetoken': {
            'Meta': {'unique_together': "(('survey_id', 'token', 'participant'),)", 'object_name': 'LimeToken'},
            'date_imported': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.Participant']"}),
            'survey_id': ('django.db.models.fields.IntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'survey_browser.participant': {
            'Meta': {'ordering': "['pid']", 'object_name': 'Participant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {})
        },
        'survey_browser.participantcontactinstance': {
            'Meta': {'object_name': 'ParticipantContactInstance'},
            'date_of_test': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.Participant']"})
        },
        'survey_browser.participantfilter': {
            'Meta': {'object_name': 'ParticipantFilter'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'argument': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'filter_field': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ParticipantFilterGroup']", 'symmetrical': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'survey_browser.participantfiltergroup': {
            'Meta': {'object_name': 'ParticipantFilterGroup'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'survey_browser.participantinductionstatic': {
            'Meta': {'object_name': 'ParticipantInductionStatic'},
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.AnswerOption']"}),
            'hisp_latino': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hisp_latino'", 'to': "orm['survey_browser.AnswerOption']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.Participant']"}),
            'racial_origin': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'racial_origin'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'racial_origin_comments': ('django.db.models.fields.TextField', [], {}),
            'retirement_year': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'us_citizen': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'survey_browser.participantinductionvolatile': {
            'Meta': {'object_name': 'ParticipantInductionVolatile'},
            'contact_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.ParticipantContactInstance']"}),
            'current_occupation': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'current_occupation'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'education_level': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'education_level'", 'to': "orm['survey_browser.AnswerOption']"}),
            'has_home_internet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_wireless_internet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'household_income': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'household_income'", 'to': "orm['survey_browser.AnswerOption']"}),
            'housing_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'housing_type'", 'to': "orm['survey_browser.AnswerOption']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leave_home_freq': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'leave_home_freq'", 'to': "orm['survey_browser.AnswerOption']"}),
            'leave_home_reasons': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'leave_home_reasons'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'limited_tranport': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marital_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'marital_status'", 'to': "orm['survey_browser.AnswerOption']"}),
            'n_perm_residents': ('django.db.models.fields.IntegerField', [], {}),
            'occupation_status': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'occupation_status'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'perm_residents': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'perm_residents'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'type_of_internet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'type_of_internet'", 'to': "orm['survey_browser.AnswerOption']"})
        },
        'survey_browser.participantmedicalcondition': {
            'Meta': {'object_name': 'ParticipantMedicalCondition'},
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.QuestionOption']"}),
            'condition_onset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.AnswerOption']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year_of_onset': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'survey_browser.participantmedication': {
            'Meta': {'object_name': 'ParticipantMedication'},
            'dose_amt': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'dose_frequency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.AnswerOption']", 'null': 'True'}),
            'dose_units': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_prescription': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'med_duration': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'med_reason': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'medication_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'side_effects': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        'survey_browser.participantmetafilter': {
            'Meta': {'object_name': 'ParticipantMetaFilter'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ParticipantFilter']", 'symmetrical': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ParticipantFilterGroup']", 'symmetrical': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'survey_browser.participantmobilityhealth': {
            'Meta': {'object_name': 'ParticipantMobilityHealth'},
            'assistive_devices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'assistive_devices'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'contact_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.ParticipantContactInstance']"}),
            'ht_in': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medical_conditions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ParticipantMedicalCondition']", 'symmetrical': 'False'}),
            'medications': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ParticipantMedication']", 'symmetrical': 'False'}),
            'mobility_aids': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mobility_aids'", 'symmetrical': 'False', 'to': "orm['survey_browser.AnswerOption']"}),
            'physical_activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'physical_activity'", 'to': "orm['survey_browser.AnswerOption']"}),
            'surgeries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ParticipantSurgeries']", 'symmetrical': 'False'}),
            'wt_lbs': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'survey_browser.participantscaleratings': {
            'Meta': {'object_name': 'ParticipantScaleRatings'},
            'contact_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.ParticipantContactInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating_scores': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.ParticipantScaleRatingScores']"}),
            'research_notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'survey_selections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ScaleQuestionAndOption']", 'symmetrical': 'False'})
        },
        'survey_browser.participantscaleratingscores': {
            'Meta': {'object_name': 'ParticipantScaleRatingScores'},
            'fma_bother_raw_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'fma_raw_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'fma_std_armh_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'fma_std_bother_index': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'fma_std_daily_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'fma_std_emot_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'fma_std_fn_index': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'fma_std_mobi_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'promis_raw_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'promis_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'tech_attitude_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'tech_confidence_score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'whoqol_bref_envir': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'whoqol_bref_health': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'whoqol_bref_psych': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'whoqol_bref_social': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'whoqol_old_aut': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'whoqol_old_sense': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'})
        },
        'survey_browser.participantsurgeries': {
            'Meta': {'object_name': 'ParticipantSurgeries'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            't_surgery': ('django.db.models.fields.TextField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'survey_browser.questionoption': {
            'Meta': {'object_name': 'QuestionOption'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'option': ('django.db.models.fields.TextField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'table': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unique_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'survey_browser.residenceentrance': {
            'Meta': {'object_name': 'ResidenceEntrance'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'floor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'floor'", 'to': "orm['survey_browser.AnswerOption']"}),
            'h_thresh': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter_id': ('django.db.models.fields.CharField', [], {'default': "'A'", 'max_length': '1'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entrance_location'", 'to': "orm['survey_browser.AnswerOption']"}),
            'n_steps': ('django.db.models.fields.IntegerField', [], {}),
            't_stairs': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t_stairs'", 'to': "orm['survey_browser.AnswerOption']"}),
            'use_freq': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entrance_use_freq'", 'to': "orm['survey_browser.AnswerOption']"}),
            'w_door': ('django.db.models.fields.FloatField', [], {}),
            'wheelchair_access': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'survey_browser.residenceinteriordoor': {
            'Meta': {'object_name': 'ResidenceInteriorDoor'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'h_thresh': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'doorroom1'", 'null': 'True', 'to': "orm['survey_browser.ResidenceRoom']"}),
            'room2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'doorroom2'", 'null': 'True', 'to': "orm['survey_browser.ResidenceRoom']"}),
            'w_door': ('django.db.models.fields.FloatField', [], {})
        },
        'survey_browser.residenceinteriorstair': {
            'Meta': {'object_name': 'ResidenceInteriorStair'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'n_steps': ('django.db.models.fields.IntegerField', [], {}),
            'narrowest_width': ('django.db.models.fields.FloatField', [], {}),
            'room1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stairroom1'", 'to': "orm['survey_browser.ResidenceRoom']"}),
            'room2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stairroom2'", 'to': "orm['survey_browser.ResidenceRoom']"}),
            't_stairs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.AnswerOption']"})
        },
        'survey_browser.residencephotograph': {
            'Meta': {'object_name': 'ResidencePhotograph'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo_path': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.ResidenceRoom']"})
        },
        'survey_browser.residenceroom': {
            'Meta': {'object_name': 'ResidenceRoom'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'connections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.AnswerOption']", 'symmetrical': 'False'}),
            'entrances': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ResidenceEntrance']", 'symmetrical': 'False'}),
            'floor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'floor_type'", 'to': "orm['survey_browser.AnswerOption']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_room': ('django.db.models.fields.FloatField', [], {}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room_location'", 'to': "orm['survey_browser.AnswerOption']"}),
            'room_id': ('django.db.models.fields.IntegerField', [], {}),
            'room_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room_type'", 'to': "orm['survey_browser.AnswerOption']"}),
            'use_freq': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'room_use_freq'", 'to': "orm['survey_browser.AnswerOption']"}),
            'w_room': ('django.db.models.fields.FloatField', [], {})
        },
        'survey_browser.scalequestionandoption': {
            'Meta': {'object_name': 'ScaleQuestionAndOption'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.AnswerOption']", 'null': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.QuestionOption']"})
        },
        'survey_browser.spmsq': {
            'Meta': {'object_name': 'SPMSQ'},
            'contact_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.ParticipantContactInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nerrors': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.SPMSQ_question']", 'symmetrical': 'False'})
        },
        'survey_browser.spmsq_question': {
            'Meta': {'object_name': 'SPMSQ_question'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.QuestionOption']"})
        },
        'survey_browser.tug': {
            'Meta': {'object_name': 'TUG'},
            'average': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'contact_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey_browser.ParticipantContactInstance']"}),
            'fall_risk': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fall_risk'", 'null': 'True', 'to': "orm['survey_browser.AnswerOption']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobility_rating': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mobility_rating'", 'null': 'True', 'to': "orm['survey_browser.AnswerOption']"}),
            'times': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.TUGTrail']", 'symmetrical': 'False'})
        },
        'survey_browser.tugtrail': {
            'Meta': {'object_name': 'TUGTrail'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        }
    }

    complete_apps = ['survey_browser']