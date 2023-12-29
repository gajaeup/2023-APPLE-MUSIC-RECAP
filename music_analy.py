import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict


song = pd.read_excel() #데이터 파일 읽어오기

song= song.dropna(how='all', axis=1)
song = song.drop(['End Position In Milliseconds','Event ID','Event Reason Hint Type','Feature Name','Media Duration In Milliseconds','Milliseconds Since Play','Personalized Name','Play Duration Milliseconds','Start Position In Milliseconds','Use Listening History'],axis=1)
spac = song[song['Container Type']=='ALBUM'].index
song.drop(spac, inplace = True)
spac = song[song['Container Type']=='RADIO'].index
song.drop(spac, inplace = True)


RECENT_THRESHOLD = 60  # 최근 몇 일 동안 들은 노래에 가중치를 부여할 것인지
SELECTION_WEIGHT = 1.7  # 직접 선택한 노래에 부여할 가중치


song['Event Received Timestamp'] = pd.to_datetime(song['Event Received Timestamp'])
song_dates = defaultdict(lambda: {'dates': [], 'score': 1.0})
top_songs = song['Song Name'].value_counts().nlargest(15).index

desired_date = datetime(2023, 12, 12)

for i, row in song.iterrows():
    song_name = row['Song Name']
    score = 2.0 if (desired_date - row['Event Received Timestamp']).days <= RECENT_THRESHOLD else 1.0
    
    if row['Auto Play'] == 'AUTO_OFF':
        score *= SELECTION_WEIGHT
    if row['Repeat Play'] == 'REPEAT_ONE':
        score *= 1.6
    if song_name in top_songs:
        score *= 1.8
        
    song_dates[song_name]['dates'].append(row['Event Received Timestamp'])
    song_dates[song_name]['score'] = score


top_songs = sorted(song_dates.items(), key=lambda x: x[1]['score'], reverse=True)[:15]
 
for rank, (song_name, data_info) in enumerate(top_songs, start=1):
    print(f"Ranking: {rank}")
    print(f"Song: {song_name}")
    print(f"Score: {data_info['score']}")
    print("\n")    