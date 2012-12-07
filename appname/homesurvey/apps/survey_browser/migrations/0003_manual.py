# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Delete old M2M table
        try:
            db.delete_table('survey_browser_participantmetafilter_metafilters')
        except:
            pass
        
        # Adding M2M table for field metafilters on 'ParticipantMetaFilter'
        db.create_table('survey_browser_participantmetafilter_metafilters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_participantmetafilter', models.ForeignKey(orm['survey_browser.participantmetafilter'], null=False)),
            ('to_participantmetafilter', models.ForeignKey(orm['survey_browser.participantmetafilter'], null=False))
        ))
        db.create_unique('survey_browser_participantmetafilter_metafilters', ['from_participantmetafilter_id', 'to_participantmetafilter_id'])


    def backwards(self, orm):
        # Removing M2M table for field metafilters on 'ParticipantMetaFilter'
        db.delete_table('survey_browser_participantmetafilter_metafilters')


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
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'filters'", 'symmetrical': 'False', 'to': "orm['survey_browser.ParticipantFilter']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['survey_browser.ParticipantFilterGroup']", 'symmetrical': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metafilters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'metafilters'", 'symmetrical': 'False', 'to': "orm['survey_browser.ParticipantMetaFilter']"}),
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