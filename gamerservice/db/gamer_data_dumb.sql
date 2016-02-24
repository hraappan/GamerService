
INSERT INTO "player"(id, username, password, status) values(1, "keke", "keke", "online");
INSERT INTO "player"(id, username, password, status) values(2, "spede", "keke", "online");
INSERT INTO "message"(id, body, title, sender, threadId) values(5, "laalaalalalala", "peruskeke", 1, 1);
INSERT INTO "game"(id, state, winner, creator, turn, opponent) values (1, "ongoing", "", 1, 1, 2);
INSERT INTO "move"(id, creator, x, y, gameId) values(1, 1, 2,3,1);
INSERT INTO "player_profile"(id, playerId, profile, nickname) values(1,1,"Ultimate player", "kekejamppa");
INSERT INTO "player_profile"(id, playerId, profile, nickname) values(2,2,"Ultimate player2", "spedejamppa");
INSERT INTO "thread"(id, messageId) values(1, 1);
INSERT INTO "transaction_log"(id, playerId, request, response) values(1, 1, "update", "x,y,z,");
INSERT INTO "player_game"(id, playerId, gameId) values(1,1,1);
