from django.conf.urls.defaults import patterns, include, url
from homesurvey.apps.survey_browser.views import *

from django.contrib import admin
admin.autodiscover()

"""

Start url:
http://localhost:8000/browser/

"""
# Keep most urls here
urlpatterns = patterns('homesurvey.apps.survey_browser.views',
    # IMPORT / EXPORT
    # url(r'^csv/$', 'upload_csv', name="convert_csv"),
    
    # HTML template output urls
    (r'^$', 'listTables'),
    (r'^test/$', 'listTables'),
    (r'^test_import/$', 'checkImport'),
    (r'^initialize_database/$', 'initializeDatabase'),
    
    (r'^filter/$', 'filterParticipants'),
    (r'^filter/filteroptions/$', 'getFilterOptions'),
    (r'^filter/visualizemeta/$', 'visualizeMeta'),
    (r'^filter/filterdependencies/$', 'getFilterDependencies'),
    (r'^filter/filterform/$', 'getValueFilterForm'), # multi-select choices
    
    (r'^filtergroup/manage/$', 'manageFilterGroups'),
    (r'^filtergroup/filtertable/$', 'visualizeFilterGroup'), # /browser/filtergroup/filtertable/?group-id=1
    
    (r'^filter/participants/$', 'participantsMatchingFilter'), # returns html
    (r'^filter/views/groups/$', 'setFilterGroups'),
    (r'^filter/views/create/$', 'createFilters'),
    (r'^filter/views/create_meta/$', 'createMetaFilters'),
    (r'^filter/views/browse/$', 'browseFilters'),
    
    # Bulk actions
    (r'^filter/actions/addfilterstogroup/$', 'addFiltersToGroup'),
    (r'^filter/actions/removefiltersfromgroup/$', 'removeFiltersFromGroup'),
    
    
    (r'^update/$', 'checkUpdateDatabase'),
    (r'^update/runupdate/$', 'updateDatabase'),
    (r'^update/progresscheck/$', 'checkUpdateProgress'),
    
    (r'^download/csv/$', 'downloadCSV'),
    
    
    
    
)