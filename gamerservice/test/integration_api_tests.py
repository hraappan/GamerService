import unittest
import flask.ext.testing
import flask, json, sqlite3, os

import src.gamer.resources as resources
import src.gamer.database

my_db_path = 'db/database.db'
my_db = src.gamer.database.GamerDatabase(my_db_path)




class IntegrationAPITestCase(unittest.TestCase):
   
    def setUp(self):
        if os.path.exists(my_db_path):
            os.remove(my_db_path)
        resources.app.config['TESTING'] = True 
        resources.app.config['DATABASE'] = my_db
        my_db.load_initial_values()
        self.client = resources.app.test_client()
        
    def tearDown(self):
        my_db.clean()



class AddMessageTestCase(IntegrationAPITestCase):
    url = '/game/api/forum/messages/'
    data = {u"playerid":"1", u"title":"keke", u"body":"ulf" }

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
        

    def test_add_message(self):
        print "Test adding a message."
        resp = self.client.post(self.url, data = json.dumps(self.data), headers={"Content-Type":"application/json"})
        self.assertEquals(resp.status_code, 201)
        
    def test_add_message_in_wrong_format(self):
        print "Test adding message in wrong format."
        resp = self.client.post(self.url, self.data, headers={"Content-Type":"application/json"})
        self.assertEquals(resp.status_code, 400)
    pass


class GetPlayersTestCase(IntegrationAPITestCase):
    url = '/game/api/players/'

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_get_players(self):
        print "Test if players are returned."
        resp = self.client.get(self.url)
        resp2 = my_db.getPlayers()
    pass


class GetPlayerTestCase(IntegrationAPITestCase):
    url = '/game/api/player/1/'

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_get_player(self):
        print "Test if player is returned."

        resp = self.client.get(self.url)
        self.assertEquals(200, resp.status_code)

        
    pass

class PlayerProfileTestCase(IntegrationAPITestCase):
    url_profile = '/game/api/players/1/player_profile/'
    url_profile2 = '/game/api/players/?1/player_profile/'
    user1 = { 'nickname':'user1', 'basic_information':'basic_information' }
    url = '/game/api/players/<player_id>/player_profile/'
    
    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_player_profile_not_found(self):
        print "Test player_profile not found."
        response = self.client.get(self.url)
        self.assertEquals(404, response.status_code)

    def test_add_profile(self):
        print "Test if profile added and returned correctly."
        resp = self.client.put(self.url_profile, self.user1)
        player_profile_in_db = self.client.get(self.url_profile2)
        self.assertEquals(200, player_profile_in_db.status_code)

    pass
pass


if __name__ == '__main__':
    print 'Start testing:'
    unittest.main()
