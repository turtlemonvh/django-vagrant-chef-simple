from django.db import connection
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist

from survey_browser.models import Participant, ParticipantScaleRatings, ParticipantScaleRatingScores, ScaleQuestionAndOption, ParticipantMobilityHealth
from survey_browser.models import IADL, TUG, SPMSQ, ParticipantInductionStatic, ParticipantInductionVolatile, HomeInventory

"""
Function takes pids and returns all survey data for latest pci for that table

export_selections = an optional list of integers denoting the fields to export

All are implemented, but:
- HomeInventory needs to be extended
- ParticipantMobilityHealth's output needs to be separated out into smaller columns instead of concatenating fields into strings

"""
def get_export_options():
    tmp_dict = {}
    tmp_dict[0] = {'formatted_name': "Survey Scores and Ratings", 'class': ParticipantScaleRatings}
    tmp_dict[1] = {'formatted_name': "Mobility and Health", 'class': ParticipantMobilityHealth}
    tmp_dict[2] = {'formatted_name': "IADL", 'class': IADL}
    tmp_dict[3] = {'formatted_name': "TUG", 'class': TUG}
    tmp_dict[4] = {'formatted_name': "SPMSQ", 'class': SPMSQ}
    tmp_dict[5] = {'formatted_name': "Static Induction Data", 'class': ParticipantInductionStatic}
    tmp_dict[6] = {'formatted_name': "Volatile Induction Data", 'class': ParticipantInductionVolatile}
    tmp_dict[7] = {'formatted_name': "Home Inventory", 'class': HomeInventory}
    return tmp_dict

def get_export_dict(pids, names = False, export_selections = range(8)):
    options = map(lambda t: t['class'], get_export_options().values())
    
    selected_options = []
    for i in export_selections:
        selected_options.append(options[i])
    
    # Set up ordered header
    ordered_header = ['pid']
    for class_obj in selected_options:
        ordered_header.extend( class_obj.get_csv_label_list())
    
    # Set up data
    export_list = []
    for pid in pids:
        tmp_dict = {'pid': pid}
        p = Participant.objects.get(pid = pid)

        for class_obj in selected_options:
            if class_obj.__name__ == "ParticipantInductionStatic":
                try:
                    obj = class_obj.objects.get(participant = p)
                    tmp_dict.update(obj.get_value_dict(names))
                except ObjectDoesNotExist:
                    pass
            else:
                # Get data for the latest contact instance
                objs = class_obj.objects.filter(contact_instance__participant = p)
                if objs.exists():
                    obj = objs.latest()
                    tmp_dict.update(obj.get_value_dict(names))
        
        # cleanup
        if 'id' in tmp_dict:
            del tmp_dict['id']
        
        export_list.append(tmp_dict)

    return (ordered_header, export_list)