'''
Created on 19.03.2014
Modified on 19.03.2014
@author: Hannu Raappana
'''

from datetime import datetime
from copy import deepcopy
import time, sqlite3, sys, re, os	

class GamerDatabaseInterface(object):


        def load_initial_values(self):
                #This loads the initial values for the database. It also creates the tables.
                pass

        def clean(self):
                #This cleans up the database.
                pass

	def getPlayer(self, player_id):
                #This method returns a player object according to the given playerId parameter.
                pass

        def addPlayerProfile(self, player_id, nickname, basic_information):
                #This method is used to store a player_profile to a specific player.
                pass

        def getPlayerProfile(self, player_id):
                #This method return a player profile for a specific player.
                pass

        def register(self, username, password):
                #This method registers a player and stores it to a database.
                pass
        
	def getPlayers(self):
                #This method returns all the players from the database.
		pass
	
	def getGames(self):
                #This method returns all the games from the database.
                pass

        def getGame(self, game_id):
                #This method return a specific game according to the given parameter.
                pass

        def move(self, x, y, player_id, game_id):
                #This method adds a move in a game along with the player and game information. It also changes the turn.
                pass

        def joinGame(self, player_id, game_id):
                #This method is used to join in a game.
                pass
        
        def createGame(self, player_id):
                #This method creates a new game.
                pass

        def postMessage(self, sender, title, body):
                #This method is used to post a new message.
                pass

	def getMessages(self):
                #This method returns all the messages from the database.
		pass

        def getMessage(self, message_id):
                #This method returns a specific message from the database according to the given parameter.
                pass
        
        def deleteMessage(self, message_id):
                #This method deleted a message from the database.
                pass

        def editPlayerInformation(self, playerid, password):
                #This method can be used to edit player information.
                pass

	pass

