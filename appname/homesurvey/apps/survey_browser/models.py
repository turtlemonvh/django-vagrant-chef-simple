import datetime
import copy
import re
from types import *

from django.db import models
from django.db.models import Sum, Avg, Max, Min, Count, ManyToManyField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.forms.models import model_to_dict


from utility.utility_functions import get_filter_option_dict

"""
PLAYING WITH THE COMMAND LINE

Destroy all schema data for nodes and start over
- First, delete all migration files, then execute the following from the command line.
** Note that it usually still works without deleting migration files
>> python manage.py reset survey_browser
>> python manage.py reset south
>> python manage.py syncdb # recreate all app databases
>> python manage.py schemamigration survey_browser --init
>> python manage.py migrate survey_browser --fake
>> python manage.py migrate survey_browser --delete-ghost-migrations

Quick clear and re-initialize:
>> python manage.py reset survey_browser
>> python manage.py loaddata loaded_options_plus_limesurvey_data.json # load the fixture with the LimeSurvey data [may not work if models in the fixture have been changed or deleted]

Individual migrations
>> python manage.py schemamigration survey_browser --auto
>> python manage.py migrate survey_browser


Create Fixtures:
>> python manage.py dumpdata survey_browser > loaded_options.json

To visualize:
$ python manage.py graph_models survey_browser -a > homelab_surveybrowser.dot
$ dot -Tpng homelab_surveybrowser.dot -o surveybrowser.png


THIS DOESN'T HAVE TO BE SUPER FLEXIBLE
- we want fast and easy to use
- this is a research database, not a data repository
- only recent data is useful
- queries should be fast and intuitive
- DON'T OVER ENGINEER IT!

- need to be able to pull all answer options currently used for a given field
- for all dated data, all fields should be optional to allow updating of just a field at a time for a visit
- allow users to create filters
    - inclusive
    - exclusive
    - use set notation to combine results easily as a set of user ids
    - this will also show them the # users excluded by each filter
    - make sure to include warnings if some fields were not answered by data or if fields look corrupted

Make sure home inventory data is associated with a location, and not with a participant

"""

# Variables
DATETIME_FORMAT = "%A %B %d, %Y %I:%M:%S %p"
JSON_DTHANDLER = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

# For display; maybe store per user?
class AppSettings(models.Model):
    setting_key = models.CharField(max_length = 100)
    setting = models.CharField(max_length = 100)
    
    @classmethod
    def _get_filter_fields(cls):
        return {}

class Participant(models.Model):
    pid = models.IntegerField()

    class Meta:
        ordering = ['pid']

    def __unicode__(self):
        return u'%s' % (self.pid)

    @classmethod
    def _get_filter_fields(cls):
        filter_fields = {}
        filter_fields["pids"] = {}
        filter_fields["pids"]["field_name"] = "pid"
        filter_fields["pids"]["short_name"] = "Participant ID"
        filter_fields["pids"]["type"] = "single_select"
        filter_fields["pids"]["model"] = "Participant"
        filter_fields["pids"]["heirarchy"] = ("Participants",)
        filter_fields["pids"]["function_handle"] = "Participant.objects.values_list('pid', flat = True)"
        filter_fields["pids"]["default_representation_type"] = "textbox"
        options = {}
        for pid in Participant.objects.order_by('pid').distinct('pid').values_list('pid',flat=True):
            options[pid] = {}
            options[pid]["id"] = pid
            options[pid]["name"] = pid
            options[pid]["is_default"] = False
            options[pid]["order"] = pid
        filter_fields["pids"]["options"] = options

        return filter_fields

class ParticipantFilterOptions(models.Model):
    filter_field = models.CharField(max_length = 100)
    option_dict = models.TextField(default = "") # stored in json
    
    def getOptionDict(self):
        return simplejson.loads(self.option_dict)

    @classmethod
    def updateFilterOptions(cls):
        option_sub_dict = get_filter_option_dict()
        for k,v in option_sub_dict.iteritems():
            c_opt = ParticipantFilterOptions.objects.get_or_create(filter_field = k)[0]
            c_opt.option_dict = simplejson.dumps(v)
            c_opt.save()

    @classmethod
    def getAllOptions(cls):
        option_sub_dict = {}
        for opt in ParticipantFilterOptions.objects.all():
            option_sub_dict[opt.filter_field] = opt.getOptionDict()
        return option_sub_dict

    @classmethod
    # Nested structure for easy presentation
    def getAllOptionsStructured(cls):
        odict = cls.getAllOptions()
        
        def get_or_create_dict_key(d,keys):
            if keys:
                # if we are not yet at the bottom of the heirarchy
                if keys[0] not in d:
                    d[keys[0]] = {}
                return get_or_create_dict_key(d[keys[0]],keys[1:])
            else:
                return d
        
        ndict = {}
        for k,v in odict.items():
            v["id"] = k
            
            if "short_name" not in v:
                v["short_name"] = v["field_name"]
    
            if "full_name" not in v:
                v["full_name"] = v["short_name"]
                    
            tmp_key = get_or_create_dict_key(ndict,v["heirarchy"])
            tmp_key[v["id"]] = {}
            tmp_key[v["id"]]["id"] = v["id"]
            tmp_key[v["id"]]["short_name"] = v["short_name"]
            tmp_key[v["id"]]["full_name"] = v["full_name"]
                    
        return ndict

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ParticipantFilterGroup(models.Model):
    user = models.ForeignKey(User, null = False)
    name = models.CharField(max_length = 100, null = False)
    description = models.CharField(max_length = 100, default = "")

    def save(self, *args, **kwargs):
        if self.user is None:
            self.user = User.objects.get(username = "guest")
        super(ParticipantFilterGroup, self).save(*args, **kwargs)

    @classmethod
    def _get_filter_fields(cls):
        return {}

# Filters that, when executes, return a list of matching participants in the form of a queryset
class ParticipantFilter(models.Model):
    """
    Types:
    ~~~~~~~~
    ratio: gt, lt, gte, lte, eq, neq 
    ordinal: gt, lt, gte, lte, eq, neq 
    boolean: eq, neq
    multi_select: any in, any not in, all in, all not in
    single_select: any in, any not in
    text: contains, not contains, is empty, is not empty
    
    NOTE: All filters by default belong to the "imaginary" DEFAULT group (this allows us to treat everything like it has a group)
    
    Filtered value will be:
    - real number [0,1 for boolean]
    - array of ids
    - string
    
    
    Need to write tests of this functionality    
    """
    name = models.CharField(max_length = 100, null = False)
    description = models.CharField(max_length = 100, default = "")
    groups = models.ManyToManyField(ParticipantFilterGroup)
    hidden = models.BooleanField(default = False)
    filter_field = models.CharField(max_length = 100) # the unique id in the dict from the _get_filter_fields function
    action = models.CharField(max_length = 100) # eq, lte, not in, etc
    argument = models.CharField(max_length = 100, null = True) # real number, comma separated list of ids, string, etc

    def admin_groups(self):
        return ', '.join(["%s | %s" %(g.name, g.user) for g in self.groups.all()])
    admin_groups.short_description = "Admin Groups"
    
    def __unicode__(self):
        return u'%s' % (self.filter_field)

    def assign_to_group(self, user, group = None):
        if not self.groups.filter(name = "DEFAULT").exists():
            # add default group
            def_group = ParticipantFilterGroup.objects.get_or_create(user = user, name = "DEFAULT")[0]
            self.groups.add( def_group)
        if group is not None:
            self.groups.add( group)

    # Return matching pids as a list
    """
    Return function handle / query set so functions can be applied to the back
    """
    def execute(self):
        option_sub_dict = ParticipantFilterOptions.objects.get(filter_field = self.filter_field).getOptionDict()
        field_name = option_sub_dict["field_name"]
        filter_field_type = option_sub_dict["type"]
        function_handle = option_sub_dict["function_handle"] # used in eval statement
        
        if self.action == "lt":
            filter_function = function_handle + ".filter(%s__lt = %s)" % (field_name, self.argument)
        elif self.action == "gt":
            filter_function = function_handle + ".filter(%s__gt = %s)" % (field_name, self.argument)
        elif self.action == "lte":
            filter_function = function_handle + ".filter(%s__lte = %s)" % (field_name, self.argument)
        elif self.action == "gte":
            filter_function = function_handle + ".filter(%s__gte = %s)" % (field_name, self.argument)
        elif self.action == "eq":
            if self.argument is None:
                filter_function = function_handle + ".filter(%s = %s)" % (field_name, self.argument)
            elif filter_field_type == "boolean":
                filter_function = function_handle + ".filter(%s = %s)" % (field_name, bool(self.argument))
            elif filter_field_type == "text":
                filter_function = function_handle + ".filter(%s = '%s')" % (field_name, self.argument)
            else:
                filter_function = function_handle + ".filter(%s = %s)" % (field_name, self.argument)
        elif self.action == "neq":
            if self.argument is None:
                filter_function = function_handle + ".exclude(%s = %s)" % (field_name, self.argument)
            elif filter_field_type == "boolean":
                filter_function = function_handle + ".exclude(%s = %s)" % (field_name, bool(self.argument))
            elif filter_field_type == "text":
                filter_function = function_handle + ".exclude(%s = '%s')" % (field_name, self.argument)
            else:
                filter_function = function_handle + ".exclude(%s = %s)" % (field_name, self.argument)
        elif self.action == "any in":
            if self.filter_field == "pids":
                filter_function = function_handle + ".filter(%s__in = [%s])" % (field_name, self.argument)
            else:
                filter_function = function_handle + ".filter(%s__id__in = [%s])" % (field_name, self.argument)
        elif self.action == "any not in":
            if self.filter_field == "pids":
                filter_function = function_handle + ".exclude(%s__in = [%s])" % (field_name, self.argument)
            else:
                filter_function = function_handle + ".exclude(%s__id__in = [%s])" % (field_name, self.argument)
        elif self.action == "all in":
            # via: http://stackoverflow.com/questions/5301996/django-many-to-many-query
            filter_argument = ""
            for ref_id in self.argument.split(","):
                filter_argument += ".filter(%s__id = %s)" %(field_name, ref_id)
            filter_function = function_handle + filter_argument
        elif self.action == "all not in":
            filter_argument = ""
            for ref_id in self.argument.split(","):
                filter_argument += ".exclude(%s__id = %s)" %(field_name, ref_id)
            filter_function = function_handle + filter_argument
        elif self.action == "contains":
            filter_function = function_handle + ".filter(%s__icontains = '%s')" % (field_name, self.argument)
        elif self.action == "ncontains":
            filter_function = function_handle + ".exclude(%s__icontains = '%s')" % (field_name, self.argument)
        else:
            raise("ERROR: Action type not found.")
        
        print filter_function
        pids = eval(filter_function)
        
        # Analysis of repeats
        tmp_len = len(pids)
        if tmp_len > len(list(set(pids))):
            print "REPEATS IN FILTER: " + filter_function + " ; type = " + filter_field_type
        
        return list(set(pids)) # may be repeats for __in filters on multi-select fields

    def getAction(self):
        return ""

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ParticipantMetaFilter(models.Model):
    name = models.CharField(max_length = 100, null = False)
    description = models.CharField(max_length = 100, default = "")
    groups = models.ManyToManyField(ParticipantFilterGroup)
    hidden = models.BooleanField(default = False)
    filters = models.ManyToManyField(ParticipantFilter, related_name = 'filters')
    metafilters = models.ManyToManyField('self', symmetrical = False, related_name = 'associated_metafilters')
    action = models.CharField(max_length = 10) # and, or, xor

    def admin_groups(self):
        return ', '.join(["%s | %s" %(g.name, g.user) for g in self.groups.all()])
    admin_groups.short_description = "Admin Groups"

    def admin_metafilters(self):
        return ', '.join([f.name for f in self.metafilters.all()])
    admin_metafilters.short_description = "Admin Metafilters"

    def admin_filters(self):
        return ', '.join([f.name for f in self.filters.all()])
    admin_filters.short_description = "Admin Filters"

    def assign_to_group(self, user, group = None):
        if not self.groups.filter(name = "DEFAULT").exists():
            # add default group
            def_group = ParticipantFilterGroup.objects.get_or_create(user = user, name = "DEFAULT")[0]
            self.groups.add( def_group)
        if group is not None:
            self.groups.add( group)
    
    # Return matching participants as a queryset (allows for more complex joins)
    def execute(self):
        all_filters = list(self.filters.all()) + list(self.metafilters.all())
        nfilters = len(all_filters)
        if nfilters:
            pids = set(all_filters[0].execute())
            for i in range(1,nfilters):
                # use set operations to handle logic: http://docs.python.org/library/sets.html
                if self.action == "and":
                    pids.intersection_update(set(all_filters[i].execute()))
                if self.action == "or":
                    pids.update(set(all_filters[i].execute()))
                if self.action == "xor":
                    pids.symmetric_difference_update(set(all_filters[i].execute()))
        else:
            pids = []

        return list(pids)

    def getAction(self):
        return self.action

    @classmethod
    def _get_filter_fields(cls):
        return {}

