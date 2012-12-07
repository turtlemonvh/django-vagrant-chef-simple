from django.db import connection
from django.utils import simplejson

def get_field_list_dict():
    ms = connection.introspection.installed_models([t if "survey_browser" in t else None for t in connection.introspection.table_names()])
    return dict((m._meta.module_name, [f.name for f in m._meta.fields]) for m in ms)

def get_filter_option_dict():
    # Get models
    ms = connection.introspection.installed_models([t if "survey_browser" in t else None for t in connection.introspection.table_names()])
    
    # Gather items into list then cast into dict
    pre_dict = dict(reduce(lambda x, m: m._get_filter_fields().items() + x, ms, []))
    #print pre_dict
    
    # Clean up entries with no members
    for k, v in pre_dict.items():
        if not v:
            del pre_dict[k]
        if "options" in v:
            for k,o in v["options"].items():
                o["is_selected"] = False
                o["label"] = o["name"]
                if "is_default" not in o:
                    o["is_default"] = True
    return pre_dict