class GamerDatabase(GamerDatabaseInterface):
        
	def __init__(self, database_path):
		super(GamerDatabase, self).__init__()
		self.database_path = database_path
		pass

	def clean(self):
                #Clean the database.
                '''
                os.remove(self.database_path)
                '''

	#Next methods create the tables for the database.
	def create_player_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE player(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                                username TEXT, password TEXT, status TEXT)'

                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None                                
		pass

	def create_game_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE game(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                                state TEXT, winner INTEGER, creator INTEGER , \
                                turn INTEGER, opponent INTEGER, \
                                FOREIGN KEY(winner) REFERENCES player(id), \
                                FOREIGN KEY(creator) REFERENCES player(id), \
                                FOREIGN KEY(opponent) REFERENCES player(id), \
                                FOREIGN KEY(turn) REFERENCES player(id))'


                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None
                pass

        def create_player_profile_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE player_profile(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                                playerId INTEGER, profile TEXT, nickname TEXT, \
                                FOREIGN KEY(playerId) REFERENCES player(id) ON DELETE CASCADE)'

                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None
                pass

        def create_move_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE move(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                                creator INTEGER, x INTEGER, y INTEGER, gameId INTEGER, \
                                FOREIGN KEY(creator) REFERENCES player(id) ON DELETE CASCADE, \
                                FOREIGN KEY(gameId) REFERENCES game(id) ON DELETE CASCADE)'

                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None
                pass

        def create_leaderboard_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE leaderboard(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                                gameId INTEGER, FOREIGN KEY(gameId) REFERENCES game(id))'

                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None
                pass

        def create_player_game_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE player_game(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                                playerId INTEGER, gameId INTEGER, \
                                FOREIGN KEY(playerId) REFERENCES player(id), \
                                FOREIGN KEY(gameId) REFERENCES game(id))'

                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None
                pass

        def create_message_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE message(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                                body TEXT, title TEXT, sender INTEGER, threadId INTEGER, \
                                FOREIGN KEY(sender) REFERENCES player(id), \
                                FOREIGN KEY(threadId) REFERENCES thread(id))'

                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None
                pass

        def create_thread_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE thread(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                        messageId INTEGER, FOREIGN KEY(messageId) REFERENCES message(id))'

                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None
                pass

        def create_transaction_log_table(self):
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'CREATE TABLE transaction_log(id INTEGER PRIMARY KEY AUTOINCREMENT , \
                                playerId INTEGER, request TEXT, response TEXT, \
                                FOREIGN KEY(playerId) REFERENCES player(id))'

                con = sqlite3.connect(self.database_path)

                with con:
                        cur = con.cursor()
                        try:
                                cur.execute(keys_on)
                                cur.execute(stmnt)
                        except sqlite3.Error, e:
                                print "Error: %s ", e.args[0]

                return None
                pass
                
        def create_tables(self):
                self.create_player_table()
                self.create_game_table()
                self.create_player_profile_table()
                self.create_move_table()
                self.create_leaderboard_table()
                self.create_player_game_table()
                self.create_message_table()
                self.create_thread_table()
                self.create_transaction_log_table()
                self.load_values_from_dumb()

        def load_initial_values(self):
                self.create_tables()
                pass

        def load_values_from_dumb(self):
                #This method load values from a dumb.
                con = sqlite3.connect(self.database_path)
                with open ('db/gamer_data_dumb.sql') as f:
                        sql = f.read()
                        cur = con.cursor()
                        cur.executescript(sql)
                pass

        def create_player_object(self, row, player_id):
                '''
                Builds a dictionary of the player object and returns it.
                '''
                
                player_nickname = row['nickname']
                player_status = row['status']
                player_username = row['username']

                if not player_id:
                        _player_id = row['playerId']
                else:
                        _player_id = player_id

                player = { 'nickname': player_nickname, 'status':player_status, 'player_id':_player_id, 'username':player_username }

                return player
                pass

        def create_message_object(self, row):
                '''
                Builds a dictionary of the message and returns it.
                '''
                message_title = row['title']
                message_body = row['body']
                message_sender = row['sender']
                message_id = row['id']

                message = { 'sender': message_sender, 'title': message_title, 'body': message_body, 'message_id':message_id }
                return message
                pass

        def create_game_object(self, game, moves):
                '''
                Builds a dictionary of the game and returns it.
                '''
                game_state = game['state']
                game_winner = game['winner']
                game_turn = game['turn']
                game_creator = game['creator']
                game_opponent = game['opponent']
                game_id = game['id']
                game_moves = moves

                message = { 'game_id': game_id, 'state': game_state, 'winner': game_winner, 'turn': game_turn, 'creator':game_creator, 'turn':game_turn, 'opponent':game_opponent, 'moves':game_moves }
                return message
                pass


        def getPlayer(self, player_id):
                '''
                Returns a specific player according to the player_id parameter.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'SELECT username, nickname, status FROM player_profile, player WHERE playerId = ?'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()

                        cur.execute(keys_on)
                        pvalue = (player_id,)
                        cur.execute(stmnt, pvalue)

                        #One value is expected.
                        row = cur.fetchone()

                        if row is None:
                                return None
                        else:
                                return self.create_player_object(row,player_id)
                        

                pass

        def editPlayerInformation(self, playerid, password):

                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'UPDATE player SET password = ? WHERE id = ?'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()

                        cur.execute(keys_on)
                        pvalue = (username,password,)
                        cur.execute(stmnt, pvalue)

                        #One value is expected.
                        row = cur.fetchone()

                        if row is None:
                                return False
                        else:
                                return True

                pass
                

        def getPlayers(self):
                '''
                Returns a specific player according to the player_id parameter.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'SELECT player.*, player_profile.* FROM player_profile, player WHERE player.id = player_profile.playerId'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()

                        cur.execute(keys_on)
                        cur.execute(stmnt)

                        #More than one value is expected.
                        rows = cur.fetchall()

                        if rows is None:
                                return None

                        players = []

                        #Add all the players to the list and return it.
                        for row in rows:
                                players.append(self.create_player_object(row,None))

                        return players
                pass

        def addPlayerProfile(self, player_id, nickname, basic_information):
                '''
                Adds / updates a player profile.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'INSERT INTO player_profile(id, playerId, profile, nickname) values(?,?,?,?)'
                stmnt1 = 'SELECT * FROM player_profile WHERE playerId = ?'
                stmnt2 = 'UPDATE player_profile set profile = ?, nickname = ? WHERE playerId = ?'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()

                        cur.execute(keys_on)
                        playerid = (player_id,)
                        cur.execute(stmnt1, playerid)

                        rows = cur.fetchall()
                        if rows is None:
                                print "IF"
                                ivalues = (None, player_id, basic_information, nickname)
                                cur.execute(stmnt, ivalues)
                                return True;
                        else:
                                print "ELSE"
                                ivalues = (basic_information, nickname, player_id)
                                cur.execute(stmnt2, ivalues)
                                return True;

        def getPlayerProfile(self, player_id):
                '''
                Returns a profile from the database.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'SELECT * FROM player_profile where playerId = ?'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)


                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()

                        cur.execute(keys_on)
                        ivalue = (player_id,)
                        cur.execute(stmnt, ivalue)

                        #One value is expected.
                        row = cur.fetchone()

                        if row is None:
                                return None
                        else:
                                return { 'nickname':row['nickname'], 'basic_information':row['profile'] }
                        

                pass

        def getMessage(self, message_id):
                '''
                Returns a specific message according to the message_id parameter.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'SELECT * FROM message WHERE id = ?'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()

                        cur.execute(keys_on)
                        pvalue = (message_id,)
                        cur.execute(stmnt, pvalue)

                        #One value is expected.
                        row = cur.fetchone()

                        if row is None:
                                return None
                        else:
                                return self.create_message_object(row)
                        

                pass

        def getMessages(self):
                '''
                Returns all the messages from the database.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'SELECT * FROM message'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()

                        cur.execute(keys_on)
                        cur.execute(stmnt)

                        #More than one value is expected.
                        rows = cur.fetchall()
                        messages = []
                        if rows is None:
                                return None

                        for row in rows:
                                messages.append(self.create_message_object(row))

                        return messages
                        

                pass

        def register(self, username, password):
                '''
                Adds a player to the database.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'INSERT INTO player(id, username, password) values (?,?,?)'
                _username = username
                query = 'SELECT id FROM player WHERE username = ?'
                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        ivalues = (None, _username, password)
                        print ivalues

                        cur.execute(keys_on)
                        cur.execute(stmnt, ivalues)

                     
                        if cur.rowcount < 1:
                                return False
                        else:
                                player_id = cur.lastrowid
                                cur.execute(keys_on)
                                ivalues = (username,)
                                cur.execute(query, ivalues)
                                return player_id             

                pass

        def getGames(self):

                '''
                Returns all the games from the database.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'SELECT * FROM game'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()

                        cur.execute(keys_on)
                        cur.execute(stmnt)

                        #More than one value is expected.
                        rows = cur.fetchall()
                        games = []
                        if rows is None:
                                return None

                        for row in rows:
                                _game = {}
                                _game_id = row['id']
                                _game_state = row['state']
                                _game["id"] = _game_id
                                _game["state"] = _game_state
                                print _game
                                games.append(_game)

                        return games

                pass

        def getGame(self, game_id):

                '''
                Returns a specific game from the database.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'SELECT * FROM game WHERE id = ?'
                stmnt_moves = 'SELECT * FROM move WHERE gameId = ?'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        pvalue = (game_id,)

                        cur.execute(keys_on)                        
                        cur.execute(stmnt, pvalue)
                        
                        #One value is expected.
                        row = cur.fetchone()
                        _game = {}
                        _game["id"] = row['id']
                        _game["state"] = row['state']
                        _game["winner"] = row['winner']
                        _game["turn"] = row['turn']
                        _game["creator"] = row['creator']
                        _game["opponent"] = row['opponent']
                        
                        if row is None:
                                return None

                        else:

                                cur.execute(keys_on)
                                cur.execute(stmnt_moves, pvalue)
        
                                #More than one value is expected for moves.
                                rows = cur.fetchall()
                                moves = []
                                if rows is None:
                                        return None

                                for move_row in rows:
                                        move = {}
                                        move["x"] = move_row['x']
                                        move["y"] = move_row['y']
                                        move["creator"] = move_row['creator']
                                        moves.append(move)
                return self.create_game_object(_game, moves)
                pass

        def move(self, x, y, player_id, game_id):
                '''
                Adds a move to a game and changes the turn.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'INSERT INTO move(id, creator, x, y, gameId) values (?,?,?,?,?)'
                query_participants = 'SELECT * FROM game_player WHERE gameId = ?'
                change_turn = 'UPDATE game SET turn = ? WHERE gameId = game_id'
        
                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        ivalues = (None, x, y, player_id, game_id)

                        cur.execute(keys_on)
                        cur.execute(stmnt, ivalues)

                     
                        if cur.rowcount < 1:
                                return False
                        else:
                                cur.execute(keys_on)
                                cur.execute(query_participants, game_id)

                                #Two rows are expected so we can run this in a loop. If there are more this must be changed because it can change the turn for a wrong player.
                                rows = cur.fetchall()
                                for row in rows:
                                        if row['playerId'] != player_id:
                                                cur.execute(keys_on)
                                                cur.execute(change_turn, row['playerId'])
                                                
                                return True            

                pass

        def createGame(self, player_id):
                '''
                Adds a new game to the database.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'INSERT INTO game(id, state, winner, creator, turn, opponent) values (?,?,?,?,?,?)'
                query = 'INSERT INTO player_game(gameId, playerId) values (?,?,?)'
        
                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        ivalues = (None, "ongoing", None, player_id, player_id, None)

                        cur.execute(keys_on)
                        cur.execute(stmnt, ivalues)

                        if cur.rowcount < 1:
                                return False
                        else:
                                game_id = cur.lastrowid
                                cur.execute(keys_on)
                                ivalues = (None, game_id, player_id)
                                cur.execute(query, ivalues)
                                return game_id             

                pass

        def postMessage(self, sender, title, body):
                '''
                Adds a new message to the database.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'INSERT INTO message(id, body, title, sender, threadid) values (?,?,?,?,?)'
        
                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        ivalues = (None, body, title, sender, None)

                        cur.execute(keys_on)
                        cur.execute(stmnt, ivalues)

                        if cur.rowcount < 1:
                                return False
                        else:
                                message_id = cur.lastrowid
                                return message_id             

                pass

        def deleteMessage(self, message_id):
                '''
                Deletes a message from the database.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'DELETE FROM message WHERE id = ?'
        
                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        ivalues = (message_id,)
                        cur.execute(keys_on)
                        cur.execute(stmnt, ivalues)

                       

                        if cur.rowcount < 1:
                                return False
                        else:

                                return True

                pass

        def joinGame(self, player_id, game_id):
                '''
                Adds a player to a game.
                '''
                
                keys_on = 'PRAGMA foreign_keys = ON'
                stmnt = 'INSERT INTO player_game(id, gameId, playerId) values (?,?,?)'
                query = 'UPDATE game SET opponent = player_id WHERE id = game_id'
        
                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        ivalues = (None, game_id, playerId)

                        cur.execute(keys_on)
                        cur.execute(stmnt, ivalues)
                        cur.execute(query)

                        if cur.rowcount < 1:
                                return False
                        else:
                                return True         

                pass

        def containsPlayer(self, username):
                '''
                Checks if the username is already in use.
                '''

                keys_on = 'PRAGMA foreign_keys = ON'
                query = 'SELECT * FROM player where username = ?'

                #Create conncetion to the database.
                con = sqlite3.connect(self.database_path)

                with con:
                        #instantiate row factory and get the cursor for executing sql- statements. 
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        ivalues = (username,)

                        cur.execute(keys_on)
                        cur.execute(query, ivalues)

                        if cur.rowcount < 1:
                                return False
                        else:
                                return True
        
pass
