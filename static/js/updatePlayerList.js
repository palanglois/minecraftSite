function reloadPlayers(){
  $( "#onlinePlayers" ).load( "onlineplayers" );
}

reloadPlayers();
setInterval(function(){
    reloadPlayers() // this will run after every 1.5 second
}, 1500);

