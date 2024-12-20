from flask import Flask, request, jsonify

app = Flask(__name__)

# store data
songs = {}
playlists = {}

# song manipulations
@app.route('/songs', methods=['POST'])
def create_song():
    data = request.get_json()
    song_id = data['id']
    song_data = {
        "name": data['name'],
        "artist": data['artist'],
        "genre": data['genre']
    }
    songs[song_id] = song_data
    return jsonify({"message": "Song created", "song": song_data}), 201

@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song = songs.get(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404
    return jsonify(song)

@app.route('/songs/<song_id>', methods=['PUT'])
def update_song(song_id):
    if song_id not in songs:
        return jsonify({"error": "Song not found"}), 404
    data = request.get_json()
    songs[song_id].update(data)
    return jsonify({"message": "Song updated", "song": songs[song_id]})

@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    if song_id not in songs:
        return jsonify({"error": "Song not found"}), 404
    del songs[song_id]
    return jsonify({"message": "Song deleted"})






# playlist manipulations
@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.get_json()
    playlist_id = data['id']
    playlist_data = {
        "name": data['name'],
        "songs": []
    }
    playlists[playlist_id] = playlist_data
    return jsonify({"message": "Playlist created", "playlist": playlist_data}), 201

@app.route('/playlists/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    playlist = playlists.get(playlist_id)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    return jsonify(playlist)

@app.route('/playlists/<playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    if playlist_id not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    data = request.get_json()
    playlists[playlist_id].update(data)
    return jsonify({"message": "Playlist updated", "playlist": playlists[playlist_id]})

@app.route('/playlists/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    if playlist_id not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    del playlists[playlist_id]
    return jsonify({"message": "Playlist deleted"})





# add-to, remove-from, and sort playlist manipulations
@app.route('/playlists/<playlist_id>/add_song', methods=['POST'])
def add_song_to_playlist(playlist_id):
    data = request.get_json()
    song_id = data['song_id']
    if playlist_id not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    if song_id not in songs:
        return jsonify({"error": "Song not found"}), 404
    playlists[playlist_id]['songs'].append(song_id)
    return jsonify({"message": "Song added to playlist", "playlist": playlists[playlist_id]})

@app.route('/playlists/<playlist_id>/remove_song', methods=['POST'])
def remove_song_from_playlist(playlist_id):
    data = request.get_json()
    song_id = data['song_id']
    if playlist_id not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    if song_id not in playlists[playlist_id]['songs']:
        return jsonify({"error": "Song not in playlist"}), 404
    playlists[playlist_id]['songs'].remove(song_id)
    return jsonify({"message": "Song removed from playlist", "playlist": playlists[playlist_id]})

@app.route('/playlists/<playlist_id>/sort', methods=['POST'])
def sort_playlist(playlist_id):
    data = request.get_json()
    sort_by = data.get('sort_by', 'name')
    if playlist_id not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    playlist_songs = playlists[playlist_id]['songs']
    sorted_songs = sorted(playlist_songs, key=lambda sid: songs[sid][sort_by])
    playlists[playlist_id]['songs'] = sorted_songs
    return jsonify({"message": "Playlist sorted", "playlist": playlists[playlist_id]})

if __name__ == '__main__':
    app.run(debug=True)
