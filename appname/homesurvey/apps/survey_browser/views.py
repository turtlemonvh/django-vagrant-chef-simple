from MySQLdb import OperationalError
import datetime
import time
import re
import pickle
import random
import string
import csv
from collections import defaultdict

from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from django.db import connection
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django import db
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from utility import import_limesurvey
from utility import option_load
from utility.export_functions import get_export_options, get_export_dict
from models import AnswerOption, QuestionOption, IADL_option, ScaleQuestionAndOption, AppSettings
from models import Participant, ParticipantContactInstance, SPMSQ_question, ParticipantFilter, ParticipantMetaFilter, ParticipantFilterOptions, ParticipantFilterGroup
from models import DATETIME_FORMAT, JSON_DTHANDLER
from apps.survey_browser.models import LimeToken
from apps.survey_browser.models import Participant, ParticipantScaleRatings, ParticipantMobilityHealth
from apps.survey_browser.models import IADL, TUG, SPMSQ, ParticipantInductionStatic, ParticipantInductionVolatile, HomeInventory

@login_required
def listTables(request):
    tables = connection.introspection.table_names()
    filtered_tables = [t for t in tables if "survey_browser" in t]
    seen_models = connection.introspection.installed_models(tables)
    print seen_models
    sm = [m.__doc__ for m in seen_models if "survey_browser" in m.__module__]
    return render_to_response('table_list.html',locals(),context_instance=RequestContext(request))

@login_required
def checkImport(request):
    try:
        surveys = import_limesurvey.get_active_surveys()
    except OperationalError:
        # can't connect to db
        return connectionError(request)
    survey_data = dict()
    for s in surveys:
        survey_data[s] = import_limesurvey.get_survey_cols(s)
    return render_to_response('import_limesurvey.html',locals(),context_instance=RequestContext(request))

def clear_database():
    while AnswerOption.objects.count() > 100:
        for obj in AnswerOption.objects.all()[:100]:
            obj.delete()
    AnswerOption.objects.all().delete()
    while QuestionOption.objects.count() > 100:
        for obj in QuestionOption.objects.all()[:100]:
            obj.delete()
    QuestionOption.objects.all().delete()
    while IADL_option.objects.count() > 100:
        for obj in IADL_option.objects.all()[:100]:
            obj.delete()
    IADL_option.objects.all().delete()
    while ScaleQuestionAndOption.objects.count() > 100:
        for obj in ScaleQuestionAndOption.objects.all()[:100]:
            obj.delete()
    ScaleQuestionAndOption.objects.all().delete()

# Either initializes or displays
@login_required
def initializeDatabase(request):
    """
    Result:
    469 Questions
    218 Answers
    31 IADL Options
    1455 ScaleQuestionAndOptions
    
    Run from cmd line:
    ~~~~~~~~~~~~~~~~~~
    from survey_browser.views import *
    from survey_browser.utility import option_load
    clear_database()
    option_load.create_options()
    
    """    
    test = "Database of possible answers now initialized."
    
    #clear_database() # uncomment to reimport
    if AnswerOption.objects.count() > 0:
        test = "Database of possible answers has already been initialized."
    else:
        print "Creating options"
        option_load.create_options()
        db.reset_queries() # these queries tend to overload the debug toolbar

    answers = AnswerOption.objects.order_by('table', 'field', 'option').values('table', 'field', 'option')
    questions = QuestionOption.objects.order_by('table', 'field', 'option').values('table', 'field', 'option')
    IADL_options = IADL_option.objects.select_related("option__option").order_by('option', 'order', 'score').values('option__option', 'order', 'score')
    SPMSQ_questions = SPMSQ_question.objects.select_related("question__option").order_by('question', 'correct').values('question__option', 'correct')
    sqos = ScaleQuestionAndOption.objects.select_related('question__option', 'option__option').order_by('question', 'order').values('question__option', 'option__option', 'order')
    
    answer_count = len(answers)
    question_count = len(questions)
    IADL_option_count = len(IADL_options)
    SPMSQ_question_count = len(SPMSQ_questions)
    sqo_count = len(sqos)
    
    print "Number questions: ", answer_count
    print "Number answers: ", question_count
    
    return render_to_response('setup_database.html',locals(),context_instance=RequestContext(request))