# store tokens; tokens are unique per user
class LimeToken(models.Model):
    survey_id = models.IntegerField()
    token = models.CharField(max_length = 20)
    participant = models.ForeignKey(Participant)
    date_imported = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return u'%s,%s,%s' % (self.survey_id, self.token, self.participant)
    
    class Meta:
        verbose_name_plural = "LimeTokens"
        unique_together = ("survey_id", "token", "participant")
        
    @classmethod
    def _get_filter_fields(cls):
        return {}


    @classmethod
    def initializeRowImport(cls, table_section, survey_id):
        """ Function used at the beginning of all functions for importing a row from the LimeSurvey Database
        
        Creates participant, LimeToken, ParticipantContactInstance as necessary.
        
        INPUT: table_row[:5], survey_id
        RETURN: participant, token_created, pci
        """
        participant = Participant.objects.get_or_create(pid = int(re.sub("[^0-9]","",table_section[4])))[0]
        (lime_token, token_created) = LimeToken.objects.get_or_create(survey_id = survey_id, token = table_section[4], participant = participant)
        pci = ParticipantContactInstance.objects.get_or_create(participant = participant, date_of_test = table_section[1])[0]
        return (participant, token_created, pci)

class AnswerOption(models.Model):
    option = models.CharField(max_length = 100)
    is_default = models.BooleanField(default = False) # true if this an option provided to the users, false if they write it in
    table = models.CharField(max_length = 100)
    field = models.CharField(max_length = 100)
    order = models.IntegerField(null = True)
    unique_name = models.CharField(max_length = 250, unique = True)
    
    def __unicode__(self):
        return u'%s,%s,%s,%s' % (self.option, self.table, self.field, self.is_default)    

    def save(self, *args, **kwargs):
        if not self.unique_name:
            self.unique_name = self.__unicode__()
        super(AnswerOption, self).save(*args, **kwargs)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class QuestionOption(models.Model):
    option = models.TextField() # the full text of the question
    is_default = models.BooleanField(default = False) # true if this an option provided to the users, false if they write it in
    table = models.CharField(max_length = 100)
    field = models.CharField(max_length = 100)
    order = models.IntegerField(null = True)
    unique_name = models.CharField(max_length = 250, unique = True)
    short_name = models.CharField(max_length = 100, default = "") # used for display

    def __unicode__(self):
        return u'%s,%s,%s,%s' % (self.option, self.table, self.field, self.is_default)  
    
    def save(self, *args, **kwargs):
        if not self.unique_name:
            self.unique_name = self.__unicode__()
        super(QuestionOption, self).save(*args, **kwargs)

    @classmethod
    def _get_filter_fields(cls):
        return {}

# Keeps track of discrete contact instances
class ParticipantContactInstance(models.Model):
    participant = models.ForeignKey(Participant)
    date_of_test = models.DateField()

    @classmethod
    def _get_filter_fields(cls):
        return {}

    class Meta:
        get_latest_by = 'date_of_test'

class SPMSQ_question(models.Model):
    question = models.ForeignKey(QuestionOption)
    correct = models.BooleanField()

    def __unicode__(self):
        return u'%s,%s' % (self.question.option, self.correct)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class SPMSQ(models.Model):
    contact_instance = models.ForeignKey(ParticipantContactInstance)
    questions = models.ManyToManyField(SPMSQ_question) # 10 of these
    nerrors = models.IntegerField(default = 0) # calculated

    class Meta:
        get_latest_by = 'contact_instance__date_of_test'

    @classmethod
    def get_csv_label_list(cls):
        tmp_list = ['SPMSQ_nerrors']
        qs = SPMSQ_question.objects.order_by('question__order').distinct('question__order').values_list('question__option', flat=True)
        tmp_list.extend(map(lambda v: "SPMSQ:" + v, qs))
        return tmp_list
    
    def get_value_dict(self, names = False):
        tmp_dict = {}
        tmp_dict['SPMSQ_nerrors'] = self.nerrors
        for q in self.questions.all():
            tmp_dict['SPMSQ:' + q.question.option] = "correct" if q.correct else "inorrect"
        return tmp_dict
    
    def __unicode__(self):
        return u'%s,%i' % (self.contact_instance, self.nerrors)

    def recalculate(self):
        # non-answers are assumed to be wrong
        self.nerrors = self.questions.filter(correct = False).count()
        self.save()

    @classmethod
    def _get_filter_fields(cls):
        filter_fields = {}
        filter_fields["SPMSQ_nerrors"] = {}
        filter_fields["SPMSQ_nerrors"]["field_name"] = "nerrors"
        filter_fields["SPMSQ_nerrors"]["short_name"] = "Number of Errors"
        filter_fields["SPMSQ_nerrors"]["type"] = "ordinal"
        filter_fields["SPMSQ_nerrors"]["model"] = "SPMSQ"
        filter_fields["SPMSQ_nerrors"]["heirarchy"] = ("Tests","SPMSQ")
        filter_fields["SPMSQ_nerrors"]["function_handle"] = "SPMSQ.objects.values_list('contact_instance__participant__pid', flat = True)"
        
        filter_fields["SPMSQ_answers"] = {}
        filter_fields["SPMSQ_answers"]["field_name"] = "questions"
        filter_fields["SPMSQ_answers"]["short_name"] = "Selected Answers"
        filter_fields["SPMSQ_answers"]["type"] = "multi_select"
        filter_fields["SPMSQ_answers"]["default_representation_type"] = "multiselect"
        filter_fields["SPMSQ_answers"]["model"] = "SPMSQ"
        filter_fields["SPMSQ_answers"]["heirarchy"] = ("Tests","SPMSQ")
        filter_fields["SPMSQ_answers"]["function_handle"] = "SPMSQ.objects.values_list('contact_instance__participant__pid', flat = True)"
        options = {}
        for sq in SPMSQ_question.objects.all():
            options[sq.id] = {}
            options[sq.id]["id"] = sq.id
            options[sq.id]["name"] = sq.question.unique_name + ":" +  ("correct" if sq.correct else "incorrect")
            options[sq.id]["order"] = None
        filter_fields["SPMSQ_answers"]["options"] = options
    
        return filter_fields

class IADL_option(models.Model):
    option = models.ForeignKey(AnswerOption)
    question = models.ForeignKey(QuestionOption)
    order = models.IntegerField()
    score = models.IntegerField()

    def __unicode__(self):
        return u'%s,%s' % (self.question.unique_name, self.option.option)

    @classmethod
    def _get_filter_fields(cls):
        return {}

