import pylast
from config import last_fm_apikey, last_fm_secret, last_fm_password, last_fm_username

last_fm_passwordMD5 = pylast.md5(last_fm_password)

last_fm_object = pylast.LastFMNetwork(api_key=last_fm_apikey, api_secret=last_fm_secret, username=last_fm_username, password_hash=last_fm_passwordMD5)
track_set = set()

def get_history(number_of_songs, username):
    #if number_of_songs = 0, then download all - minimum, 500
    user_object = last_fm_object.get_user(username)

    if number_of_songs == 0:
        all_songs = True 
        limit = 'None'
        loop_counter = 0
    else:
        limit = number_of_songs%500 + 1
        loop_counter = number_of_songs//500
    
    listening_history = user_object.get_recent_tracks(limit=limit, cacheable=True)
    for PlayedTrack in listening_history:
        last_retrieved_track_timestamp = ''
        last_retrieved_track_timestamp = str(PlayedTrack[3])
        temp_str = PlayedTrack[0]
        try:
            print(temp_str)
            temp_str = str(temp_str)
            track_set.add(temp_str)
        except UnicodeEncodeError:
            pass
    
    while 0 < loop_counter:
        listening_history = user_object.get_recent_tracks(limit=500, cacheable=True, time_to=last_retrieved_track_timestamp)
        for PlayedTrack in listening_history:
            last_retrieved_track_timestamp = ''
            last_retrieved_track_timestamp = str(PlayedTrack[3])
            temp_str = PlayedTrack[0]
            try:
                print(temp_str)
                temp_str = str(temp_str)
                track_set.add(temp_str)
            except UnicodeEncodeError:
                pass
        loop_counter = loop_counter - 1
            

        



    print(track_set)
    print(last_retrieved_track_timestamp)

    



    
def get_artist():
    return(input("Name an Artist\n"))

def main():
    #print("Hello world")
    get_history(850, 'seaty6')
    #print(get_artist())

if __name__ == "__main__":
    main()