from commands.PUBG.dataframe2image import export_image
import pandas as pd
import requests
import interactions
import os

col_lang = 'kor'
if col_lang == 'eng':
  MDTR_col=['Rank', 'Username', 'Total kill', 'Total damage', 'Avg. distance']
  MDTS_col=['(Username)', 'kill', 'Damage', 'Assists', 'DBNO', 'Survived time']
  MDO_col=[['Combat', 'Combat', 'Combat', 'Combat', 'Distance', 'Distance', 'Distance', 'Survival', 'Survival'], 
           ['Damage', 'Kill (Headshot)', 'Assists', 'DBNO', 'Move Distance', 'Walk Distance', 'Ride Distance', 'Heals/Boosts', 'Revives']]
  MDO_KD_col = ['Category', 'Time', 'Name', 'Rank', 'Weapon', 'Distance']
elif col_lang == 'kor':
  MDTR_col=['순위', '닉네임', '총 킬', '총 데미지', '평균 이동 거리']
  MDTS_col=['(닉네임)', '킬', '데미지', '어시스트', '기절시킴', '생존시간']
  MDO_col=[['전투', '전투', '전투', '전투', '이동', '이동', '이동', '생존', '생존'], 
           ['데미지', '킬 (헤드샷)', '어시스트', '기절시킴', '이동거리', '걸은거리', '탑승거리', '치유/부스트', '부활 시킨 횟수']]
  MDO_KD_col = ['구분', '시간', '이름', '순위', '무기', '거리']

import datetime

def datetime_convert(time, telemetry=True):
  if telemetry:
    time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
  else:
    time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
  return time

import math 

def distance_calc(location1, location2):
  x1 = location1.get('x')
  y1 = location1.get('y')
  z1 = location1.get('z')
  x2 = location2.get('x')
  y2 = location2.get('y')
  z2 = location2.get('z')
  return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

header = {
  "Authorization": "(My PUBG API Key)",
  "Accept": "application/vnd.api+json"
}

