"""
Add AnswerOption and QuestionOption objects

This can then be moved into a fixture and loaded for tests and to populate db after changes

Use bulk_create for speed

"""

#from django.db.models import bulk_create

from survey_browser.models import AnswerOption, QuestionOption, IADL_option, ScaleQuestionAndOption, SPMSQ_question

def create_options():

    answerOptions = []
    questionOptions = []
    
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
    
    unique_names = ["SPMSQDate",
                "SPMSQDay",
                "SPMSQPlace",
                "SPMSQPhone",
                "SPMSQAge",
                "SPMSQBorn",
                "SPMSQPresident",
                "SPMSQPrevPres",
                "SPMSQMomName",
                "SPMSQBackCount"]
    
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = None)

    table = "IADL_option"

    field = "question"
    options = ["Ability to use telephone",
               "Shopping",
               "Food Preparation",
               "Housekeeping",
               "Laundry",
               "Mode of Transportation",
               "Responsibility for own medications",
               "Ability to Handle Finances"]

    unique_names = ["IADLPhone",
                    "IADLShop",
                    "IADLFoodPrep",
                    "IADLHouse",
                    "IADLLaundry",
                    "IADLTransport",
                    "IADLMed",
                    "IADLFinance"]
    
    short_names = [ "IADL Phone",
                    "IADL Shopping",
                    "IADL Food Preparation",
                    "IADL Housekeeping",
                    "IADL Laundry",
                    "IADL Mode of Transportation",
                    "IADL Responsibility for Medications",
                    "IADL Ability to Handle Finances"]
    
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)
    
    field = "option"
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
    addAnswerOptions(answerOptions,table,field,options)

    # TUG
    table = "TUG"
    field = "mobility_rating"
    options = ["1","2","3"]
    addAnswerOptions(answerOptions,table,field,options,True)
    
    field = "fall_risk"
    options = ["high","normal"]
    addAnswerOptions(answerOptions,table,field,options,True)

    # ParticipantInductionStatic
    table = "ParticipantInductionStatic"
    
    field = "hisp_latino"
    options = ["No, not of Hispanic, Latino, or Spanish orgin",
               "Yes, Mexican, Mexican American, Chicano",
               "Yes, Puerto Rican",
               "Yes, Cuban"]
    addAnswerOptions(answerOptions,table,field,options,True) # starts at 0 for some reason

    field = "gender"
    options = ["Male","Female"]
    addAnswerOptions(answerOptions,table,field,options,True)
    
    field = "racial_origin"
    options = ["White",
               "Black, African American, or Negro",
               "American Indian or Alaska Native",
               "Asian Indian",
               "Chinese",
               "Filipino",
               "Japanese",
               "Vietnamese",
               "Guamanian or Chamorro",
               "Native Hawaiian",
               "Samoan",
               "Other Asian",
               "Other Pacific Islander",
               "Some other race"]
    addAnswerOptions(answerOptions,table,field,options)

    # ParticipantInductionVolatile
    table = "ParticipantInductionVolatile"

    field = "education_level"
    options = [ "Less than high school graduate",
                "High school graduate/GED",
                "Vocational training",
                "Some college/Associate's degree",
                "Bachelor's degree (BA, BS, etc.)",
                "Master's degree (or other post-graduate training)",
                "Doctoral degree (PhD, MD, EdD, DDS, JD, etc.)"]
    addAnswerOptions(answerOptions,table,field,options,True)
    
    field = "marital_status"
    options = [ "Single",
                "Married",
                "Separated",
                "Divorced",
                "Widowed"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "perm_residents"
    options = [ "No additional people",
                "Spouse",
                "Adult relatives, such as adult children, cousins, or in-laws",
                "Adult nonrelatives, such as roommates",
                "Children, under the age of 18"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "housing_type"
    options = [ "House",
                "Apartment/condominium",
                "Independent living facility",
                "Assisted living facility",
                "Nursing home",
                "Relative's home"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "household_income"
    options = [ "Less than $5,000",
                "$5,000 - $9,999",
                "$10,000 - $14,999",
                "$15,000 - $19,999",
                "$20,000 - $29,999",
                "$30,000 - $39,999",
                "$40,000 - $49,999",
                "$50,000 - $69,999",
                "$70,000 - $99,999",
                "$100,000 or more",
                "Do not know for certain",
                "Do not wish to answer"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "occupation_status"
    options = [ "Work full-time",
                "Work part-time",
                "Self-employed",
                "Homemaker",
                "Volunteer worker",
                "Retired"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "leave_home_freq"
    options = [ "Several times a day",
                "Every day",
                "Several times a week",
                "Once a week",
                "Once a month or less"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "leave_home_reasons"
    options = [ "Work",
                "Errands (post office, grocery store, etc.)",
                "Social activities (church, restaurant, entertainment, etc.)",
                "Activities around the home (walking to the mailbox, gardening, etc.)",
                "Doctor/medical appointments",
                "Emergencies"]
    addAnswerOptions(answerOptions,table,field,options,True)

    # ParticipantMedicalCondition
    table = "ParticipantMedicalCondition"
    field = "condition"
    options = [ "Alzheimer's",
                "Arthritis:Osteoarthritis",
                "Arthritis:Rheumatoid Arthritis",
                "Arthritis:Gout",
                "Arthritis:Fibromyalgia",
                "Asthma or Bronchitis",
                "Balance Problems",
                "Cancer",
                "Chronic Obstructive Pulmonary Disease (COPD)",
                "Deafness",
                "Hardness of Hearing",
                "Eye Conditions:Blindness",
                "Eye Conditions:Cataracts",
                "Eye Conditions:Glaucoma",
                "Eye Conditions:Low Vision",
                "Dementia",
                "Depression",
                "Diabetes",
                "Enlarged Prostate",
                "Epilepsy",
                "Fall Injuries",
                "Heart Disease / Cardiovascular Disease",
                "High Cholesterol",
                "Hypertension / High Blood Pressure",
                "Hypotension / Low Blood Pressure",
                "Osteoporosis",
                "Parkinson's Disease",
                "Plantar Fasciitis",
                "Renal Disease / Kidney and Bladder Problems",
                "Stroke"]

    unique_names = ["MedCond_1",
                    "MedCond_2",
                    "MedCond_3",
                    "MedCond_4",
                    "MedCond_5",
                    "MedCond_6",
                    "MedCond_7",
                    "MedCond_8",
                    "MedCond_9",
                    "MedCond_10",
                    "MedCond_11",
                    "MedCond_12",
                    "MedCond_13",
                    "MedCond_14",
                    "MedCond_15",
                    "MedCond_16",
                    "MedCond_17",
                    "MedCond_18",
                    "MedCond_19",
                    "MedCond_20",
                    "MedCond_21",
                    "MedCond_22",
                    "MedCond_23",
                    "MedCond_24",
                    "MedCond_25",
                    "MedCond_26",
                    "MedCond_27",
                    "MedCond_28",
                    "MedCond_29",
                    "MedCond_30"]
    
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names)    

    field = "condition_onset" # starts at 0
    options = [ "Never",
               "In your lifetime",
                "Now"]
    addAnswerOptions(answerOptions,table,field,options,True)

    # ParticipantMobilityHealth
    table = "ParticipantMobilityHealth"
    
    field = "assistive_devices"
    options = [ "Glasses",
                "Orthosis (e.g., knee brace)",
                "Contacts",
                "Prosthesis",
                "Hearing aid"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "mobility_aids"
    options = [ "Cane",
                "Scooter",
                "Crutch(es)",
                "Manual wheelchair",
                "Walker",
                "Power wheelchair"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "physical_activity"
    options = [ "Very sedentary",
                "Moderately sedentary",
                "Mildly active",
                "Active",
                "Very active"]
    addAnswerOptions(answerOptions,table,field,options,True)

    table = "ParticipantMedication"
    
    field = "dose_frequency"
    options = [ "Once a day",
                "Twice a day",
                "Three times a day",
                "Every other day",
                "As needed"]
    addAnswerOptions(answerOptions,table,field,options,True)

    # ScaleQuestionAndOption
    table = "ScaleQuestionAndOption"
    
    field = "question"
    options = [ "Difficulty:How difficult is it for you to get in or out of a low chair?",
                "Difficulty:How difficult is it for you to open medicine bottles or jars?",
                "Difficulty:How difficult is it for you to shop for groceries or other things?",
                "Difficulty:How difficult is it for you to climb stairs?",
                "Difficulty:How difficult is it for you to make a tight fist?",
                "Difficulty:How difficult is it for you to get in or out of the bathtub or shower?",
                "Difficulty:How difficult is it for you to get comfortable to sleep?",
                "Difficulty:How difficult is it for you to bend or kneel down?",
                "Difficulty:How difficult is it for you to use buttons, snaps, hooks, or zippers?",
                "Difficulty:How difficult is it for you to cut your own fingernails?", #10
                "Difficulty:How difficult is it for you to dress yourself?",
                "Difficulty:How difficult is it for you to walk?",
                "Difficulty:How difficult is it for you to get moving after you have been sitting or lying down?",
                "Difficulty:How difficult is it for you to go out by yourself?",
                "Difficulty:How difficult is it for you to drive?",
                "Difficulty:How difficult is it for you to clean yourself after going to the bathroom?",
                "Difficulty:How difficult is it for you to turn knobs or levers (for example, to open doors or to roll down car windows)?",
                "Difficulty:How difficult is it for you to write or type?",
                "Difficulty:How difficult is it for you to pivot?",
                "Difficulty:How difficult is it for you to do your usual physical recreational activities, such as bicycling, jogging, or walking?", # 20
                "Difficulty:How difficult is it for you to do your usual leisure activities, such as hobbies, crafts, gardening, card-playing, or going out with friends?",
                "Difficulty:How difficult is it for you to do light housework or yard work, such as dusting, washing dishes, or watering plants?", # 22 (missing on paper, so replaced with 23)
                "Difficulty:How difficult is it for you to do heavy housework or yard work, such as washing floors, vacuuming, or mowing lawns?", # 23
                "Difficulty:How difficult is it for you to do your usual work, such as a paid job, housework, or volunteer activities?", # 24
                "Difficulty:How difficult is it for you to get in or out of bed?", # xx = 25
                "Frequency:How often do you walk with a limp?", #26
                "Frequency:How often do you avoid using your painful limb(s) or back?",
                "Frequency:How often does your leg lock or give-way?",
                "Frequency:How often do you have problems with concentration?",
                "Frequency:How often does doing too much in one day affect what you do the next day?",
                "Frequency:How often do you act irritable toward those around you (for example, snap at people, give sharp answers, or criticize easily)?",
                "Frequency:How often are you tired?",
                "Frequency:How often do you feel disabled?",
                "Frequency:How often do you feel angry or frustrated that you have an injury or arthritis?",
                "Bothered:How much are you bothered by problems using your hands, arms, or legs?",
                "Bothered:How much are you bothered by problems using your back?",
                "Bothered:How much are you bothered by problems doing work around your home?",
                "Bothered:How much are you bothered by problems with bathing, dressing, toileting, or other personal care?",
                "Bothered:How much are you bothered by problems with sleep and rest?",
                "Bothered:How much are you bothered by problems with leisure or recreational activities?",
                "Bothered:How much are you bothered by problems with your friends, family, or other important people in your life?",
                "Bothered:How much are you bothered by problems with thinking, concentrating, or remembering?",
                "Bothered:How much are you bothered by problems adjusting or coping with an injury or arthritis?",
                "Bothered:How much are you bothered by problems doing your usual work?",
                "Bothered:How much are you bothered by problems with feeling dependent on others?",
                "Bothered:How much are you bothered by problems with stiffness and pain?"] #46
    
    unique_names = ["MoveAbility1_1",
                    "MoveAbility1_2",
                    "MoveAbility1_3",
                    "MoveAbility1_4",
                    "MoveAbility1_5",
                    "MoveAbility1_6",
                    "MoveAbility1_7",
                    "MoveAbility1_8",
                    "MoveAbility1_9",
                    "MoveAbility1_10",
                    "MoveAbility1_11",
                    "MoveAbility1_12",
                    "MoveAbility1_13",
                    "MoveAbility1_14",
                    "MoveAbility1_15",
                    "MoveAbility1_16",
                    "MoveAbility1_17",
                    "MoveAbility1_18",
                    "MoveAbility1_19",
                    "MoveAbility1_20",
                    "MoveAbility1_21",
                    "MoveAbility1_22",
                    "MoveAbility1_23",
                    "MoveAbility1_24",
                    "MoveAbility1_xx",
                    "MoveAbility2_26",
                    "MoveAbility2_27",
                    "MoveAbility2_28",
                    "MoveAbility2_29",
                    "MoveAbility2_30",
                    "MoveAbility2_31",
                    "MoveAbility2_32",
                    "MoveAbility2_33",
                    "MoveAbility2_34",
                    "MoveAbility3_35",
                    "MoveAbility3_36",
                    "MoveAbility3_37",
                    "MoveAbility3_38",
                    "MoveAbility3_39",
                    "MoveAbility3_40",
                    "MoveAbility3_41",
                    "MoveAbility3_42",
                    "MoveAbility3_43",
                    "MoveAbility3_44",
                    "MoveAbility3_45",
                    "MoveAbility3_46"]
    
    short_names = [ "Get in/out chair",
                    "Open bottles/jars",
                    "Shop for groceries, etc.",
                    "Climb stairs",
                    "Make a fist",
                    "Get in/out bathtub/shower",
                    "Comfortable to sleep",
                    "Bend or kneel",
                    "Use bottons, snaps, hooks, zippers",
                    "Cut fingernails",
                    "Dress yourself",
                    "Walk",
                    "Get moving after rest",
                    "Go out alone",
                    "Drive",
                    "Clean yourself after going to the bathroom",
                    "Turn knobs or levers",
                    "Write or type",
                    "Pivot",
                    "Physical recreational activities",
                    "Leisure activities",
                    "Light housework/yardwork",
                    "Heavy housework/yardwork",
                    "Usual work",
                    "Get in/out bed",
                    "Walk with limp",
                    "Avoid using painful limb",
                    "Leg-lock or give-way",
                    "Concentration problems",
                    "Activity one day affects next day",
                    "Act irritable",
                    "Tired",
                    "Feel disabled",
                    "Feel angry/frustrated about injury/arthritis",
                    "Using hands, arms, legs",
                    "Using back",
                    "Doing work around the home",
                    "Bathing, dressing, toileting, personal care",
                    "Sleep and rest",
                    "Leisure or recreational activities",
                    "Friends, family, important people",
                    "Thinking, concentrating, remembering",
                    "Adjusting / coping with injury, arthritis",
                    "Usual work",
                    "Feeling dependent on others",
                    "Stiffness and pain"]
    
    for i, op in enumerate(options):
        options[i] = "Functional Movement Abilities: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "I am satisfied with my ability to do things for my family.",
                "I am satisfied with my ability to do things for fun with others.",
                "I feel good about my ability to do things for my friends.",
                "I am satisfied with my ability to perform my daily routines.",
                "I am satisfied with my ability to do things for fun outside my home.",
                "I am satisfied with my ability to meet the needs of my friends.",
                "I am satisfied with my ability to do the work that is really important to me (include work at home).",
                "I am satisfied with my ability to meet the needs of my family."]
    
    unique_names = ["SocialSatis_1",
                    "SocialSatis_2",
                    "SocialSatis_3",
                    "SocialSatis_4",
                    "SocialSatis_5",
                    "SocialSatis_6",
                    "SocialSatis_7",
                    "SocialSatis_8"]

    short_names = ["Things for family",
                    "Things for fun with others",
                    "Things for friends",
                    "Perform daily routines",
                    "Things for fun outside home",
                    "Meet needs of friends",
                    "Do work that is important to me",
                    "Meet needs of family"]

    for i, op in enumerate(options):
        options[i] = "Satisfaction with Social Roles and Activities: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "How would you rate your quality of life?",
                "How satisfied are you with your health?",
                "To what extent do you feel that physical pain prevents you from doing what you need to do?",
                "How much do you need any medical treatment to function in your daily life?",
                "How much do you enjoy life?",
                "To what extent do you feel your life to be meaningful?",
                "How well are you able to concentrate?",
                "How safe do you feel in your daily life?",
                "How healthy is your physical environment?",
                "Do you have enough energy for everyday life?",
                "Are you able to accept your bodily appearance?",
                "Have you enough money to meet your needs?",
                "How available to you is the information that you need in your day-to-day life?",
                "To what extent do you have the opportunity for leisure activities?",
                "How well are you able to get around?",
                "How satisfied are you with your sleep?",
                "How satisfied are you with your ability to perform your daily living activities?",
                "How satisfied are you with your capacity for work?",
                "How satisfied are you with yourself?",
                "How satisfied are you with your personal relationships?",
                "How satisfied are you with your weight?",
                "How satisfied are you with the support you get from your friends?",
                "How satisfied are you with the conditions of your living place?",
                "How satisfied are you with your access to health services?",
                "How satisfied are you with your transport?",
                "How often do you have negative feelings such as blue mood, despair, anxiety, depression?"]
    
    unique_names = ["QualityLife1_1",
                    "QualityLife2_1",
                    "QualityLife3_3",
                    "QualityLife3_4",
                    "QualityLife3_5",
                    "QualityLife3_6",
                    "QualityLife4_7",
                    "QualityLife4_8",
                    "QualityLife4_9",
                    "QualityLife5_10",
                    "QualityLife5_11",
                    "QualityLife5_12",
                    "QualityLife5_13",
                    "QualityLife5_14",
                    "QualityLife6_15",
                    "QualityLife7_16",
                    "QualityLife7_17",
                    "QualityLife7_18",
                    "QualityLife7_19",
                    "QualityLife7_20",
                    "QualityLife7_xx",
                    "QualityLife7_22",
                    "QualityLife7_23",
                    "QualityLife7_24",
                    "QualityLife7_25",
                    "QualityLife8_26"]

    short_names = ["Quality of life",
                    "Health satisfaction",
                    "Feel pain preventing from doing things",
                    "Need medical treatment to function",
                    "Enjoy life",
                    "Meaningful life",
                    "Concentrate",
                    "Feel safe",
                    "Healthy physical environment",
                    "Energy for everyday",
                    "Accept bodily appearance",
                    "Money to meet needs",
                    "Availability of information",
                    "Chance for leisure activities",
                    "Able to get around",
                    "Sleep satisfaction",
                    "Daily activity satisfaction",
                    "Work capacity satisfaction",
                    "Self satisfaction",
                    "Personal relationship satisfaction",
                    "Weight satisfaction",
                    "Social support satisfaction",
                    "Living condition satisfaction",
                    "Health service access satisfaction",
                    "Transportation satisfaction",
                    "Negative feelings"]
    
    for i, op in enumerate(options):
        options[i] = "Quality of Life: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "To what extent do impairments to your senses (e.g., hearing, vision, taste, smell, touch) affect your daily life?",
                "To what extent does loss of, for example, hearing, vision, taste, smell, or touch affect your ability to participate in activities?",
                "How much freedom do you have to make your own decisions?",
                "To what extent do you feel in control of your future?",
                "How much do you feel that the people around you are respectful of your freedom?",
                "To what extent do problems with your sensory functioning (e.g., hearing, vision, taste, smell, touch) affect your ability to interact with others?",
                "To what extent are you able to do the things you'd like to do?",
                "How would you rate your sensory functioning (e.g., hearing, vision, taste, smell, touch)?"]
    
    unique_names = ["QualityLife9_1",
                    "QualityLife9_2",
                    "QualityLife9_3",
                    "QualityLife10_4",
                    "QualityLife10_5",
                    "QualityLife11_10",
                    "QualityLife11_11",
                    "QualityLife12_20"]

    short_names = ["Sensory loss affect daily life",
                    "Sensory loss affect participation",
                    "Sense of freedom",
                    "Sense of control",
                    "Sense of respect for freedom",
                    "Sensory loss affect interaction with others",
                    "Ability to do things you want",
                    "Sensory functioning"]
    
    for i, op in enumerate(options):
        options[i] = "Last Two Weeks: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

        
    options = [ "Tablet (iPad, etc.)",
                "Laptop",
                "Desktop (less than 3 years old)",
                "Desktop (3 or more years old)",
                "Printer",
                "Scanner",
                "Telephone (fixed/land line)",
                "Basic cellular telephone",
                "Smartphone (iPhone, Android, etc.)",
                "Standard television (CRT)",
                "Flat panel television (LCD, plasma, etc.)",
                "Cable/satellite box (to watch TV)",
                "Digital video recorder (to record TV)",
                "DVD/Blu-Ray player",
                "Video game console (PlayStation, Wii, etc.)",
                "Digital music player (iPod, etc.)",
                "CD player",
                "Digital (photo) camera",
                "Video camera/camcorder",
                "eBook reader (Kindle, Nook, etc.)",
                "Stove/oven",
                "Microwave oven",
                "Dishwasher",
                "Coffee maker",
                "Washer/dryer",
                "Vacuum cleaner",
                "Programmable thermostat"]
    
    unique_names = ["TechUse1_1",
                    "TechUse1_2",
                    "TechUse1_3",
                    "TechUse1_4",
                    "TechUse1_5",
                    "TechUse1_6",
                    "TechUse1_7",
                    "TechUse1_8",
                    "TechUse1_9",
                    "TechUse2_10",
                    "TechUse2_11",
                    "TechUse2_12",
                    "TechUse2_13",
                    "TechUse2_14",
                    "TechUse2_15",
                    "TechUse3_16",
                    "TechUse3_17",
                    "TechUse3_18",
                    "TechUse3_19",
                    "TechUse3_20",
                    "TechUse4_21",
                    "TechUse4_22",
                    "TechUse4_23",
                    "TechUse4_24",
                    "TechUse4_25",
                    "TechUse4_26",
                    "TechUse4_27"]

    short_names = ["Tablet",
                    "Laptop",
                    "Desktop (< 3 years old)",
                    "Desktop  (3+ years old)",
                    "Printer",
                    "Scanner",
                    "Telephone",
                    "Telephone",
                    "Telephone",
                    "TV",
                    "TV",
                    "Cable/satellite box",
                    "DVR",
                    "DVD/Blu-ray player",
                    "Video game console",
                    "Digital music player",
                    "CD player",
                    "Digital camera",
                    "Video camera",
                    "eBook reader",
                    "Stove/oven",
                    "Microwave",
                    "Dishwasher",
                    "Coffee maker",
                    "Washer/dryer",
                    "Vacuum cleaner",
                    "Programmable thermostat"]
        
    for i, op in enumerate(options):
        options[i] = "Technology: Consumer Technology Access and Use: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "Digital video recorder (to record TV): Manually recording TV programs as they are broadcast",
                "Digital video recorder (to record TV): Program the device to record a TV program at a later time",
                "Stove/oven: Use the oven's digital timer",
                "Stove/oven: Program the oven to automatically start or stop at a later time",
                "Coffee maker: Program the coffee maker to automatically brew coffee at a later time",
                "Microwave oven: Use 1-touch controls (Popcorn, Reheat, 1-minute key, etc.)",
                "Microwave oven: Program the microwave to cook at a desired power level or to a desired temperature",
                "Programmable thermostat: Adjust the temperature manually",
                "Programmable thermostat: Program the thermostat to adjust the temperature automatically according to a schedule"]

    unique_names = ["TechPurpose_1",
                    "TechPurpose_6",
                    "TechPurpose_7",
                    "TechPurpose_8",
                    "TechPurpose_10",
                    "TechPurpose_16",
                    "TechPurpose_17",
                    "TechPurpose_21",
                    "TechPurpose_22"]

    short_names = ["Frequency:Record live TV on DVR",
                    "Frequency:Record future TV on DVR",
                    "Frequency:Use oven digital timer",
                    "Frequency:Program oven to start/stop at later time",
                    "Frequency:Program coffee maker",
                    "Frequency:Use 1-touch microwave controls",
                    "Frequency:Program microwave to cook at desired power/temp",
                    "Frequency:Adjust programmable thermostat manually",
                    "Frequency:Program thermostat to adjust temp automatically"]
    
    for i, op in enumerate(options):
        options[i] = "Technology: Consumer Technology Personal Access and Use: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "Talking on the phone",
                "Text messaging (SMS) or instant messaging",
                "Email",
                "Social networking (Facebook, Twitter, message boards, etc.)",
                "Obtaining news or weather information",
                "Obtaining leisure or hobby information (sports, dining, travel, lifestyle, etc.)",
                "Searching for information (Google, Bing, etc.)",
                "Personal entertainment (video, music, games, etc.)",
                "Productivity (office apps, calendar, to-do list, etc.)",
                "Taking or viewing photos/video",
                "Maps, GPS, navigation",
                "Shopping"]

    unique_names = ["PhonePurpose_1",
                    "PhonePurpose_2",
                    "PhonePurpose_3",
                    "PhonePurpose_4",
                    "PhonePurpose_5",
                    "PhonePurpose_6",
                    "PhonePurpose_7",
                    "PhonePurpose_8",
                    "PhonePurpose_9",
                    "PhonePurpose_10",
                    "PhonePurpose_11",
                    "PhonePurpose_12"]

    short_names = ["Talking",
                    "Texting",
                    "Email",
                    "Social networking",
                    "News/weather",
                    "Leisure/hobby info",
                    "Information (web search)",
                    "Personal entertainment (video, games, etc.)",
                    "Productivity (calendar, to-do, etc.)",
                    "Photos/video",
                    "Maps,GPS,naviation",
                    "Shopping"]
    
    for i, op in enumerate(options):
        options[i] = "Technology: Computer and Cellular Phone Use: Cell: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "Instant messaging or other communications (Skype, video conferencing, etc.)",
                "Email",
                "Social networking (Facebook, Twitter, message boards, etc.)",
                "Personal entertainment (video, music, games, etc.)",
                "Photo or video management or editing",
                "Productivity (office apps, calendar, to-do list, etc.)",
                "Obtaining news or weather information",
                "Obtaining leisure or hobby information (sports, dining, travel, lifestyle, etc.)",
                "Searching for information (Google, Bing, etc.)",
                "Maps and directions",
                "Shopping"]

    unique_names = ["PCPurpose_1",
                    "PCPurpose_2",
                    "PCPurpose_3",
                    "PCPurpose_4",
                    "PCPurpose_5",
                    "PCPurpose_6",
                    "PCPurpose_7",
                    "PCPurpose_8",
                    "PCPurpose_9",
                    "PCPurpose_10",
                    "PCPurpose_11"]

    short_names = ["Instant messaging (Skype, video conference, etc.)",
                    "Email",
                    "Social networking",
                    "Personal entertainment (video, games, etc.)",
                    "Photos/video",
                    "Productivity (calendar, to-do, etc.)",
                    "News/weather",
                    "Leisure/hobby info",
                    "Information (web search)",
                    "Maps,GPS,naviation",
                    "Shopping"]
    
    for i, op in enumerate(options):
        options[i] = "Technology: Computer and Cellular Phone Use: Computer: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "Adjustable bed",
                "Blood glucose monitor",
                "Blood pressure monitor",
                "Digital scale",
                "Digital thermometer",
                "Heart rate monitor",
                "Pedometer",
                "Wearable emergency alert device"]

    unique_names = ["HealthTechUse_1",
                    "HealthTechUse_2",
                    "HealthTechUse_3",
                    "HealthTechUse_4",
                    "HealthTechUse_5",
                    "HealthTechUse_6",
                    "HealthTechUse_7",
                    "HealthTechUse_8"]

    short_names = ["Adjustable bed",
                    "Blood glucose monitor",
                    "Blood pressure monitor",
                    "Digital scale",
                    "Digital thermometer",
                    "Heart rate monitor",
                    "Pedomoter",
                    "Emergency alert device"]
    
    for i, op in enumerate(options):
        options[i] = "Technology: Health Technology Access and Use: Listed Technologies: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "if there were no one around to tell me what to do as I go.",
                "if I had never used a product like it before.",
                "if I had only the product manuals for reference.",
                "if I had seen someone else using it before trying it myself.",
                "if I could call someone for help if I got stuck.",
                "if someone else had helped me get started.",
                "if I had a lot of time to complete the job for which the product was provided.",
                "if I had just the built-in help facility for assistance.",
                "if someone showed me how to do it first.",
                "if I had used similar products before this one to do the same job."]

    unique_names = ["ConfidenceTech_1",
                    "ConfidenceTech_2",
                    "ConfidenceTech_3",
                    "ConfidenceTech_4",
                    "ConfidenceTech_5",
                    "ConfidenceTech_6",
                    "ConfidenceTech_7",
                    "ConfidenceTech_8",
                    "ConfidenceTech_9",
                    "ConfidenceTech_10"]

    short_names = ["No one around to help",
                    "Never used anything like it before",
                    "Had product manuals",
                    "Seen someone else using it",
                    "Could call for help",
                    "Someone helped to get started",
                    "Ample time",
                    "Had built-in help",
                    "Showed how by someone else",
                    "Used similar products"]
    
    for i, op in enumerate(options):
        options[i] = "Technology: Confidence with Technology: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    options = [ "The way you pursue your hobbies or interests.",
                "Your ability to do your job.",
                "Your ability to learn new things.",
                "Your ability to keep in touch with friends and family.",
                "Your ability to share your ideas and creations with others.",
                "Your ability to work with others in your community or in groups you belong to."]

    unique_names = ["AttIT_1",
                    "AttIT_2",
                    "AttIT_3",
                    "AttIT_4",
                    "AttIT_5",
                    "AttIT_6"]

    short_names = ["Improve:Pursue hobbies/interests",
                    "Improve:Ability to do job",
                    "Improve:Ability to learn new things",
                    "Improve:Ability to keep in touch with friends/family",
                    "Improve:Ability to share ideas",
                    "Improve:Ability to work with others"]
    
    for i, op in enumerate(options):
        options[i] = "Technology: Attitudes Toward Information Technology: " + op
    addQuestionOptions(questionOptions,table,field,options,ordered = True, unique_names = unique_names, short_names = short_names)

    # ScaleQuestionAndOption
    table = "ScaleQuestionAndOption"
    
    field = "option" # need to give field a name that allows identification on per question level

    scale1 = ["Not at all difficult",
              "A little difficult",
              "Moderately difficult",
              "Very difficult",
              "Unable to do"]
    scale1.reverse() # the 'code' is opposite the 'sortorder'
    unique_names = ["scale1:"+i for i in scale1]
    addAnswerOptions(answerOptions,table,field,scale1,ordered = True, unique_names = unique_names)

    scale2 = ["None of the time",
              "A little of the time",
              "Some of the time",
              "Most of the time",
              "All of the time"]
    scale2.reverse()
    unique_names = ["scale2:"+i for i in scale2]
    addAnswerOptions(answerOptions,table,field,scale2,ordered = True, unique_names = unique_names)
    
    scale3 = ["Not at all bothered",
              "A little bothered",
              "Moderately bothered",
              "Very bothered",
              "Extremely bothered"]
    scale3.reverse()
    unique_names = ["scale3:"+i for i in scale3]
    addAnswerOptions(answerOptions,table,field,scale3,ordered = True, unique_names = unique_names)

    scale4 = ["Not at all",
              "A little bit",
              "Somewhat",
              "Quite a bit",
              "Very much"]
    unique_names = ["scale4:"+i for i in scale4]
    addAnswerOptions(answerOptions,table,field,scale4,ordered = True, unique_names = unique_names)

    scale5 = ["Very poor",
              "Poor",
              "Neither poor nor good",
              "Good",
              "Very good"]
    unique_names = ["scale5:"+i for i in scale5]
    addAnswerOptions(answerOptions,table,field,scale5,ordered = True, unique_names = unique_names)

    scale6 = ["Very dissatisfied",
              "Dissatisfied",
              "Neither satisfied nor dissatisfied",
              "Satisfied",
              "Very satisfied"]
    unique_names = ["scale6:"+i for i in scale6]
    addAnswerOptions(answerOptions,table,field,scale6,ordered = True, unique_names = unique_names)

    scale7 = ["Not at all",
              "A little",
              "A moderate amount",
              "Very much",
              "An extreme amount"]
    unique_names = ["scale7:"+i for i in scale7]
    addAnswerOptions(answerOptions,table,field,scale7,ordered = True, unique_names = unique_names)

    scale8 = ["Not at all",
              "A little",
              "A moderate amount",
              "Very much",
              "Extremely"]
    unique_names = ["scale8:"+i for i in scale8]
    addAnswerOptions(answerOptions,table,field,scale8,ordered = True, unique_names = unique_names)

    scale9 = ["Never",
              "Seldom",
              "Quite often",
              "Very often",
              "Always"]
    unique_names = ["scale9:"+i for i in scale9]
    addAnswerOptions(answerOptions,table,field,scale9,ordered = True, unique_names = unique_names)
    
    scale10 = ["Not at all",
              "Slightly",
              "Moderately",
              "Very much",
              "Extremely"]
    unique_names = ["scale10:"+i for i in scale10]
    addAnswerOptions(answerOptions,table,field,scale10,ordered = True, unique_names = unique_names)

    scale11 = ["Not at all",
              "A little",
              "Moderately",
              "Mostly",
              "Completely"]
    unique_names = ["scale11:"+i for i in scale11]
    addAnswerOptions(answerOptions,table,field,scale11,ordered = True, unique_names = unique_names)

    scale12 = ["Don't have",
              "Once a month or less",
              "Once a week",
              "Several times a week",
              "Every day",
              "Several times a day"]
    unique_names = ["scale12:"+i for i in scale12]
    addAnswerOptions(answerOptions,table,field,scale12,ordered = True, unique_names = unique_names)

    scale13 = ["N/A",
              "Never",
              "Once a month or less",
              "Once a week",
              "Several times a week",
              "Every day",
              "Several times a day"]
    unique_names = ["scale13:"+i for i in scale13]
    addAnswerOptions(answerOptions,table,field,scale13,ordered = True, unique_names = unique_names)

    scale14 = ["Never",
              "Once a month or less",
              "Once a week",
              "Several times a week",
              "Every day",
              "Several times a day",
              "N/A"] # add on blank spaces to get "N/A" to correct index
    unique_names = ["scale14:"+i for i in scale14]
    orders = [1,2,3,4,5,6,10]
    addAnswerOptions(answerOptions,table,field,scale14,ordered = True, unique_names = unique_names, orders = orders)    
    

    scale15 = ["Confidence 1",
                "Confidence 2",
                "Confidence 3",
                "Confidence 4",
                "Confidence 5",
                "Confidence 6",
                "Confidence 7",
                "Confidence 8",
                "Confidence 9",
                "Confidence 10"]
    unique_names = ["scale15:"+i for i in scale15]
    addAnswerOptions(answerOptions,table,field,scale15,ordered = True, unique_names = unique_names)    

    scale16 = ["Not at all",
              "Only a little",
              "Some",
              "A lot"]
    unique_names = ["scale16:"+i for i in scale16]
    addAnswerOptions(answerOptions,table,field,scale16,ordered = True, unique_names = unique_names)

    # ResidenceEntrance
    table = "ResidenceEntrance"
    
    field = "location"
    options = [ "Front",
                "Back",
                "Side",
                "Garage",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "floor"
    options = [ "Basement",
                "1st",
                "2nd",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "t_stairs"
    options = [ "None",
                "Straight",
                "Landing(s)",
                "Porch/Deck",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "use_freq"
    options = [ "Several Times A Day",
                "Daily",
                "Weekly",
                "Monthly",
                "Rarely",
                "Never"]
    addAnswerOptions(answerOptions,table,field,options,True)

    # ResidenceRoom
    table = "ResidenceRoom"
    
    field = "room_type"
    options = [ "Bathroom",
                "Bedroom",
                "Bonus Room",
                "Carport",
                "Den/Family Room",
                "Dining Room",
                "Entry/Foyer",
                "Garage",
                "Hallway",
                "Kitchen",
                "Laundry Room",
                "Library",
                "Living Room",
                "Master Bath",
                "Master Bedroom",
                "Office",
                "Outbuilding",
                "Porch/Deck",
                "Rec Room",
                "Storage Room",
                "Sunroom",
                "Workshop",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "location"
    options = [ "Basement",
                "1st Floor",
                "2nd Floor",
                "3rd Floor",
                "Attic",
                "Exterior",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "floor_type"
    options = [ "Carpet",
                "Hardwood",
                "Tile",
                "Vinyl",
                "Concrete",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "use_freq"
    options = [ "Several Times A Day",
                "Daily",
                "Weekly",
                "Monthly",
                "Rarely",
                "Never"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "connections"
    options = [ "power",
                "phone",
                "cable"]
    addAnswerOptions(answerOptions,table,field,options,True)

    # ResidenceInteriorStair
    table = "ResidenceInteriorStair"

    field = "location_description"
    options = [ "Basement to 1st floor",
                "1st floor to 2nd floor",
                "2nd floor to 3rd floor",
                "To attic"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "t_stairs"
    options = [ "Straight",
                "Landing(s)",
                "Spiral",
                "Folding",
                "Ladder",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    # HomeInventory
    table = "HomeInventory"
    
    field = "type_of_internet"
    options = [ "Dial-up",
                "Broadband (Cable, DSL, Clear, etc.)",
                "Not sure"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "home_features"
    options = [ "Attic",
                "Basement",
                "Crawlspace foundation",
                "Slab foundation",
                "Swimming pool (in-ground)",
                "Swimming pool (above ground)",
                "Hot tub"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "home_cooling"
    options = [ "Central A/C",
                "Portable A/C",
                "Window A/C",
                "No A/C (includes fans, etc.)",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "home_heating"
    options = [ "Central heat",
                "Fireplace/wood stove",
                "Portable heater(s)",
                "Radiator(s)",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)

    field = "bed_size"
    options = [ "Twin",
                "Double",
                "Queen",
                "King",
                "California King",
                "Other"]
    addAnswerOptions(answerOptions,table,field,options,True)


    bulk_create_wrapper(answerOptions)
    bulk_create_wrapper(questionOptions)

    # Create SPMSQ mappings
    for qo in QuestionOption.objects.filter(table = "SPMSQ_question"):
        SPMSQ_question.objects.create(question = qo, correct = True)
        SPMSQ_question.objects.create(question = qo, correct = False)

    # Create IADL mappings
    iadl_q_options = [  "Ability to use telephone",
                       "Shopping",
                       "Food Preparation",
                       "Housekeeping",
                       "Laundry",
                       "Mode of Transportation",
                       "Responsibility for own medications",
                       "Ability to Handle Finances"]
    
    
    iadl_a = QuestionOption.objects.get(table = "IADL_option",field = "question",option = iadl_q_options[0])
    iadl_b = QuestionOption.objects.get(table = "IADL_option",field = "question",option = iadl_q_options[1])
    iadl_c = QuestionOption.objects.get(table = "IADL_option",field = "question",option = iadl_q_options[2])
    iadl_d = QuestionOption.objects.get(table = "IADL_option",field = "question",option = iadl_q_options[3])
    iadl_e = QuestionOption.objects.get(table = "IADL_option",field = "question",option = iadl_q_options[4])
    iadl_f = QuestionOption.objects.get(table = "IADL_option",field = "question",option = iadl_q_options[5])
    iadl_g = QuestionOption.objects.get(table = "IADL_option",field = "question",option = iadl_q_options[6])
    iadl_h = QuestionOption.objects.get(table = "IADL_option",field = "question",option = iadl_q_options[7])

    iadl_a1 = AnswerOption.objects.get(table = "IADL_option",option = "Operates telephone on own initiative; looks up and dials numbers, etc.")
    iadl_a2 = AnswerOption.objects.get(table = "IADL_option",option = "Dials a few well-known numbers")
    iadl_a3 = AnswerOption.objects.get(table = "IADL_option",option = "Answers telephone but does not dial")
    iadl_a4 = AnswerOption.objects.get(table = "IADL_option",option = "Does not use telephone at all.")
    iadl_b1 = AnswerOption.objects.get(table = "IADL_option",option = "Takes care of all shopping needs independently")
    iadl_b2 = AnswerOption.objects.get(table = "IADL_option",option = "Shops independently for small purchases")
    iadl_b3 = AnswerOption.objects.get(table = "IADL_option",option = "Needs to be accompanied on any shopping trip")
    iadl_b4 = AnswerOption.objects.get(table = "IADL_option",option = "Completely unable to shop")
    iadl_c1 = AnswerOption.objects.get(table = "IADL_option",option = "Plans, prepares and serves adequate meals independently")
    iadl_c2 = AnswerOption.objects.get(table = "IADL_option",option = "Prepares adequate meals if supplied with ingredients")
    iadl_c3 = AnswerOption.objects.get(table = "IADL_option",option = "Heats, serves and prepares meals or prepares meals but does not maintain adequate diet.")
    iadl_c4 = AnswerOption.objects.get(table = "IADL_option",option = "Needs to have meals prepared and served")
    iadl_d1 = AnswerOption.objects.get(table = "IADL_option",option = "Maintains house alone or with occasional assistance (e.g. 'heavy work domestic help')")
    iadl_d2 = AnswerOption.objects.get(table = "IADL_option",option = "Performs light daily tasks such as dishwashing, bed making")
    iadl_d3 = AnswerOption.objects.get(table = "IADL_option",option = "Performs light daily tasks but cannot maintain acceptable level of cleanliness.")
    iadl_d4 = AnswerOption.objects.get(table = "IADL_option",option = "Needs help with all home maintenance tasks.")
    iadl_d5 = AnswerOption.objects.get(table = "IADL_option",option = "Does not participate in any housekeeping tasks.")
    iadl_e1 = AnswerOption.objects.get(table = "IADL_option",option = "Does personal laundry completely")
    iadl_e2 = AnswerOption.objects.get(table = "IADL_option",option = "Launders small items; rinses stockings, etc.")
    iadl_e3 = AnswerOption.objects.get(table = "IADL_option",option = "All laundry must be done by others")
    iadl_f1 = AnswerOption.objects.get(table = "IADL_option",option = "Travels independently on public transportation or drives own car")
    iadl_f2 = AnswerOption.objects.get(table = "IADL_option",option = "Arranges own travel via taxi, but does not otherwise use public transportation")
    iadl_f3 = AnswerOption.objects.get(table = "IADL_option",option = "Travels on public transportation when accompanied by another")
    iadl_f4 = AnswerOption.objects.get(table = "IADL_option",option = "Travel limited to taxi or automobile with assistance of another")
    iadl_f5 = AnswerOption.objects.get(table = "IADL_option",option = "Does not travel at all.")
    iadl_g1 = AnswerOption.objects.get(table = "IADL_option",option = "Is responsible for taking medication in correct dosages at correct time")
    iadl_g2 = AnswerOption.objects.get(table = "IADL_option",option = "Takes responsibility if medication is prepared in advance in separate dosage")
    iadl_g3 = AnswerOption.objects.get(table = "IADL_option",option = "Is not capable of dispensing own medication")
    iadl_h1 = AnswerOption.objects.get(table = "IADL_option",option = "Manages financial matters independently (budgets, writes checks, pays rent, bills goes to back), collects and keeps track of income.")
    iadl_h2 = AnswerOption.objects.get(table = "IADL_option",option = "Manages day-to-day purchases, but needs help with banking, major purchases, etc.")
    iadl_h3 = AnswerOption.objects.get(table = "IADL_option",option = "Incapable of handling money.")
    
    IADL_option.objects.create( option = iadl_a1, question = iadl_a, order = 1, score = 1)
    IADL_option.objects.create( option = iadl_a2, question = iadl_a, order = 2, score = 1)
    IADL_option.objects.create( option = iadl_a3, question = iadl_a, order = 3, score = 1)
    IADL_option.objects.create( option = iadl_a4, question = iadl_a, order = 4, score = 0)
    IADL_option.objects.create( option = iadl_b1, question = iadl_b, order = 1, score = 1)
    IADL_option.objects.create( option = iadl_b2, question = iadl_b, order = 2, score = 0)
    IADL_option.objects.create( option = iadl_b3, question = iadl_b, order = 3, score = 0)
    IADL_option.objects.create( option = iadl_b4, question = iadl_b, order = 4, score = 0)
    IADL_option.objects.create( option = iadl_c1, question = iadl_c, order = 1, score = 1)
    IADL_option.objects.create( option = iadl_c2, question = iadl_c, order = 2, score = 0)
    IADL_option.objects.create( option = iadl_c3, question = iadl_c, order = 3, score = 0)
    IADL_option.objects.create( option = iadl_c4, question = iadl_c, order = 4, score = 0)
    IADL_option.objects.create( option = iadl_d1, question = iadl_d, order = 1, score = 1)
    IADL_option.objects.create( option = iadl_d2, question = iadl_d, order = 2, score = 1)
    IADL_option.objects.create( option = iadl_d3, question = iadl_d, order = 3, score = 1)
    IADL_option.objects.create( option = iadl_d4, question = iadl_d, order = 4, score = 1)
    IADL_option.objects.create( option = iadl_d5, question = iadl_d, order = 5, score = 0)
    IADL_option.objects.create( option = iadl_e1, question = iadl_e, order = 1, score = 1)
    IADL_option.objects.create( option = iadl_e2, question = iadl_e, order = 2, score = 1)
    IADL_option.objects.create( option = iadl_e3, question = iadl_e, order = 3, score = 0)
    IADL_option.objects.create( option = iadl_f1, question = iadl_f, order = 1, score = 1)
    IADL_option.objects.create( option = iadl_f2, question = iadl_f, order = 2, score = 1)
    IADL_option.objects.create( option = iadl_f3, question = iadl_f, order = 3, score = 1)
    IADL_option.objects.create( option = iadl_f4, question = iadl_f, order = 4, score = 0)
    IADL_option.objects.create( option = iadl_f5, question = iadl_f, order = 5, score = 0)
    IADL_option.objects.create( option = iadl_g1, question = iadl_g, order = 1, score = 1)
    IADL_option.objects.create( option = iadl_g2, question = iadl_g, order = 2, score = 0)
    IADL_option.objects.create( option = iadl_g3, question = iadl_g, order = 3, score = 0)
    IADL_option.objects.create( option = iadl_h1, question = iadl_h, order = 1, score = 1)
    IADL_option.objects.create( option = iadl_h2, question = iadl_h, order = 2, score = 1)
    IADL_option.objects.create( option = iadl_h3, question = iadl_h, order = 3, score = 0)
    
    # Create ScaleQuestionAndOption objects
    scale_questions = QuestionOption.objects.filter(option__contains = "Functional Movement Abilities: ").filter(option__contains = "How difficult is it for you")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale1:")
    create_scale_qa(scale_questions, scale_answers)

    scale_questions = QuestionOption.objects.filter(option__contains = "Functional Movement Abilities: ").filter(option__contains = "How often")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale2:")
    create_scale_qa(scale_questions, scale_answers)

    scale_questions = QuestionOption.objects.filter(option__contains = "Functional Movement Abilities: ").filter(option__contains = "How much are you bothered by problems")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale3:")
    create_scale_qa(scale_questions, scale_answers)

    scale_questions = QuestionOption.objects.filter(option__contains = "Satisfaction with Social Roles and Activities: ")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale4:")
    create_scale_qa(scale_questions, scale_answers)

    # Come back to these
    scale_questions = QuestionOption.objects.filter(option__contains = "Quality of Life: ")
    options = [ "How would you rate your quality of life?",
                "How satisfied are you with your health?",
                "To what extent do you feel that physical pain prevents you from doing what you need to do?",
                "How much do you need any medical treatment to function in your daily life?",
                "How much do you enjoy life?",
                "To what extent do you feel your life to be meaningful?",
                "How well are you able to concentrate?",
                "How safe do you feel in your daily life?",
                "How healthy is your physical environment?",
                "Do you have enough energy for everyday life?",
                "Are you able to accept your bodily appearance?",
                "Have you enough money to meet your needs?",
                "How available to you is the information that you need in your day-to-day life?",
                "To what extent do you have the opportunity for leisure activities?",
                "How well are you able to get around?",
                "How satisfied are you with your sleep?",
                "How satisfied are you with your ability to perform your daily living activities?",
                "How satisfied are you with your capacity for work?",
                "How satisfied are you with yourself?",
                "How satisfied are you with your personal relationships?",
                "How satisfied are you with your weight?",
                "How satisfied are you with the support you get from your friends?",
                "How satisfied are you with the conditions of your living place?",
                "How satisfied are you with your access to health services?",
                "How satisfied are you with your transport?",
                "How often do you have negative feelings such as blue mood, despair, anxiety, depression?"]
    for i, op in enumerate(options):
        options[i] = "Quality of Life: " + op

    table = "ScaleQuestionAndOption"
    field = "option"

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale5:")
    create_scale_qa(scale_questions.filter(option = options[0]), scale_answers)

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale6:")
    create_scale_qa(scale_questions.filter(option = options[1]), scale_answers)
    
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale7:")
    create_scale_qa(scale_questions.filter(option__in = options[2:6]), scale_answers)

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale8:")
    create_scale_qa(scale_questions.filter(option__in = options[6:9]), scale_answers)
 
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale11:")
    create_scale_qa(scale_questions.filter(option__in = options[9:14]), scale_answers)

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale5:")
    create_scale_qa(scale_questions.filter(option = options[14]), scale_answers)

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale6:")
    create_scale_qa(scale_questions.filter(option__in = options[15:25]), scale_answers)

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale9:")
    create_scale_qa(scale_questions.filter(option = options[25]), scale_answers)

    scale_questions = QuestionOption.objects.filter(option__contains = "Last Two Weeks: ")
    options = [ "To what extent do impairments to your senses (e.g., hearing, vision, taste, smell, touch) affect your daily life?",
                "To what extent does loss of, for example, hearing, vision, taste, smell, or touch affect your ability to participate in activities?",
                "How much freedom do you have to make your own decisions?",
                "To what extent do you feel in control of your future?",
                "How much do you feel that the people around you are respectful of your freedom?",
                "To what extent do problems with your sensory functioning (e.g., hearing, vision, taste, smell, touch) affect your ability to interact with others?",
                "To what extent are you able to do the things you'd like to do?",
                "How would you rate your sensory functioning (e.g., hearing, vision, taste, smell, touch)?"]
    for i, op in enumerate(options):
        options[i] = "Last Two Weeks: " + op
    
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale7:")
    create_scale_qa(scale_questions.filter(option__in = options[0:3]), scale_answers)

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale10:")
    create_scale_qa(scale_questions.filter(option__in = options[3:5]), scale_answers)

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale11:")
    create_scale_qa(scale_questions.filter(option__in = options[5:7]), scale_answers)

    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale5:")
    create_scale_qa(scale_questions.filter(option__in = [options[7]]), scale_answers) # not found


    """
    cons tech (695) - NA; NA => Don't Have, others start at 1
    pers tech (722) - 0 index, NA; NA => N/A, others start at 0
    
    cell tech (732) - 0 index; 9 => NA, others start at 0 with NEVER
    comp tech (743) - 0 index; 9 => NA, others start at 0 with NEVER
    
    health tech (755) - NA; NA => Don't Have, others start at 1
    
    attitudes (785) - 0 index
    
    
    """

    scale_questions = QuestionOption.objects.filter(option__contains = "Technology: Consumer Technology Access and Use: ")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale12:")
    create_scale_qa(scale_questions, scale_answers, index_offset = 0, na_index = True)

    scale_questions = QuestionOption.objects.filter(option__contains = "Technology: Consumer Technology Personal Access and Use: ")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale13:")
    create_scale_qa(scale_questions, scale_answers, index_offset = -1, na_index = True) # [None, 0, 1 etc.]

    scale_questions = QuestionOption.objects.filter(option__contains = "Technology: Computer and Cellular Phone Use: Cell: ")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale14:")
    create_scale_qa(scale_questions, scale_answers, index_offset = 0)

    scale_questions = QuestionOption.objects.filter(option__contains = "Technology: Computer and Cellular Phone Use: Computer: ")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale14:")
    create_scale_qa(scale_questions, scale_answers, index_offset = 0)

    scale_questions = QuestionOption.objects.filter(option__contains = "Technology: Health Technology Access and Use: Listed Technologies: ")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale12:")
    create_scale_qa(scale_questions, scale_answers, index_offset = 0, na_index = True)

    scale_questions = QuestionOption.objects.filter(option__contains = "Technology: Confidence with Technology: ")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale15:")
    create_scale_qa(scale_questions, scale_answers)

    scale_questions = QuestionOption.objects.filter(option__contains = "Technology: Attitudes Toward Information Technology: ")
    scale_answers = AnswerOption.objects.filter(unique_name__icontains = "scale16:")
    create_scale_qa(scale_questions, scale_answers, index_offset = 0)


def addAnswerOptions(answerOptions,table,field,options,ordered = False, unique_names = None, orders = None):
    for i, op in enumerate(options):
        new_option = AnswerOption(option = op, is_default = True, table = table, field = field)
        if ordered:
            if orders:
                new_option.order = orders[i]
            else:
                new_option.order = i+1
        if unique_names:
            new_option.unique_name = unique_names[i]
        answerOptions.append(new_option)

def addQuestionOptions(questionOptions,table,field,options,ordered = False, unique_names = None, short_names = None):
    for i, op in enumerate(options):
        new_option = QuestionOption(option = op, is_default = True, table = table, field = field)
        if ordered:
            new_option.order = i+1
        if unique_names:
            new_option.unique_name = unique_names[i]
        if short_names:
            new_option.short_name = short_names[i]
        questionOptions.append(new_option)

# Used b/c no bulk_create in Django 1.3
def bulk_create_wrapper(objects):
    for obj in objects:
        obj.save()

# index_offset = 1; start numbering at 1
# if na_index == True, first AnswerOption is associated with order == None
def create_scale_qa(scale_questions, scale_answers, index_offset = 1, na_index = False):
    for q in scale_questions:
        for i, a in enumerate(scale_answers):
            if i == 0 and na_index:
                ScaleQuestionAndOption.objects.create(question = q, option = a, order = None)
            else:
                ScaleQuestionAndOption.objects.create(question = q, option = a, order = i + index_offset)

# scale_list is a list of strings in order specifying the 
# returns a list of AnswerOption objects ordered the same as the options in scale_list
def filterAnswerOptionRetainListOrder(scale_list, table = "ScaleQuestionAndOption", field = "option"):    
    scale_answers = AnswerOption.objects.filter(option__in = scale_list, table = table, field = field)
    return [scale_answers.get(option = scale_option) for scale_option in scale_list]
                