# Score needs to exist (not just calculated) so objects are query-able based in this value
class IADL(models.Model):
    contact_instance = models.ForeignKey(ParticipantContactInstance)
    questions = models.ManyToManyField(IADL_option) # 8 of these
    score = models.IntegerField(null = True) # calculated

    @classmethod
    def get_csv_label_list(cls):
        tmp_list = ['IADL_Score']
        qs = IADL_option.objects.order_by('question__order').distinct('question__order').values_list('question__option', flat=True)
        tmp_list.extend(map(lambda v: "IADL:" + v, qs))
        return tmp_list
    
    def get_value_dict(self, names = False):
        tmp_dict = {}
        tmp_dict['IADL_Score'] = self.score
        for q in self.questions.all():
            tmp_dict['IADL:' + q.question.option] = getOptionOrOrder(q, names)
        return tmp_dict

    class Meta:
        get_latest_by = 'contact_instance__date_of_test'
        
    def recalculate(self):
        # mising scores are incorrect -> score = 0
        self.score = self.questions.aggregate(score = Sum('score'))['score']
        self.save()

    @classmethod
    def _get_filter_fields(cls):
        filter_fields = {}
        filter_fields["IADL_score"] = {}
        filter_fields["IADL_score"]["field_name"] = "score"
        filter_fields["IADL_score"]["short_name"] = "IADL Score"
        filter_fields["IADL_score"]["type"] = "ratio"
        filter_fields["IADL_score"]["model"] = "IADL"
        filter_fields["IADL_score"]["heirarchy"] = ("Tests","IADL")
        filter_fields["IADL_score"]["function_handle"] = "IADL.objects.values_list('contact_instance__participant__pid', flat = True)"

        filter_fields["IADL_answers"] = {}
        filter_fields["IADL_answers"]["field_name"] = "questions"
        filter_fields["IADL_answers"]["short_name"] = "Selected Answers"
        filter_fields["IADL_answers"]["type"] = "multi_select"
        filter_fields["IADL_answers"]["default_representation_type"] = "multiselect"
        filter_fields["IADL_answers"]["model"] = "IADL"
        filter_fields["IADL_answers"]["heirarchy"] = ("Tests","IADL")
        filter_fields["IADL_answers"]["function_handle"] = "IADL.objects.values_list('contact_instance__participant__pid', flat = True)"
        options = {}
        for io in IADL_option.objects.all():
            options[io.id] = {}
            options[io.id]["id"] = io.id
            options[io.id]["name"] = io.__unicode__()
            options[io.id]["order"] = io.order
        filter_fields["IADL_answers"]["options"] = options
        
        return filter_fields

class TUGTrail(models.Model):
    order = models.IntegerField()
    time = models.FloatField(null = True)

    @classmethod
    def _get_filter_fields(cls):
        return {}

# Keep times as separate fields because 
class TUG(models.Model):
    contact_instance = models.ForeignKey(ParticipantContactInstance)
    times = models.ManyToManyField(TUGTrail)
    average = models.FloatField(null = True) # calculated
    mobility_rating = models.ForeignKey(AnswerOption, null = True, related_name = 'mobility_rating') # calculated
    fall_risk = models.ForeignKey(AnswerOption, null = True, related_name = 'fall_risk') # calculated

    class Meta:
        get_latest_by = 'contact_instance__date_of_test'
        
    @classmethod
    def get_csv_label_list(cls):
        return ['TUG_time 1', 'TUG_time 2', 'TUG_time 3','TUG_average_time','TUG_mobility_rating','TUG_fall_risk']
    
    def get_value_dict(self, names = False):
        tmp_dict = {}
        for i, time in enumerate(self.times.order_by('order')):
            tmp_dict['TUG_time %s' %(i+1)] = time.time
        tmp_dict['TUG_average_time'] = self.average
        tmp_dict['TUG_mobility_rating'] = getOptionOrOrder(self.mobility_rating, names)
        tmp_dict['TUG_fall_risk'] = getOptionOrOrder(self.fall_risk, names)
        return tmp_dict
    
    def recalculate(self):
        self.average = self.times.aggregate(average = Avg('time'))['average']
        
        # Calculate mobility
        if self.average < 10:
            self.mobility_rating = AnswerOption.objects.get(table = "TUG", option = "1")
        elif self.average < 20:
            self.mobility_rating = AnswerOption.objects.get(table = "TUG", option = "2")
        else:
            self.mobility_rating = AnswerOption.objects.get(table = "TUG", option = "3")
        
        # Calculate fall risk
        if self.average >= 14:
            self.fall_risk = AnswerOption.objects.get(table = "TUG", option = "high")
        else:
            self.fall_risk = AnswerOption.objects.get(table = "TUG", option = "normal")
        
        self.save()

    @classmethod
    def _get_filter_fields(cls):
        filter_fields = {}
        filter_fields["average"] = {}
        filter_fields["average"]["field_name"] = "average"
        filter_fields["average"]["short_name"] = "Average"
        filter_fields["average"]["type"] = "ratio"

        filter_fields["mobility_rating"] = {}
        filter_fields["mobility_rating"]["field_name"] = "mobility_rating"
        filter_fields["mobility_rating"]["short_name"] = "Mobility Rating"
        filter_fields["mobility_rating"]["type"] = "single_select"
        filter_fields["mobility_rating"]["options"] = get_select_options("TUG", "mobility_rating")

        filter_fields["fall_risk"] = {}
        filter_fields["fall_risk"]["field_name"] = "fall_risk"
        filter_fields["fall_risk"]["short_name"] = "Fall Risk"
        filter_fields["fall_risk"]["type"] = "single_select"
        filter_fields["fall_risk"]["options"] = get_select_options("TUG", "fall_risk")
                
        for k,v in filter_fields.items():
            v["heirarchy"] = ("Tests","TUG")
            v["model"] = "TUG"
            v["function_handle"] = "TUG.objects.values_list('contact_instance__participant__pid', flat = True)"
        
        return filter_fields

# Data from this section that doeasn't change with time
class ParticipantInductionStatic(models.Model):
    participant = models.ForeignKey(Participant)
    us_citizen = models.BooleanField() # may change
    hisp_latino = models.ForeignKey(AnswerOption, related_name = 'hisp_latino')
    racial_origin = models.ManyToManyField(AnswerOption, related_name = 'racial_origin') # handle blanks as additional non-default fields
    racial_origin_comments = models.TextField()
    retirement_year = models.IntegerField(null = True)
    gender = models.ForeignKey(AnswerOption) # male, female, ??

    def admin_racial_origin(self):
        return ', '.join([o.option for o in self.racial_origin.all()])
    admin_racial_origin.short_description = "Admin Racial Origin Selections"

    @classmethod
    def get_csv_label_list(cls):
        return ['us_citizen','hisp_latino','racial_origin','racial_origin_comments','retirement_year','gender']
    
    def get_value_dict(self, names = False):
        tmp_dict = {}
        tmp_dict['us_citizen'] = self.us_citizen
        tmp_dict['hisp_latino'] = getOptionOrOrder(self.hisp_latino, names)
        tmp_dict['racial_origin'] = getManyToManySingleValue(self.racial_origin)
        tmp_dict['racial_origin_comments'] = self.racial_origin_comments
        tmp_dict['retirement_year'] = self.retirement_year
        tmp_dict['gender'] = self.gender.option
        return tmp_dict

    @classmethod
    def _get_filter_fields(cls):
        filter_fields = {}
        filter_fields["us_citizen"] = {}
        filter_fields["us_citizen"]["field_name"] = "us_citizen"
        filter_fields["us_citizen"]["short_name"] = "US Citizen?"
        filter_fields["us_citizen"]["type"] = "boolean"

        filter_fields["hisp_latino"] = {}
        filter_fields["hisp_latino"]["field_name"] = "hisp_latino"
        filter_fields["hisp_latino"]["short_name"] = "Hispanic/Latino"
        filter_fields["hisp_latino"]["type"] = "single_select"
        filter_fields["hisp_latino"]["options"] = get_select_options("ParticipantInductionStatic", "hisp_latino")
        
        filter_fields["racial_origin"] = {}
        filter_fields["racial_origin"]["field_name"] = "racial_origin"
        filter_fields["racial_origin"]["short_name"] = "Racial Origin"
        filter_fields["racial_origin"]["type"] = "multi_select"
        filter_fields["racial_origin"]["options"] = get_select_options("ParticipantInductionStatic", "racial_origin")
        filter_fields["racial_origin"]["default_representation_type"] = "multiselect"

        filter_fields["racial_origin_comments"] = {}
        filter_fields["racial_origin_comments"]["field_name"] = "racial_origin_comments"
        filter_fields["racial_origin_comments"]["short_name"] = "Recial Origin Comments"
        filter_fields["racial_origin_comments"]["type"] = "text"

        filter_fields["retirement_year"] = {}
        filter_fields["retirement_year"]["field_name"] = "retirement_year"
        filter_fields["retirement_year"]["short_name"] = "Retirement Year"
        filter_fields["retirement_year"]["type"] = "ordinal"

        filter_fields["gender"] = {}
        filter_fields["gender"]["field_name"] = "gender"
        filter_fields["gender"]["short_name"] = "Gender"
        filter_fields["gender"]["type"] = "single_select"
        filter_fields["gender"]["options"] = get_select_options("ParticipantInductionStatic", "gender")

        for k,v in filter_fields.items():
            v["heirarchy"] = ("Participant Induction","Static")
            v["model"] = "ParticipantInductionStatic"
            v["function_handle"] = "ParticipantInductionStatic.objects.values_list('participant__pid', flat = True)"

        return filter_fields

