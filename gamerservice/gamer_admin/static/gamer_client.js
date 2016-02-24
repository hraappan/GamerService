//Debugging.
var DEBUG = true,
//Url for the application.
APP_URL = "http://localhost:5000/game/api",
//Only JSON for now.
RESPONSE_FORMAT = "json",
//Request format
CONTENT_TYPE = "application/"+ RESPONSE_FORMAT;



//Gets all the players from the database that are online.
function getPlayers() {
	var uarr = [APP_URL, "players/"]
	var apiurl = uarr.join("/")

		return $.ajax({
			url: apiurl,
			dataType: RESPONSE_FORMAT
			
		}).always(function(){
			$("#player_list").empty();
			$("#game").hide();
			$("#bottom_part").hide();
			$("#messages_list_divider").hide();
			$("#player_information").hide();
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);
			}
			
			if(RESPONSE_FORMAT == "json") {
				var players = data['players']
				
				for(var i=0; i<players.length; i++) {
						var player = players[i]
						console.log("" + players[i].status);
						if(player.status == "online") {
							appendPlayerToList(player.player, player.link.href);
					 }
				}
			}
	
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			alert ("Could not fetch the player data from the server.");
			
		});
 
}

//Gets all the games from the database that are ongoing.
function getGames() {
	var uarr = [APP_URL, "games/"]
	var apiurl = uarr.join("/")

		return $.ajax({
			url: apiurl,
			dataType: RESPONSE_FORMAT
			
		}).always(function(){
			$("#game_list").empty();
			$("#game").hide();
			$("#messages_list_divider").hide();
			$("#player_information").hide();
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);
			}
			
			if(RESPONSE_FORMAT == "json") {
				var games = data['games']
				
				for(var i=0; i<games.length; i++) {
						var game = games[i]
						if(game.state == "ongoing") {
							appendGameToList(game.id, game.link.href);
					 }
				}
			}
	
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			alert ("Could not fetch the player data from the server.");
			
		});
 
}
//Add a game to the list.
function appendGameToList(game, url) {

	var $game = $('<li>').html('<a href="'+url+'"> Game '+game+'</a>');
	console.log("Adding Game"+game+" to list...");
	$("#game_list").append($game);
	return $game;

}

//Add a player to the list.
function appendPlayerToList(player, url) {

	var $player = $('<li>').html('<a href="'+url+'">'+player+'</a>');
	console.log("Adding Player "+player+ " to list...");
	$("#player_list").append($player);
	return $player;

}

//Add a player to the list.
function appendMessageToList(message, url) {
	
	var $message = $('<li>').html('<a href="'+url+'">'+message+'</a>' +
	"<div class='commands'><input id='deleteMessage' type='button' value='Delete'/></div>");
	console.log("Adding message "+message+ " to list...");
	$("#message_list").append($message);
	return $message;

}

//Search user with an username.
function handleSearchUser(event) {

	if(DEBUG) {
		console.log("Triggered handleSearchUser.")
	}
}

function selectPlayer(apiurl) {
		//Get the selected player
	

		return $.ajax({
			url: apiurl,
			dataType: RESPONSE_FORMAT
			
		}).always(function(){
			$("#game").hide();
			$("#messages_list_divider").hide();
			$("#player_information").show();
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);
			}
			
			if(RESPONSE_FORMAT == "json") {
			
				var player = data['player'];
				var username = player.username;
				var nickname = player.nickname;
				document.getElementById('username').value = username;
				document.getElementById('profile_nickname').value = nickname;
				getPlayerProfile(player.player_profile.href);
				
				
			}
	
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			var error_message = $.parseJSON(jqXHR.responseText).message
			alert ("Could not fetch the player data from the server.\n"+error_message);
			
		});

}

function getPlayerProfile(apiurl) {

return $.ajax({
			url: apiurl,
			dataType: RESPONSE_FORMAT
			
		}).always(function(){
		
			$("#basic_information").empty();
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);
			}
			
			if(RESPONSE_FORMAT == "json") {
				//Player profile for display.
				var profile = data['player_profile'];
				var information = profile.basic_information;
				//Player url for later use.
				var links = data['links'];
				var url = links[0].href;
				document.getElementById('playerid').value = url;
				document.getElementById('basic_information').value = information;
			}
	
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			var error_message = $.parseJSON(jqXHR.responseText).message
			alert ("Could not fetch the player data from the server.\n"+error_message);
			
		});
	

}

function handleSelectPlayer(event) {
	if(DEBUG) {
		console.log("Triggered handleSelectPlayer.");
	}

	var apiurl = $(this).children("a").attr("href");
	selectPlayer(apiurl);
	return false;
}
function handleSelectGame(event) {
	
	console.log("Triggered handleSelectGame.");
		
		var apiurl = $(this).children("a").attr("href");
		selectGame(apiurl);
		return false;
		
}
function selectGame(apiurl) {
	if(DEBUG) {
		
	}
		return $.ajax({
			url: apiurl,
			dataType: RESPONSE_FORMAT
			
		}).always(function(){
			
		$("#player_information").hide();
		$("#messages_list_divider").hide();
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);
			}
			
			if(RESPONSE_FORMAT == "json") {
				var game = data['game']
				
				document.getElementById("#player1").setAttribute('href', "/game/api/player/"+ game.creator);
				document.getElementById("#player2").setAttribute('href', "/game/api/player/"+ game.opponent);
				document.getElementById("#player_turn").setAttribute('href', "/game/api/player/"+ game.turn);
				
	
			}
	$("#game").show();
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			var error_message = $.parseJSON(jqXHR.responseText).message
			alert ("Could not fetch the game from the server.\n"+error_message);
			
			
		});
	

}