@login_required
def filterParticipants(request):    
    return render_to_response('filter.html',locals(),context_instance=RequestContext(request))

@login_required
def getFilterOptions(request):
    if request.GET.get("formatted_for_list") == "true":
        t_json = simplejson.dumps(ParticipantFilterOptions.getAllOptionsStructured())
    else:
        t_json = simplejson.dumps(ParticipantFilterOptions.getAllOptions())
    return HttpResponse(t_json, content_type = 'application/json; charset=utf8')

@login_required
def getFilterDependencies(request):
    filter_id = int(request.GET.get("filter-id"))
    filter_type = request.GET.get("filter-type")
    
    if filter_type == "meta":
        ids = ParticipantMetaFilter.objects.values_list("id", flat = True).filter(metafilters__id = filter_id)
    elif filter_type == "value":
        ids = ParticipantMetaFilter.objects.values_list("id", flat = True).filter(filters__id = filter_id)
    else:
        raise Http404()
    
    while True:
        nids = []
        nids += list(ids)
        pre_len = len(nids)
        for tid in list(ids):
            nids += list(ParticipantMetaFilter.objects.values_list("id", flat = True).filter(metafilters__id = tid))
        nids = list(set(nids))
        ids = nids
        if pre_len == len(nids):
            break
    
    return HttpResponse(simplejson.dumps(nids), content_type = 'application/json; charset=utf8')

@login_required
def visualizeMeta(request):
    filter_id = request.GET.get("filter-id",None)
    if filter_id:
        f = ParticipantMetaFilter.objects.get(id = filter_id)
    else:
        raise Http404()
    
    return HttpResponse(getHTMLRepresentation(f), content_type = 'html')

def getHTMLRepresentation(pfilter):
    html = "<span class='name'>%s:%s</span><span class='description'>%s</span>" %(pfilter.name, pfilter.getAction(), pfilter.description)
    
    if pfilter.__class__.__name__ == "ParticipantMetaFilter":
        html = "<div class='meta'>" + html
        for vf in pfilter.filters.all():
            html += getHTMLRepresentation(vf)
        for mf in pfilter.metafilters.all():
            html += getHTMLRepresentation(mf)
    else:
        html = "<div class='value'>" + html
        
    html += "</div>"
    return html

@login_required
def getValueFilterForm(request):
    filtertype_id = request.GET.get("filtertype-id",None)
    filter_id = request.GET.get("filter-id",None)
    if filter_id:
        pf = ParticipantFilter.objects.filter(id = filter_id).values()[0]
        filtertype_id = pf['filter_field']
    if filtertype_id is None:
        raise Http404()
    
    # Collect data needed to display html options
    option_sub_dict = ParticipantFilterOptions.objects.get(filter_field = filtertype_id).getOptionDict()
    
    # Add fields
    option_sub_dict["filter_field"] = filtertype_id
    if filter_id:
        option_sub_dict["filter"] = pf
        if 'options' in option_sub_dict:
            for k, o in option_sub_dict['options'].iteritems():
                if str(k) in pf['argument'].split(","):
                    o["is_selected"] = True
        
    
    html_resp = render_to_response('new_value_filter_form.html',locals(),context_instance=RequestContext(request))
    option_sub_dict['html'] = html_resp.content
    
    return HttpResponse(simplejson.dumps(option_sub_dict), content_type = 'application/json; charset=utf8')

@login_required
def setFilterGroups(request):
    return render_to_response('set_filter_groups.html',locals(),context_instance=RequestContext(request))

