from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

valid_value_names = ['LV_Incoming_TER_EH1', 'LV_Incoming_TER_EM', 'LV_Incoming_TER_EMA', 'LV_Incoming_TER_EMB', 'LV_Incoming_TER_EMC', 'LV_Incoming_TER_EMD', 'LV_Incoming_TER_EME', 'LV_Incoming_TER_MDB_LT_GSM', 'LV_Incoming_TER_NR', 'LV_Incoming_TER_NR1', 'LV_Incoming_TER_NR2', 'LV_Incoming_TER_NR3', 'LV_Incoming_TER_NR4', 'Terraces - NR6', 'Terraces - NR7', 'Terraces - NR8', 'Terraces - T10', 'Terraces - T11', 'Terraces - T12', 'Terraces - T13', 'Terraces - T14', 'Terraces - T7', 'Terraces - T8', 'Terraces - T9', 'HS1 Public Lighting', 'L Public Lighting', 'ISC Public Lighting', 'MC Public Lighting', 'TC Public Lighting', 'U Public Lighting', 'Mont Park', 'Agora East Building', 'Animal_and_Glass Houses', 'Agricultural Reserve', 'LV_Incoming_BEN_AS2.AS1_Main_Switch', 'LV_Incoming_BEN_AS2.AS2_Main_Switch', 'Agora Theatre', 'LV_Incoming_WOD_SMSB.AW-1_Main_Supply', 'Albury-Wodonga - B1', 'Albury-Wodonga - B3', 'Albury-Wodonga - B3A', 'Albury-Wodonga - B4', 'Albury-Wodonga - B5A', 'Albury-Wodonga - B6', 'Albury-Wodonga - B8', 'Boilerhouse Building', 'Beth Gleeson Building', 'LV_Incoming_MIL.BGR_Main_Supply', 'BS1 Building', 'BS2 Building', 'Childrens Centre', 'Chisholm College', 'CS Buildings CS1 CS2 CS3', 'David Myers Building', 'Donald Whitehead Building', 'ED1 Building HEUD', 'ED2 Building', 'Eastern Lecture Theatre', 'Glenn College', 'George Singer Building', 'Health Sciences Buildings123', 'Health Sciences Clinic', 'Hooper Szental Building', 'Humanities2 Building', 'Humanities3 Building', 'Indoor Sports Centre', 'John Scott Meeting House', 'Library', 'LIMS1', 'LIMS2 Building', 'Latrobe Uni Mediucal Centre', 'Wildlife Reserve', 'Martin Building', 'Menzies College Main Supply', 'Menzies College Annexe', 'Albury-Wodonga - MH1', 'Albury-Wodonga - MH2', 'Peribolos East Building', 'Physical Sciences1 Building', 'Physical Sciences2 Building', 'Peribolos West Building', 'RLR Building', 'SPF Specialised Pathogen Facility', 'LV_Incoming_SHS.SHS_Main_Supply', 'SFP', 'SFP2', 'Social Sciences Building', 'Sylvia Walton Building', 'Thomas Cherry Shared Load', 'Thomas Cherry Building', 'The Learning Commons Building', 'Union', 'Zoological Reserve']


def column_value_Matches(valid_value_names, value_extract):
    sim_vect = []
    print(valid_value_names)
    for v in valid_value_names:
        if(v.isnumeric()):
            sig = similar(str(v), str(value_extract))
        else:
            sig = similar(str(v.lower()), str(value_extract.lower()))
        sim_vect.append([v, sig])

    sim_vect = sorted(sim_vect,key=lambda l:l[1])
    print(sim_vect[-4:])
    return sim_vect[-1]


column_value_Matches(valid_value_names,'terraces - nr7')