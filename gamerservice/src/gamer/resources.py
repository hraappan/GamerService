'''
Created on 19.03.2014
Modified on 19.03.2014
@author: Hannu Raappana
'''

#Import the needed libraries.
from flask import Flask, url_for, request, Response, make_response, json, g
from flask.ext.restful import Resource, Api, reqparse, abort
from werkzeug.exceptions import NotFound, UnsupportedMediaType
import database

app = Flask(__name__)

#Path for the database.
MY_DATABASE_PATH = 'db/database.db'

app.config.update({'DATABASE':database.GamerDatabase(MY_DATABASE_PATH)})

api = Api(app)

#Helper for the database. //From the Flask- documentation.
@app.before_request
def set_database():
    g.my_db = app.config['DATABASE']
		
        
        


class Players(Resource):

    '''
    This class includes methods for player registration and making a collection of the Player resource.
    '''
    
    '''
Method: GET
headers={"Content-Type":"application/json",'Authorization':<player_id>}
getPlayers() /Output
{
'links': [{'title':'Games','rel':'related','href':'/game/api/games/'}],'players':[]}
}
#players is:
[{
'player':player,'link':{'title':'player', 'status',status, 'rel':'self','href':'/game/api/players/<player_id>'}
}]
    '''

    #Get all players from the database.
    def get(self):
	
	#Get the players from the database.
	_players_db = g.my_db.getPlayers()
	#If the player_list is empty.
	if not _players_db:
		return_message = {'message': "Players not found.", 'resource': 'Player', 'resource_url':request.path }
		abort(404, **return_message)
		
	_players = []
	
	#Go through the users in a loop and append the users to the dictionary.
	for player_db in _players_db:

		_playername = player_db["nickname"]
		_player_id = player_db["player_id"]
		_playerurl = api.url_for(Player, player_id=_player_id)
		_status = player_db["status"]

		_player = {}
		_player['player'] = _playername
		_player['status'] = _status
		_player['link'] = { 'title':'player', 'rel':'self', 'href':_playerurl }
		_players.append(_player)
		
	#Create the envelope and send it.
	envelope = {}
	envelope['links'] = [{'title':'games', 'rel':'related', 'href':api.url_for(Games)}]
	envelope['players'] = _players
	return envelope
	
    

    #Register a new player.    
    def post(self):
        

        try:
            self._parse_data()
        except:
            return_message = { 'message' : "The player %s has received a wrong request format.", 'resource_type': 'Player', 'resource_url':request.path,  'reource': "player"}
            abort(400, **return_message)
        data = request.parsed_data
        if not data:
            abort(415)
        
        username = data["username"]

        if g.my_db.containsPlayer(username):
		return_message = { 'message' : "The username %s is already in use." % username, 'resource': 'Player', 'resource_url':request.path }
		abort(404, **return_message)

        password = data ['password']

        _player_id = g.my_db.register(username, password)
        return_message = { 'title':'register', 'player_id':_player_id, 'links': [{'rel':'self', 'href':api.url_for(Player, player_id = _player_id) }]}
        return return_message, 201
        


    #parser for JSON.
    def _parse_json():

        return request.get_json()


    #Different parsers at use.
    parsers = {'application/json': _parse_json }

    #Parser function to select right parser for the request.
    def _parse_data(self):
        request.parsed_data = None
        content_type = request.headers.get("Content-Type", None)
        parser = self.parsers.get(content_type, None)
        if callable (parser):
            try:
                request.parsed_data = parser()
            except Exception as e:
                print e
                raise ValueError("Malformed data in Players request.")
        

                
class Player(Resource):

    '''
    This class includes methods for getting a specific player and deleting a player from the database.
    '''

    #Get a player.
    def get(self, player_id):
        player_db = g.my_db.getPlayer(player_id)
            
        if not player_db:
            return_message = { 'message' : "The player %s not found." %player_id, 'resource': 'Player', 'resource_url' : request.path }
            abort(404, **return_message)
        envelope = {}
        envelope['links'] = [{'title':'players', 'rel':'collection', 'href':api.url_for(Players) }]
        player = { 'nickname': player_db["nickname"], 'status': player_db["status"], 'username': player_db["username"] }
        player['player_profile'] = {'title':'playerprofile', 'rel':'child', 'href':api.url_for(Player_profile, player_id=player_id) }
            
        envelope['player'] = player

        return envelope

    #Modify player.
    def put(self, playerid):
        player_db = g.my_db.getPlayer(playerid)
            
        if not player_db:
            return_message = { 'message' : "The player %s not found." %player_id, 'resource': 'Player', 'resource_url' : request.path }
            abort(404, **return_message)

        
        
    
    
    #Delete player.
    def delete(self, player_id):
        if not g.my_db.getPlayer(player_id):
            return_message = { 'message' : "The player %s not found." %player_id, 'resource': 'Player', 'resource_url' : request.path }
            abort(403, **return_message)
	    g.my_db.deletePlayer(player_id)
	    return None, 204
    
	

