import requests 
import json
import test106 as test

class Artist():
	def __init__ (self, artist, popularity):
		self.artist = artist
		self.popularity = popularity
		self.events = []

	def get_events(self):
		ticketmaster_baseurl = "https://app.ticketmaster.com/discovery/v1/events.json"
		response = requests.get(ticketmaster_baseurl, params={
			'apikey' : 'UVnb1hGAEPt7pAYAY3DD0mj5FG7gxocc',
			'keyword' : self.artist

		})
		r = response.json()
		if '_embedded' in r:
			for x in r['_embedded']['events']:
				name = x['name']
				location = x['_embedded']['venue'][0]['name']
				start_date = x['dates']['start']['localDate']
				self.events.append((name, location, start_date))


	def pretty_print(self):
		self.get_events()
		x = u"The artist {} has a popularity level of {}.".format(self.artist, self.popularity)
		print x
		if len(self.events) > 0:
			for t in self.events:
				if t:
					print_string =  u"       The event {} at {} is on {}.".format(t[0], t[1], t[2])
					print print_string

spotify_baseurl = 'https://api.spotify.com/v1'
def get_related_artists(aid):
	response = requests.get(spotify_baseurl + '/artists/' + aid + '/related-artists')
	r = response.json()

	L = []
	for artist in r['artists']:
		name = artist['name']
		popularity = artist['popularity']
		s = Artist(name, popularity)
		L.append(s)
	new_list = [person for person in L if person.popularity > 60] #remove artists with low pop score
	return new_list
def get_artist_id():
	response = requests.get(spotify_baseurl + '/search', params= {
		'q':raw_input('Enter an artist: '), 
		'type':'artist'
	})
	r = response.json()
	return r['artists']['items'][0]['id']


	
def main():
	try:
		print "Accessing Spotify API"

		artist_id = get_artist_id()
		
		related_artists = get_related_artists(artist_id)

		for x in related_artists:
			x.get_events()

		sort_lst = sorted(related_artists, key=lambda x: x.popularity, reverse = True)

#testing artist constructor
		p = Artist('testName', 0)

		test.testEqual(p.artist, 'testName')
		test.testEqual(p.popularity, 0)

#testing get_related_artists using Adele's artist ID
		testList = get_related_artists('4dpARuHxo51G3z768sgnrY')
		test.testEqual("Amy Winehouse", str(testList[0].artist))

#testing get_events
		s = Artist('Ellie Goulding', 88)
		s.get_events()
		test.testEqual('Ellie Goulding', str(s.events[0][0]))
		test.testEqual('Xcel Energy Center', str(s.events[0][1]))
		test.testEqual('2016-05-05', str(s.events[0][2]))

		for artist in sort_lst:
			artist.pretty_print()
	except ValueError: 
		print 'Program Failed'

main()
