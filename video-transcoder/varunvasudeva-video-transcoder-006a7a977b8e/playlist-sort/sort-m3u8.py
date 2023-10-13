import m3u8

def sortPlaylist(masterfn):
	srcf=open(masterfn,'r')
	playlist_text=srcf.read()
	srcf.close()
	parsed_playlist = m3u8.loads(playlist_text)
	parsed_playlist.playlists.sort(key=lambda x: x.stream_info.average_bandwidth)
	new_playlist_text = parsed_playlist.dumps()
	print(new_playlist_text)
	f=open('master_new.m3u8','w+')
	f.write(new_playlist_text)
	f.close()
	return(True)

url="master.m3u8"
sortPlaylist(url)