class Player_profile(Resource):
        '''
        This class includes methods for adding a player profile, and getting a profile belonging to a player.
        '''


        #Add a player profile.
        def put(self, player_id):
            
            player_profile = g.my_db.getPlayerProfile(player_id)
            if not player_profile:
                return_message = { 'message' : "The player %s not found." %player_id, 'resource': 'Player_profile', 'resource_url' : request.path }
                abort(404, **return_message)
            
            try:
                self._parse_data()
            except:
                return_message = { 'message' : "The player_profile %s has received a wrong request format." %player_id, 'resource_type': 'Player_profile', 'resource_url':request.path,  'reource_id':player_profile }
                abort(400, **return_message)
            data = request.parsed_data
            if not data:
                abort(415)

            print data

            #TODO: Only the nickname should be checked.
            try:
                
                nickname = data["nickname"]
                basic_information = data["basic_profile"]
            except:
                abort(400)
            else:
                g.my_db.addPlayerProfile(player_id, nickname, basic_information)
                return None, 204
            
        
        #Get a player profile.
	def get(self, player_id):
            player_profile = g.my_db.getPlayerProfile(player_id)
            print player_profile
            if not player_profile:
                return_message = { 'message' : "The player %s not found." %player_id, 'resource': 'Player', 'reource_url' : request.path }
                abort(404, **return_message)
            envelope = {}
            envelope['links'] = [{'title':'player', 'rel':'parent', 'href':api.url_for(Player, player_id = player_id) },
                                  {'title':'playerprofile', 'rel':'related', 'href':api.url_for(Player_profile, player_id = player_id) }]
            player_profile = {'nickname':player_profile["nickname"], 'basic_information':player_profile["basic_information"] }
            envelope['player_profile'] = player_profile
            return envelope
            
        
        
        
           
        #parser for JSON.
        def _parse_json():

            return request.get_json()

        

        #Different parsers at use.
        parsers = {'application/json': _parse_json }

        #Parser function to select right parser for the request.
        def _parse_data(self):
            request.parsed_data = None
            content_type = request.headers.get("Content-Type", None)
            parser = self.parsers.get(content_type, None)
            if callable (parser):
                try:
                    request.parsed_data = parser()
          
                except Exception as e:
                    print e
                    raise ValueError("Malformed data in Players request.")
                    
            
            
	
	
class Messages(Resource):
        '''
        This class includes methods for creating a collection of Message resource, and for posting a message.
        '''
        
        #Get all messages from the database.
	def get(self):
            _messages_db = g.my_db.getMessages()
            if not _messages_db:
                return_message = { 'message':"Messages not found", 'resource':'Message', 'resource_url':request.path }
                abort(404, **return_message)

            _messages = []

            for message_db in _messages_db:
                message = {}
                _title = message_db["title"]
                _message_id = message_db["message_id"]
                _url = api.url_for(Message, message_id = _message_id)
                message['title'] = _title
                message['link'] = { 'rel':'related', 'href':_url }
                _messages.append(message)

            envelope =  {}
            envelope['links'] = [{ 'title':'players', 'rel':'related', 'href':api.url_for(Messages) }]
            envelope['messages'] = _messages
            return envelope;
	    

	#Post a message.
	def post(self):

            try:
                self._parse_data()
            except:
                return_message = { 'message' : "The message received is in wrong format.", 'resource_type':'Message','resource_url':request.path }
                abort(400, **return_message)

            data = request.parsed_data     
            if not data:
                abort(415)

            _sender = data['playerid']
            _title = data['title']
            _body = data['body']
            print _sender

            message_id = g.my_db.postMessage(_sender, _title, _body)
            return_message = { 'title':'message', 'message_id':message_id, 'rel':'related', 'href':api.url_for(Message, message_id = message_id) }
            #print return_message
            return return_message, 201;

	#parser for JSON.
        def _parse_json():
            return request.get_json()


        #Different parsers at use.
        parsers = {'application/json': _parse_json }

        #Parser function to select right parser for the request.
        def _parse_data(self):
            request.parsed_data = None
            content_type = request.headers.get("Content-Type", None)
            parser = self.parsers.get(content_type, None)
            if callable (parser):
                try:
                    request.parsed_data = parser()
                    
                except Exception as e:
                    print e
                    raise ValueError("Malformed data in Messages request.")
            
	