# Data that may be useful to track
class ParticipantInductionVolatile(models.Model):
    contact_instance = models.ForeignKey(ParticipantContactInstance)
    education_level = models.ForeignKey(AnswerOption, related_name = 'education_level')
    marital_status = models.ForeignKey(AnswerOption, related_name = 'marital_status')
    n_perm_residents = models.IntegerField()
    perm_residents = models.ManyToManyField(AnswerOption, related_name = 'perm_residents')
    housing_type = models.ForeignKey(AnswerOption, related_name = 'housing_type')
    household_income = models.ForeignKey(AnswerOption, related_name = 'household_income')
    occupation_status = models.ManyToManyField(AnswerOption, related_name = 'occupation_status')
    current_occupation = models.ManyToManyField(AnswerOption, related_name = 'current_occupation')
    leave_home_freq = models.ForeignKey(AnswerOption, related_name = 'leave_home_freq')
    leave_home_reasons = models.ManyToManyField(AnswerOption, related_name = 'leave_home_reasons')
    limited_tranport = models.BooleanField()
    has_home_internet = models.BooleanField()
    has_wireless_internet = models.BooleanField()
    type_of_internet = models.ForeignKey(AnswerOption, related_name="type_of_internet") # dialup, broadband, not sure
        
    @classmethod
    def get_csv_label_list(cls):
        return ['education_level','marital_status','n_perm_residents','perm_residents','housing_type','household_income',
                'occupation_status','current_occupation','leave_home_freq','leave_home_reasons','limited_tranport','has_home_internet','has_wireless_internet','type_of_internet']
    
    def get_value_dict(self, names = False):
        tmp_dict = {}
        tmp_dict['education_level'] = getOptionOrOrder(self.education_level, names)
        tmp_dict['marital_status'] = getOptionOrOrder(self.marital_status, names)
        tmp_dict['n_perm_residents'] = self.n_perm_residents
        tmp_dict['perm_residents'] = getManyToManySingleValue(self.perm_residents)
        tmp_dict['housing_type'] = getOptionOrOrder(self.housing_type, names)
        tmp_dict['household_income'] = getOptionOrOrder(self.household_income, names)
        tmp_dict['occupation_status'] = getManyToManySingleValue(self.occupation_status)
        tmp_dict['current_occupation'] = getManyToManySingleValue(self.current_occupation)
        tmp_dict['leave_home_freq'] = getOptionOrOrder(self.leave_home_freq, names)
        tmp_dict['leave_home_reasons'] = getManyToManySingleValue(self.leave_home_reasons)
        tmp_dict['limited_tranport'] = self.limited_tranport
        tmp_dict['has_home_internet'] = self.has_home_internet
        tmp_dict['has_wireless_internet'] = self.has_wireless_internet
        tmp_dict['type_of_internet'] = getOptionOrOrder(self.type_of_internet, names)
        return tmp_dict

    class Meta:
        get_latest_by = 'contact_instance__date_of_test'

    @classmethod
    def _get_filter_fields(cls):
        filter_fields = {}
        filter_fields["education_level"] = {}
        filter_fields["education_level"]["field_name"] = "education_level"
        filter_fields["education_level"]["short_name"] = "Education Level"
        filter_fields["education_level"]["type"] = "single_select"
        filter_fields["education_level"]["options"] = get_select_options("ParticipantInductionVolatile", "education_level")

        filter_fields["marital_status"] = {}
        filter_fields["marital_status"]["field_name"] = "marital_status"
        filter_fields["marital_status"]["short_name"] = "Marital Status?"
        filter_fields["marital_status"]["type"] = "single_select"
        filter_fields["marital_status"]["options"] = get_select_options("ParticipantInductionVolatile", "marital_status")

        filter_fields["n_perm_residents"] = {}
        filter_fields["n_perm_residents"]["field_name"] = "n_perm_residents"
        filter_fields["n_perm_residents"]["short_name"] = "# Permenant Residents"
        filter_fields["n_perm_residents"]["type"] = "ordinal"

        filter_fields["perm_residents"] = {}
        filter_fields["perm_residents"]["field_name"] = "perm_residents"
        filter_fields["perm_residents"]["short_name"] = "Permenant Residents"
        filter_fields["perm_residents"]["type"] = "multi_select"
        filter_fields["perm_residents"]["options"] = get_select_options("ParticipantInductionVolatile", "perm_residents")
        filter_fields["perm_residents"]["default_representation_type"] = "multiselect"

        filter_fields["housing_type"] = {}
        filter_fields["housing_type"]["field_name"] = "housing_type"
        filter_fields["housing_type"]["short_name"] = "Housing Type"
        filter_fields["housing_type"]["type"] = "single_select"
        filter_fields["housing_type"]["options"] = get_select_options("ParticipantInductionVolatile", "housing_type")

        filter_fields["household_income"] = {}
        filter_fields["household_income"]["field_name"] = "household_income"
        filter_fields["household_income"]["short_name"] = "Household Income"
        filter_fields["household_income"]["type"] = "single_select"
        filter_fields["household_income"]["options"] = get_select_options("ParticipantInductionVolatile", "household_income")

        filter_fields["occupation_status"] = {}
        filter_fields["occupation_status"]["field_name"] = "occupation_status"
        filter_fields["occupation_status"]["short_name"] = "Occupation Status"
        filter_fields["occupation_status"]["type"] = "multi_select"
        filter_fields["occupation_status"]["options"] = get_select_options("ParticipantInductionVolatile", "occupation_status")
        filter_fields["occupation_status"]["default_representation_type"] = "multiselect"

        filter_fields["current_occupation"] = {}
        filter_fields["current_occupation"]["field_name"] = "current_occupation"
        filter_fields["current_occupation"]["short_name"] = "Current Occupation"
        filter_fields["current_occupation"]["type"] = "multi_select"
        filter_fields["current_occupation"]["options"] = get_select_options("ParticipantInductionVolatile", "current_occupation")
        filter_fields["current_occupation"]["default_representation_type"] = "multiselect"

        filter_fields["leave_home_freq"] = {}
        filter_fields["leave_home_freq"]["field_name"] = "leave_home_freq"
        filter_fields["leave_home_freq"]["short_name"] = "Frequency of leaving home"
        filter_fields["leave_home_freq"]["type"] = "single_select"
        filter_fields["leave_home_freq"]["options"] = get_select_options("ParticipantInductionVolatile", "leave_home_freq")

        filter_fields["leave_home_reasons"] = {}
        filter_fields["leave_home_reasons"]["field_name"] = "leave_home_reasons"
        filter_fields["leave_home_reasons"]["short_name"] = "Reasons for leaving home"
        filter_fields["leave_home_reasons"]["type"] = "multi_select"
        filter_fields["leave_home_reasons"]["options"] = get_select_options("ParticipantInductionVolatile", "leave_home_reasons")
        filter_fields["leave_home_reasons"]["default_representation_type"] = "multiselect"

        filter_fields["limited_tranport"] = {}
        filter_fields["limited_tranport"]["field_name"] = "limited_tranport"
        filter_fields["limited_tranport"]["short_name"] = "Limited Transportation?"
        filter_fields["limited_tranport"]["type"] = "boolean"

        filter_fields["has_home_internet"] = {}
        filter_fields["has_home_internet"]["field_name"] = "has_home_internet"
        filter_fields["has_home_internet"]["short_name"] = "Has home internet?"
        filter_fields["has_home_internet"]["type"] = "boolean"

        filter_fields["has_wireless_internet"] = {}
        filter_fields["has_wireless_internet"]["field_name"] = "has_wireless_internet"
        filter_fields["has_wireless_internet"]["short_name"] = "Has wireless internet?"
        filter_fields["has_wireless_internet"]["type"] = "boolean"

        filter_fields["type_of_internet"] = {}
        filter_fields["type_of_internet"]["field_name"] = "type_of_internet"
        filter_fields["type_of_internet"]["short_name"] = "Type of Internet"
        filter_fields["type_of_internet"]["type"] = "single_select"
        filter_fields["type_of_internet"]["options"] = get_select_options("ParticipantInductionVolatile", "type_of_internet")

        for k,v in filter_fields.items():
            v["heirarchy"] = ("Participant Induction","Volatile")
            v["model"] = "ParticipantInductionVolatile"
            v["function_handle"] = "ParticipantInductionVolatile.objects.values_list('contact_instance__participant__pid', flat = True)"
        
        return filter_fields