@login_required
def createFilters(request):
    return render_to_response('create_filters.html',locals(),context_instance=RequestContext(request))

@login_required
def createMetaFilters(request):
    return render_to_response('create_meta_filters.html',locals(),context_instance=RequestContext(request))

@login_required
def browseFilters(request):
    export_options = get_export_options()
    print export_options
    return render_to_response('browse_filters.html',locals(),context_instance=RequestContext(request))

# Modify to pass in filter
@login_required
def participantsMatchingFilter(request):
    # Either filter or load all
    if request.GET.get("filter_id"):
        filter_id = request.GET.get("filter_id")
        pf = ParticipantFilter.objects.get(id = filter_id)
        pids = pf.execute()
    elif request.GET.get("meta_filter_id"):
        filter_id = request.GET.get("meta_filter_id")
        pf = ParticipantMetaFilter.objects.get(id = filter_id)
        pids = pf.execute()
    else:
        pids = list(Participant.objects.values_list('pid', flat=True))

    # Return json or html
    if request.GET.get("format") == 'json':
        return HttpResponse(simplejson.dumps(pids), content_type = 'application/json; charset=utf8')
    else:
        participants = Participant.objects.filter(pid__in = list(pids)).values()

        available_data_dict = {}
        for k, v in get_export_options().iteritems():
            if v['class'].__name__ == "ParticipantInductionStatic":
                tmp_pids = v['class'].objects.values_list('participant__pid', flat=True)
            else:
                tmp_pids = v['class'].objects.order_by('contact_instance__participant').distinct('contact_instance__participant').values_list('contact_instance__participant__pid', flat=True)
            available_data_dict[v['formatted_name']] = tmp_pids
        
        for p in participants:
            #p["tokens"] = LimeToken.objects.filter(participant__id = p['id']).values_list('token', flat=True)
            p["contact_dates"] = ParticipantContactInstance.objects.filter(participant__id = p['id']).order_by('date_of_test').values_list('date_of_test', flat=True)
            # return available data
            p["available_data"] = []
            for k,v in available_data_dict.iteritems():
                if p["pid"] in v:
                    p["available_data"].append(k)
            p["available_data"] = ", ".join(p["available_data"])
        return render_to_response('participant_table.html',locals(),context_instance=RequestContext(request))

# Connect to database and re-import
@login_required
def checkUpdateDatabase(request):
    try:
        last_update = import_limesurvey.get_database_update_dict()
        missing_token_rows = import_limesurvey.get_missing_token_rows()
        return render_to_response('update_database.html',locals(),context_instance=RequestContext(request))
    except OperationalError:
        # can't connect to db
        return connectionError(request)

def connectionError(request):
    return render_to_response('database_connect_error.html',locals(),context_instance=RequestContext(request))

# Add missing data as needed
# Update cache object along the way to provide message back to front end 
@login_required
def updateDatabase(request):
    #force_load = bool(request.GET.get("force_load", None))
    progress_cache_id = request.GET.get("X-Progress-ID")
            
    selected_surveys = defaultdict(list)
    for v in [(re.sub("\[.*\]","",k), v) for k,v in request.GET.items() if "lime_survey" in k]:
        selected_surveys[v[0]].append(v[1])
    print selected_surveys.items()

    try:
        """
        time.sleep(5) # test progress updating by adding delay
        
        # check to see which need updating and sync accordingly
        last_update = import_limesurvey.import_all_surveys(force_load = force_load)
        """
        
        last_update = import_limesurvey.import_selected_surveys(selected_surveys)
        return render_to_response('active_survey_table.html',locals(),context_instance=RequestContext(request))
    except OperationalError:
        # can't connect to db
        return connectionError(request)

@login_required
def checkUpdateProgress(request):
    progress_cache_id = request.GET.get("X-Progress-ID")
    cache_result = "TEST CACHE RESULT; CURRENT TIME: %s" %(datetime.datetime.now().strftime("%I:%M:%S %p"))
    return HttpResponse(cache_result, content_type='text')

