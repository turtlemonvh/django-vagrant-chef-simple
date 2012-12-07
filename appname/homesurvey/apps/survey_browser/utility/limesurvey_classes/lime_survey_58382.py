"""
Administered Instruments

"""

import re
from survey_browser.models import Participant, ParticipantContactInstance, LimeToken
from survey_browser.models import AnswerOption, QuestionOption, SPMSQ_question, SPMSQ, IADL_option, IADL, TUGTrail, TUG

class lime_survey_58382:
    col_names = ["id",
            "submitdate",
            "lastpage",
            "startlanguage",
            "token",
            "58382X206X112591", # start SPMSQ; 1 = correct, 0 = incorrect
            "58382X206X112592",
            "58382X206X112593",
            "58382X206X112594",
            "58382X206X112595",
            "58382X206X112596",
            "58382X206X112597",
            "58382X206X112598",
            "58382X206X112599",
            "58382X206X1125910", # end SPQSQ
            "58382X206X11268", # calculated field
            "58382X206X11270", # total SPQSQ score
            "58382X207X11260", # start IADL
            "58382X207X11261",
            "58382X207X11262",
            "58382X207X11263",
            "58382X207X11264",
            "58382X207X11265",
            "58382X207X11266",
            "58382X207X11267", # end IADL
            "58382X207X11269", # calculated field
            "58382X207X11271", # total IADL score
            "58382X250X139301", # TUG time 1
            "58382X250X139302", # TUG time 2
            "58382X250X139303", # TUG time 3
            "58382X250X13931", # TUG avg
            "58382X250X13932", # mobility rating
            "58382X250X13933", # high/low risk
            "58382X250X13934", # ?
            "58382X250X13935"] # notes

    def __init__(self, table_row, verbose = False):
        self.table_row = table_row
        if table_row[1] is not None: # entries with no date are corrupted
            (self.participant, token_created, self.pci) = LimeToken.initializeRowImport(self.table_row[:5], 58382)
            
            # skip import if the token is already in the database
            if not token_created:
                return
            else:
                print "Adding token %s for survey %s" %(self.table_row[4], 58382)
                
            # Each function returns an array of objects that will be appended to the existing object array, which is passed into bulk_create at the end
            self.object_array = []
            self.save_SPMSQ(5,14)
            self.save_IADL(17,24)
            self.save_TUG(27,29)
            
            # Keeping track of created objects
            if verbose:
                print self.object_array

    def save_SPMSQ(self, start_index, end_index):
        # Get question data
        table = "SPMSQ_question"
        field = "question"
        options = ["What is the day, month, and year?",
                   "What is the day of the week?",
                   "Whis is the name of this place?",
                   "What is your phone number?",
                   "How old are you?",
                   "When were you born?",
                   "Who is the current president?",
                   "Who was the president before him?",
                   "What was your mother's maiden name?",
                   "Can you count backward from 20 by 3's?"]

        # Create objects and add to array
        tmp = SPMSQ.objects.create(contact_instance = self.pci)
        for i in range(10):
            answer = self.table_row[i + start_index]
            question = QuestionOption.objects.get(option = options[i], table = table, field = field)
            sq_tmp = SPMSQ_question.objects.get(question = question, correct = (answer == "1"))
            self.object_array.append(sq_tmp)
            tmp.questions.add(sq_tmp)
        # Recalculate value
        tmp.recalculate()
        tmp.save()
        self.object_array.append(tmp)

    def save_IADL(self, start_index, end_index):
        # Get question data
        ans_table = "IADL_option"
        ans_field = "option"
        options = [  "Operates telephone on own initiative; looks up and dials numbers, etc.",
                     "Dials a few well-known numbers",
                     "Answers telephone but does not dial",
                     "Does not use telephone at all.",
                     "Takes care of all shopping needs independently",
                     "Shops independently for small purchases",
                     "Needs to be accompanied on any shopping trip",
                     "Completely unable to shop",
                     "Plans, prepares and serves adequate meals independently",
                     "Prepares adequate meals if supplied with ingredients",
                     "Heats, serves and prepares meals or prepares meals but does not maintain adequate diet.",
                     "Needs to have meals prepared and served",
                     "Maintains house alone or with occasional assistance (e.g. 'heavy work domestic help')",
                     "Performs light daily tasks such as dishwashing, bed making",
                     "Performs light daily tasks but cannot maintain acceptable level of cleanliness.",
                     "Needs help with all home maintenance tasks.",
                     "Does not participate in any housekeeping tasks.",
                     "Does personal laundry completely",
                     "Launders small items; rinses stockings, etc.",
                     "All laundry must be done by others",
                     "Travels independently on public transportation or drives own car",
                     "Arranges own travel via taxi, but does not otherwise use public transportation",
                     "Travels on public transportation when accompanied by another",
                     "Travel limited to taxi or automobile with assistance of another",
                     "Does not travel at all.",
                     "Is responsible for taking medication in correct dosages at correct time",
                     "Takes responsibility if medication is prepared in advance in separate dosage",
                     "Is not capable of dispensing own medication",
                     "Manages financial matters independently (budgets, writes checks, pays rent, bills goes to back), collects and keeps track of income.",
                     "Manages day-to-day purchases, but needs help with banking, major purchases, etc.",
                     "Incapable of handling money."]
        
        q_table = "IADL_option"
        q_field = "question"
        q_options = [  "Ability to use telephone",
                       "Shopping",
                       "Food Preparation",
                       "Housekeeping",
                       "Laundry",
                       "Mode of Transportation",
                       "Responsibility for own medications",
                       "Ability to Handle Finances"]

        # Create objects and add to array
        tmp = IADL.objects.create(contact_instance = self.pci)
        for i, qo in enumerate(q_options):
            question = QuestionOption.objects.get(option = qo, table = q_table, field = q_field)
            try:
                tmp_opt = IADL_option.objects.get(question = question, order = int(self.table_row[i + start_index]))
                tmp.questions.add(tmp_opt)
                self.object_array.append(tmp_opt)
            except ValueError:
                print "ERROR: Token: ", self.table_row[4], " Question: ", question

        tmp.recalculate()
        tmp.save()
        self.object_array.append(tmp)

    def save_TUG(self, start_index, end_index):
        tmp = TUG.objects.create(contact_instance = self.pci)
        for i in range(3):
            try:
                tmp_trial = TUGTrail.objects.create(order = i, time = float(self.table_row[i + start_index])) # 27-29
            except:
                tmp_trial = TUGTrail.objects.create(order = i, time = None) # 27-29
            tmp.times.add(tmp_trial)
            self.object_array.append(tmp_trial)     
        
        tmp.recalculate()
        tmp.save()
        self.object_array.append(tmp)