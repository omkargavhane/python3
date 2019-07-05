#import pprint as pp
import csv
global all_data
global district_name
global season_name
algorithm='''for inputted district\nfor each season\nfind prodution/area for each crop\nThen find mean of prod/area for each  crop\nreturn crop with max value of mean'''
def find_bestcrop(dn,sn):
    crop_filter={}
    mean_mapper={}
    for data in all_data:
        if data[0].lower().strip()==dn.lower().strip() and \
        data[1].lower().strip()==sn.lower().strip():
            try:
                crop_filter.setdefault(data[-1],[]).append(float(data[-2])/float(data[-3]))
            except Exception:
                pass
    for crop in crop_filter:
        try:
            mean_mapper[crop]=sum(crop_filter[crop])/len(crop_filter[crop])
        except Exception:
            pass
    sorted_mapper=sorted(list(mean_mapper.items()),key=lambda x:x[1],reverse=True)
    if len(sorted_mapper):
        return sorted_mapper[0][0],sorted_mapper[0][1]
    return 'NONE',0

def get_knowns(fp):
    global all_data
    global district_name
    global season_name
    all_data=list(csv.reader(fp))[1:]
    district_name=set()
    season_name=set()
    for data in all_data:
        district_name.add(data[0])
        season_name.add(data[1])
    #print('Known District\'s\n'+'='*20)
    #pp.pprint(district_name)
    #print('Known Season\'s\n'+'='*20) 
    #pp.pprint(season_name)
    #print('='*64)
    return district_name,season_name
def get_bestcrop(dn,sn):
    #dn=input('Enter District name: ')
    #sn=input('Enter Season name: ')
    #print('='*64)
    #if dn not in [e.lower().strip() for e in district_name] or sn not in [e.lower().strip()for e in season_name]:
    #    return 'District or season  not found!!!'
    all_season=list(season_name)
    suggested_crops_prod=[]
    for season in all_season:
        suggested_crops_prod.append({season.lower().strip():find_bestcrop(dn,season)})
#head_foot='+'+'-'*20+'+'+'-'*20+'+'+'-'*20+'+'
#colmn='|'+'{:<20}'+'|'+'{:<20}'+'|'+'{:<20}'+'|'
#print(head_foot+'\n'+colmn.format('Season','Suggested Crop',' Avg Prod/Area'))
#print(head_foot+'\n'+head_foot)
    return suggested_crops_prod
'''for_input_season=''
for_whole_year=''
for season,sugg_crop_prod in zip(all_season,suggested_crops_prod):
    if season.lower().strip()==sn:
        for_input_season=sugg_crop_prod
    if season.lower().strip()=='whole year':
        for_whole_year=sugg_crop_prod
    print(colmn.format(season,sugg_crop_prod[0],sugg_crop_prod[1]))
    print(head_foot)
print('='*64)
if for_input_season[1]>for_whole_year[1]:
    print("[SUGGESTION] Crop for Season {} is {}".format(sn,for_input_season[0]))
else:    
    print("[SUGGESTION] Crop for Season {} is {}".format(sn,for_whole_year[0]))
print('='*64)'''