@login_required
def manageFilterGroups(request):
    groups = ParticipantFilterGroup.objects.filter(user = request.user)
    return render_to_response('manage_groups.html',locals(),context_instance=RequestContext(request))

@login_required
def visualizeFilterGroup(request):
    group_id = request.GET.get("group-id")
    try:
        group = ParticipantFilterGroup.objects.get(id=group_id)
        filters = list(ParticipantFilter.objects.filter(groups = group).values()) + list(ParticipantMetaFilter.objects.filter(groups = group).values())
        for f in filters:
            if 'argument' in f:
                f['type'] = 'value'
            else:
                f['type'] = 'meta'
        
    except ObjectDoesNotExist:
        raise Http404()
    
    return render_to_response('group_table.html',locals(),context_instance=RequestContext(request))

@login_required
# convenience function for bulk action
def addFiltersToGroup(request):
    filters = request.POST.get("filters") # {'type': 'edit', 'id': 2}
    group_id = request.POST.get("group-id")
    
    try:
        tgt_group = ParticipantFilterGroup.objects.get(id=int(group_id), user = request.user)
        filters = simplejson.loads(filters)
        for f in filters:
            cfilter_id = int(f["filter-id"])
            if f["filter-type"] == u'value':
                vf = ParticipantFilter.objects.get(id = cfilter_id)
                vf.groups.add(tgt_group)
                vf.save()
                print vf
            elif f["filter-type"] == u'meta':
                mf = ParticipantMetaFilter.objects.get(id = cfilter_id)
                mf.groups.add(tgt_group)
                mf.save()
        return redirect("/browser/filtergroup/filtertable/?group-id=%s" %(group_id))
    except ObjectDoesNotExist:
        raise Http404()
    except ValueError:
        raise Http404()

@login_required
# convenience function for bulk action
def removeFiltersFromGroup(request):
    filters = request.POST.get("filters") # {'type': 'edit', 'id': 2}
    group_id = request.POST.get("group-id")
    
    try:
        tgt_group = ParticipantFilterGroup.objects.get(id=int(group_id), user = request.user)
        filters = simplejson.loads(filters)
        for f in filters:
            cfilter_id = int(f["filter-id"])
            if f["filter-type"] == u'value':
                vf = ParticipantFilter.objects.get(id = cfilter_id)
                vf.groups.remove(tgt_group)
                vf.save()
                print vf
            elif f["filter-type"] == u'meta':
                mf = ParticipantMetaFilter.objects.get(id = cfilter_id)
                mf.groups.remove(tgt_group)
                mf.save()
        return redirect("/browser/filtergroup/filtertable/?group-id=%s" %(group_id))
    except ObjectDoesNotExist:
        raise Http404()
    except ValueError:
        raise Http404()

# export data given list of pids and list of export sections
@login_required
def downloadCSV(request):
    filter_id = request.GET.get("filter-id") # int
    filter_type = request.GET.get("filter-type") # string; meta or value
    export_sections = request.GET.get("export_sections") # list of ints
    
    if not (filter_id and filter_type):
        pids = Participant.objects.values_list('pid', flat=True)
    else:
        filter_id = int(filter_id)
        if filter_type == "meta":
            pids = ParticipantMetaFilter.objects.get(id = filter_id).execute()
        else:
            pids = ParticipantFilter.objects.get(id = filter_id).execute()
    if export_sections:
        (ordered_header, export_dict) =  get_export_dict(pids, True, simplejson.loads(export_sections))
    else:
        (ordered_header, export_dict) =  get_export_dict(pids, True)
    
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participant_data.csv"'
    
    export_writer = csv.DictWriter(response, ordered_header, restval = None)
    export_writer.writeheader()
    export_writer.writerows(export_dict)
    
    return response
   
    
    
