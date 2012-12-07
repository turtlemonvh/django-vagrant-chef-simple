"""
MODULE NOTES

Approach:
+++++++++++++++++++
Class per survey table with functions for dealing with data

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SPSS Data Tranformations (from Vanessa):
mean.x notation: http://www.ats.ucla.edu/stat/spss/modules/functions.htm
- assign missing value if # non-missing values < x, else take avg of supplied (non-missing) values


SPS: 1:
Clean up induction interview values
Induction Interview
Multiples pages (p.xx)
- convert everything with 'NA' on scale values to a value of 9
- convert all string number values (from above) to float values
- add on labels for numerical values (already handled for all I think)
- change all ft-in height values to in
- missing medication values default to 0
- med duration values from yr-mo to mo
** should also check that they did not accidently put a start year here, if so convert


SPS: 2:
Calculate FMA Score
Induction Interview
FMA (p.7-8)
- reverse scores (5-1 instead of 1-5)
- 50%+ response rate required
- SYSMIS - missing value, replace with calculated avaerage value
- calculate: section sums (DAILYS, EMOTF, ARMHF, MOBILF), FMA raw score, FMA std index,
    raw score for bother index, std bother index

SPS: 3
Calculate PROMIS Score
Induction Interview
Satisfaction with Social Roles and Activities (p.9)
- 50%+ response rate required
- SYSMIS - missing value, replace with calculated avaerage value
- calculate: get score from lookup value based on sum of responses

SPS 4:
Calculate WHOQOL scores
Induction Interview
Quality of Life (p. 10-12)
- reverse scores (5-1 instead of 1-5) for 3 of the questions in WHOQOL BREF and 3 in WHOQOL OLD
- 80%+ response rate required for WHOQOL BREF and WHOQOL OLD
- calculate: WHOQOL BREF, sub-section (QOLHEALTH, QOLPSYCH, QOLSOCIAL, QOLENVIR), WHOQOL OLD, 
        sub-section (QOLSENSE, QOLAUT)

SPS 5:
Calculate Tech Efficacy Score
Induction Interview
- missing = 0
- calculate: score

SPS 6: 
Calculate Tech Attitude Rating
Induction Interview
- 50%+ response rate required

SPS 7: 
Calculate SPMSQ and IADL scores
Administered Instruments
- 50%+ response rate required
- SPMSQ: missing data = false response
- SPMSQ: flip value [so high is good]
- IADL: convert response index to score
- calculate: SPMSQTest, SPMSQ, IADLTest, IADL

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Class                Corresponding survey        Commented?        Submission Dates
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
lime_survey_58382    Administered Instruments      y                3/29/2012 - 8/27/2012
lime_survey_61262    Initial Interview             y                3/28/2012 - 8/25/2012  NOTE: This is no longer included for data privacy reasons
lime_survey_49672    Home inventory                n                4/27/2012 - 8/27/2012
lime_survey_65387    Induction Interview           y                6/24/2012 - 8/27/2012
lime_survey_98517    Induction Interview?          y (= 65387)      8/08/2012 - 8/27/2012

see this site to visualize: http://localhost:7000/browser/test_import/


NOTES:
===========
(yes/no) = Y/N

58382
- import is pretty much done
- need to add fields for notes

61262
- even the people with the PO box said mail address = home address, and no second address recorded

49672
- # fields includes label field
- entrance (15 fields, 9 repeats [lettered]):
    - FIELDS: location (links); location (other); floor (links); floor (other); nsteps; t_stairs(link); t_stairs (other); door width (ft); door width (in)
                threshheight(link); threshheight(other); wheelchair (y/n); use_freq (link); comments

- room (17 fields, 30 repeats):
    - FIELDS: type (links); type (other); location (links); location (other); entrance letter (link, including X for none); t_floor(link); t_floor (other); use_freq (link);
                room width (ft); room width (in); room length (ft); room length (in); power? (y/n); cable? (y/n); phone? (y/n); comments

- interior door (10 fields, 30 repeats):
    - FIELDS: room 1 (links); room 1 (other); room 2 (links); room 2 (other); door width (ft); door width (in); threshheight(link); threshheight(other); comments

- interior stair (13 fields, 9 repeats):
    - FIELDS: room 1 (links); room 1 (other); room 2 (links); room 2 (other); location (links); location (other); nsteps; t_stairs(link); t_stairs (other); 
                narrowest width (ft); narrowest width (in); comments

65387
- medications; add answer option: how often
- in FMA ratings, #25 is missing (but xx is there)
- has exactly same # fields as 98517
- 98517 is an "update" of this data
    - confirmed by looking at field types, numering, etc in Excel
    - perhaps incomplete?
    - uses different links to diff answer options, aside from that, it's the same


"""

from .lime_survey_58382 import lime_survey_58382
from .lime_survey_49672 import lime_survey_49672
from .lime_survey_65387 import lime_survey_65387
