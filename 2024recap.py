import pandas as pd

file_path=
song = pd.read_csv(file_path,encoding='cp949')

song= song.dropna(how='all', axis=1)


spac=song[song['Container Type']=='UNKNOWN'].index
song.drop(spac, inplace = True)

spac=song[song['Container Type']==''].index
song.drop(spac, inplace = True)

spac = song[song['Container Type']=='ALBUM'].index
song.drop(spac, inplace = True)

spac = song[song['Container Type']=='RADIO'].index
song.drop(spac, inplace = True)

from datetime import datetime, timedelta
from collections import defaultdict

RECENT_THRESHOLD = 60  # 최근 몇 일 동안 들은 노래에 가중치를 부여할 것인지
SELECTION_WEIGHT = 1.5  # 직접 선택한 노래에 부여할 가중치

song['Event Received Timestamp'] = pd.to_datetime(song['Event Received Timestamp'], errors='coerce')

# 2024년에 들은 노래만 필터링
song2024 = song[song['Event Received Timestamp'].dt.year == 2024].copy()

song2024['Event Received Timestamp'] = pd.to_datetime(song2024['Event Received Timestamp'])
song_dates = defaultdict(lambda: {'dates': [], 'score': 1.0})
top_songs = song2024['Song Name'].value_counts().nlargest(15).index

desired_date = datetime(2024, 12, 13)

x
    

for i, row in song.iterrows():
    song_name = row['Song Name']
    score = 2.0 if (desired_date - row['Event Received Timestamp']).days <= RECENT_THRESHOLD else 1.0
    days_since_played = (desired_date - row['Event Received Timestamp']).days
    score = max(1.0, 2.0 - (days_since_played / RECENT_THRESHOLD))
    
    if row['Auto Play'] == 'AUTO_OFF':
        score *= SELECTION_WEIGHT
    if row['Repeat Play'] == 'REPEAT_ONE':
        score *= 1.7
    if song_name in top_songs:
        score *= 1.9
        
    song_dates[song_name]['dates'].append(row['Event Received Timestamp'])
    song_dates[song_name]['score'] = score


top_songs = sorted(song_dates.items(), key=lambda x: x[1]['score'], reverse=True)[:15]

new_song_cnt=len(get_newsongs_2024(song))
print(f"2024년에 추가된 노래 개수 : {new_song_cnt}곡\n")
for rank, (song_name, data_info) in enumerate(top_songs, start=1):
    print(f"Ranking: {rank}")
    print(f"Song: {song_name}")
    print(f"Score: {data_info['score']}")
    print("\n")    