class ParticipantSurgeries(models.Model):
    t_surgery = models.TextField()
    year = models.IntegerField()

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ParticipantMedicalCondition(models.Model):
    condition = models.ForeignKey(QuestionOption) # see full list
    condition_onset = models.ForeignKey(AnswerOption) # lifetime, now, never
    year_of_onset = models.IntegerField(null = True) #

    def __unicode__(self):
        if self.year_of_onset:
            return u'%s, %s, %s' % (self.condition.option,self.condition_onset.option,self.year_of_onset)
        else:
            return u'%s, %s' % (self.condition.option,self.condition_onset.option)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ParticipantMedication(models.Model):
    medication_name = models.CharField(max_length = 100)
    dose_amt = models.FloatField(null = True) # numerical value
    dose_units = models.CharField(max_length = 10, null = True) # table, mg, ml, etc. - use most precise measurement
    dose_frequency = models.ForeignKey(AnswerOption, null = True)
    med_reason = models.CharField(max_length = 100, null = True) # why are they taking this
    med_duration = models.IntegerField(null = True) # days
    side_effects = models.TextField(null = True) # should probably formalize this at some point into options
    is_prescription = models.BooleanField()
    notes = models.TextField(null = True) # store information (like other units) here

    def __unicode__(self):
        return u'%s' % (self.medication_name)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ParticipantMobilityHealth(models.Model):
    contact_instance = models.ForeignKey(ParticipantContactInstance)
    ht_in = models.FloatField()
    wt_lbs = models.FloatField(null = True)
    assistive_devices = models.ManyToManyField(AnswerOption, related_name = 'assistive_devices')
    mobility_aids = models.ManyToManyField(AnswerOption, related_name = 'mobility_aids')
    physical_activity = models.ForeignKey(AnswerOption, related_name = 'physical_activity')
    surgeries = models.ManyToManyField(ParticipantSurgeries) # these can be paired with any visit this way
    medical_conditions = models.ManyToManyField(ParticipantMedicalCondition) # these can be paired with any visit this way
    medications = models.ManyToManyField(ParticipantMedication) # these can be paired with any visit this way

    class Meta:
        get_latest_by = 'contact_instance__date_of_test'

    @classmethod
    def get_csv_label_list(cls):
        tmp_list = ['ht_in', 'wt_lbs', 'physical_activity']
        
        ndev = ParticipantMobilityHealth.objects.annotate(ndev = Count('assistive_devices')).aggregate(Max('ndev'))['ndev__max']
        nmob = ParticipantMobilityHealth.objects.annotate(nmob = Count('mobility_aids')).aggregate(Max('nmob'))['nmob__max']
        nsurgeries = ParticipantMobilityHealth.objects.annotate(nsurgeries = Count('surgeries')).aggregate(Max('nsurgeries'))['nsurgeries__max']
        nmed = ParticipantMobilityHealth.objects.annotate(nmed = Count('medications')).aggregate(Max('nmed'))['nmed__max']
        
        for i in range(ndev):
            tmp_list.append('assistive_device %s' %(i+1))
        for i in range(nmob):
            tmp_list.append('mobility_aid %s' %(i+1))
        for i in range(nsurgeries):
            tmp_list.append('surgery %s' %(i+1))
        for c in ParticipantMedicalCondition.objects.order_by('condition__option').distinct('condition__option').values_list('condition__option', flat=True):
            tmp_list.append('medical_condition: %s' %(c))
        for i in range(nmed):
            tmp_list.append('medication %s' %(i+1))
                    
        return tmp_list
    
    def get_value_dict(self, names = False):
        # reduce(lambda o, n: o + 1 + n.find('medical_condition'), labels, 0) # count
        # filter(lambda l: l.find('medical') != -1, t) # fields
        
        tmp_dict = {'ht_in': self.ht_in, 'wt_lbs': self.wt_lbs, 'physical_activity': getOptionOrOrder(self.physical_activity, names)}
        
        for k, v in enumerate(self.assistive_devices.all()):
            tmp_dict['assistive_device %s' %(k+1)] = getOptionOrOrder(v, names)
        for k, v in enumerate(self.mobility_aids.all()):
            tmp_dict['mobility_aid %s' %(k+1)] = getOptionOrOrder(v, names)
        for k, v in enumerate(self.surgeries.all()):
            tmp_dict['surgery %s' %(k+1)] = "%s, %s" % (v.t_surgery, v.year)
        for v in self.medical_conditions.all():
            tmp_dict['medical_condition: %s' %(v.condition.option)] = "%s, %s" %(getOptionOrOrder(v.condition_onset, names), v.year_of_onset)
        for k, v in enumerate(self.medications.all()):
            freq = v.dose_frequency
            if freq is not None:
                freq = getOptionOrOrder(v.dose_frequency, names)
            tmp_dict['medication %s' %(k+1)] = "%s, %s %s, %s" %(v.medication_name, v.dose_amt, v.dose_units, freq)
        
        return tmp_dict

    @classmethod
    def _get_filter_fields(cls):
        filter_fields = {}
        filter_fields["ht_in"] = {}
        filter_fields["ht_in"]["field_name"] = "ht_in"
        filter_fields["ht_in"]["short_name"] = "Height (in)"
        filter_fields["ht_in"]["type"] = "ratio"

        filter_fields["wt_lbs"] = {}
        filter_fields["wt_lbs"]["field_name"] = "wt_lbs"
        filter_fields["wt_lbs"]["short_name"] = "Weight (lbs)"
        filter_fields["wt_lbs"]["type"] = "ratio"

        filter_fields["assistive_devices"] = {}
        filter_fields["assistive_devices"]["field_name"] = "assistive_devices"
        filter_fields["assistive_devices"]["short_name"] = "Assistive devices"
        filter_fields["assistive_devices"]["type"] = "multi_select"
        filter_fields["assistive_devices"]["default_representation_type"] = "multiselect"
        filter_fields["assistive_devices"]["options"] = get_select_options("ParticipantMobilityHealth", "assistive_devices")

        filter_fields["mobility_aids"] = {}
        filter_fields["mobility_aids"]["field_name"] = "mobility_aids"
        filter_fields["mobility_aids"]["type"] = "multi_select"
        filter_fields["mobility_aids"]["short_name"] = "Mobility Aids"
        filter_fields["mobility_aids"]["default_representation_type"] = "multiselect"
        filter_fields["mobility_aids"]["options"] = get_select_options("ParticipantMobilityHealth", "mobility_aids")

        filter_fields["physical_activity"] = {}
        filter_fields["physical_activity"]["field_name"] = "physical_activity"
        filter_fields["physical_activity"]["short_name"] = "Physical Activity"
        filter_fields["physical_activity"]["type"] = "single_select"
        filter_fields["physical_activity"]["options"] = get_select_options("ParticipantMobilityHealth", "physical_activity")

        #  Fix the way all three of these are handled
        # sort type of surgery as text, year range of surgeries as int
        filter_fields["surgeries"] = {}
        filter_fields["surgeries"]["field_name"] = "surgeries"
        filter_fields["surgeries"]["short_name"] = "Surgeries"
        filter_fields["surgeries"]["type"] = "multi_select"
        filter_fields["surgeries"]["options"] = get_select_options("ParticipantMobilityHealth", "surgeries")
        filter_fields["surgeries"]["default_representation_type"] = "multiselect"

        # for each condition, sort onset as single select, year of onset as int
        filter_fields["medical_conditions"] = {}
        filter_fields["medical_conditions"]["field_name"] = "medical_conditions"
        filter_fields["medical_conditions"]["short_name"] = "Medical Conditions"
        filter_fields["medical_conditions"]["type"] = "multi_select"
        filter_fields["medical_conditions"]["options"] = get_select_options("ParticipantMobilityHealth", "medical_conditions")
        filter_fields["medical_conditions"]["default_representation_type"] = "multiselect"

        # search medication_name as text, side effects as text
        filter_fields["medications"] = {}
        filter_fields["medications"]["field_name"] = "medications"
        filter_fields["medications"]["short_name"] = "Medications"
        filter_fields["medications"]["type"] = "multi_select"
        filter_fields["medications"]["options"] = get_select_options("ParticipantMobilityHealth", "medications")
        filter_fields["medications"]["default_representation_type"] = "multiselect"

        for k,v in filter_fields.items():
            v["heirarchy"] = ("Participant Induction","Mobility and Health")
            v["model"] = "ParticipantMobilityHealth"
            v["function_handle"] = "ParticipantMobilityHealth.objects.values_list('contact_instance__participant__pid', flat = True)"
        
        return filter_fields