async def 배그전적(ctx, match_No, my_name):
    url_player = "https://api.pubg.com/shards/steam/players?filter[playerNames]="
    
    endpoint_url = url_player + my_name
    stat_url = 'https://pubg.op.gg/user/' + my_name
    if requests.get(endpoint_url, headers=header).json().get('data') != None:
        player_data = requests.get(endpoint_url, headers=header).json().get('data')[0]
    else:
        await ctx.send('유저 {}을(를) 찾을 수 없습니다. 닉네임을 정확히 입력했는지 확인해주세요.'.format(my_name))
        return
    if match_No >= 60:
        await ctx.send('매치는 59번째 매치까지 검색할 수 있습니다.')
        return
    my_account_id = player_data.get('id')
    
    recent_match_id = []
    for data in player_data.get('relationships').get('matches').get('data'):
        recent_match_id.append(data.get('id'))
    print('내 정보\n')
    print(my_name)
    print(my_account_id)
    print(recent_match_id[match_No-1])
    
    #매치정보
    url_matches = 'https://api.pubg.com/shards/steam/matches/' 
    endpoint_url = url_matches + recent_match_id[match_No-1]
    
    r = requests.get(endpoint_url, headers=header).json()
    match_attributes = r.get('data').get('attributes')
    
    #기본 정보
    print('\n기본 정보 \n')
    print('match information of match', recent_match_id[match_No-1])
    time = datetime_convert(match_attributes.get('createdAt'), telemetry=False)
    time_path = str(time).replace(" ", "_")
    time_path = time_path.replace(":", "_")
    print('game played at :', time)
    duration = match_attributes.get('duration')
    print('duration : %d:%d' %(duration//60, duration%60))
    print('mode :', match_attributes.get('gameMode'))
    print('map :', match_attributes.get('mapName'))
    print('match type :', match_attributes.get('matchType'))
    
    map_name = match_attributes.get('mapName')
    map_url = ""
    
    if map_name == 'Baltic_Main':
        map_url = "http://battlegrounds.party/map/map/Baltic/tiles/0/0/0.webp"
        map_name = '에란겔'
    elif map_name == 'Chimera_Main':
        map_url = "http://battlegrounds.party/map/map/Chimera/tiles/0/0/0.webp"
        map_name = '파라모'
    elif map_name == 'Desert_Main':
        map_url = "http://battlegrounds.party/map/map/Desert/tiles/0/0/0.webp"
        map_name = '미라마'
    elif map_name == 'DihorOtok_Main':
        map_url = "http://battlegrounds.party/map/map/DihorOtok/tiles/0/0/0.webp"
        map_name = '비켄디'
    elif map_name == 'Heaven_Main':
        map_url = "http://battlegrounds.party/map/map/Heaven/tiles/0/0/0.webp"
        map_name = '헤이븐'
    elif map_name == 'Kiki_Main':
        map_url = "http://battlegrounds.party/map/map/Kiki/tiles/0/0/0.webp"
        map_name = '데스턴'
    elif map_name == 'Savage_Main':
        map_url = "http://battlegrounds.party/map/map/Savage/tiles/0/0/0.webp"
        map_name = '사녹'
    elif map_name == 'Summerland_Main':
        map_url = "http://battlegrounds.party/map/map/Summerland/tiles/0/0/0.webp"
        map_name = '카라킨'
    elif map_name == 'Tiger_Main':
        map_url = "http://battlegrounds.party/map/map/Tiger/tiles/0/0/0.webp"
        map_name = '테이고'
    
    print(map_name)
    print(map_url)
    
    #인덱싱
    included = r.get('included') # included에는 roster와 participant를 모두 포함
    roster_data = {} # 팀 ex)49개
    participant_data = {} # 참가자 ex)98명
    for i in range(len(included)):
        if included[i].get('type') == 'roster':
            roster_data[included[i].get('id')] = [included[i].get('attributes').get('stats'), included[i].get('relationships').get('participants').get('data')]
        elif included[i].get('type') == 'participant':
            participant_data[included[i].get('id')] = included[i].get('attributes').get('stats')
        elif included[i].get('type') == 'asset':
            asset_url = included[i].get('attributes').get('URL')
    
    #Table 1
    image_name_re_1 = my_name + '_stat_' + 'match_detail_Total_Rank' + '_re_' + time_path + '.png'
    
    if os.path.isfile(image_name_re_1):
        match_detail_Total_Rank_True = False
        for team_id in roster_data:
            rank = roster_data[team_id][0].get('rank')
            member = roster_data[team_id][1]
            member_id = [item.get('id') for item in member]
            for item in member_id:
                member_stat = participant_data[item]
                if member_stat.get('playerId') == my_account_id:
                    my_team_rank = rank
    else:
        match_detail_Total_Rank = pd.DataFrame(columns=MDTR_col)
        rows_table_1 = []
        
        for team_id in roster_data:
            rank = roster_data[team_id][0].get('rank')
            member = roster_data[team_id][1]
            member_id = [item.get('id') for item in member]
            member_name = []
            kill, dmg, dist = 0, 0, 0
            for item in member_id:
                member_stat = participant_data[item]
                member_name.append(member_stat.get('name'))
                if member_stat.get('playerId') == my_account_id:
                    my_participant_id = item
                    my_team_rank = rank
                    my_team_id = team_id
                    my_distance = [member_stat.get('walkDistance') + member_stat.get('rideDistance') + member_stat.get('swimDistance'), member_stat.get('walkDistance'), member_stat.get('rideDistance')]
                kill += member_stat.get('kills')
                dmg += member_stat.get('damageDealt')
                dist += member_stat.get('walkDistance') + member_stat.get('rideDistance') + member_stat.get('swimDistance')
            
            rows_table_1.append(pd.Series([rank, member_name, kill, dmg, dist/len(member_id)], index=MDTR_col))
        
        match_detail_Total_Rank = pd.concat([match_detail_Total_Rank, pd.DataFrame(rows_table_1)],axis=0, ignore_index=True)
        
        match_detail_Total_Rank = match_detail_Total_Rank.sort_values(by=[MDTR_col[0]])
        match_detail_Total_Rank = match_detail_Total_Rank.head(10)
        blankIndex=[''] * len(match_detail_Total_Rank)
        match_detail_Total_Rank.index=blankIndex
        
        match_detail_Total_Rank_True = True
    

    # 전적 엠베드
    if my_team_rank == 1:
        stat_embed_color: int = 0xffd700
    else:
        stat_embed_color: int = 0x5865F2

    stat_embed = interactions.Embed(title = my_name + "의 전적" , url = stat_url, color = stat_embed_color) #전적 엠베드
    stat_embed.set_author(name = "PUBG")
    stat_embed.set_footer(text = "from PUBG API")
    stat_embed.set_thumbnail(url = map_url)
    
    stat_embed.description = '**최근 매치 정보**\n시간 : ' + str(time) + '\n' \
        + '매치시간 : ' + str(duration//60) + ':' + str(duration%60) + '\n' \
        + match_attributes.get('gameMode') + ', {}등'.format(my_team_rank) + '\n' \
        + map_name + '\n'
    
    #Table 2
    image_name_re_2 = my_name + '_stat_' + 'match_detail_Team_Stats' + '_re_' + time_path + '.png'
    
    if os.path.isfile(image_name_re_2):
        match_detail_Team_Stats_True = False
    else:
        match_detail_Team_Stats = pd.DataFrame(columns=MDTS_col)
        rows_table_2 = []
        
        total_kill, total_dmg, total_assist, total_dbno = 0, 0, 0, 0
        for item in roster_data[my_team_id][1]:
            member = participant_data[item.get('id')]
            name = member.get('name')
            kill = member.get('kills')
            total_kill += kill
            dmg = member.get('damageDealt')
            total_dmg += dmg
            assist = member.get('assists')
            total_assist += assist
            dbno = member.get('DBNOs')
            total_dbno += dbno
            survive_time = member.get('timeSurvived')
            survive_time = '%d:%d'%(survive_time//60, survive_time%60)
            
            rows_table_2.append(pd.Series([name, kill, dmg, assist, dbno, survive_time], index=MDTS_col))
            
        match_detail_Team_Stats = pd.concat([match_detail_Team_Stats, pd.DataFrame(rows_table_2)],axis=0, ignore_index=True)
        
        row_table_2_final = pd.Series(['Total', total_kill, total_dmg, total_assist, total_dbno, ''], index=MDTS_col)
        row_table_2_final_match_detail_Team_Stats = pd.DataFrame.from_records([row_table_2_final])
        match_detail_Team_Stats = pd.concat([match_detail_Team_Stats, row_table_2_final_match_detail_Team_Stats], ignore_index=True, axis=0)
        blankIndex=[''] * len(match_detail_Team_Stats)
        match_detail_Team_Stats.index=blankIndex
        
        match_detail_Team_Stats_True = True
    
    #Table 3
    image_name_re_3_1 = my_name + '_stat_' + 'match_detail_Overall_1' + '_re_' + time_path + '.png'
    image_name_re_3_2 = my_name + '_stat_' + 'match_detail_Overall_2' + '_re_' + time_path + '.png'
    image_name_re_3_KD = my_name + '_stat_' + 'match_detail_Overall_KD' + '_re_' + time_path + '.png'
    
    if os.path.isfile(image_name_re_3_1) & os.path.isfile(image_name_re_3_2) & os.path.isfile(image_name_re_3_KD):
        match_detail_Overall_1_True = False
        match_detail_Overall_2_True = False
        match_detail_Overall_KD_True = False
    else:
        asset = requests.get(asset_url, headers=header).json()
        
        match_detail_Overall = pd.DataFrame(columns=MDO_col)
        match_detail_Overall_KD = pd.DataFrame(columns=MDO_KD_col)
        
        dmg = 0
        kill, head = 0, 0
        assist = 0
        dbno = 0
        heals = 0
        boosts = 0
        revives = 0
        x = []
        y = []
        grid_to_pixel = 7.423920956812841e-4 * 1.73
        rows_table_3 = []
        
        for i in range(len(asset)):
            # start time
            if asset[i].get('_T') == 'LogMatchStart':
                starttime = datetime_convert(asset[i].get('_D'))
            # kill, death
            if asset[i].get('_T') == 'LogPlayerKillV2':
                # death
                if asset[i].get('victim').get('accountId') == my_account_id:
                    death_location = asset[i].get('victim').get('location')
                    x.append(asset[i].get('victim').get('location').get('x')*grid_to_pixel)
                    y.append(asset[i].get('victim').get('location').get('y')*grid_to_pixel)
                    time = str(datetime_convert(asset[i].get('_D'))-starttime)
                    if asset[i].get('killer') != None:
                        if asset[i].get('attackId') > 0:
                            for id in roster_data:
                                if roster_data[id][0].get('teamId') == asset[i].get('killer').get('teamId'):
                                    rank = roster_data[id][0].get('rank')
                            distance = distance_calc(asset[i].get('victim').get('location'), asset[i].get('killer').get('location'))
                            
                            distance_3f = "{:.3f}".format(distance*grid_to_pixel/0.13125)
                            rows_table_3.append(pd.Series(
                                ['Death', time[-12:], asset[i].get('killer').get('name'), rank, asset[i].get('killerDamageInfo').get('damageCauserName'), distance_3f], 
                                index=MDO_KD_col))
                        
                        else:
                            rows_table_3.append(pd.Series(
                                ['Death', time[-12:], '', '', asset[i].get('killerDamageInfo').get('damageCauserName'), asset[i].get('killerDamageInfo').get('distance')], 
                                index=MDO_KD_col))
                    break
                
                # assist
                else:
                    assist_list = asset[i].get('assists_AccountId')
                    if my_account_id in assist_list:
                        assist += 1
                
                # kill, headshot
                if asset[i].get('isSuicide') == False:
                    if asset[i].get('killer') != None:
                        if asset[i].get('attackId') > 0 or asset[i].get('dBNOId') > 0:
                            if asset[i].get('killer').get('accountId') == my_account_id:
                                x.append(asset[i].get('victim').get('location').get('x')*grid_to_pixel)
                                y.append(asset[i].get('victim').get('location').get('y')*grid_to_pixel)
                                time = str(datetime_convert(asset[i].get('_D'))-starttime)
                                kill += 1
                                for id in roster_data:
                                    if roster_data[id][0].get('teamId') == asset[i].get('victim').get('teamId'):
                                      rank = roster_data[id][0].get('rank')
                                if asset[i].get('killerDamageInfo').get('damageReason') == 'HeadShot':
                                    head += 1
                                distance = distance_calc(asset[i].get('victim').get('location'), asset[i].get('killer').get('location')) 
                                
                                distance_3f = "{:.3f}".format(distance*grid_to_pixel/0.13125)
                                rows_table_3.append(pd.Series(
                                    ['Kill', time[-12:], asset[i].get('victim').get('name'), rank, asset[i].get('killerDamageInfo').get('damageCauserName'), distance_3f], 
                                    index=MDO_KD_col))
                            
            # damage
            if asset[i].get('_T') == 'LogPlayerTakeDamage':
                if asset[i].get('attacker') != None:
                    if asset[i].get('attackId') > 0:
                        if asset[i].get('attacker').get('accountId') == my_account_id:
                            if asset[i].get('victim').get('accountId') != my_account_id:
                                dmg += asset[i].get('damage')
            # dbno      
            if asset[i].get('_T') == 'LogPlayerMakeGroggy':
                if asset[i].get('attacker') != None:
                    if asset[i].get('attackId') > 0:
                        if asset[i].get('attacker').get('accountId') == my_account_id:
                            dbno += 1
            # heals, boosts
            if asset[i].get('_T') == 'LogItemUse':
                if asset[i].get('character').get('accountId') == my_account_id:
                    if asset[i].get('item').get('subCategory') == 'Heal':
                        heals += 1
                    if asset[i].get('item').get('subCategory') == 'Boost':
                        boosts += 1
            # revives
            if asset[i].get('_T') == 'LogPlayerRevive':
                if asset[i].get('reviver').get('accountId') == my_account_id:
                    revives += 1


        row_match_detail_Overall = pd.Series(
            [dmg, '%d(%d)'%(kill, head), assist, dbno, my_distance[0], my_distance[1], my_distance[2], '%d/%d'%(heals, boosts), revives], 
            index=MDO_col)
        row_match_detail_Overall_df = pd.DataFrame.from_records([row_match_detail_Overall])
        match_detail_Overall = pd.concat([match_detail_Overall, row_match_detail_Overall_df], ignore_index = True, axis=0)

        # 3-1
        match_detail_Overall_1 = match_detail_Overall.iloc[:,:4]
        blankIndex=[''] * len(match_detail_Overall_1)
        match_detail_Overall_1.index=blankIndex

        # 3-2
        match_detail_Overall_2 = match_detail_Overall.iloc[:,4:]
        blankIndex=[''] * len(match_detail_Overall_2)
        match_detail_Overall_2.index=blankIndex

        match_detail_Overall_1_True = True
        match_detail_Overall_2_True = True
        
        match_detail_Overall_KD = pd.concat([match_detail_Overall_KD, pd.DataFrame(rows_table_3)], axis = 0, ignore_index = True) 
        blankIndex=[''] * len(match_detail_Overall_KD)
        match_detail_Overall_KD.index=blankIndex

        match_detail_Overall_KD_True = True


    # export missing image
    if match_detail_Total_Rank_True:
        export_image(match_detail_Total_Rank, 'match_detail_Total_Rank', my_name, time_path)
    if match_detail_Team_Stats_True:
        export_image(match_detail_Team_Stats, 'match_detail_Team_Stats', my_name, time_path)
    if match_detail_Overall_1_True:
        export_image(match_detail_Overall_1, 'match_detail_Overall_1', my_name, time_path, font_size = 0.75)
    if match_detail_Overall_2_True:
        export_image(match_detail_Overall_2, 'match_detail_Overall_2', my_name, time_path)
    if match_detail_Overall_KD_True:
        export_image(match_detail_Overall_KD, 'match_detail_Overall_KD', my_name, time_path)

    #read images
    files_to_read: list[str] = [image_name_re_1, image_name_re_2, image_name_re_3_1, image_name_re_3_2, image_name_re_3_KD]
    files_to_send: interactions.File = [] # image list to send
    for filename in files_to_read:
        file = interactions.File(filename)
        files_to_send.append(file)

    stat_embed.set_image(
        url = 'attachment://{}'.format(image_name_re_1)
        )

    image_embed_1 = interactions.Embed(
        title = '팀 스탯',
        color = interactions.Color.fuchsia()
        )
    image_embed_1.set_image(
        url = 'attachment://{}'.format(image_name_re_2)
        )

    image_embed_2 = interactions.Embed(
        title = '개인 스탯',
        color = interactions.Color.fuchsia()
        )
    image_embed_2.set_image(
        url = 'attachment://{}'.format(image_name_re_3_1)
        )

    image_embed_3 = interactions.Embed(
        color = interactions.Color.fuchsia()
        )
    image_embed_3.set_image(
        url = 'attachment://{}'.format(image_name_re_3_2)
        )

    image_embed_4 = interactions.Embed(
        title = '개인 KD',
        color = interactions.Color.fuchsia()
        )
    image_embed_4.set_image(
        url = 'attachment://{}'.format(image_name_re_3_KD)
        )

    await ctx.send(embeds = [stat_embed, image_embed_1, image_embed_2, image_embed_3, image_embed_4], files = files_to_send)
