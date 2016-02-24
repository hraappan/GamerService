import unittest
import flask.ext.testing
import flask, json

import src.gamer.resources as resources
import src.gamer.database

my_db_path = 'db/database.db'
my_db = src.gamer.database.GamerDatabase(my_db_path)

class ResourcesAPITestCase(unittest.TestCase):
   
    def setUp(self):
        resources.app.config['TESTING'] = True 
        resources.app.config['DATABASE'] = my_db
        #my_db.load_initial_values()
        self.client = resources.app.test_client()
        
    def tearDown(self):
        my_db.clean()


class PlayersTestCase(ResourcesAPITestCase):

    url1 = '/game/api/players/'
    url2 = '/game/api/players/'

    
    @classmethod
    def setUpClass(cls):
        print 'Testing PlayersTestCase'
        
    def setUp(self):
        super(PlayersTestCase,self).setUp()

        self.player = {u"username": u"Playerdude", u"password": u"Playerdude" }
        self.player_wrong = {"username": "Playerdude", "password": "Playerdude" }
                                   
        

    def test_url(self):
        print "Test url."
        with resources.app.test_request_context(self.url1):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Players)

    def test_players_found(self):
        print "Test get players."
        response = self.client.get(self.url2)
        self.assertEquals(200, response.status_code)

    def test_add_player(self):
        print "Test add player."
        resp = self.client.post(self.url2, data=json.dumps(self.player), headers={"Content-Type":"application/json"})
        self.assertEquals(resp.status_code, 201)
        
    def test_add_player_wrong_format(self):
        print "Test add player with wrong format."
        resp = self.client.post(self.url2, self.player_wrong, headers={"Content-Type":"application/json"})
        self.assertEquals(resp.status_code, 400)
        

    
        

class PlayerProfileTestCase(ResourcesAPITestCase):

    url = '/game/api/player/<player_id>/player_profile/'
    url_profile = '/game/api/player/1/player_profile/'
    url_profile2 = '/game/api/player/?1/player_profile/'
    
    user1 = { 'nickname':'user1', 'basic_information':'basic_information' }
    @classmethod
    def setUpClass(cls):
        print 'Testing PlayerProfileTestCase'

    def setUp(self):
        super(PlayerProfileTestCase,self).setUp()


    def test_url(self):
        print "Test url."
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Player_profile)

    def test_player_profile_not_found(self):
        print "Test player not found."
        response = self.client.get(self.url)
        self.assertEquals(404, response.status_code)

    def test_add_profile(self):
        print "Test add profile."
        resp = self.client.put(self.url_profile, self.user1)
        player_profile_in_db = self.client.get(self.url_profile)
        self.assertEquals(200, player_profile_in_db.status_code)
        

class PlayerTestCase(ResourcesAPITestCase):

    url = '/game/api/player/<player_id>/'
    
    @classmethod
    def setUpClass(cls):
        print 'Testing PlayerTestCase'

    def setUp(self):
        super(PlayerTestCase,self).setUp()

    def test_url(self):
        print "Test url."
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Player)

    def test_player_not_found(self):
        print "Test player not found."
        response = self.client.get(self.url)
        self.assertEquals(404, response.status_code)

    

class GamesTestCase(ResourcesAPITestCase):

    url = '/game/api/games/'
    @classmethod
    def setUpClass(cls):
        print 'Testing GamesTestCase'

    def setUp(self):
        super(GamesTestCase,self).setUp()

    def test_url(self):
        print "Test url."
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Games)

    def test_games_found(self):
        print "Test get games."
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)

    def test_add_game(self):
        print "Test add game."
        response = self.client.put(self.url, 1, headers={"Content-Type":"application/json"})
        self.assertEquals(200, response.status_code)
        

class GameTestCase(ResourcesAPITestCase):
    url = '/game/api/games/?1/'
    @classmethod
    def setUpClass(cls):
        print 'Testing GameTestCase'

    def setUp(self):
        super(GameTestCase,self).setUp()
        
    def test_url(self):
        print "Test url."
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Games)

    def test_game_found(self):
        print "Test getGame."
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)
        

class MessagesTestCase(ResourcesAPITestCase):

    url = '/game/api/forum/messages/'

    @classmethod
    def setUpClass(cls):
        print 'Testing MessagesTestCase'

    def setUp(self):
        super(MessagesTestCase,self).setUp()

    def test_url(self):
        print "Test url."
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Messages)

    def test_messages_found(self):
        print "Test getMessages."
        response = self.client.get(self.url)
        self.assertEquals(200, response.status_code)

        


class MessageTestCase(ResourcesAPITestCase):

    url = '/game/api/forum/message/<message_id>/'
    url = '/game/api/forum/message/h1/'

    @classmethod
    def setUpClass(cls):
        print 'Testing MessageTestCase'

    def setUp(self):
        super(MessageTestCase,self).setUp()

    def test_url(self):
        print "Test url."
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Message)

    def test_message_not_found(self):
        print "Test message not found."
        response = self.client.get(self.url)
        self.assertEquals(404, response.status_code)

    
    def test_delete_message(self):
        print "Test delete message."
        resp = self.client.delete(self.url)
        self.assertEquals(resp.status_code, 404)


class MoveTestCase(ResourcesAPITestCase):
    
    url = '/game/api/games/<game_id>/move/'
    
    @classmethod
    def setUpClass(cls):
        print 'Testing MoveTestCase'

    def setUp(self):
        super(MoveTestCase,self).setUp()

    def test_url(self):
        print "Test url."
        with resources.app.test_request_context(self.url):
            rule = flask.request.url_rule
            view_point = resources.app.view_functions[rule.endpoint].view_class
            self.assertEquals(view_point, resources.Move)

class HeadersTestCase(ResourcesAPITestCase):
    
    url1 = '/game/api/players/'
    url2 = '/game/api/player/<player_id>/'
    url3 = '/game/api/players/<player_id>/player_profile/'
    url4 = '/game/api/forum/messages/'
    url5 = '/game/api/forum/message/<message_id>'
    url6 = '/game/api/games/'
    url7 = '/game/api/games/<game_id>/'
    url8 = '/game/api/games/leaderboard/'
    url9 = '/game/api/games/<game_id>/move/'
    url10 = '/game/api/forum/<thread_id>/thread/'
    headers = {'Content-Type': 'application/json'}

    
    @classmethod
    def setUpClass(cls):
        print 'Testing HeadersTestCase'

    def setUp(self):
        super(HeadersTestCase,self).setUp()

    def test_headers(self):
        pass

if __name__ == '__main__':
    print 'Start testing:'
    unittest.main()
