"""
Induction Interview




"""
from django.core.exceptions import ObjectDoesNotExist

from survey_browser.models import Participant, ParticipantContactInstance, LimeToken
from survey_browser.models import AnswerOption, QuestionOption
from survey_browser.models import ParticipantInductionVolatile, ParticipantInductionStatic, ParticipantSurgeries, ParticipantMobilityHealth, \
                                  ParticipantMedicalCondition, ParticipantMedication, ParticipantScaleRatings, ScaleQuestionAndOption

from helper_functions import handle_null_or_blank

class lime_survey_65387:
    col_names = ["id",
            "submitdate",
            "lastpage",
            "startlanguage",
            "token",
            "65387X222X12597", # education; links answers
            "65387X222X12598", # marital; links answers
            "65387X222X12598other", # marital; other
            "65387X222X12599", # n perm res
            "65387X222X126001", # start perm res options, 5 options total??; maybe only after "No additional people" is shown
            "65387X222X126002", 
            "65387X222X126003",
            "65387X222X126004", # end perm res options
            "65387X222X12600other", # perm res other
            "65387X222X12606", # us citizen
            "65387X222X12607", # hisp lat; links answers
            "65387X222X12607other", # hisp lat; other
            "65387X222X126121", # start race and comment
            "65387X222X126121comment",
            "65387X222X126122",
            "65387X222X126122comment",
            "65387X222X126123",
            "65387X222X126123comment",
            "65387X222X126124",
            "65387X222X126124comment",
            "65387X222X126125",
            "65387X222X126125comment",
            "65387X222X126126",
            "65387X222X126126comment",
            "65387X222X126127",
            "65387X222X126127comment",
            "65387X222X126128",
            "65387X222X126128comment",
            "65387X222X126129",
            "65387X222X126129comment",
            "65387X222X1261210",
            "65387X222X1261210comment",
            "65387X222X1261211",
            "65387X222X1261211comment",
            "65387X222X1261212",
            "65387X222X1261212comment",
            "65387X222X1261213",
            "65387X222X1261213comment",
            "65387X222X1261214",
            "65387X222X1261214comment",
            "65387X222X1261215",
            "65387X222X1261215comment",  # start race and comment
            "65387X222X12628", # house type; links answers
            "65387X222X12628other", # house type; other
            "65387X222X12629", # income
            "65387X222X126301", # occ status start
            "65387X222X126301comment", # occ, present
            "65387X222X126302",
            "65387X222X126302comment", # occ, present
            "65387X222X126303",
            "65387X222X126303comment", # occ, present
            "65387X222X126304",
            "65387X222X126304comment", # [blank]
            "65387X222X126305",
            "65387X222X126305comment", # [blank]
            "65387X222X126306",
            "65387X222X126306comment", # occ, past
            "65387X222X126307",
            "65387X222X126307comment", # occ status end; "other"
            "65387X222X12639",  # retire year
            "65387X222X12640", # leave home freq; links answers
            "65387X222X126411", # leave home reason; start (yes/no)
            "65387X222X126412",
            "65387X222X126413",
            "65387X222X126414",
            "65387X222X126415",
            "65387X222X126416", # leave home reason; end
            "65387X222X12642", # tranport diff (yes/no)
            "65387X223X12643", # gender; links answers
            "65387X223X12644Ft", # ht, ft
            "65387X223X12644In", # ht, in
            "65387X223X12647", # wt, lbs
            "65387X223X126481", # start ass dev (y/n)
            "65387X223X126482",
            "65387X223X126483",
            "65387X223X126484",
            "65387X223X126485", # end ass dev
            "65387X223X126541", # start mob aids (y/n)
            "65387X223X126542",
            "65387X223X126543",
            "65387X223X126544",
            "65387X223X126545",
            "65387X223X126546",
            "65387X223X12654other", # end mob aids
            "65387X223X12662", # level of activity; links answers
            "65387X224X12663", # start missing fields [labels for table]
            "65387X224X12664",
            "65387X224X12665", # end missing fields
            "65387X224X12666", # surgey 1: blank[label], year, surgery
            "65387X224X12667",
            "65387X224X12668",
            "65387X224X12669", # surgey 2: blank[label], year, surgery
            "65387X224X12670",
            "65387X224X12671",
            "65387X224X12672", # surgey 3: blank[label], year, surgery
            "65387X224X12673",
            "65387X224X12674",
            "65387X224X12675", # surgey 4: blank[label], year, surgery
            "65387X224X12676",
            "65387X224X12677",
            "65387X224X12678", # surgey 5: blank[label], year, surgery
            "65387X224X12679",
            "65387X224X12680",
            "65387X224X12681", # surgey 6: blank[label], year, surgery
            "65387X224X12682",
            "65387X224X12683",
            "65387X224X12684", # surgey 7: blank[label], year, surgery
            "65387X224X12685",
            "65387X224X12686",
            "65387X224X12687", # surgey 8: blank[label], year, surgery
            "65387X224X12688",
            "65387X224X12689",
            "65387X226X126971", # start medical conditions; links to asnwers
            "65387X226X126972",
            "65387X226X126973",
            "65387X226X126974",
            "65387X226X126975",
            "65387X226X126976",
            "65387X226X126977",
            "65387X226X126978",
            "65387X226X126979",
            "65387X226X1269710",
            "65387X226X1269711",
            "65387X226X1269712",
            "65387X226X1269713",
            "65387X226X1269714",
            "65387X226X1269715",
            "65387X226X1269716",
            "65387X226X1269717",
            "65387X226X1269718",
            "65387X226X1269719",
            "65387X226X1269720",
            "65387X226X1269721",
            "65387X226X1269722",
            "65387X226X1269723",
            "65387X226X1269724",
            "65387X226X1269725",
            "65387X226X1269726",
            "65387X226X1269727",
            "65387X226X1269728",
            "65387X226X1269729",
            "65387X226X1269730",  # end medical conditions
            "65387X226X127301", # start medical conditions onset year; may be null
            "65387X226X127302",
            "65387X226X127303",
            "65387X226X127304",
            "65387X226X127305",
            "65387X226X127306",
            "65387X226X127307",
            "65387X226X127308",
            "65387X226X127309",
            "65387X226X1273010",
            "65387X226X1273011",
            "65387X226X1273012",
            "65387X226X1273013",
            "65387X226X1273014",
            "65387X226X1273015",
            "65387X226X1273016",
            "65387X226X1273017",
            "65387X226X1273018",
            "65387X226X1273019",
            "65387X226X1273020",
            "65387X226X1273021",
            "65387X226X1273022",
            "65387X226X1273023",
            "65387X226X1273024",
            "65387X226X1273025",
            "65387X226X1273026",
            "65387X226X1273027",
            "65387X226X1273028",
            "65387X226X1273029",
            "65387X226X1273030", # end medical conditions onset year
            "65387X228X12770", # start empty; table layout setup
            "65387X228X12771",
            "65387X228X12772",
            "65387X228X12773",
            "65387X228X12774",
            "65387X228X12775",
            "65387X228X12776",
            "65387X228X12793",
            "65387X228X12787",
            "65387X228X12788",
            "65387X228X12789",
            "65387X228X12790",
            "65387X228X12791",
            "65387X228X12792",
            "65387X228X12777", # med 1: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X12778",
            "65387X228X12779",
            "65387X228X12781",
            "65387X228X12781other",
            "65387X228X12782",
            "65387X228X12783Yr",
            "65387X228X12783Mo",
            "65387X228X12786",
            "65387X228X12794", # med 2: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X12795",
            "65387X228X12796",
            "65387X228X12797",
            "65387X228X12797other",
            "65387X228X12798",
            "65387X228X12799Yr",
            "65387X228X12799Mo",
            "65387X228X12802",
            "65387X228X12803", # med 3: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X12804",
            "65387X228X12805",
            "65387X228X12806",
            "65387X228X12806other",
            "65387X228X12807",
            "65387X228X12808Yr",
            "65387X228X12808Mo",
            "65387X228X12811",
            "65387X228X13278", # med 4: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13279",
            "65387X228X13280",
            "65387X228X13281",
            "65387X228X13281other",
            "65387X228X13282",
            "65387X228X13283Yr",
            "65387X228X13283Mo",
            "65387X228X13286",
            "65387X228X13287", # med 5: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13288",
            "65387X228X13289",
            "65387X228X13290",
            "65387X228X13290other",
            "65387X228X13291",
            "65387X228X13292Yr",
            "65387X228X13292Mo",
            "65387X228X13295",
            "65387X228X13314", # start re-label [blank]
            "65387X228X13315",
            "65387X228X13316",
            "65387X228X13317",
            "65387X228X13318",
            "65387X228X13319",
            "65387X228X13320", # end re-label
            "65387X228X13296", # med 6: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13297",
            "65387X228X13298",
            "65387X228X13299",
            "65387X228X13299other",
            "65387X228X13300",
            "65387X228X13301Yr",
            "65387X228X13301Mo",
            "65387X228X13304",
            "65387X228X13305", # med 7: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13306",
            "65387X228X13307",
            "65387X228X13308",
            "65387X228X13308other",
            "65387X228X13309",
            "65387X228X13310Yr",
            "65387X228X13310Mo",
            "65387X228X13313",
            "65387X228X13321", # med 8: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13322",
            "65387X228X13323",
            "65387X228X13324",
            "65387X228X13324other",
            "65387X228X13325",
            "65387X228X13326Yr",
            "65387X228X13326Mo",
            "65387X228X13329",
            "65387X228X13330",# med 8: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13331",
            "65387X228X13332",
            "65387X228X13333",
            "65387X228X13333other",
            "65387X228X13334",
            "65387X228X13335Yr",
            "65387X228X13335Mo",
            "65387X228X13338",
            "65387X228X13339",# med 10: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13340",
            "65387X228X13341",
            "65387X228X13342",
            "65387X228X13342other",
            "65387X228X13343",
            "65387X228X13344Yr",
            "65387X228X13344Mo",
            "65387X228X13347",
            "65387X228X13348", # start re-label [blank]
            "65387X228X13349",
            "65387X228X13350",
            "65387X228X13351",
            "65387X228X13352",
            "65387X228X13353",
            "65387X228X13354", # end re-label
            "65387X228X13355", # med 11: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13356",
            "65387X228X13357",
            "65387X228X13358",
            "65387X228X13358other",
            "65387X228X13359",
            "65387X228X13360Yr",
            "65387X228X13360Mo",
            "65387X228X13363",
            "65387X228X13364", # med 12: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13365",
            "65387X228X13366",
            "65387X228X13367",
            "65387X228X13367other",
            "65387X228X13368",
            "65387X228X13369Yr",
            "65387X228X13369Mo",
            "65387X228X13372",
            "65387X228X13373", # med 13: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13374",
            "65387X228X13375",
            "65387X228X13376",
            "65387X228X13376other",
            "65387X228X13377",
            "65387X228X13378Yr",
            "65387X228X13378Mo",
            "65387X228X13381",
            "65387X228X13382", # med 14: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13383",
            "65387X228X13384",
            "65387X228X13385",
            "65387X228X13385other",
            "65387X228X13386",
            "65387X228X13387Yr",
            "65387X228X13387Mo",
            "65387X228X13390",
            "65387X228X13391", # med 15: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13392",
            "65387X228X13393",
            "65387X228X13394",
            "65387X228X13394other",
            "65387X228X13395",
            "65387X228X13396Yr",
            "65387X228X13396Mo",
            "65387X228X13399",
            "65387X228X13400", # start re-label [blank]
            "65387X228X13401",
            "65387X228X13402",
            "65387X228X13403",
            "65387X228X13404",
            "65387X228X13405",
            "65387X228X13406",
            "65387X228X13407", # med 16: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13408",
            "65387X228X13409",
            "65387X228X13410",
            "65387X228X13410other",
            "65387X228X13411",
            "65387X228X13412Yr",
            "65387X228X13412Mo",
            "65387X228X13415",
            "65387X228X13416", # med 17: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13417",
            "65387X228X13418",
            "65387X228X13419",
            "65387X228X13419other",
            "65387X228X13420",
            "65387X228X13421Yr",
            "65387X228X13421Mo",
            "65387X228X13424",
            "65387X228X13425", # med 18: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13426",
            "65387X228X13427",
            "65387X228X13428",
            "65387X228X13428other",
            "65387X228X13429",
            "65387X228X13430Yr",
            "65387X228X13430Mo",
            "65387X228X13433",
            "65387X228X13434", # med 19: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13435",
            "65387X228X13436",
            "65387X228X13437",
            "65387X228X13437other",
            "65387X228X13438",
            "65387X228X13439Yr",
            "65387X228X13439Mo",
            "65387X228X13442",
            "65387X228X13443", # med 20: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X228X13444",
            "65387X228X13445",
            "65387X228X13446",
            "65387X228X13446other",
            "65387X228X13447",
            "65387X228X13448Yr",
            "65387X228X13448Mo",
            "65387X228X13451",
            "65387X241X13667", # start label OTC medications [blank]
            "65387X241X13668",
            "65387X241X13669",
            "65387X241X13670",
            "65387X241X13671",
            "65387X241X13672",
            "65387X241X13673",
            "65387X241X13674",
            "65387X241X13675",
            "65387X241X13676",
            "65387X241X13677",
            "65387X241X13678",
            "65387X241X13679",
            "65387X241X13680", # end label OTC medications
            "65387X241X13681", # otc med 1: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13682",
            "65387X241X13683",
            "65387X241X13684",
            "65387X241X13684other",
            "65387X241X13685",
            "65387X241X13686Yr",
            "65387X241X13686Mo",
            "65387X241X13687",
            "65387X241X13688", # otc med 2: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13689",
            "65387X241X13690",
            "65387X241X13691",
            "65387X241X13691other",
            "65387X241X13692",
            "65387X241X13693Yr",
            "65387X241X13693Mo",
            "65387X241X13694",
            "65387X241X13695", # otc med 3: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13696",
            "65387X241X13697",
            "65387X241X13698",
            "65387X241X13698other",
            "65387X241X13699",
            "65387X241X13700Yr",
            "65387X241X13700Mo",
            "65387X241X13701",
            "65387X241X13702", # otc med 4: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13703",
            "65387X241X13704",
            "65387X241X13705",
            "65387X241X13705other",
            "65387X241X13706",
            "65387X241X13707Yr",
            "65387X241X13707Mo",
            "65387X241X13708",
            "65387X241X13709", # otc med 5: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13710",
            "65387X241X13711",
            "65387X241X13712",
            "65387X241X13712other",
            "65387X241X13713",
            "65387X241X13714Yr",
            "65387X241X13714Mo",
            "65387X241X13715",
            "65387X241X13716", # start re-label [blank]
            "65387X241X13717",
            "65387X241X13718",
            "65387X241X13719",
            "65387X241X13720",
            "65387X241X13721",
            "65387X241X13722",
            "65387X241X13723", # otc med 6: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13724",
            "65387X241X13725",
            "65387X241X13726",
            "65387X241X13726other",
            "65387X241X13727",
            "65387X241X13728Yr",
            "65387X241X13728Mo",
            "65387X241X13729",
            "65387X241X13730", # otc med 7: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13731",
            "65387X241X13732",
            "65387X241X13733",
            "65387X241X13733other",
            "65387X241X13734",
            "65387X241X13735Yr",
            "65387X241X13735Mo",
            "65387X241X13736",
            "65387X241X13737", # otc med 8: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13738",
            "65387X241X13739",
            "65387X241X13740",
            "65387X241X13740other",
            "65387X241X13741",
            "65387X241X13742Yr",
            "65387X241X13742Mo",
            "65387X241X13743",
            "65387X241X13744", # otc med 9: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13745",
            "65387X241X13746",
            "65387X241X13747",
            "65387X241X13747other",
            "65387X241X13748",
            "65387X241X13749Yr",
            "65387X241X13749Mo",
            "65387X241X13750",
            "65387X241X13751", # otc med 10: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13752",
            "65387X241X13753",
            "65387X241X13754",
            "65387X241X13754other",
            "65387X241X13755",
            "65387X241X13756Yr",
            "65387X241X13756Mo",
            "65387X241X13757",
            "65387X241X13758", # start re-label [blank]
            "65387X241X13759",
            "65387X241X13760",
            "65387X241X13761",
            "65387X241X13762",
            "65387X241X13763",
            "65387X241X13764",
            "65387X241X13765", # otc med 11: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13766",
            "65387X241X13767",
            "65387X241X13768",
            "65387X241X13768other",
            "65387X241X13769",
            "65387X241X13770Yr",
            "65387X241X13770Mo",
            "65387X241X13771",
            "65387X241X13772", # otc med 12: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13773",
            "65387X241X13774",
            "65387X241X13775",
            "65387X241X13775other",
            "65387X241X13776",
            "65387X241X13777Yr",
            "65387X241X13777Mo",
            "65387X241X13778",
            "65387X241X13779", # otc med 13: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13780",
            "65387X241X13781",
            "65387X241X13782",
            "65387X241X13782other",
            "65387X241X13783",
            "65387X241X13784Yr",
            "65387X241X13784Mo",
            "65387X241X13785",
            "65387X241X13786",# otc med 14: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13787",
            "65387X241X13788",
            "65387X241X13789",
            "65387X241X13789other",
            "65387X241X13790",
            "65387X241X13791Yr",
            "65387X241X13791Mo",
            "65387X241X13792",
            "65387X241X13793", # otc med 15: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13794", 
            "65387X241X13795",
            "65387X241X13796",
            "65387X241X13796other",
            "65387X241X13797",
            "65387X241X13798Yr",
            "65387X241X13798Mo",
            "65387X241X13799",
            "65387X241X13800",  # start re-label [blank]
            "65387X241X13801",
            "65387X241X13802",
            "65387X241X13803",
            "65387X241X13804",
            "65387X241X13805",
            "65387X241X13806",
            "65387X241X13807", # otc med 16: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13808",
            "65387X241X13809",
            "65387X241X13810",
            "65387X241X13810other",
            "65387X241X13811",
            "65387X241X13812Yr",
            "65387X241X13812Mo",
            "65387X241X13813",
            "65387X241X13814", # otc med 17: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13815",
            "65387X241X13816",
            "65387X241X13817",
            "65387X241X13817other",
            "65387X241X13818",
            "65387X241X13819Yr",
            "65387X241X13819Mo",
            "65387X241X13820",
            "65387X241X13821", # otc med 18: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13822",
            "65387X241X13823",
            "65387X241X13824",
            "65387X241X13824other",
            "65387X241X13825",
            "65387X241X13826Yr",
            "65387X241X13826Mo",
            "65387X241X13827",
            "65387X241X13828", # otc med 19: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13829",
            "65387X241X13830",
            "65387X241X13831",
            "65387X241X13831other",
            "65387X241X13832",
            "65387X241X13833Yr",
            "65387X241X13833Mo",
            "65387X241X13834",
            "65387X241X13835", # otc med 20: label[blank], name, how much; how often[links to ans]; how often [other]; why; dur (yr); dur (mo); side effects
            "65387X241X13836",
            "65387X241X13837",
            "65387X241X13838",
            "65387X241X13838other",
            "65387X241X13839",
            "65387X241X13840Yr",
            "65387X241X13840Mo",
            "65387X241X13841", # section label [blank]
            "65387X230X128531", # start FMA rating; links to answer
            "65387X230X128532",
            "65387X230X128533",
            "65387X230X128534",
            "65387X230X128535",
            "65387X230X128536",
            "65387X230X128537",
            "65387X230X128538",
            "65387X230X128539",
            "65387X230X1285310",
            "65387X230X1285311",
            "65387X230X1285312",
            "65387X230X1285313",
            "65387X230X1285314",
            "65387X230X1285315",
            "65387X230X1285316",
            "65387X230X1285317",
            "65387X230X1285318",
            "65387X230X1285319",
            "65387X230X1285320",
            "65387X230X1285321",
            "65387X230X1285322", # 23 from paper
            "65387X230X1285323", # 24 from paper
            "65387X230X1285324", # 25 from paper
            "65387X230X12853xx", # xx from paper
            "65387X230X1287926", # 26 from paper; back on track
            "65387X230X1287927",
            "65387X230X1287928",
            "65387X230X1287929",
            "65387X230X1287930",
            "65387X230X1287931",
            "65387X230X1287932",
            "65387X230X1287933",
            "65387X230X1287934",
            "65387X230X1288935",
            "65387X230X1288936",
            "65387X230X1288937",
            "65387X230X1288938",
            "65387X230X1288939",
            "65387X230X1288940",
            "65387X230X1288941",
            "65387X230X1288942",
            "65387X230X1288943",
            "65387X230X1288944",
            "65387X230X1288945",
            "65387X230X1288946", # end FMA rating
            "65387X231X129021", # start social role rating; links to answer
            "65387X231X129022",
            "65387X231X129023",
            "65387X231X129024",
            "65387X231X129025",
            "65387X231X129026",
            "65387X231X129027",
            "65387X231X129028", # end social rating
            "65387X232X129111", # start QOL rating; links to answer
            "65387X232X129131",
            "65387X232X129153",
            "65387X232X129154",
            "65387X232X129155",
            "65387X232X129156",
            "65387X232X129207",
            "65387X232X129208",
            "65387X232X129209",
            "65387X232X1292710",
            "65387X232X1292711",
            "65387X232X1292712",
            "65387X232X1292713",
            "65387X232X1292714",
            "65387X232X1293315",
            "65387X232X1293516",
            "65387X232X1293517",
            "65387X232X1293518",
            "65387X232X1293519",
            "65387X232X1293520",
            "65387X232X12935xx",
            "65387X232X1293522",
            "65387X232X1293523",
            "65387X232X1293524",
            "65387X232X1293525",
            "65387X232X1294626", # end QOL rating
            "65387X242X129481", # start 2 week rating; links to answer
            "65387X242X129482",
            "65387X242X129483",
            "65387X242X129544",
            "65387X242X129545",
            "65387X242X1295910",
            "65387X242X1295911",
            "65387X242X1296620", # end 2 week rating
            "65387X233X129681", # start tech rating; links to answer
            "65387X233X129682",
            "65387X233X129683",
            "65387X233X129684",
            "65387X233X129685",
            "65387X233X129686",
            "65387X233X129687",
            "65387X233X129688",
            "65387X233X129689",
            "65387X233X1314610",
            "65387X233X1314611",
            "65387X233X1314612",
            "65387X233X1314613",
            "65387X233X1314614",
            "65387X233X1314615",
            "65387X233X1317416",
            "65387X233X1317417",
            "65387X233X1317418",
            "65387X233X1317419",
            "65387X233X1317420",
            "65387X233X1320221",
            "65387X233X1320222",
            "65387X233X1320223",
            "65387X233X1320224",
            "65387X233X1320225",
            "65387X233X1320226",
            "65387X233X1320227", # end tech rating
            "65387X233X129981", # start 2nd tech rating; links to answer (NA allowed as sep answer)
            "65387X233X129986",
            "65387X233X129987",
            "65387X233X129988",
            "65387X233X1299810",
            "65387X233X1299816",
            "65387X233X1299817",
            "65387X233X1299821",
            "65387X233X1299822", # end 2nd tech rating
            "65387X234X130261", # start cell and comp rating; links to answers
            "65387X234X130262",
            "65387X234X130263",
            "65387X234X130264",
            "65387X234X130265",
            "65387X234X130266",
            "65387X234X130267",
            "65387X234X130268",
            "65387X234X130269",
            "65387X234X1302610",
            "65387X234X1302611",
            "65387X234X1302612", # end cell
            "65387X234X131221",
            "65387X234X131222",
            "65387X234X131223",
            "65387X234X131224",
            "65387X234X131225",
            "65387X234X131226",
            "65387X234X131227",
            "65387X234X131228",
            "65387X234X131229",
            "65387X234X1312210",
            "65387X234X1312211", # end comp
            "65387X235X130501", # start health tech rating; links to answers
            "65387X235X130502",
            "65387X235X130503",
            "65387X235X130504",
            "65387X235X130505",
            "65387X235X130506",
            "65387X235X130507",
            "65387X235X130508", # end
            "65387X235X130781", # start add devices
            "65387X235X130782",
            "65387X235X130783",
            "65387X235X130784",
            "65387X235X130785", # end add device
            "65387X235X130841", # start add device ratings; links to answers
            "65387X235X130842",
            "65387X235X130843",
            "65387X235X130844",
            "65387X235X130845", # end add device ratings
            "65387X236X130901", # start tech confidence; links to answers
            "65387X236X130902",
            "65387X236X130903",
            "65387X236X130904",
            "65387X236X130905",
            "65387X236X130906",
            "65387X236X130907",
            "65387X236X130908",
            "65387X236X130909",
            "65387X236X1309010", # end tech confidence
            "65387X237X13101", # internet access (y/n)
            "65387X237X13102", # type of internet; links to answers
            "65387X237X13103", # wireless (y/n)
            "65387X238X131041", # start attitudes ratings; links to answers
            "65387X238X131042",
            "65387X238X131043",
            "65387X238X131044",
            "65387X238X131045",
            "65387X238X131046", # end attitudes ratings
            "65387X238X13111"] # notes

    def __init__(self, table_row, verbose = False, table_id = 65387):
        self.table_row = table_row
        if self.table_row[1] is not None and not "SAMPLE" in self.table_row[4]: # entries with no date are corrupted
            (self.participant, token_created, self.pci) = LimeToken.initializeRowImport(self.table_row[:5], table_id)
            
            # skip import if the token is already in the database
            if not token_created:
                return
            else:
                print "Adding token %s for survey %s" %(self.table_row[4], table_id)
            
            # Each function returns an array of objects that will be appended to the existing object array, which is passed into bulk_create at the end
            self.object_array = []
            self.save_ParticipantInductionVolatile()
            self.save_ParticipantInductionStatic()
            self.save_ParticipantMobilityHealth()
            self.save_ParticipantScaleRatings()
            
            # Keeping track of created objects
            if verbose:
                print self.object_array
    
    def save_ParticipantInductionVolatile(self):
        # education_level
        if self.table_row[5] is None or self.table_row[5] == "":
            education_level = AnswerOption.objects.get_or_create(option = "NA", table = "ParticipantInductionVolatile", field = "education_level")[0]
        else:
            education_level = AnswerOption.objects.get(order = int(self.table_row[5]), table = "ParticipantInductionVolatile", field = "education_level")

        # marital_status
        if self.table_row[6] is None or self.table_row[6] == "" or self.table_row[6] == "-oth-":
            marital_status = AnswerOption.objects.get_or_create(option = self.table_row[7], table = "ParticipantInductionVolatile", field = "marital_status")[0]
        else:
            marital_status = AnswerOption.objects.get(order = int(self.table_row[6]), table = "ParticipantInductionVolatile", field = "marital_status")

        # housing_type
        if self.table_row[47] is None or self.table_row[47] == "" or self.table_row[47] == "-oth-":
            housing_type = AnswerOption.objects.get_or_create(option = self.table_row[48], table = "ParticipantInductionVolatile", field = "housing_type")[0]
        else:
            housing_type = AnswerOption.objects.get(order = int(self.table_row[47]), table = "ParticipantInductionVolatile", field = "housing_type")

        # household_income
        if self.table_row[49] is None or self.table_row[49] == "":
            household_income = AnswerOption.objects.get_or_create(option = "NA", table = "ParticipantInductionVolatile", field = "household_income")[0]
        else:
            household_income = AnswerOption.objects.get(order = int(self.table_row[49]), table = "ParticipantInductionVolatile", field = "household_income")

        # leave_home_freq
        if self.table_row[65] is None or self.table_row[65] == "":
            leave_home_freq = AnswerOption.objects.get_or_create(option = "NA", table = "ParticipantInductionVolatile", field = "leave_home_freq")[0]
        else:
            leave_home_freq = AnswerOption.objects.get(order = int(self.table_row[65]), table = "ParticipantInductionVolatile", field = "leave_home_freq")

        # limited_tranport
        if self.table_row[72] == "Y":
            limited_tranport = True
        else:
            limited_tranport = False

        # has_home_internet
        if self.table_row[782] == "Y":
            has_home_internet = True
        else:
            has_home_internet = False

        # has_wireless_internet
        if self.table_row[784] == "Y":
            has_wireless_internet = True
        else:
            has_wireless_internet = False

        # type_of_internet
        if self.table_row[783] is None or self.table_row[783] == "":
            type_of_internet = AnswerOption.objects.get_or_create(option = "NA", table = "HomeInventory", field = "type_of_internet")[0]
        else:
            type_of_internet = AnswerOption.objects.get(order = int(self.table_row[783]), table = "HomeInventory", field = "type_of_internet")

        tmp = ParticipantInductionVolatile.objects.create(contact_instance = self.pci,
                                                          education_level = education_level,
                                                          marital_status = marital_status,
                                                          n_perm_residents = int(handle_null_or_blank(self.table_row[8],0)),
                                                          housing_type = housing_type,
                                                          household_income = household_income,
                                                          leave_home_freq = leave_home_freq,
                                                          limited_tranport = limited_tranport,
                                                          has_home_internet = has_home_internet,
                                                          has_wireless_internet = has_wireless_internet,
                                                          type_of_internet = type_of_internet)

        # perm_residents
        if self.table_row[13] is not None and self.table_row[13] != "":
            tmp.perm_residents.add(AnswerOption.objects.get_or_create(option = self.table_row[13], table = "ParticipantInductionVolatile", field = "perm_residents")[0])
        if self.table_row[9] == "Y":
            tmp.perm_residents.add(AnswerOption.objects.get(option = "Spouse", table = "ParticipantInductionVolatile", field = "perm_residents"))
        if self.table_row[10] == "Y":
            tmp.perm_residents.add(AnswerOption.objects.get(option = "Adult relatives, such as adult children, cousins, or in-laws", table = "ParticipantInductionVolatile", field = "perm_residents"))
        if self.table_row[11] == "Y":
            tmp.perm_residents.add(AnswerOption.objects.get(option = "Adult nonrelatives, such as roommates", table = "ParticipantInductionVolatile", field = "perm_residents"))
        if self.table_row[12] == "Y":
            tmp.perm_residents.add(AnswerOption.objects.get(option = "Children, under the age of 18", table = "ParticipantInductionVolatile", field = "perm_residents"))
        if tmp.perm_residents.count() == 0:
            tmp.perm_residents.add(AnswerOption.objects.get(option = "No additional people", table = "ParticipantInductionVolatile", field = "perm_residents"))

        # occupation_status and current_occupation
        if self.table_row[62] == "Y":
            tmp.occupation_status.add(AnswerOption.objects.get_or_create(option = self.table_row[63], table = "ParticipantInductionVolatile", field = "occupation_status")[0])
        if self.table_row[50] == "Y":
            tmp.occupation_status.add(AnswerOption.objects.get(option = "Work full-time", table = "ParticipantInductionVolatile", field = "occupation_status"))
            tmp.current_occupation.add(AnswerOption.objects.get_or_create(option = "Full time " + self.table_row[51], table = "ParticipantInductionVolatile", field = "current_occupation")[0])
        if self.table_row[52] == "Y":
            tmp.occupation_status.add(AnswerOption.objects.get(option = "Work part-time", table = "ParticipantInductionVolatile", field = "occupation_status"))
            tmp.current_occupation.add(AnswerOption.objects.get_or_create(option =  "Part time " + self.table_row[53], table = "ParticipantInductionVolatile", field = "current_occupation")[0])
        if self.table_row[54] == "Y":
            tmp.occupation_status.add(AnswerOption.objects.get(option = "Self-employed", table = "ParticipantInductionVolatile", field = "occupation_status"))
            tmp.current_occupation.add(AnswerOption.objects.get_or_create(option =  "Self employed " + self.table_row[55], table = "ParticipantInductionVolatile", field = "current_occupation")[0])
        if self.table_row[56] == "Y":
            tmp.occupation_status.add(AnswerOption.objects.get(option = "Homemaker", table = "ParticipantInductionVolatile", field = "occupation_status"))
        if self.table_row[58] == "Y":
            tmp.occupation_status.add(AnswerOption.objects.get(option = "Volunteer worker", table = "ParticipantInductionVolatile", field = "occupation_status"))
        if self.table_row[60] == "Y":
            tmp.occupation_status.add(AnswerOption.objects.get(option = "Retired", table = "ParticipantInductionVolatile", field = "occupation_status"))
            tmp.current_occupation.add(AnswerOption.objects.get_or_create(option = "Retired " + self.table_row[51], table = "ParticipantInductionVolatile", field = "current_occupation")[0])

        # leave_home_reasons
        if self.table_row[66] == "Y":
            tmp.leave_home_reasons.add(AnswerOption.objects.get(option = "Work", table = "ParticipantInductionVolatile", field = "leave_home_reasons"))
        if self.table_row[67] == "Y":
            tmp.leave_home_reasons.add(AnswerOption.objects.get(option = "Errands (post office, grocery store, etc.)", table = "ParticipantInductionVolatile", field = "leave_home_reasons"))
        if self.table_row[68] == "Y":
            tmp.leave_home_reasons.add(AnswerOption.objects.get(option = "Social activities (church, restaurant, entertainment, etc.)", table = "ParticipantInductionVolatile", field = "leave_home_reasons"))
        if self.table_row[69] == "Y":
            tmp.leave_home_reasons.add(AnswerOption.objects.get(option = "Activities around the home (walking to the mailbox, gardening, etc.)", table = "ParticipantInductionVolatile", field = "leave_home_reasons"))
        if self.table_row[70] == "Y":
            tmp.leave_home_reasons.add(AnswerOption.objects.get(option = "Doctor/medical appointments", table = "ParticipantInductionVolatile", field = "leave_home_reasons"))
        if self.table_row[71] == "Y":
            tmp.leave_home_reasons.add(AnswerOption.objects.get(option = "Emergencies", table = "ParticipantInductionVolatile", field = "leave_home_reasons"))

        tmp.save()
        self.object_array.append(tmp)

    def save_ParticipantInductionStatic(self):
        # us_citizen
        if self.table_row[14] == "Y":
            us_citizen = True
        else:
            us_citizen = False        
        
        # hisp_latino
        if self.table_row[15] is None or self.table_row[15] == "" or self.table_row[15] == "-oth-":
            hisp_latino = AnswerOption.objects.get_or_create(option = self.table_row[16], table = "ParticipantInductionStatic", field = "hisp_latino")[0]
        else:
            hisp_latino = AnswerOption.objects.get(order = int(self.table_row[15]) + 1, table = "ParticipantInductionStatic", field = "hisp_latino")

        # retirement_year
        if self.table_row[64] is not None and self.table_row[15] != "":
            retirement_year = int(self.table_row[64])
        else:
            retirement_year = None

        # gender
        if self.table_row[73] == "M":
            gender = AnswerOption.objects.get(option = "Male", table = "ParticipantInductionStatic", field = "gender")
        elif self.table_row[73] == "F":
            gender = AnswerOption.objects.get(option = "Female", table = "ParticipantInductionStatic", field = "gender")
        else:
            gender = AnswerOption.objects.get_or_create(option = self.table_row[73], table = "ParticipantInductionStatic", field = "gender")[0]

        tmp = ParticipantInductionStatic.objects.create(  participant = self.participant,
                                                          us_citizen = us_citizen,
                                                          hisp_latino = hisp_latino,
                                                          retirement_year = retirement_year,
                                                          gender = gender,
                                                          racial_origin_comments = "")

        # racial_origin
        racial_origin_comments = ""
        if self.table_row[17] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "White", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "White comments: " + self.table_row[18] + ", "
        if self.table_row[19] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Black, African American, or Negro", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Black, African American, or Negro comments: " + self.table_row[20] + ", "
        if self.table_row[21] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "American Indian or Alaska Native", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "American Indian or Alaska Native comments: " + self.table_row[22] + ", "
        if self.table_row[23] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Asian Indian", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Asian Indian comments: " + self.table_row[22] + ", "
        if self.table_row[25] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Chinese", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Chinese comments: " + self.table_row[22] + ", "
        if self.table_row[27] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Filipino", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Filipino comments: " + self.table_row[22] + ", "
        if self.table_row[29] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Japanese", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Japanese comments: " + self.table_row[22] + ", "
        if self.table_row[31] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Vietnamese", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Vietnamese comments: " + self.table_row[22] + ", "
        if self.table_row[33] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Guamanian or Chamorro", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Guamanian comments: " + self.table_row[22] + ", "
        if self.table_row[35] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Native Hawaiian", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Native Hawaiian comments: " + self.table_row[22] + ", "
        if self.table_row[37] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Samoan", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Samoan comments: " + self.table_row[22] + ", "
        if self.table_row[39] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Other Asian", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Other Asian comments: " + self.table_row[22] + ", "    
        if self.table_row[41] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Other Pacific Islander", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Other Pacific Islander comments: " + self.table_row[22] + ", "
        if self.table_row[43] == "Y":
            tmp.racial_origin.add(AnswerOption.objects.get(option = "Some other race", table = "ParticipantInductionStatic", field = "racial_origin"))
            racial_origin_comments = racial_origin_comments + "Some other race comments: " + self.table_row[22] + ", "

        tmp.racial_origin_comments = racial_origin_comments;
        tmp.save()
        self.object_array.append(tmp)
    
    # ParticipantMobilityHealth
    def save_ParticipantMobilityHealth(self):
        # physical_activity
        if self.table_row[89] is None or self.table_row[89] == "":
            physical_activity = AnswerOption.objects.get_or_create(option = "NA", table = "ParticipantMobilityHealth", field = "physical_activity")[0]
        else:
            physical_activity = AnswerOption.objects.get(order = int(self.table_row[89]), table = "ParticipantMobilityHealth", field = "physical_activity")

        # ht_in
        try:
            ht_ft = float(self.table_row[74])
        except (TypeError, ValueError):
            ht_ft = 0
        try:
            ht_in = float(self.table_row[75])
        except (TypeError, ValueError):
            ht_in = 0
        total_ht = ht_ft*12.0 + ht_in

        # wt_lbs
        try:
            wt_lbs = float(self.table_row[76])
        except (TypeError, ValueError):
            wt_lbs = None

        tmp = ParticipantMobilityHealth.objects.create(contact_instance = self.pci,
                                                       ht_in = total_ht, wt_lbs = wt_lbs,
                                                       physical_activity = physical_activity)

        # assistive_devices
        if self.table_row[77] == "Y":
            tmp.assistive_devices.add(AnswerOption.objects.get(option = "Glasses", table = "ParticipantMobilityHealth", field = "assistive_devices"))
        if self.table_row[78] == "Y":
            tmp.assistive_devices.add(AnswerOption.objects.get(option = "Orthosis (e.g., knee brace)", table = "ParticipantMobilityHealth", field = "assistive_devices"))
        if self.table_row[79] == "Y":
            tmp.assistive_devices.add(AnswerOption.objects.get(option = "Contacts", table = "ParticipantMobilityHealth", field = "assistive_devices"))
        if self.table_row[80] == "Y":
            tmp.assistive_devices.add(AnswerOption.objects.get(option = "Prosthesis", table = "ParticipantMobilityHealth", field = "assistive_devices"))
        if self.table_row[81] == "Y":
            tmp.assistive_devices.add(AnswerOption.objects.get(option = "Hearing aid", table = "ParticipantMobilityHealth", field = "assistive_devices"))

        # mobility_aids
        if self.table_row[82] == "Y":
            tmp.mobility_aids.add(AnswerOption.objects.get(option = "Cane", table = "ParticipantMobilityHealth", field = "mobility_aids"))
        if self.table_row[83] == "Y":
            tmp.mobility_aids.add(AnswerOption.objects.get(option = "Scooter", table = "ParticipantMobilityHealth", field = "mobility_aids"))
        if self.table_row[84] == "Y":
            tmp.mobility_aids.add(AnswerOption.objects.get(option = "Crutch(es)", table = "ParticipantMobilityHealth", field = "mobility_aids"))
        if self.table_row[85] == "Y":
            tmp.mobility_aids.add(AnswerOption.objects.get(option = "Manual wheelchair", table = "ParticipantMobilityHealth", field = "mobility_aids"))
        if self.table_row[86] == "Y":
            tmp.mobility_aids.add(AnswerOption.objects.get(option = "Walker", table = "ParticipantMobilityHealth", field = "mobility_aids"))
        if self.table_row[87] == "Y":
            tmp.mobility_aids.add(AnswerOption.objects.get(option = "Power wheelchair", table = "ParticipantMobilityHealth", field = "mobility_aids"))
        if self.table_row[88] is not None and self.table_row[88] != "":
            tmp.mobility_aids.add(AnswerOption.objects.get_or_create(option = self.table_row[88], table = "ParticipantMobilityHealth", field = "mobility_aids")[0])

        # ParticipantSurgeries
        surgery_indecies = [93,96,99,102,105,108,111,114]
        for i in surgery_indecies:
            surg_tmp = self.save_ParticipantSurgery(i)
            if surg_tmp is not None:
                tmp.surgeries.add(surg_tmp)
        
        # medical_conditions
        self.save_ParticipantMedicalConditions(tmp)
        
        # medications
        medication_indecies = [191,200,209,218,227,243,252,261,270,279,295,306,313,322,331,347,356,365,374,383]
        for i in medication_indecies:
            med_tmp = self.save_ParticipantMedication(i,True) # prescription meds
            if med_tmp is not None:
                tmp.medications.add(med_tmp)

        otc_medication_indecies = [406,415,424,433,442,458,467,476,485,494,510,519,528,537,546,562,571,580,589,598]
        for i in otc_medication_indecies:
            med_tmp = self.save_ParticipantMedication(i,False) # OTC meds
            if med_tmp is not None:
                tmp.medications.add(med_tmp)
        
        tmp.save()
        self.object_array.append(tmp)


    # ParticipantSurgeries
    def save_ParticipantSurgery(self,start_index):
        if self.table_row[1 + start_index] is not "" and self.table_row[1 + start_index] is not None:
            try:
                year = int(self.table_row[2 + start_index])
            except (ValueError, TypeError):
                year = 0
        
            # save the created object
            tmp = ParticipantSurgeries.objects.create(t_surgery = self.table_row[1 + start_index], year = year)

            self.object_array.append(tmp)
            return tmp
        else:
            return None
    
    # ParticipantMedication
    def save_ParticipantMedication(self, start_index, is_prescription):
        if self.table_row[1 + start_index] is not "" and self.table_row[1 + start_index] is not None: # med name must be present
            # medication_name
            medication_name = self.table_row[1 + start_index]

            # dose_amt & units / notes
            notes = self.table_row[2 + start_index]

            # dose_frequency
            try:
                dose_frequency = AnswerOption.objects.get(order = int(self.table_row[3 + start_index]), table = "ParticipantMedication", field = "dose_frequency")
            except (ValueError, TypeError, ObjectDoesNotExist):
                if self.table_row[4 + start_index] is not None and self.table_row[4 + start_index] != "":
                    dose_frequency = AnswerOption.objects.get_or_create(option = self.table_row[4 + start_index], table = "ParticipantMedication", field = "dose_frequency")[0]
                else:
                    dose_frequency = None
            
            # med_reason
            med_reason = self.table_row[5 + start_index]

            # med_duration in days
            # empty field = 0
            try:
                med_duration_yr = float(self.table_row[6 + start_index])
            except (TypeError, ValueError):
                med_duration_yr = 0
            try:
                med_duration_mo = float(self.table_row[7 + start_index])
            except (TypeError, ValueError):
                med_duration_mo = 0
            
            # check to see if they used start year instead of time amt
            # not seen in current data set...
            if med_duration_yr > 1900 and med_duration_yr < 2100:
                med_duration = (self.pci.date_of_test.year - med_duration_yr)*365
                print "WARNING: YEAR ENTERED INCORRECTLY.  CHANGING %s to %s" %(med_duration_yr, med_duration/365.0)
            else:
                med_duration = med_duration_yr*365 + med_duration_mo*30
            
            # side_effects
            side_effects = self.table_row[8 + start_index]

            # save the created object
            tmp = ParticipantMedication.objects.create(medication_name = medication_name,
                                                      dose_amt = 0, 
                                                      dose_units = "NA",
                                                      dose_frequency = dose_frequency,
                                                      med_reason = med_reason, 
                                                      med_duration = med_duration,
                                                      side_effects = side_effects,
                                                      is_prescription = is_prescription,
                                                      notes = notes)

            self.object_array.append(tmp)
            return tmp
        else:
            return None


    # ParticipantSurgeries
    def save_ParticipantMedicalConditions(self,ParticipantMobilityHealth_instance):
        qs = QuestionOption.objects.filter(table = "ParticipantMedicalCondition", field = "condition", is_default = True).order_by('order')
        
        condition_start_index = 117
        year_of_onset_start_index = 147
        for i, q in enumerate(qs):
            # condition_onset
            if self.table_row[condition_start_index + i] is None or self.table_row[condition_start_index + i] == "":
                condition_onset = AnswerOption.objects.get_or_create(option = "NA", table = "ParticipantMedicalCondition", field = "condition_onset")[0]
            else:
                condition_onset = AnswerOption.objects.get(order = int(self.table_row[condition_start_index + i]) + 1, table = "ParticipantMedicalCondition", field = "condition_onset")
            
            # year_of_onset
            try:
                year_of_onset = int(self.table_row[i + year_of_onset_start_index])
            except (ValueError, TypeError):
                year_of_onset = None
            
            # save the created object
            tmp = ParticipantMedicalCondition.objects.create(condition = q, 
                                                      condition_onset = condition_onset,
                                                      year_of_onset = year_of_onset)

            # Add it to this object
            ParticipantMobilityHealth_instance.medical_conditions.add(tmp)
            self.object_array.append(tmp)

    # ParticipantSurgeries
    def save_ParticipantScaleRatings(self):
        # create the object
        tmp = ParticipantScaleRatings.objects.create(contact_instance = self.pci, 
                                                     research_notes = self.table_row[791])

        # FMA
        qs = QuestionOption.objects.filter(option__icontains = "Functional Movement Abilities: ").order_by("order")
        self.save_QuestionSection(607,qs,tmp)

        #print "Functional Movement Abilities:"
        #print self.table_row[607:653]

        qs = QuestionOption.objects.filter(option__icontains = "Satisfaction with Social Roles and Activities: ").order_by("order")
        self.save_QuestionSection(653,qs,tmp)

        #print "Satisfaction with Social Roles and Activities:"
        #print self.table_row[653:661]

        qs = QuestionOption.objects.filter(option__icontains = "Quality of Life: ").order_by("order")
        self.save_QuestionSection(661,qs,tmp)
        
        #print "Quality of Life:"
        #print self.table_row[661:687]

        qs = QuestionOption.objects.filter(option__icontains = "Last Two Weeks: ").order_by("order")
        self.save_QuestionSection(687,qs,tmp)

        #print "WHO-QOL:"
        #print self.table_row[687:695]

        qs = QuestionOption.objects.filter(option__icontains = "Technology: Consumer Technology Access and Use: ").order_by("order") # scale12
        self.save_QuestionSection(695,qs,tmp, default_order = 9) # handle NA and assign index 9

        qs = QuestionOption.objects.filter(option__icontains = "Technology: Consumer Technology Personal Access and Use: ").order_by("order") # scale13
        self.save_QuestionSection(722,qs,tmp, default_order = 9)

        qs = QuestionOption.objects.filter(option__icontains = "Technology: Computer and Cellular Phone Use: Cell: ").order_by("order")
        self.save_QuestionSection(731,qs,tmp)

        qs = QuestionOption.objects.filter(option__icontains = "Technology: Computer and Cellular Phone Use: Computer: ").order_by("order")
        self.save_QuestionSection(743,qs,tmp)

        qs = QuestionOption.objects.filter(option__icontains = "Technology: Health Technology Access and Use: Listed Technologies: ").order_by("order") # scale12
        self.save_QuestionSection(754,qs,tmp, default_order = 9)
        
        # Add devices
        # Device names = 762-766
        # Device ratings = 767-771
        options = AnswerOption.objects.filter(unique_name__icontains = "scale12:", table = "ScaleQuestionAndOption", field = "option")
        for i in range(0,5):
            try:
                device_rating = int(self.table_row[767 + i])
                device_name = self.table_row[762 + i]
                option = options[device_rating - 1]
                question = QuestionOption.objects.get_or_create(option = "Technology: Health Technology Access and Use: Additional Technologies: " + device_name,
                                                                table = "ScaleQuestionAndOption", field = "question")
                tmp_sqo = ScaleQuestionAndOption.objects.get_or_create(question = question, option = option, order = -1)[0]
                self.object_array.append(tmp_sqo)
                tmp.survey_selections.add(tmp_sqo)
            except (ValueError, TypeError):
                pass # not a valid response
            

        qs = QuestionOption.objects.filter(option__icontains = "Technology: Confidence with Technology: ").order_by("order")
        self.save_QuestionSection(772,qs,tmp)

        qs = QuestionOption.objects.filter(option__icontains = "Technology: Attitudes Toward Information Technology: ").order_by("order")
        self.save_QuestionSection(785,qs,tmp)

        #print "Technology: Confidence with Technology:"
        #print self.table_row[772:782]

        #print "Technology: Attitudes Toward Information Technology:"
        #print self.table_row[785:791]

        # calculate scores
        tmp.rating_scores.recalculate()
        
        #print LimeToken.objects.filter(participant = self.pci.participant)[0].token
        #print tmp.rating_scores.__dict__
        #print "<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>"
        #raw_input()
        
        self.object_array.append(tmp)

    # Deal with NA answer separately; create NA option if not found
    """
    handle 0 index
        - create entries in db with indecies corresponding to mysql db
        - right now all 0 indexed; make most 1 indexed, and only 0 indexed where needed
            - requires re-run of import process
    handle "NA" entry separately from NULL and ""
    fix combined scale for Technology: Consumer Technology Access and Use
        - have to divide these to index correctly
    """
    def save_QuestionSection(self, index_start, questions, ParticipantScaleRatings_instance, default_order = -1):
        """
        1) pass in ordered questions for section + start index for section
        2) iterate through questions and index at same time
        3) find ScaleQuestionAndOption w/ Q & order = int(x)
        4) create ScaleSelection obj from this and add to tmp.survey_selections
        """
        for i, q in enumerate(questions):
            try:
                order = int(self.table_row[index_start + i]) # choice

                try:
                    tmp = ScaleQuestionAndOption.objects.get(question = q, order = order)
                except ObjectDoesNotExist:
                    print "EXCEPTION: ObjectDoesNotExist"
                    print ScaleQuestionAndOption.objects.filter(question = q)
                    tmp = ScaleQuestionAndOption.objects.get_or_create(question = q, option = None, order = -1)[0]
                    print "[%i, %s, %i, %s]" % (i, q.option, order, tmp)
                    raw_input()
            except (ValueError, TypeError):
                # Handle NA and Not Answered
                order = -1
                tmp = ScaleQuestionAndOption.objects.get_or_create(question = q, option = None, order = -1)[0]
            
            #print "[%i, %s, %i, %s]" % (i, q.option, order, tmp)
            
            # Add to object array and ParticipantScaleRatings object
            #self.object_array.append(tmp)
            ParticipantScaleRatings_instance.survey_selections.add(tmp)# ScaleSelection