# Used for most of the questions in the Induction Interview
class ScaleQuestionAndOption(models.Model):
    question = models.ForeignKey(QuestionOption)
    option = models.ForeignKey(AnswerOption, null = True)
    order = models.IntegerField(default = None, null = True)
    
    def __unicode__(self):
        try:
            return u'%s, %s, %s' % (self.question.option,self.option.option, self.order)
        except AttributeError:
            return u'%s, %s, %s' % (self.question.option,self.option, self.order)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ParticipantScaleRatingScores(models.Model):
    fma_std_fn_index = models.FloatField(null = True, default = None)
    fma_raw_score = models.FloatField(null = True, default = None)
    fma_std_daily_score = models.FloatField(null = True, default = None)
    fma_std_emot_score = models.FloatField(null = True, default = None)
    fma_std_armh_score = models.FloatField(null = True, default = None)
    fma_std_mobi_score = models.FloatField(null = True, default = None)
    fma_std_bother_index = models.FloatField(null = True, default = None)
    fma_bother_raw_score = models.FloatField(null = True, default = None)
    
    promis_raw_score = models.FloatField(null = True, default = None)
    promis_score = models.FloatField(null = True, default = None)
    
    whoqol_bref_health = models.FloatField(null = True, default = None)
    whoqol_bref_psych = models.FloatField(null = True, default = None)
    whoqol_bref_social = models.FloatField(null = True, default = None)
    whoqol_bref_envir = models.FloatField(null = True, default = None)
    whoqol_old_sense = models.FloatField(null = True, default = None)
    whoqol_old_aut = models.FloatField(null = True, default = None)
    
    tech_confidence_score = models.FloatField(null = True, default = None)
    tech_attitude_score = models.FloatField(null = True, default = None)
    
    @classmethod
    def _get_filter_fields(cls):
        return {}
    
    def getSurveySelections(self):
        return ParticipantScaleRatings.objects.get(rating_scores = self).survey_selections.all() # ScaleQuestionAndOption objects
    
    def _score_calculation(self, ids, qs, reverse_order_indecies = [], response_rate = 0.499, score_range = range(1,6), replace_missing = True, calc_std = True, raw_fn_handle = sum):        
        qs = qs.filter(order__in = ids)
        sqas = self.getSurveySelections().filter(question__in = qs, order__in = score_range)

        #print [q.order for q in qs]
        #print len(qs)
        #print len(sqas)
        #print len(ids)
        
        if len(sqas) > len(ids)*response_rate:
            # get average of matching values
            orders = [((max(score_range) + 1) - o['order']) # order scoring switched, e.g. [5->1, 4->2, 3->3, 2->4, 1->5] if score_range = [1,2,3,4,5]
                      if o['question__order'] in reverse_order_indecies else 
                      o['order'] 
                      for o in sqas.values('order', 'question__order')]
            
            # get the total sum of values
            if replace_missing:
                # use average for missing values
                raw = average(orders)
                raw_sum = raw_fn_handle(orders) + (len(ids) - len(orders))*raw
            else:
                raw_sum = float(raw_fn_handle(orders))
            
            if calc_std:
                min_score = len(ids) # 1 for each
                max_adj_score = min_score*(max(score_range) - 1) # subtract 1 from max score for each
                std_score = (raw_sum - min_score)/max_adj_score * 100
            else:
                std_score = None
            
            return (std_score, raw_sum)
        else:
            return (None, None)
    
    def recalculate(self):
        # Calculate scores based on survey question responses
        
        # question index for ordered sections starts with 1
        fma_daily_ids = [3,14,15,20,21,22,23,24,33] # 9
        fma_emot_ids = [7,27,29,30,31,32,34] # 7
        fma_armh_ids = [2,5,9,10,11,16,17,18] # 8
        fma_mobil_ids = [1,4,6,8,12,13,19,26,28] # 9
        
        fma_qs = QuestionOption.objects.filter(table = "ScaleQuestionAndOption", field = "question", is_default = True, option__contains = "Functional Movement Abilities: ")
        (self.fma_std_daily_score, raw_dail) = self._score_calculation(fma_daily_ids, fma_qs, reverse_order_indecies = fma_daily_ids)
        (self.fma_std_emot_score, raw_emot) = self._score_calculation(fma_emot_ids, fma_qs, reverse_order_indecies = fma_emot_ids)
        (self.fma_std_armh_score, raw_armh) = self._score_calculation(fma_armh_ids, fma_qs, reverse_order_indecies = fma_armh_ids)
        (self.fma_std_mobi_score, raw_mobi) = self._score_calculation(fma_mobil_ids, fma_qs, reverse_order_indecies = fma_mobil_ids)
        
        if (self.fma_std_daily_score is not None
            and self.fma_std_emot_score is not None
            and self.fma_std_armh_score is not None
            and self.fma_std_mobi_score is not None):
            min_total_score = len(fma_daily_ids) + len(fma_emot_ids) + len(fma_armh_ids) + len(fma_mobil_ids)
            self.fma_raw_score = raw_dail + raw_emot + raw_armh + raw_mobi
            self.fma_std_fn_index = (self.fma_raw_score - min_total_score)/(min_total_score*4)*100 # 4 = max_score - 1
        
        fma_bother_ids = [35,36,37,38,39,40,41,42,43,44,45,46] # 12
        (self.fma_std_bother_index, self.fma_bother_raw_score) = self._score_calculation(fma_bother_ids, fma_qs, reverse_order_indecies = fma_bother_ids, replace_missing = False)
        
        # Calculate PROMIS score - verified to work
        satis_qs = QuestionOption.objects.filter(table = "ScaleQuestionAndOption", field = "question", is_default = True, option__contains = "Satisfaction with Social Roles and Activities: ")
        sqas = self.getSurveySelections().filter(question__in = satis_qs, order__in = range(1,6))
        orders = [o['order'] for o in sqas.values('order')]
        self.promis_raw_score = float(sum(orders))
        if len(sqas) > 4:
            promis_pro_rate = round(self.promis_raw_score/len(sqas) * 8) # == promis_raw_score if len(sqas) == 8
            promis_scores = [26.2,30.0,31.7,33.1,34.2,35.2,36.1,36.9,37.7,38.5,39.4,40.2,41.0,41.8,42.7,43.5,44.4,45.3,46.2,47.1,47.9,48.8,49.7,50.6,51.6,52.5,53.4,54.4,55.5,56.8,58.3,60.4,65.6]
            self.promis_score = promis_scores[int(promis_pro_rate) - 8] # 8->0, 48->40, etc for accessing score index

        # WHOQOL
        whoqol_bref_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26]
        whoqol_bref_health_ids = [3,4,10,15,16,17,18]
        whoqol_bref_psych_ids = [5,6,7,11,19,26]
        whoqol_bref_social_ids = [20,22]
        whoqol_bref_envir_ids = [8,9,12,13,14,23,24,25]

        qol_qs = QuestionOption.objects.filter(table = "ScaleQuestionAndOption", field = "question", is_default = True, option__contains = "Quality of Life: ")
        sqas = self.getSurveySelections().filter(question__in = qol_qs, order__in = whoqol_bref_ids)
        if len(sqas) > len(whoqol_bref_ids)*0.8:
            # 80% tresponse rate
            (_, self.whoqol_bref_health) = self._score_calculation(whoqol_bref_health_ids, qol_qs, response_rate = 0.7, reverse_order_indecies = [3,4,26], calc_std = False, raw_fn_handle = average) # 5/7 = 0.71
            (_, self.whoqol_bref_psych) = self._score_calculation(whoqol_bref_psych_ids, qol_qs, response_rate = 0.65, reverse_order_indecies = [3,4,26], calc_std = False, raw_fn_handle = average) # 4/6 = 0.67
            (_, self.whoqol_bref_social) = self._score_calculation(whoqol_bref_social_ids, qol_qs, response_rate = 0.99, reverse_order_indecies = [3,4,26], calc_std = False, raw_fn_handle = average) # 2/2 = 1
            (_, self.whoqol_bref_envir) = self._score_calculation(whoqol_bref_envir_ids, qol_qs, response_rate = 0.74, reverse_order_indecies = [3,4,26], calc_std = False, raw_fn_handle = average) # 6/8 = 0.75

            if self.whoqol_bref_health is not None:
                self.whoqol_bref_health *= 4
            if self.whoqol_bref_psych is not None:
                self.whoqol_bref_psych *= 4
            if self.whoqol_bref_social is not None:
                self.whoqol_bref_social *= 4
            if self.whoqol_bref_envir is not None:
                self.whoqol_bref_envir *= 4
        
        whoqol_old_ids = [1,2,3,4,5,6,7,8]
        whoqol_old_sense_ids = [1,2,6,8]
        whoqol_old_aut_ids = [3,4,5,7]
        qol_old_qs = QuestionOption.objects.filter(table = "ScaleQuestionAndOption", field = "question", is_default = True, option__contains = "Last Two Weeks: ")
        sqas = self.getSurveySelections().filter(question__in = qol_old_qs, order__in = whoqol_old_ids)
        if len(sqas) > len(qol_old_qs)*0.8:
            (_, self.whoqol_old_sense) = self._score_calculation(whoqol_old_sense_ids, qol_old_qs, response_rate = 0.8, reverse_order_indecies = [1,2,6], calc_std = False, raw_fn_handle = average)
            (_, self.whoqol_old_aut) = self._score_calculation(whoqol_old_aut_ids, qol_old_qs, response_rate = 0.8, reverse_order_indecies = [1,2,6], calc_std = False, raw_fn_handle = average)
            if self.whoqol_old_sense is not None:
                self.whoqol_old_sense *= 4
            if self.whoqol_old_aut is not None:
                self.whoqol_old_aut *= 4

        # Tech attitude score
        tech_attitude_ids = [1,2,3,4,5,6]
        tech_attitude_qs = QuestionOption.objects.filter(table = "ScaleQuestionAndOption", field = "question", is_default = True, option__contains = "Technology: Attitudes Toward Information Technology: ")
        (_, self.tech_attitude_score) = self._score_calculation(tech_attitude_ids, tech_attitude_qs, score_range = range(1,4), calc_std = False, raw_fn_handle = average)
        
        # Tech confidence score
        tech_confidence_qs = QuestionOption.objects.filter(table = "ScaleQuestionAndOption", field = "question", is_default = True, option__contains = "Technology: Confidence with Technology: ")
        sqas = self.getSurveySelections().filter(question__in = tech_confidence_qs, order__in = range(1,11))
        self.tech_confidence_score = sum([q.order if q.order is not None else 0 for q in sqas])        
        
        # save changes
        self.save()

