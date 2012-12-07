from django.contrib import admin
from models import *

class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
                'pid',
            )

class LimeTokenAdmin(admin.ModelAdmin):
    list_display = (
                'survey_id',
                'token',
                'participant',
                'date_imported',
            )

class AppSettingsAdmin(admin.ModelAdmin):
    list_display = (
                'setting_key',
                'setting',
            )

class ParticipantFilterOptionsAdmin(admin.ModelAdmin):
    list_display = (
                'filter_field',
                'option_dict',
            )

class ParticipantFilterAdmin(admin.ModelAdmin):
    list_display = (
                'id',
                'name',
                'description',
                #'groups',
                'admin_groups',
                'hidden',
                'filter_field',
                'action',
                'argument',
            )

class ParticipantMetaFilterAdmin(admin.ModelAdmin):
    list_display = (
                'id',
                'name',
                'description',
                #'groups',
                'admin_groups',
                'hidden',
                #'filters',
                'admin_filters',
                #'metafilters',
                'admin_metafilters',
                'action',
            )

class ParticipantContactInstanceAdmin(admin.ModelAdmin):
    list_display = (
                'participant',
                'date_of_test',
            )

class ParticipantInductionStaticAdmin(admin.ModelAdmin):
    list_display = (
                'participant',
                'us_citizen',
                'hisp_latino',
                #'racial_origin',
                'admin_racial_origin',
                'racial_origin_comments',
                'retirement_year',
                'gender',
            )
    filter_vertical = (
                
            )

class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = (
                'option',
                'is_default',
                'table',
                'field',
                'order',
                'unique_name',
            )
    
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = (
                'option',
                'is_default',
                'table',
                'field',
                'order',
                'unique_name',
                'short_name',
            )
    

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(LimeToken, LimeTokenAdmin)
admin.site.register(AppSettings, AppSettingsAdmin)
admin.site.register(ParticipantFilterOptions, ParticipantFilterOptionsAdmin)
admin.site.register(ParticipantFilter, ParticipantFilterAdmin)
admin.site.register(ParticipantMetaFilter, ParticipantMetaFilterAdmin)
admin.site.register(ParticipantContactInstance, ParticipantContactInstanceAdmin)
admin.site.register(ParticipantInductionStatic, ParticipantInductionStaticAdmin)
admin.site.register(AnswerOption, AnswerOptionAdmin)
admin.site.register(QuestionOption, QuestionOptionAdmin)