function handleGetMessages(event) {
if(DEBUG) {
		console.log("Triggered handleGetMessages.");
	
	}
	
	getMessages();
}

function getMessages() {

		
	var uarr = [APP_URL, "forum/messages/"]
	var apiurl = uarr.join("/")

		return $.ajax({
			url: apiurl,
			dataType: RESPONSE_FORMAT
			
		}).always(function(){
			$("#game").hide();
			$("#player_information").hide();
			$("#message_list").empty();
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);
			}
			
			if(RESPONSE_FORMAT == "json") {
				var messages = data['messages']
				
				for(var i=0; i<messages.length; i++) {
						var message = messages[i]
						
							appendMessageToList(message.title, message.link.href);
				}
				
				
			}
			$("#messages_list_divider").show();
	
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			var error_message = $.parseJSON(jqXHR.responseText).message
			alert ("Could not fetch the messages from the server.\n"+error_message);
			$("#messages_list_divider").show();
			
		});
	

}

function postMessage(message) {
	
	if(DEBUG) {
		console.log("Posting message: " + message.body + "with title: " + message.title);
	}
	
	var uarr = [APP_URL, "forum/messages/"]
	var apiurl = uarr.join("/")

		return $.ajax({
			url: apiurl,
			dataType: RESPONSE_FORMAT,
			type: "POST",
			data:message,
			processData:false,
			contentType: CONTENT_TYPE
			
		}).always(function(){
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);
			}
			
			getMessages();
			document.getElementById('#title').value = "";
			document.getElementById('#post').value = "";
	
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			var error_message = $.parseJSON(jqXHR.responseText).message
			alert ("Could not post the message\n"+error_message);
			
		});
	

}


function handlePostMessage(event) {

if(DEBUG) {
	console.log("Triggered handlePostMessage");
	}
	
	//Get the values from the document.
	var message_title = document.getElementById("#title").value;
	var message_body = document.getElementById("#post").value;
	//In this implementation the sender is hardcoded playerid 1.
	var playerid = 1;
	
	var message = {}
	message.title = message_title;
	message.body = message_body;
	message.playerid = playerid;
	postMessage(JSON.stringify(message));
}

function deleteMessage(messageurl) {


	return $.ajax({
			url: messageurl,
			dataType: RESPONSE_FORMAT,
			type: "DELETE",
			processData:false,
			contentType: CONTENT_TYPE
			
		}).always(function(){
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);
					getMessages();
			}
	
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			var error_message = $.parseJSON(jqXHR.responseText).message
			alert ("Could not delete the message\n"+error_message);
			
		});
		
	

}

function handleDeleteMessage(event) {
	if(DEBUG) {
	console.log("Triggered handleDeleteMessage");
	}
	
	//The messagelink.
	messageurl = $(this).find("a").attr("href");
	console.log("Delete message: " + messageurl);
	
	deleteMessage(messageurl);
}

function handleEditUser(event) {
//Edit the user info.
	if(DEBUG) {
	console.log("Triggered handleEditUser");
	}
	
	var apiurl = document.getElementById('playerid').value;
	var profile = {}
	profile.nickname = document.getElementById('profile_nickname').value;
	profile.basic_profile = document.getElementById('basic_information').value;
	
	editUser(apiurl, JSON.stringify(profile));
	
}

function editUser(apiurl, profile) {

	var uurl = [apiurl, "player_profile/"]
	var apiurl = uurl.join("");

return $.ajax({
			url: apiurl,
			dataType: RESPONSE_FORMAT,
			type: "PUT",
			data: profile,
			processData:false,
			contentType: CONTENT_TYPE
			
		}).always(function(){
			
	
		}).done(function(data, textStatus, jqXHR) {
		
			if(DEBUG) {
				console.log("Received response: data: ", data, "; Status: ", textStatus);

			}
			
	
		}).fail(function(jqXHR, textStatus, errorThrown) {
		
			if(DEBUG) {
				console.log("Received error: ", textStatus, ";error:", errorThrown);
			}
	
			var error_message = $.parseJSON(jqXHR.responseText).message
			alert ("Could not edit the user.\n"+error_message);
			
		});
}

function handleSendChatMessage(event) {
	if(DEBUG) {
	console.log("Triggered handleSendChatMessage");
	}
}

//Execute when the program is loaded.
$(function(){
$("#search_button").on("click", handleSearchUser);
$("#messages_link").click(handleGetMessages);
$("#post_button").click(handlePostMessage);
$("#save_button").click(handleEditUser);
$("#send_button").click(handleSendChatMessage);



$("#player_list").delegate("li", "click", "#player_list li", handleSelectPlayer);
$("#game_list").delegate("li", "click", "#game_list li", handleSelectGame);
$("#message_list").delegate("li",  "click", "deleteMessage",  handleDeleteMessage);
//Get the online players and the ongoing games.
 getPlayers();
 getGames();
 

})