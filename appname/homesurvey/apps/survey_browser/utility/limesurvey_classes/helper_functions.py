"""
Helper functions
"""
def handle_null_or_blank(survey_field, default):
    if survey_field is None or survey_field == "" or survey_field == "-oth-":
        return default
    else:
        return survey_field