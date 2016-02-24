import unittest
import flask.ext.testing
import flask, json, sqlite3, os

import src.gamer.resources as resources
import src.gamer.database

my_db_path = 'db/database.db'
my_db = src.gamer.database.GamerDatabase(my_db_path)

class DatabaseAPITestCase(unittest.TestCase):
   
    def setUp(self):
        if os.path.exists(my_db_path):
            os.remove(my_db_path)
        my_db.load_initial_values()
        self.client = resources.app.test_client()
        
    def tearDown(self):
        
       my_db.clean()
        

class MessageApiTestCase(DatabaseAPITestCase):

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_if_table_created(self):
        print "Test if message table is created."

        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT * FROM message'

        con = sqlite3.connect(my_db_path)

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)
            cur.execute(stmnt)

            #One message expected.
            row = cur.fetchone()

            message_title = row['title']
            self.assertEquals("peruskeke", message_title)

          
    pass

class PlayerApiTestCase(DatabaseAPITestCase):

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
    
    def test_if_table_created(self):
        print "Test if player table is created."

        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT * FROM player'

        con = sqlite3.connect(my_db_path)

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)
            cur.execute(stmnt)

            #One message expected.
            row = cur.fetchone()

            username = row['username']
            self.assertEquals("keke", username)

class GameApiTestCase(DatabaseAPITestCase):

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
    
    def test_if_table_created(self):
        print "Test if game table is created."

        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT * FROM game'

        con = sqlite3.connect(my_db_path)

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)
            cur.execute(stmnt)

            #One message expected.
            row = cur.fetchone()

            game_id = row['id']
            self.assertEquals(1, game_id)


pass

class MoveApiTestCase(DatabaseAPITestCase):

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
    
    def test_if_table_created(self):
        print "Test if move table is created."

        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT * FROM move'

        con = sqlite3.connect(my_db_path)

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)
            cur.execute(stmnt)

            #One message expected.
            row = cur.fetchone()

            move_id = row['id']
            self.assertEquals(1, move_id)


pass

class PlayerProfileApiTestCase(DatabaseAPITestCase):

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
    
    def test_if_table_created(self):
        print "Test if player_profile table is created."

        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT * FROM player_profile'

        con = sqlite3.connect(my_db_path)

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)
            cur.execute(stmnt)

            #One message expected.
            row = cur.fetchone()

            profile_id = row['id']
            self.assertEquals(1, profile_id)


pass

class ThreadApiTestCase(DatabaseAPITestCase):

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
    
    def test_if_table_created(self):
        print "Test if thread table is created."

        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT * FROM thread'

        con = sqlite3.connect(my_db_path)

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)
            cur.execute(stmnt)

            #One message expected.
            row = cur.fetchone()

            thread_id = row['id']
            self.assertEquals(1, thread_id)


pass

class TransactionlogApiTestCase(DatabaseAPITestCase):

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
    
    def test_if_table_created(self):
        print "Test if transaction_log table is created."

        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT * FROM transaction_log'

        con = sqlite3.connect(my_db_path)

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)
            cur.execute(stmnt)

            #One message expected.
            row = cur.fetchone()

            log_id = row['id']
            self.assertEquals(1, log_id)


pass

class PlayerGameApiTestCase(DatabaseAPITestCase):

    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__
    
    def test_if_table_created(self):
        print "Test if player_game table is created."

        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'SELECT * FROM player_game'

        con = sqlite3.connect(my_db_path)

        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            cur.execute(keys_on)
            cur.execute(stmnt)

            #One message expected.
            row = cur.fetchone()

            id = row['id']
            self.assertEquals(1, id)


pass
if __name__ == '__main__':
    print 'Start testing:'
    unittest.main()
