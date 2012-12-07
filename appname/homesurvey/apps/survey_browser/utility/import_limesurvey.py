"""
Get into database
http://www.kitebird.com/articles/pydbapi.html

Fill up question, answer data

Do some basic displaying of information

- Use decorator

"""
import MySQLdb
import re
import sys
import traceback
import datetime
import pickle

from django.core.exceptions import ObjectDoesNotExist

from survey_browser.models import Participant, LimeToken, AppSettings, DATETIME_FORMAT
from limesurvey_classes import lime_survey_58382, lime_survey_49672, lime_survey_65387

SKIPPED_SURVEYS = [61262]

def connect_dump():
    # Call functions with cursor to get data
    surveys = get_active_surveys()
    answers = get_answers()
    questions = get_questions()
    
    #print surveys
    #print answers
    #print questions
    
    print "Survey 1 id = %s" % (surveys[0][0])
    
    return surveys

# Decorator function
def with_connection(func):
    def _exec(*args, **argd):
        conn = MySQLdb.connect (host = "localhost",
                               user = "root",
                               passwd = "",
                               db = "limesurveytb")
        cursor = conn.cursor ()
        try:
            tmp = func(cursor, *args, **argd)
        except Exception, err:
            traceback.print_exc()
        finally:
            cursor.close ()
            conn.close ()
            if vars().has_key('tmp'):
                return tmp
            else:
                return None
    return _exec

@with_connection
def get_last_update_time(cursor):
    # return dictionary of name: date for surveys and tokens
    survey_time_dict = dict()
    surveys = get_active_surveys()
    for s in surveys:
        #query = "select submitdate from %s where submitdate is not null order by submitdate limit 1;" %(s)
        query = "select max(submitdate) from %s where submitdate is not null;" %(s)
        cursor.execute (query)
        survey_time_dict[s] = cursor.fetchone ()[0]
    return survey_time_dict

@with_connection
def get_missing_token_rows(cursor):
    # return dictionary of pid, date (from LimeSurvey) for tokens not in 
    missing_tokens = dict()
    surveys = get_active_surveys()
    tokens = LimeToken.objects.all()
    for s in surveys:
        query = "select submitdate, token from %s where submitdate is not null;" %(s)
        cursor.execute (query)
        db_tokens = tokens.filter(survey_id = int(re.sub("[^0-9]","",s))).values_list('token', flat=True) # saved tokens
        ls_tokens = cursor.fetchall() # LimeSurvey tokens
        missing_tokens[s] = [{"date": t[0], "token": t[1]} for t in ls_tokens if t[1] not in db_tokens]
    return missing_tokens

@with_connection
def get_version(cursor):
    cursor.execute ("SELECT VERSION()")
    row = cursor.fetchone ()
    print "server version:", row[0]
    return row[0]

@with_connection
def get_tables(cursor):
    cursor.execute ("SHOW TABLES")
    tables = []
    for i in range(0,cursor.rowcount):
        row = cursor.fetchone ()
        if row == None:
            break
        tables.append(row[0])
    return tables

@with_connection
def get_active_surveys(cursor):
    cursor.execute("SELECT sid, active FROM lime_surveys")
    
    print "Number of rows returned: %d" % cursor.rowcount
    surveys = list()
    for i in range(0,cursor.rowcount):
        row = cursor.fetchone ()
        if int(row[0]) in SKIPPED_SURVEYS:
            continue
        if row == None:
            continue
        if row[1] == "Y":
            sname = "lime_survey_" + str(row[0])
            surveys.append(sname)
    return surveys

@with_connection
def get_answers(cursor):
    cursor.execute("SELECT qid, code, answer, sortorder FROM lime_answers")
    
    #print "Number of rows returned: %d" % cursor.rowcount
    answers = dict()
    for i in range(0,cursor.rowcount):
        row = cursor.fetchone ()
        if row == None:
            break
        if row[0] not in answers:
            answers[row[0]] = []
        #answers[row[0]].append([row[0], row[1], row[2]])
        answers[row[0]].append(row)
    return answers

@with_connection
def get_questions(cursor):
    cursor.execute("SELECT qid, sid, gid, question, question_order FROM lime_questions")
    
    #print "Number of rows returned: %d" % cursor.rowcount
    questions = dict()
    for i in range(0,cursor.rowcount):
        row = cursor.fetchone ()
        if row == None:
            break
        # Get rid of added html / js
        #question = row[3].split('<')[0].split('{')[0]
        question = row[3]
        questions[row[0]] = [question]
    return questions

# Build this using sidXgidXqid model for finding
@with_connection
def get_responses(cursor):
    pass

# get ordered list of active surveys, linking each item to a question, and each question to its options (count)
@with_connection
def get_survey_cols(cursor, result_table_name):
    cursor.execute("DESCRIBE " + result_table_name)
    print result_table_name, " has ", cursor.rowcount, " cols"
    
    col_names = []
    bad_cols = []
    q_s = get_questions()
    a_s = get_answers()
    for i in range(0,cursor.rowcount):
        col = cursor.fetchone ()
        if col == None:
            break
        tmp = col[0].split('X') # group, question
        if len(tmp) > 2: # correct format for identifier
            group = tmp[1]
            re_question = re.search("(\d{1,5})", str(tmp[2]))
            question = re_question.group(0)
            
            if question == str(tmp[2]):
                c_question = q_s[int(question)][0]
                if int(question) in a_s:
                    col_names.append([col[0],group,question,c_question,a_s[int(question)]])
                else:
                    col_names.append([col[0],group,question,c_question])
            else:
                col_names.append([col[0],group,question])
        else:
            bad_cols.append(col)
    
    print "BEFORE: ", cursor.rowcount, ", AFTER: ", len(col_names), ", MISSING: ", cursor.rowcount - len(col_names)
    print bad_cols
        # set questions
        # {long_id, group_id, question_id, question}
        
    return col_names

