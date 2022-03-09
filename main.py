import pylast
from config import last_fm_apikey, last_fm_secret, last_fm_password, last_fm_username, spotify_client_ID, spotify_client_secret
from youtubesearchpython import VideosSearch
#TODO - take list of unlistened tracks, provide youtube and spotify links to easily view them


last_fm_passwordMD5 = pylast.md5(last_fm_password)

last_fm_object = pylast.LastFMNetwork(api_key=last_fm_apikey, api_secret=last_fm_secret, username=last_fm_username, password_hash=last_fm_passwordMD5)


test_list = []

def get_history(number_of_songs, username):
    #if number_of_songs = 0, then download all - minimum, 500
    track_set = set()
    user_object = last_fm_object.get_user(username)

    if number_of_songs == 0:
        limit = None
        loop_counter = 0
    else:
        limit = number_of_songs%500 + 1
        loop_counter = number_of_songs//500
    
    listening_history = user_object.get_recent_tracks(limit=limit, cacheable=True, stream=True)
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
        listening_history = user_object.get_recent_tracks(limit=500, cacheable=True, time_to=last_retrieved_track_timestamp, stream=True)
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
    return track_set         

        



    print(track_set)
    print(len(track_set))
    print(last_retrieved_track_timestamp)
    
def get_artist(artist_name, num_songs):
    artist_set = set()
    artist_object = last_fm_object.get_artist(artist_name)
    things = artist_object.get_top_tracks(limit=num_songs, stream=True)
    for element in things:
        temp_str = (element[0])
        try:
           # prints song name just pulled 
            print(temp_str) 
            temp_str = str(temp_str)
            artist_set.add(temp_str)
        except UnicodeEncodeError:
            pass
    for element in artist_set:
        artist_name_corrected = element.split(' - ')[0].strip()
        break
    return artist_set, artist_name_corrected
    

def process_set(input_set):
    processed_set = set()
    for element in input_set:
        remove_chars = ['(', '[', 'ft.', 'feat.']
        for phrase in remove_chars:
            if element.find(phrase) != -1:
                element = element[:element.find(phrase)].strip()
        if element.count(' - ') == 1:
            processed_set.add(element)
        elif element.count(' - ') > 1:
            first_found_location = (element.find(' - '))
            element = element[:(element.find(' - ',first_found_location+1,-1))]
            processed_set.add(element)
    return processed_set

def trim_track_set(track_set_processed, artist_name_corrected):
    track_set_trimmed = set()
    for element in track_set_processed:
        if element.split(' - ')[0].strip() == artist_name_corrected:
            track_set_trimmed.add(element)
    return track_set_trimmed

def main():
    track_set = get_history(0, 'seaty6')
    print("Length of track Set, Unprocessed: " + str(len(track_set)))
    track_set_processed = process_set(track_set)
    print("Length of track Set, processed: " + str(len(track_set_processed)))

    artist_set, artist_name_corrected = get_artist('Kanye', 500)

    print(artist_name_corrected)
    print("Length of artist Set, Unprocessed: " + str(len(artist_set)))

    artist_set_processed = process_set(artist_set)

    print("Length of artist Set, processed: "    + str(len(artist_set_processed)))

    track_set_trimmed = trim_track_set(track_set_processed, artist_name_corrected)
    unlistened_songs = artist_set_processed - track_set_trimmed
    
    print(artist_set_processed)
    print(track_set_trimmed)
    print(unlistened_songs)


if __name__ == "__main__":
    main()