class ParticipantScaleRatings(models.Model):
    contact_instance = models.ForeignKey(ParticipantContactInstance)
    survey_selections = models.ManyToManyField(ScaleQuestionAndOption) # these can be paired with any visit this way
    rating_scores = models.ForeignKey(ParticipantScaleRatingScores)
    research_notes = models.TextField(null = True) # for this visit

    class Meta:
        get_latest_by = 'contact_instance__date_of_test'

    def save(self, *args, **kwargs):
        if self.id is None:
            # create the field
            self.rating_scores = ParticipantScaleRatingScores.objects.create()
        super(ParticipantScaleRatings, self).save(*args, **kwargs)

    @classmethod
    def get_csv_label_list(cls):
        # Headers for scores and for Q and As
        tmp_dict = map(lambda f: f.name, ParticipantScaleRatingScores._meta.fields)
        tmp_dict.extend( ScaleQuestionAndOption.objects.order_by('question__option').distinct('question__option').values_list('question__option', flat=True))        
        tmp_dict.remove('id')
        return tmp_dict

    def get_value_dict(self, names = False):
        tmp_dict = model_to_dict(self.rating_scores) # dict of {'score_name': val}
    
        ss = self.survey_selections.order_by('question__option').values('question__option','option__option','option__order') # dict of {'score_name': val}
        for s in ss:
            tmp_dict[s["question__option"]] = s["option__option"] if (names) else s["option__order"]
        return tmp_dict


    @classmethod
    def _get_filter_fields(cls):
        
        # Questions
        survey_filter_fields = {}
        
        for q in QuestionOption.objects.filter(table = 'ScaleQuestionAndOption', is_default = True): # may be looping over more than necessary
            name = q.unique_name
            
            if name == "":
                print q.__dict__
            
            survey_filter_fields[name] = {}
            survey_filter_fields[name]["field_name"] = "survey_selections"
            survey_filter_fields[name]["heirarchy"] = tuple([u'Survey Selections'] + q.option.split(":")[:-1])
            survey_filter_fields[name]["short_name"] = q.short_name
            survey_filter_fields[name]["full_name"] = q.option
            survey_filter_fields[name]["type"] = "multi_select"
            survey_filter_fields[name]["default_representation_type"] = "multiselect"
            survey_filter_fields[name]["function_handle"] = "ParticipantScaleRatings.objects.values_list('contact_instance__participant__pid', flat = True)"
            options = {}
            for o in ScaleQuestionAndOption.objects.filter(question__id = q.id):
                options[o.id] = {}
                options[o.id]["id"] = o.id
                if o.option is None:
                    options[o.id]["name"] = None
                    options[o.id]["order"] = None
                    options[o.id]["is_default"] = False
                else:
                    options[o.id]["name"] = o.option.option
                    options[o.id]["order"] = o.option.order
                    options[o.id]["is_default"] = o.option.is_default
            
            survey_filter_fields[name]["options"] = options
        
        for k,v in survey_filter_fields.items():
            v["model"] = "ScaleQuestionAndOption"
        
        # SCORES
        score_filter_fields = {}
        score_filter_fields["fma_std_fn_index"] = {}
        score_filter_fields["fma_std_fn_index"]["field_name"] = "rating_scores__fma_std_fn_index"
        score_filter_fields["fma_std_fn_index"]["short_name"] = "FMA Standardized Function Index"
        score_filter_fields["fma_std_fn_index"]["type"] = "ratio"
        
        score_filter_fields["fma_raw_score"] = {}
        score_filter_fields["fma_raw_score"]["field_name"] = "rating_scores__fma_raw_score"
        score_filter_fields["fma_raw_score"]["short_name"] = "FMA Raw Scores"
        score_filter_fields["fma_raw_score"]["type"] = "ratio"

        score_filter_fields["fma_std_daily_score"] = {}
        score_filter_fields["fma_std_daily_score"]["field_name"] = "rating_scores__fma_std_daily_score"
        score_filter_fields["fma_std_daily_score"]["short_name"] = "FMA Standardized Daily Score"
        score_filter_fields["fma_std_daily_score"]["type"] = "ratio"

        score_filter_fields["fma_std_emot_score"] = {}
        score_filter_fields["fma_std_emot_score"]["field_name"] = "rating_scores__fma_std_emot_score"
        score_filter_fields["fma_std_emot_score"]["short_name"] = "FMA Standardized Emotion Index"
        score_filter_fields["fma_std_emot_score"]["type"] = "ratio"

        score_filter_fields["fma_std_armh_score"] = {}
        score_filter_fields["fma_std_armh_score"]["field_name"] = "rating_scores__fma_std_armh_score"
        score_filter_fields["fma_std_armh_score"]["short_name"] = "FMA Standardized Arm/Hand Score"
        score_filter_fields["fma_std_armh_score"]["type"] = "ratio"

        score_filter_fields["fma_std_mobi_score"] = {}
        score_filter_fields["fma_std_mobi_score"]["field_name"] = "rating_scores__fma_std_mobi_score"
        score_filter_fields["fma_std_mobi_score"]["short_name"] = "FMA Standardized Mobility Score"
        score_filter_fields["fma_std_mobi_score"]["type"] = "ratio"

        score_filter_fields["fma_std_bother_index"] = {}
        score_filter_fields["fma_std_bother_index"]["field_name"] = "rating_scores__fma_std_bother_index"
        score_filter_fields["fma_std_bother_index"]["short_name"] = "FMA Standardized Bother Index"
        score_filter_fields["fma_std_bother_index"]["type"] = "ratio"

        score_filter_fields["fma_bother_raw_score"] = {}
        score_filter_fields["fma_bother_raw_score"]["field_name"] = "rating_scores__fma_bother_raw_score"
        score_filter_fields["fma_bother_raw_score"]["short_name"] = "FMA Bother Raw Score"
        score_filter_fields["fma_bother_raw_score"]["type"] = "ratio"

        score_filter_fields["promis_raw_score"] = {}
        score_filter_fields["promis_raw_score"]["field_name"] = "rating_scores__promis_raw_score"
        score_filter_fields["promis_raw_score"]["short_name"] = "PROMIS Raw Score"
        score_filter_fields["promis_raw_score"]["type"] = "ratio"

        score_filter_fields["promis_score"] = {}
        score_filter_fields["promis_score"]["field_name"] = "rating_scores__promis_score"
        score_filter_fields["promis_score"]["short_name"] = "PROMIS Score"
        score_filter_fields["promis_score"]["type"] = "ratio"

        score_filter_fields["whoqol_bref_health"] = {}
        score_filter_fields["whoqol_bref_health"]["field_name"] = "rating_scores__whoqol_bref_health"
        score_filter_fields["whoqol_bref_health"]["short_name"] = "WHOQOL Brief Health Score"
        score_filter_fields["whoqol_bref_health"]["type"] = "ratio"

        score_filter_fields["whoqol_bref_psych"] = {}
        score_filter_fields["whoqol_bref_psych"]["field_name"] = "rating_scores__whoqol_bref_psych"
        score_filter_fields["whoqol_bref_psych"]["short_name"] = "WHOQOL Brief Psych Score"
        score_filter_fields["whoqol_bref_psych"]["type"] = "ratio"
 
        score_filter_fields["whoqol_bref_social"] = {}
        score_filter_fields["whoqol_bref_social"]["field_name"] = "rating_scores__whoqol_bref_social"
        score_filter_fields["whoqol_bref_social"]["short_name"] = "WHOQOL Brief Social Score"
        score_filter_fields["whoqol_bref_social"]["type"] = "ratio"
        
        score_filter_fields["whoqol_bref_envir"] = {}
        score_filter_fields["whoqol_bref_envir"]["field_name"] = "rating_scores__whoqol_bref_envir"
        score_filter_fields["whoqol_bref_envir"]["short_name"] = "WHOQOL Brief Environment Score"
        score_filter_fields["whoqol_bref_envir"]["type"] = "ratio"

        score_filter_fields["whoqol_old_sense"] = {}
        score_filter_fields["whoqol_old_sense"]["field_name"] = "rating_scores__whoqol_old_sense"
        score_filter_fields["whoqol_old_sense"]["short_name"] = "WHOQOL Old Sense Score"
        score_filter_fields["whoqol_old_sense"]["type"] = "ratio"

        score_filter_fields["whoqol_old_aut"] = {}
        score_filter_fields["whoqol_old_aut"]["field_name"] = "rating_scores__whoqol_old_aut"
        score_filter_fields["whoqol_old_aut"]["short_name"] = "WHOQOL Old Aut Score"
        score_filter_fields["whoqol_old_aut"]["type"] = "ratio"

        score_filter_fields["tech_confidence_score"] = {}
        score_filter_fields["tech_confidence_score"]["field_name"] = "rating_scores__tech_confidence_score"
        score_filter_fields["tech_confidence_score"]["short_name"] = "Tech Confidence Score"
        score_filter_fields["tech_confidence_score"]["type"] = "ratio"

        score_filter_fields["tech_attitude_score"] = {}
        score_filter_fields["tech_attitude_score"]["field_name"] = "rating_scores__tech_attitude_score"
        score_filter_fields["tech_attitude_score"]["short_name"] = "Tech Attitude Score"
        score_filter_fields["tech_attitude_score"]["type"] = "ratio"

        for k,v in score_filter_fields.items():
            v["heirarchy"] = ("Tests","Survey Scores")
            v["model"] = "ParticipantScaleRatingScores"
            v["function_handle"] = "ParticipantScaleRatings.objects.values_list('contact_instance__participant__pid', flat = True)"
        
        filter_fields = dict(survey_filter_fields.items() + score_filter_fields.items())
        
        return filter_fields

# HOME INVENTORY
class ResidenceEntrance(models.Model):
    letter_id = models.CharField(max_length = 1, default = "A")
    location = models.ForeignKey(AnswerOption, related_name = 'entrance_location') # front, back, side, garage, other
    floor = models.ForeignKey(AnswerOption, related_name = 'floor') # basement, 1st, 2nd, Other
    n_steps = models.IntegerField()
    t_stairs = models.ForeignKey(AnswerOption, related_name = 't_stairs') # none, straight, landing, porch/deck, other
    w_door = models.FloatField() # door width in inches
    h_thresh = models.FloatField() # threshhold height in inches
    wheelchair_access = models.BooleanField()
    use_freq = models.ForeignKey(AnswerOption, related_name = 'entrance_use_freq') # several times a day, daily, weekly, monthly, rarely, never
    comments = models.TextField(null = True)

    def __unicode__(self):
        return u'%s,%s,%s,%s,%s' % (self.floor.option,self.n_steps,self.t_stairs.option,self.w_door,self.h_thresh)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ResidenceRoom(models.Model):
    room_id = models.IntegerField()
    room_type = models.ForeignKey(AnswerOption, related_name = 'room_type') # bedroom, bathroom, etc
    location = models.ForeignKey(AnswerOption, related_name = 'room_location') # basement, 1st floor, 2nd floor, 3rd floor, attic, exterior, other
    entrances = models.ManyToManyField(ResidenceEntrance) # many be multiple
    floor_type = models.ForeignKey(AnswerOption, related_name = 'floor_type') # carpet, hardwood, etc.
    use_freq = models.ForeignKey(AnswerOption, related_name = 'room_use_freq') # several times a day, daily, weekly, monthly, rarely, never
    w_room = models.FloatField() # room width in inches
    l_room = models.FloatField() # room length in inches
    connections = models.ManyToManyField(AnswerOption) # power, cable, phone
    comments = models.TextField(null = True)

    def __unicode__(self):
        return u'%s,%s,%s' % (self.room_type.option,self.w_room,self.l_room)

    @classmethod
    def _get_filter_fields(cls):
        return {}

# Maintain directionality from survey
class ResidenceInteriorDoor(models.Model):
    room1 = models.ForeignKey(ResidenceRoom, related_name="doorroom1", null = True)
    room2 = models.ForeignKey(ResidenceRoom, related_name="doorroom2", null = True)
    w_door = models.FloatField() # door width in inches
    h_thresh = models.FloatField() # threshhold height in inches
    comments = models.TextField(null = True)

    def __unicode__(self):
        if not self.room1:
            room1 = None
        else:
            room1 = self.room1.room_id
        if not self.room2:
            room2 = None
        else:
            room2 = self.room2.room_id
        return u'%s,%s,%s' % (room1,room2,self.w_door)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ResidenceInteriorStair(models.Model):
    room1 = models.ForeignKey(ResidenceRoom, related_name="stairroom1")
    room2 = models.ForeignKey(ResidenceRoom, related_name="stairroom2")
    location_description = models.CharField(max_length = 100) # basement to 1st floor, 1st floor to 2nd floor, etc.
    n_steps = models.IntegerField()
    t_stairs = models.ForeignKey(AnswerOption) # none, straight, landing, spiral, folding, ladder, other
    narrowest_width = models.FloatField() # narrowest width of stairway in inches
    comments = models.TextField(null = True)

    def __unicode__(self):
        if not self.room1:
            room1 = None
        else:
            room1 = self.room1.room_id
        if not self.room2:
            room2 = None
        else:
            room2 = self.room2.room_id
        return u'%s,%s,%s' % (room1,room2,self.n_steps)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class ResidencePhotograph(models.Model):
    room = models.ForeignKey(ResidenceRoom)
    photo_path = models.TextField(max_length = 100) # location on disk
    description = models.TextField(null = True)

    @classmethod
    def _get_filter_fields(cls):
        return {}