"""
Functions:


"""
def get_database_update_dict(add_updated_field = False):
    # Get times the live active surveys were last updated with information
    last_update = get_last_update_time()
   
    # Get the last time the research database was synched to the live data
    try:
        last_fetch = AppSettings.objects.get(setting_key = "last_fetch_time") # store json string form of current date
    except ObjectDoesNotExist:
        last_fetch = AppSettings.objects.create(setting_key = "last_fetch_time", setting = datetime.datetime(2012, 1, 1, 1, 1, 1, 1).strftime(DATETIME_FORMAT))
    
    # Format data about last update times for surveys
    for k, v in last_update.items():
        last_update[k] = {}
        last_update[k]["time"] = v.strftime(DATETIME_FORMAT)
        last_update[k]["update_needed"] = bool(v > datetime.datetime.strptime(last_fetch.setting, DATETIME_FORMAT))
        if add_updated_field:
            last_update[k]["updated"] = False
    
    return last_update

@with_connection
def import_all_surveys(cursor, force_load = False):
    last_update = get_database_update_dict(add_updated_field = True)
    
    run_update = False
    for v in last_update.itervalues():
        if v['update_needed']:
            run_update = True
    
    if run_update or force_load:
        # Set last update time to now
        last_fetch = AppSettings.objects.get(setting_key = "last_fetch_time")
        last_fetch.setting = datetime.datetime.now().strftime(DATETIME_FORMAT)
        last_fetch.save()

        # Update out of date fields
        if last_update["lime_survey_58382"]["update_needed"] or force_load:
            import_lime_survey_58382()
            last_update["lime_survey_98517"]["updated"] = True
        if last_update["lime_survey_49672"]["update_needed"] or force_load:
            import_lime_survey_49672()
            last_update["lime_survey_98517"]["updated"] = True
        if last_update["lime_survey_65387"]["update_needed"] or force_load:
            import_lime_survey_65387()
            last_update["lime_survey_98517"]["updated"] = True
        if last_update["lime_survey_98517"]["update_needed"] or force_load:
            import_lime_survey_98517()
            last_update["lime_survey_98517"]["updated"] = True
    
    return last_update

@with_connection
def import_selected_surveys(cursor, selected_surveys):
    last_update = get_database_update_dict(add_updated_field = True)

    # Update variable storing last update time
    last_fetch = AppSettings.objects.get(setting_key = "last_fetch_time")
    last_fetch.setting = datetime.datetime.now().strftime(DATETIME_FORMAT)
    last_fetch.save()
    
    for k,v in selected_surveys.items():
        last_update[k]["updated"] = True
        for token in v:
            cursor.execute("SELECT * FROM %s where token = '%s'" %(k,token))
            row = cursor.fetchone ()
            if row == None:
                continue
            if k == "lime_survey_58382":
                lime_survey_58382(row, False)
                #print "Importing using lime_survey_58382"
            elif k == "lime_survey_49672":
                lime_survey_49672(row, False)
                #print "Importing using lime_survey_49672"
            elif k == "lime_survey_65387":
                lime_survey_65387(row, False, table_id = 65387)
                #print "Importing using lime_survey_65387"
            elif k == "lime_survey_98517":
                lime_survey_65387(row, False, table_id = 98517)
                #print "Importing using lime_survey_98517"
    return last_update

@with_connection
def import_lime_survey_58382(cursor, fetchn = None, verbose = False):
    if not fetchn:
        cursor.execute("SELECT * FROM lime_survey_58382")
    else:
        cursor.execute("SELECT * FROM lime_survey_58382 LIMIT %s" %(fetchn))
    
    print "Number of rows returned: %d" % cursor.rowcount
    for i in range(0,cursor.rowcount):
        row = cursor.fetchone ()
        if row == None:
            break
        lime_survey_58382(row, verbose)

@with_connection
def import_lime_survey_49672(cursor, fetchn = None, verbose = False):
    if not fetchn:
        cursor.execute("SELECT * FROM lime_survey_49672")
    else:
        cursor.execute("SELECT * FROM lime_survey_49672 LIMIT %s" %(fetchn))
    
    print "Number of rows returned: %d" % cursor.rowcount
    for i in range(0,cursor.rowcount):
        row = cursor.fetchone ()
        if row == None:
            break
        lime_survey_49672(row, verbose)

@with_connection
def import_lime_survey_65387(cursor, fetchn = None, verbose = False):
    if not fetchn:
        cursor.execute("SELECT * FROM lime_survey_65387")
    else:
        cursor.execute("SELECT * FROM lime_survey_65387 LIMIT %s" %(fetchn))
    
    print "Number of rows returned: %d" % cursor.rowcount
    for i in range(0,cursor.rowcount):
        row = cursor.fetchone ()
        if row == None:
            break
        lime_survey_65387(row, verbose, table_id = 65387)

@with_connection
def import_lime_survey_98517(cursor, fetchn = None, verbose = False):
    if not fetchn:
        cursor.execute("SELECT * FROM lime_survey_98517")
    else:
        cursor.execute("SELECT * FROM lime_survey_98517 LIMIT %s" %(fetchn))
    
    print "Number of rows returned: %d" % cursor.rowcount
    for i in range(0,cursor.rowcount):
        row = cursor.fetchone ()
        if row == None:
            break
        lime_survey_65387(row, verbose, table_id = 98517) # use class for identical structure to handle import