class Message(Resource):
        '''
        This class includes methods for getting a specific message, deleting a message and modifying a message.
        '''

        #Get a specific message.
	def get(self, message_id):
            _message_db = g.my_db.getMessage(message_id)
            if not _message_db:
                return_message = { 'message':"Message not found %s" % message_id, 'resource':'Message', 'resource_url':request.path, 'resource_id':message_id }
                abort(404, **return_message)

            _title = _message_db['title']
            _body = _message_db['body']
            _sender = _message_db['sender']


            envelope = {}
            envelope['links'] = [{'title':'messages', 'rel':'related', 'href':api.url_for(Messages)},
                                {'sender':_sender, 'rel':'related', 'href':api.url_for(Player, player_id=_sender)}]
            envelope['title'] = _title
            envelope['body'] = _body

            return envelope
            
	    

	#Modify a message.
	def put(self, player_id, message_id):

            

            try:
               self._parse_data()
            except:
                return_message = { 'message' : "The message received is in wrong format.", 'resource_type':'Message','resource_url':request.path }
                abort(400, **return_message)
            data = request.parsed_data
            if not data:
                abort(415)

            _title = data['title']
            _body = data['body']

            g.my_db.modifyMessage(_title, _body, message_id, player_id)
            

        #Delete a message.
	def delete(self, message_id):
            if not g.my_db.getMessage(message_id):
                return_message = { 'message':"There are no message id %s" % message_id, 'resource':'Message', 'resource_url':request.path, 'resource_id':message_id }
                abort(404, **return_message)

            g.my_db.deleteMessage(message_id)
            return None, 204
	    
	#parser for JSON.
        def _parse_json():
            return request.get_json()

        

        #Different parsers at use.
        parsers = {'application/json': _parse_json }

        #Parser function to select right parser for the request.
        def _parse_data(self):
            request.parsed_data = None
            content_type = request.headers.get("Content-Type", None)
            parser = self.parsers.get(content_type, None)
            if callable (parser):
                try:
                    request.parsed_data = parser()
                except Exception as e:
                    print e
                    raise ValueError("Malformed data in Players request.")
                    
	
class Games(Resource):
        '''
        This class includes methods for creating a collection of Game resource, and for creating a new game. I is also used to create a game againts an A.I.
        '''
        
        #Get all ongoing games.
	def get(self):
            _games_db = g.my_db.getGames()
            if not _games_db:
                return_message = {'message': "There are no ongoing games currently in the database.", 'resource': 'Games', 'resource_url':request.path }
		abort(404, **return_message)

            _games = []
            for game_db in _games_db:
                print game_db
                _game = {}
                _game_id = game_db['id']
                _game_state = game_db['state']
                _game_url = api.url_for(Game, game_id =_game_id)
                print _game_url
                _game['link'] = {'title':'game', 'rel':'self', 'href':_game_url }
                _game['id'] = _game_id
                _game['state'] = _game_state
                _games.append(_game)

            envelope = {}
            envelope['links'] = [{ 'title':'players', 'rel':'related', 'href':api.url_for(Games) }]
            envelope['games'] = _games
            return envelope
            
            
        #Create a new game.
	def put(player_id):
            if not player_id:
                return_message = { 'message':"You must specify a player_id.", 'resource':'Games', 'resource_url': request.path}
                abort(404, **return_message)
            '''
            try:
                self._parse_data()
                
            except:
                return_message = { 'message' : "The message received is in wrong format.", 'resource_type':'Games','resource_url':request.path }
                abort(400, **return_message)

            data = request.parsed_data
            if not data:
                abort(415)

            '''
            
            _opponent = "Artificial intelligence"
            _game = "Othello"

            #Artificial intelligence not yet implemented. Also the game is always othello.
            if _opponent is not "Artificial intelligence":
                game_id = g.my_db.createGame(player_id)
                return_message = {'title':'game', 'game_id':game_id, 'rel':'related', 'href':api.url_for(Move, game_id=game_id) }
                return 201, return_message
     

	#parser for JSON.
        def _parse_json():

            return request.get_json()

        

        #Different parsers at use.
        parsers = {'application/json': _parse_json }

        #Parser function to select right parser for the request.
        def _parse_data(self):
            request.parsed_data = None
            parser = self.parsers.get(content_type, None)
            if callable (parser):
                try:
                    request.parsed_data = parser()
                except Exception as e:
                    print e
                    raise ValueError("Malformed data in Players request.")
                    
	
