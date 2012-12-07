"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.test import TestCase

from models import *
from utility.utility_functions import get_filter_option_dict

class SimpleTest(TestCase):
    def setUp(self):
        from utility import option_load
        option_load.create_options()
    
    def tearDown(self):
        pass
    
    def test_basic(self):
        self.p1 = Participant.objects.create(pid = 1)
        self.assertEqual(self.p1.id, 1)
        
        self.p1c1 = ParticipantContactInstance.objects.create(participant = self.p1, date_of_test = datetime.datetime.today())

        self.p1spmsq = SPMSQ.objects.create(contact_instance = self.p1c1)
        
        spmsq_qs = QuestionOption.objects.filter(table="SPMSQ_question", field = "question")
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 1), correct = True))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 2), correct = True))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 3), correct = True))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 4), correct = True))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 5), correct = False))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 6), correct = True))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 7), correct = True))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 8), correct = False))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 9), correct = True))
        self.p1spmsq.questions.add(SPMSQ_question.objects.create(question = spmsq_qs.get(order = 10), correct = True))
        
        self.assertEqual(self.p1spmsq.nerrors, 0)
        self.p1spmsq.recalculate()
        self.assertEqual(self.p1spmsq.nerrors, 2)
        
        # Add answers to IADL
        self.iadl_q_a = QuestionOption.objects.get(table = "IADL_option", field = "question", option = "Ability to use telephone")
        self.iadl_q_b = QuestionOption.objects.get(table = "IADL_option", field = "question", option = "Shopping")
        self.iadl_q_c = QuestionOption.objects.get(table = "IADL_option", field = "question", option = "Food Preparation")
        self.iadl_q_d = QuestionOption.objects.get(table = "IADL_option", field = "question", option = "Housekeeping")
        self.iadl_q_e = QuestionOption.objects.get(table = "IADL_option", field = "question", option = "Laundry")
        self.iadl_q_f = QuestionOption.objects.get(table = "IADL_option", field = "question", option = "Mode of Transportation")
        self.iadl_q_g = QuestionOption.objects.get(table = "IADL_option", field = "question", option = "Responsibility for own medications")
        self.iadl_q_h = QuestionOption.objects.get(table = "IADL_option", field = "question", option = "Ability to Handle Finances")

        self.iadl_a1 = AnswerOption.objects.get(table = "IADL_option",option = "Operates telephone on own initiative; looks up and dials numbers, etc.")
        self.iadl_a2 = AnswerOption.objects.get(table = "IADL_option",option = "Dials a few well-known numbers")
        self.iadl_a3 = AnswerOption.objects.get(table = "IADL_option",option = "Answers telephone but does not dial")
        self.iadl_a4 = AnswerOption.objects.get(table = "IADL_option",option = "Does not use telephone at all.")
        self.iadl_b1 = AnswerOption.objects.get(table = "IADL_option",option = "Takes care of all shopping needs independently")
        self.iadl_b2 = AnswerOption.objects.get(table = "IADL_option",option = "Shops independently for small purchases")
        self.iadl_b3 = AnswerOption.objects.get(table = "IADL_option",option = "Needs to be accompanied on any shopping trip")
        self.iadl_b4 = AnswerOption.objects.get(table = "IADL_option",option = "Completely unable to shop")
        self.iadl_c1 = AnswerOption.objects.get(table = "IADL_option",option = "Plans, prepares and serves adequate meals independently")
        self.iadl_c2 = AnswerOption.objects.get(table = "IADL_option",option = "Prepares adequate meals if supplied with ingredients")
        self.iadl_c3 = AnswerOption.objects.get(table = "IADL_option",option = "Heats, serves and prepares meals or prepares meals but does not maintain adequate diet.")
        self.iadl_c4 = AnswerOption.objects.get(table = "IADL_option",option = "Needs to have meals prepared and served")
        self.iadl_d1 = AnswerOption.objects.get(table = "IADL_option",option = "Maintains house alone or with occasional assistance (e.g. 'heavy work domestic help')")
        self.iadl_d2 = AnswerOption.objects.get(table = "IADL_option",option = "Performs light daily tasks such as dishwashing, bed making")
        self.iadl_d3 = AnswerOption.objects.get(table = "IADL_option",option = "Performs light daily tasks but cannot maintain acceptable level of cleanliness.")
        self.iadl_d4 = AnswerOption.objects.get(table = "IADL_option",option = "Needs help with all home maintenance tasks.")
        self.iadl_d5 = AnswerOption.objects.get(table = "IADL_option",option = "Does not participate in any housekeeping tasks.")
        self.iadl_e1 = AnswerOption.objects.get(table = "IADL_option",option = "Does personal laundry completely")
        self.iadl_e2 = AnswerOption.objects.get(table = "IADL_option",option = "Launders small items; rinses stockings, etc.")
        self.iadl_e3 = AnswerOption.objects.get(table = "IADL_option",option = "All laundry must be done by others")
        self.iadl_f1 = AnswerOption.objects.get(table = "IADL_option",option = "Travels independently on public transportation or drives own car")
        self.iadl_f2 = AnswerOption.objects.get(table = "IADL_option",option = "Arranges own travel via taxi, but does not otherwise use public transportation")
        self.iadl_f3 = AnswerOption.objects.get(table = "IADL_option",option = "Travels on public transportation when accompanied by another")
        self.iadl_f4 = AnswerOption.objects.get(table = "IADL_option",option = "Travel limited to taxi or automobile with assistance of another")
        self.iadl_f5 = AnswerOption.objects.get(table = "IADL_option",option = "Does not travel at all.")
        self.iadl_g1 = AnswerOption.objects.get(table = "IADL_option",option = "Is responsible for taking medication in correct dosages at correct time")
        self.iadl_g2 = AnswerOption.objects.get(table = "IADL_option",option = "Takes responsibility if medication is prepared in advance in separate dosage")
        self.iadl_g3 = AnswerOption.objects.get(table = "IADL_option",option = "Is not capable of dispensing own medication")
        self.iadl_h1 = AnswerOption.objects.get(table = "IADL_option",option = "Manages financial matters independently (budgets, writes checks, pays rent, bills goes to back), collects and keeps track of income.")
        self.iadl_h2 = AnswerOption.objects.get(table = "IADL_option",option = "Manages day-to-day purchases, but needs help with banking, major purchases, etc.")
        self.iadl_h3 = AnswerOption.objects.get(table = "IADL_option",option = "Incapable of handling money.")
        
        self.iadl_p1_a = IADL_option.objects.get(option = self.iadl_a1, question = self.iadl_q_a)
        self.iadl_p1_b = IADL_option.objects.get(option = self.iadl_b2, question = self.iadl_q_b)
        self.iadl_p1_c = IADL_option.objects.get(option = self.iadl_c1, question = self.iadl_q_c)
        self.iadl_p1_d = IADL_option.objects.get(option = self.iadl_d1, question = self.iadl_q_d)
        self.iadl_p1_e = IADL_option.objects.get(option = self.iadl_e3, question = self.iadl_q_e)
        self.iadl_p1_f = IADL_option.objects.get(option = self.iadl_f1, question = self.iadl_q_f)
        self.iadl_p1_g = IADL_option.objects.get(option = self.iadl_g2, question = self.iadl_q_g)
        self.iadl_p1_h = IADL_option.objects.get(option = self.iadl_h1, question = self.iadl_q_h)

        self.p1iad1 = IADL.objects.create(contact_instance = self.p1c1)
        self.p1iad1.questions.add(self.iadl_p1_a)
        self.p1iad1.questions.add(self.iadl_p1_b)
        self.p1iad1.questions.add(self.iadl_p1_c)
        self.p1iad1.questions.add(self.iadl_p1_d)
        self.p1iad1.questions.add(self.iadl_p1_e)
        self.p1iad1.questions.add(self.iadl_p1_f)
        self.p1iad1.questions.add(self.iadl_p1_g)
        self.p1iad1.questions.add(self.iadl_p1_h)

        self.assertEqual(self.p1iad1.score, None)
        self.p1iad1.recalculate()
        self.assertEqual(self.p1iad1.score, 5)
        
        # TUG tests
        self.p1tug = TUG.objects.create(contact_instance = self.p1c1)
        self.p1tug.times.add(TUGTrail.objects.create(order = 1, time = 12.1))
        self.p1tug.times.add(TUGTrail.objects.create(order = 2, time = 11.7))
        self.p1tug.times.add(TUGTrail.objects.create(order = 3, time = 9))
        
        self.assertEqual(self.p1tug.average, None)
        self.assertEqual(self.p1tug.mobility_rating, None)
        self.assertEqual(self.p1tug.fall_risk, None)
        self.p1tug.recalculate()
        self.assertEqual(self.p1tug.mobility_rating.option, "2")
        self.assertEqual(self.p1tug.fall_risk, AnswerOption.objects.get(table = "TUG", option = "normal"))

        # Personal induction; static data
        self.p1PIS = ParticipantInductionStatic.objects.create(participant = self.p1, us_citizen = True, 
                                                               hisp_latino = AnswerOption.objects.get(field = "hisp_latino", option__contains = "No,"),
                                                               retirement_year = 2002, 
                                                               gender = AnswerOption.objects.get(field = "gender", option = "Male"))
        self.p1PIS.racial_origin.add(AnswerOption.objects.get(table = "ParticipantInductionStatic", field = "racial_origin", option = "White"))
        self.p1PIS.racial_origin.add(AnswerOption.objects.get(table = "ParticipantInductionStatic", field = "racial_origin", option = "Chinese"))
        
        
        # Personal induction; changing data
        self.a_hs_grad = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "education_level", option = "Less than high school graduate")
        self.a_married = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "marital_status", option = "Married")
        self.a_spouse = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "perm_residents", option = "Spouse")
        self.a_apt = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "housing_type", option = "Apartment/condominium")
        self.a_income_me = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "household_income", option = "$50,000 - $69,999")
        self.a_fulltime = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "occupation_status", option = "Work full-time")
        self.a_several = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "leave_home_freq", option = "Several times a day")
        self.a_leavework = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "leave_home_reasons", option = "Work")
        self.a_leavegroc = AnswerOption.objects.get(table = "ParticipantInductionVolatile", field = "leave_home_reasons", option = "Errands (post office, grocery store, etc.)")
        self.a_occ_sailor = AnswerOption.objects.get_or_create(table = "ParticipantInductionVolatile", field = "current_occupation", option = "Retired Sailor")[0]
        self.a_occ_plumber = AnswerOption.objects.get_or_create(table = "ParticipantInductionVolatile", field = "current_occupation", option = "Plumber")[0]
        self.a_dialup = AnswerOption.objects.get(table = "HomeInventory", field = "type_of_internet", option = "Dial-up")

        self.p1PIV = ParticipantInductionVolatile.objects.create(contact_instance = self.p1c1, education_level = self.a_hs_grad, marital_status = self.a_married,
                                                    n_perm_residents = 2, housing_type = self.a_apt, household_income = self.a_income_me, 
                                                    leave_home_freq = self.a_several, limited_tranport = True, has_home_internet = True,
                                                    has_wireless_internet = False, type_of_internet = self.a_dialup)

        self.p1PIV.perm_residents.add(self.a_spouse)
        self.p1PIV.leave_home_reasons.add(self.a_leavework, self.a_leavegroc)
        self.p1PIV.current_occupation.add(self.a_occ_sailor, self.a_occ_plumber)
        self.p1PIV.occupation_status.add(self.a_fulltime)
        
        # Medical data
        ParticipantSurgeries.objects.create(t_surgery = "knee", year = 2005)
        ParticipantSurgeries.objects.create(t_surgery = "finger", year = 1997)

        # Conditions
        self.a_onset_life = AnswerOption.objects.get(field = "condition_onset", option = "In your lifetime")
        self.a_onset_now = AnswerOption.objects.get(field = "condition_onset", option = "Now")
        self.a_onset_never = AnswerOption.objects.get(field = "condition_onset", option = "Never") # link back with a field like TABLENAMExID
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Alz"), condition_onset = self.a_onset_life, year_of_onset = 1998)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Osteoarthritis"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Rheumatoid"), condition_onset = self.a_onset_now, year_of_onset = 2001)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Gout"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Fibromyalgia"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Bronchitis"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Balance"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Cancer"), condition_onset = self.a_onset_now, year_of_onset = 1978)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "COPD"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Deafness"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Hardness"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Blindness"), condition_onset = self.a_onset_life, year_of_onset = 1994)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Cataracts"), condition_onset = self.a_onset_life, year_of_onset = 1992)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Glaucoma"), condition_onset = self.a_onset_life, year_of_onset = 1962)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Low Vision"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Dementia"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Depression"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Diabetes"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Enlarged Prostate"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Epilepsy"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Fall Injuries"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Cardiovascular Disease"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "High Cholesterol"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Hypertension"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Hypotension"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Osteoporosis"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Parkinson's"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Plantar Fasciitis"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Renal Disease"), condition_onset = self.a_onset_never)
        ParticipantMedicalCondition.objects.create(condition = QuestionOption.objects.get(table = "ParticipantMedicalCondition", option__contains = "Stroke"), condition_onset = self.a_onset_never)

        a_dailydose = AnswerOption.objects.get(table = "ParticipantMedication", field = "dose_frequency", option = "Once a day")
        self.p1med1 = ParticipantMedication.objects.create( medication_name = "Advil", dose_amt = 100, dose_units = "mg", dose_frequency = a_dailydose,
                                                            med_reason = "headaches", med_duration = 180, side_effects = "sick to stomach, hives", 
                                                            is_prescription = False, notes = "This is their main medication")
        self.p1med2 = ParticipantMedication.objects.create( medication_name = "Lipitor", dose_amt = 250, dose_units = "mg", dose_frequency = a_dailydose,
                                                            med_reason = "cholesterol", med_duration = 1800, side_effects = "makes me sleepy", 
                                                            is_prescription = True, notes = "1 tablet")
        # Health mobility
        self.p1pmh = ParticipantMobilityHealth.objects.create(contact_instance = self.p1c1, ht_in = 74.0, wt_lbs = 185, 
                                                              physical_activity = AnswerOption.objects.get(table = "ParticipantMobilityHealth", option = "Active"))
                
        self.p1pmh.assistive_devices.add(AnswerOption.objects.get(option = "Glasses"),AnswerOption.objects.get(table = "ParticipantMobilityHealth", option = "Contacts"))
        self.p1pmh.mobility_aids.add(AnswerOption.objects.get(option = "Cane"),AnswerOption.objects.get(table = "ParticipantMobilityHealth", option = "Scooter"))
        
        for surg in ParticipantSurgeries.objects.all():
            self.p1pmh.surgeries.add(surg)
        for cond in ParticipantMedicalCondition.objects.all():
            self.p1pmh.medical_conditions.add(cond)
        self.p1pmh.medications.add(self.p1med1, self.p1med2)
        

        # Survey stuff
        tmp_scale_option1 = ScaleQuestionAndOption.objects.get(question__option__contains = "How difficult is it for you to get in or out of a low chair?", 
                                                              option__option = "Very difficult")
        tmp_scale_option2 = ScaleQuestionAndOption.objects.get(question__option__contains = "How difficult is it for you to climb stairs?", 
                                                              option__option = "A little difficult")

        self.p1r1 = ParticipantScaleRatings.objects.create(contact_instance = self.p1c1, research_notes = "They seems nice")
        self.p1r1.survey_selections.add(tmp_scale_option1, tmp_scale_option2)
        self.p1r1.rating_scores.recalculate()
        
        # Home Inventory
        self.p1h1 = HomeInventory.objects.create(nstories = 2, bed_ht = 89.5, 
                                                 bed_size = AnswerOption.objects.get(table="HomeInventory", field = "bed_size", option = "King"),
                                                 bed_adjustable = False, home_notes = "A bit dirty and dark inside")
        
        
        self.p1_re1 = ResidenceEntrance.objects.create(letter_id = "A", location = AnswerOption.objects.get(option = "Front"), 
                                         floor = AnswerOption.objects.get(option__iexact = "1st"), n_steps = 0,
                                         t_stairs = AnswerOption.objects.get(option = "None", table = "ResidenceEntrance", field = "t_stairs"), 
                                         w_door = 48, h_thresh = 0.5, wheelchair_access = False, 
                                         use_freq = AnswerOption.objects.get(option = "Daily", field = "use_freq", table = "ResidenceEntrance"),
                                         comments = "only exterior entrance to apartment")

        self.p1_re2 = ResidenceEntrance.objects.create(letter_id = "B", location = AnswerOption.objects.get_or_create(option = "Porch", field = "location", table = "ResidenceEntrance")[0], 
                                                     floor = AnswerOption.objects.get(option__iexact = "1st", field = "floor", table = "ResidenceEntrance"), 
                                                     n_steps = 0,
                                                     t_stairs = AnswerOption.objects.get(option = "None", table = "ResidenceEntrance", field = "t_stairs"), 
                                                     w_door = 48, h_thresh = 2, wheelchair_access = False, 
                                                     use_freq = AnswerOption.objects.get(option = "Weekly", field = "use_freq", table = "ResidenceEntrance"),
                                                     comments = "balcony")
        
        self.p1_r1 = ResidenceRoom.objects.create(room_id = 1, room_type = AnswerOption.objects.get_or_create(option = "Living Room", field = "room_type", table = "ResidenceRoom")[0], 
                                                 location = AnswerOption.objects.get_or_create(option = "1st Floor", field = "location", table = "ResidenceRoom")[0], 
                                                 floor_type = AnswerOption.objects.get_or_create(option = "Carpet", field = "location", table = "ResidenceRoom")[0],
                                                 use_freq = AnswerOption.objects.get_or_create(option = "Daily", field = "location", table = "ResidenceRoom")[0],
                                                 w_room = 20*12, l_room = 15*12, comments = "")
        self.p1_r1.entrances.add(self.p1_re1)
        self.p1_r1.connections.add(AnswerOption.objects.get_or_create(option = "Power", field = "connections", table = "ResidenceRoom")[0],
                                   AnswerOption.objects.get_or_create(option = "Phone", field = "connections", table = "ResidenceRoom")[0])

        self.p1_r2 = ResidenceRoom.objects.create(room_id = 2, room_type = AnswerOption.objects.get_or_create(option = "Bedroom", field = "room_type", table = "ResidenceRoom")[0], 
                                                 location = AnswerOption.objects.get_or_create(option = "1st Floor", field = "location", table = "ResidenceRoom")[0], 
                                                 floor_type = AnswerOption.objects.get_or_create(option = "Carpet", field = "location", table = "ResidenceRoom")[0],
                                                 use_freq = AnswerOption.objects.get_or_create(option = "Daily", field = "location", table = "ResidenceRoom")[0],
                                                 w_room = 10*12, l_room = 12*12, comments = "")
        self.p1_r2.entrances.add()
        self.p1_r2.connections.add(AnswerOption.objects.get_or_create(option = "Power", field = "connections", table = "ResidenceRoom")[0])

        ResidenceInteriorDoor.objects.create(room1 = self.p1_r1,
                                             room2 = self.p1_r2,
                                             w_door = 36, h_thresh = 0, comments = "")
        
        ResidenceInteriorStair.objects.create(room1 = self.p1_r1,
                                              room2 = self.p1_r2,
                                              location_description = "Ivisible stairs from living room to bedroom", n_steps = 5,
                                              t_stairs = AnswerOption.objects.get_or_create(option__icontains = "Ladder", field = "t_stairs", table = "ResidenceInteriorStair")[0],
                                              narrowest_width = 24, comments = "These don't really exist")

        ResidencePhotograph.objects.create(room = self.p1_r1,
                                           photo_path = "/test/dir/location/picture/[hash]", description = "Look, they're smiling!")


        self.p1h1.contact_instance.add(self.p1c1)
        self.p1h1.home_features.add(AnswerOption.objects.get(table="HomeInventory", field = "home_features", option__icontains = "attic"),
                                    AnswerOption.objects.get(table="HomeInventory", field = "home_features", option__icontains = "basement"),
                                    AnswerOption.objects.get(table="HomeInventory", field = "home_features", option__icontains = "in-ground"))
        self.p1h1.home_cooling.add(AnswerOption.objects.get(table="HomeInventory", field = "home_cooling", option__icontains = "central"),
                                   AnswerOption.objects.get(table="HomeInventory", field = "home_cooling", option__icontains = "window"))
        self.p1h1.home_heating.add(AnswerOption.objects.get(table="HomeInventory", field = "home_heating", option__icontains = "central"),
                                   AnswerOption.objects.get(table="HomeInventory", field = "home_heating", option__icontains = "fireplace"),
                                   AnswerOption.objects.get(table="HomeInventory", field = "home_heating", option__icontains = "portable"))

        self.p1h1.entrances.add(self.p1_re1,self.p1_re2)
        self.p1h1.rooms.add(self.p1_r1,self.p1_r2)
        self.p1h1.interior_doors.add(ResidenceInteriorDoor.objects.all()[0])
        self.p1h1.interior_stairs.add(ResidenceInteriorStair.objects.all()[0])
        self.p1h1.photographs.add(ResidencePhotograph.objects.all()[0])
    
    def test_functions(self):
        get_filter_option_dict()