class HomeInventory(models.Model):
    contact_instance = models.ManyToManyField(ParticipantContactInstance) # because multiple participants can be in same residence

    # From home inventory
    nstories = models.IntegerField()
    home_features = models.ManyToManyField(AnswerOption, related_name="home_features") # attic, basement, crawlspace, slab foundation, swimming pool (above/below), hot tub
    home_cooling = models.ManyToManyField(AnswerOption, related_name="home_cooling") # central, portable, window, or no AC (or other)
    home_heating = models.ManyToManyField(AnswerOption, related_name="home_heating") # central, fireplace, portable, radiator, other
    bed_ht = models.FloatField() # inches
    bed_size = models.ForeignKey(AnswerOption, related_name="bed_size") # twin, double, queen, king, cal king, other
    bed_adjustable = models.BooleanField()
    home_notes = models.TextField(null = True) # noteworthy anf strange features

    # Lists
    entrances = models.ManyToManyField(ResidenceEntrance) # these can be paired with any visit this way
    rooms = models.ManyToManyField(ResidenceRoom) # these can be paired with any visit this way
    interior_doors = models.ManyToManyField(ResidenceInteriorDoor) # these can be paired with any visit this way    
    interior_stairs = models.ManyToManyField(ResidenceInteriorStair) # these can be paired with any visit this way
    photographs = models.ManyToManyField(ResidencePhotograph)

    @classmethod
    def get_field_lists(cls):
        entrance_fields = ResidenceEntrance._meta.get_all_field_names()
        entrance_fields.remove('id')
        entrance_fields.remove('residenceroom') # reverse link
        entrance_fields.remove('homeinventory')
        
        room_fields = ResidenceRoom._meta.get_all_field_names()
        room_fields.remove('id')
        room_fields.remove('homeinventory')
        room_fields.remove('doorroom1') # reverse link
        room_fields.remove('doorroom2') # reverse link
        room_fields.remove('residencephotograph') # reverse link
        room_fields.remove('stairroom1') # reverse link
        room_fields.remove('stairroom2') # reverse link

        interior_door_fields = ResidenceInteriorDoor._meta.get_all_field_names()
        interior_door_fields.remove('id')
        interior_door_fields.remove('homeinventory')

        interior_stair_fields = ResidenceInteriorStair._meta.get_all_field_names()
        interior_stair_fields.remove('id')
        interior_stair_fields.remove('homeinventory')

        photograph_fields = ResidencePhotograph._meta.get_all_field_names()
        photograph_fields.remove('id')
        photograph_fields.remove('homeinventory')
        
        return (entrance_fields, room_fields, interior_door_fields, interior_stair_fields, photograph_fields)


    @classmethod
    def get_csv_label_list(cls):
        tmp_list = ['nstories','home_features','home_cooling','home_heating','bed_ht_in','bed_size','bed_adjustable','home_notes']
    
        nentrances = HomeInventory.objects.annotate(nentrances = Count('entrances')).aggregate(Max('nentrances'))['nentrances__max']
        nrooms = HomeInventory.objects.annotate(nrooms = Count('rooms')).aggregate(Max('nrooms'))['nrooms__max']
        ninterior_doors = HomeInventory.objects.annotate(ninterior_doors = Count('interior_doors')).aggregate(Max('ninterior_doors'))['ninterior_doors__max']
        ninterior_stairs = HomeInventory.objects.annotate(ninterior_stairs = Count('interior_stairs')).aggregate(Max('ninterior_stairs'))['ninterior_stairs__max']
        nphotographs = HomeInventory.objects.annotate(nphotographs = Count('photographs')).aggregate(Max('nphotographs'))['nphotographs__max']
        
        (entrance_fields, room_fields, interior_door_fields, interior_stair_fields, photograph_fields) = cls.get_field_lists()
        for i in range(nentrances):
            for f in entrance_fields:
                tmp_list.append('entrance %s %s' %(i+1, f))
        for i in range(nrooms):
            for f in room_fields:
                tmp_list.append('room %s %s' %(i+1, f))
        for i in range(ninterior_doors):
            for f in interior_door_fields:
                tmp_list.append('interior_door %s %s' %(i+1, f))
        for i in range(ninterior_stairs):
            for f in interior_stair_fields:
                tmp_list.append('interior_stair %s %s' %(i+1, f))
        for i in range(nphotographs):
            for f in photograph_fields:
                tmp_list.append('photograph %s %s' %(i+1, f))           
    
        return tmp_list
    
    def get_value_dict(self, names = False):
        tmp_dict = {}
        tmp_dict['nstories'] = self.nstories
        tmp_dict['home_features'] = getManyToManySingleValue(self.home_features)
        tmp_dict['home_cooling'] = getManyToManySingleValue(self.home_cooling)
        tmp_dict['home_heating'] = getManyToManySingleValue(self.home_heating)
        tmp_dict['bed_ht_in'] = self.bed_ht
        tmp_dict['bed_size'] = getOptionOrOrder(self.bed_size, names)
        tmp_dict['bed_adjustable'] = self.bed_adjustable
        tmp_dict['home_notes'] = self.home_notes
        
        # Break it out into separate fields
        def addToTempDict(tmp_dict, objects, print_string, value_list):
            for k, v in enumerate(objects):
                for n in v._meta.get_all_field_names():
                    if n in value_list:
                        c_attr = getattr(v, n)
                        value = None
                        if type(c_attr) == AnswerOption:
                            value = getOptionOrOrder(c_attr, names)
                        elif type(c_attr) in [BooleanType, IntType, FloatType, StringType, UnicodeType, NoneType]:
                            value = str(c_attr) # cast to string to handle unicode formatting
                        elif c_attr.__class__.__name__ == 'ResidenceRoom':
                            value = str(c_attr.room_id)
                        elif c_attr.__class__.__name__ == 'ManyRelatedManager':
                            if n == "connections": # room connections; AnswerOption
                                value = getManyToManySingleValue(c_attr)
                            elif n == "entrances": # room entrances; ResidenceEntrance
                                value =  ",".join(map(lambda s: str(s), c_attr.values_list('letter_id', flat=True)))
                        else:
                            #raise("Attempted to export unexpected type %s" %(type(c_attr)))
                            print "Attempted to export unexpected type %s" %(type(c_attr))
                            value = "ERROR"
                        if value:
                            tmp_dict[print_string %(k+1, n)] = value
            return tmp_dict
        
        (entrance_fields, room_fields, interior_door_fields, interior_stair_fields, photograph_fields) = self.get_field_lists()
        
        tmp_dict = addToTempDict(tmp_dict, self.entrances.all(), 'entrance %s %s', entrance_fields)
        tmp_dict = addToTempDict(tmp_dict, self.rooms.all(), 'room %s %s', room_fields)
        tmp_dict = addToTempDict(tmp_dict, self.interior_doors.all(), 'interior_door %s %s', interior_door_fields)
        tmp_dict = addToTempDict(tmp_dict, self.interior_stairs.all(), 'interior_stair %s %s', interior_stair_fields)
        tmp_dict = addToTempDict(tmp_dict, self.photographs.all(), 'photograph %s %s', photograph_fields)

        return tmp_dict

    class Meta:
        get_latest_by = 'contact_instance__date_of_test'

    @classmethod
    def _get_filter_fields(cls):
        filter_fields = {}
        filter_fields["nstories"] = {}
        filter_fields["nstories"]["field_name"] = "nstories"
        filter_fields["nstories"]["short_name"] = "# Stories"
        filter_fields["nstories"]["type"] = "ordinal"
        filter_fields["nstories"]["model"] = "HomeInventory"
        
        filter_fields["bed_ht"] = {}
        filter_fields["bed_ht"]["field_name"] = "bed_ht"
        filter_fields["bed_ht"]["short_name"] = "Bed Height (in)"
        filter_fields["bed_ht"]["type"] = "ratio"
        filter_fields["bed_ht"]["model"] = "HomeInventory"

        filter_fields["bed_size"] = {}
        filter_fields["bed_size"]["field_name"] = "bed_size"
        filter_fields["bed_size"]["short_name"] = "Bed Size"
        filter_fields["bed_size"]["type"] = "single_select"
        filter_fields["bed_size"]["model"] = "HomeInventory"
        filter_fields["bed_size"]["options"] = get_select_options("HomeInventory", "bed_size")

        filter_fields["bed_adjustable"] = {}
        filter_fields["bed_adjustable"]["field_name"] = "bed_adjustable"
        filter_fields["bed_adjustable"]["short_name"] = "Adjustable Bed?"
        filter_fields["bed_adjustable"]["type"] = "boolean"
        filter_fields["bed_adjustable"]["model"] = "HomeInventory"

        for k,v in filter_fields.items():
            v["heirarchy"] = ("Participant Induction","Home Inventory")
            v["model"] = "HomeInventory"
            v["function_handle"] = "HomeInventory.objects.values_list('contact_instance__participant__pid', flat = True)"

        return filter_fields

"""
Miscellaneous utility functions
"""
# Get the options dictionary for a particular table, field combination for use in the _get_filter_fields function
def get_select_options(table_name, field_name):
    options = {}
    for ao in AnswerOption.objects.filter(table = table_name, field = field_name).values('id','option','is_default','order'):
        if ao is None:
            options["None"] = {}
            options["None"]["id"] = None
            options["None"]["name"] = None
            options["None"]["is_default"] = False
            options["None"]["order"] = None
        else:
            options[ao['id']] = {}
            options[ao['id']]["id"] = ao['id']
            options[ao['id']]["name"] = ao['option']
            options[ao['id']]["is_default"] = ao['is_default']
            options[ao['id']]["order"] = ao['order']
        
    return options

# Return the mean of a set of values
def average(vals):
    if (len(vals) > 0):
        return sum(vals)/(len(vals) + 0.0)
    else:
        return 0.0

# For use in get_value_dict functions
def getOptionOrOrder(object_field, names):
    return str(object_field.option) if names else object_field.order

# join options in string
def getManyToManySingleValue(object_field):
    return ",".join(map(lambda s: str(s), object_field.values_list('option', flat=True)))