class Game(Resource):
        '''
        This class includes methods for updating a game (getGame), and joining into a game.
        '''

        #Get game.
	def get(self, game_id):
            _game = g.my_db.getGame(game_id)
            if not _game:
                return_message = {'message':"Invalid game %s." %game_id, 'resource': 'Game', 'resource_url':request.path}
                abort(404, **return_message)

            print _game
            _moves = _game['moves']
            _creator = _game['creator']
            _opponent = _game['opponent']
            _state = _game['state']
            _winner = _game['winner']
            _turn = _game['turn']
            _game_id = _game['game_id']

            envelope = {}
            #envelope = {'state':_state, 'creator': _creator, 'opponent':_opponent, 'winner':_winner, 'turn':_turn, 'link':[{'rel':'related', 'href':api.url_for(Move, game_id = _game_id) }]}
            envelope['game'] = _game
            return envelope
            

        #Join game.
	def put(self, player_id, game_id):
            _game = g.my_db.getGame(game_id)
            if not _game:
                return_message = {'message':"Invalid game id %s." %game_id, 'resource': 'Game', 'resource_url':request.path}
                abort(404, **return_message)

            if not _game["opponent"]:
                g.my_db.joinGame(player_id, game_id)
            #TODO: error message if the game is full already.

            return None, 204
            

class Move(Resource):
        '''
        This class includes methods for making a move in a game.
        '''
        
        def get(self):

            pass

        #Make a move in the game.
	def put(self, game_id):

            if not g.my_db.getGame(game_id):    
                return_message = {'message':"Invalid game %s." %game_id, 'resource': 'Game', 'resource_url':request.path}
                abort(404, **return_message)

           

            try:
                self._parse_data()
                
            except:
                return_message = { 'message' : "The move to game %s has received a wrong request format." %game_id, 'resource_type':'Move','resource_url':request.path,'reource_id': game_id }
                abort(400, **return_message)
            data = request.parsed_data
            if not data:
                abort(415)

            _x = data["x"]
            _Y = data["y"]
            _player_id = data["player_id"]
            g.my_db.move(_x, _y, _player_id, game_id)
            return None, 204
	    

	#parser for JSON.
        def _parse_json():

            return request.get_json()

        

        #Different parsers at use.
        parsers = {'application/json': _parse_json }

        #Parser function to select right parser for the request.
        def _parse_data(self):
            request.parsed_data = None
            content_type = request.headers.get("Content-Type", None)
            parser = self.parsers.get(content_type, None)
            if callable (parser):
                try:
                    request.parsed_data = parser()
                except Exception as e:
                    print e
                    raise ValueError("Malformed data in Players request.")
        
	
class Leaderboard(Resource):
        '''
        This class includes the methods for getting the leaderboards.
        '''
        
	def get(self):
		
            pass
class Thread(Resource):
        '''
        This class includes the methods for getting the message threads.
        '''
        
	def get(self):
            pass
		

#Add the resources.
api.add_resource(Players, '/game/api/players/', endpoint='players')
api.add_resource(Player, '/game/api/player/<player_id>/', endpoint='player')
api.add_resource(Player_profile, '/game/api/player/<player_id>/player_profile/', endpoint='player_profile')
api.add_resource(Messages, '/game/api/forum/messages/', endpoint='messages')
api.add_resource(Message, '/game/api/forum/message/<message_id>/', endpoint='message')
api.add_resource(Games, '/game/api/games/', endpoint='games')
api.add_resource(Game, '/game/api/game/<game_id>/', endpoint='game')
api.add_resource(Leaderboard, '/game/api/games/leaderboard/', endpoint='leaderboard')
api.add_resource(Move, '/game/api/games/<game_id>/move/', endpoint='move')
api.add_resource(Thread, '/game/api/forum/<thread_id>/thread/', endpoint='thread')


#Run the program.
if __name__ == "__main__":
#Run in debug mode so we don't need to restart the server manually all the time.
	app.debug = True
	app.run()