# >> python manage.py test survey_browser.DBConnectionTest.test_basic
class DBConnectionTest(TestCase):
    fixtures = ['loaded_options.json']
    
    def setUp(self):
        from utility.import_limesurvey import connect_dump
        connect_dump()
    def tearDown(self):
        pass
    
    def test_basic(self):
        from utility.import_limesurvey import import_lime_survey_49672, import_lime_survey_58382, import_lime_survey_65387, import_lime_survey_98517

        import_lime_survey_58382(fetchn = 5, verbose = False)
        import_lime_survey_49672(fetchn = 5, verbose = False)
        import_lime_survey_65387(fetchn = 5, verbose = False)
        import_lime_survey_98517(fetchn = 5, verbose = False)

        # Check to make sure all tokens and users are loaded correctly
        self.assertEqual(Participant.objects.count(), 19)
        self.assertEqual(LimeToken.objects.count(), 20)        
        
        print "Found ", Participant.objects.count(), " unique participants"   
        print Participant.objects.all()
        print "Found ", LimeToken.objects.count(), " unique tokens"   
        print LimeToken.objects.order_by('participant__pid')

class FilterTest(TestCase):
    #fixtures = ['loaded_options_plus_limesurvey_data.json'] # takes a while to load; about 60s
    fixtures = ['loaded_options_plus_limesurvey_data_small.json'] # takes a while to load; about 8s
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_basic(self):
        # Create filters and test execution
        ParticipantFilterOptions.updateFilterOptions()
        
        self.f1 = ParticipantFilter.objects.create(name = "One Story House", description = "Participants matching this live in a one story house",
                                         filter_field = "nstories", action = "eq", argument = "1")
        self.assertEqual(len(self.f1.execute()), 4)
        
        self.f2 = ParticipantFilter.objects.create(name = "High Promis", filter_field = "promis_score", action = "gt", argument = "30")
        self.assertEqual(len(self.f2.execute()), 10)

        self.f3 = ParticipantFilter.objects.create(name = "Low Promis", filter_field = "promis_score", action = "lt", argument = "30")
        self.assertEqual(len(self.f3.execute()), 0)
        self.f3.argument = "50"
        self.assertEqual(len(self.f3.execute()), 5)

        self.f4 = ParticipantFilter.objects.create(name = "Some devices", filter_field = "assistive_devices", action = "any in", argument = "112,114")
        self.assertEqual(len(self.f4.execute()), 9)

        self.f5 = ParticipantFilter.objects.create(name = "Many devices", filter_field = "assistive_devices", action = "all in", argument = "112,114")
        self.assertEqual(len(self.f5.execute()), 2)

        self.f6 = ParticipantFilter.objects.create(name = "OK Reason", filter_field = "leave_home_reasons", action = "any not in", argument = "103")
        self.assertEqual(len(self.f6.execute()), 6)

        self.f7 = ParticipantFilter.objects.create(name = "self centered", filter_field = "racial_origin_comments", action = "contains", argument = "I")
        self.assertEqual(len(self.f7.execute()), 10)
        
        self.f8 = ParticipantFilter.objects.create(name = "no comments on race", filter_field = "racial_origin_comments", action = "eq", argument = "")
        self.assertEqual(len(self.f8.execute()), 0)

        self.f8 = ParticipantFilter.objects.create(name = "really no comments on race", filter_field = "racial_origin_comments", action = "eq", argument = None)
        self.assertEqual(len(self.f8.execute()), 0)

        # ScaleQuestionAndOption.objects.filter(question__id = 95)
        self.f9 = ParticipantFilter.objects.create(name = "low to medium satisfaction with social roles", filter_field = "SocialSatis_1", action = "any in", argument = "231,232,233")
        self.assertEqual(len(self.f9.execute()), 2)
        
        self.f9.argument = "234,235"
        self.assertEqual(len(self.f9.execute()), 8) # 2+8 = 10 total participants, from lime_survey_65387 then lime_survey_98517

        # "all in" should always yield zero for single-select fields
        self.f9.action = "all in"
        self.assertEqual(len(self.f9.execute()), 0)
        
        self.f10 = ParticipantFilter.objects.create(name = "first half SPMSQ ok", filter_field = "SPMSQ_answers", action = "all in", argument = "1,3,5,7,9")
        self.assertEqual(len(self.f10.execute()), 5)

        self.f10 = ParticipantFilter.objects.create(name = "missed one of the last 3 SPMSQ", filter_field = "SPMSQ_answers", action = "any in", argument = "16,18,20")
        self.assertEqual(len(self.f10.execute()), 1)

        self.f11 = ParticipantFilter.objects.create(name = "Nothing missed, first half IADL", filter_field = "SPMSQ_answers", action = "all in", argument = "1,5,9,13")
        self.assertEqual(len(self.f11.execute()), 5)
        
        # Create filter groups
        self.user1 = User.objects.create_user("bobby", email = "bob@gtri.gatech.edu", password = "bobisthebest")
        
        self.fg1 = ParticipantFilterGroup.objects.create(user = self.user1, name = "admin group 1")        
        self.fg2 = ParticipantFilterGroup.objects.create(user = self.user1, name = "admin group 2", description = "The second group")
        
        self.f1.assign_to_group(user = self.user1)
        self.f1.assign_to_group(user = self.user1, group = self.fg1)
        self.f2.assign_to_group(user = self.user1, group = self.fg2)
        self.assertEqual(self.f1.groups.count(), 2)
        self.assertEqual(self.f2.groups.count(), 2) # should be assigned to DEFAULT automatically

        # Meta filters
        print self.f1.execute()
        print self.f2.execute()        
        
        self.mf2 = ParticipantMetaFilter.objects.create(name = "Single story, High PROMIS", action = "or")
        self.mf2.filters.add( self.f1)
        self.mf2.filters.add( self.f2)
        print self.mf2.execute()
        self.mf2.action = "xor"
        print self.mf2.execute()
        self.mf2.action = "and"
        print self.mf2.execute()

class QAPopulateTest(TestCase):
    def setUp(self):
        from utility import option_load
        option_load.create_options()
    def tearDown(self):
        pass
    
    def test_basic(self):
        pass

class ExportTest(TestCase):
    fixtures = ['loaded_options_plus_limesurvey_data_small.json'] # takes a while to load; about 8s
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_basic(self):
        ParticipantFilterOptions.updateFilterOptions()
        self.pids = Participant.objects.values_list('pid', flat=True)
        
        from utility.export_functions import get_export_dict
        (ordered_header, export_dict) =  get_export_dict(self.pids, True)
        
        import csv
        with open('participant_data.csv', 'wb') as csvfile:
            export_writer = csv.DictWriter(csvfile, ordered_header, restval = None)
            export_writer.writeheader()
            export_writer.writerows(export_dict)
                
    