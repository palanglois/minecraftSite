function reloadPlayers(){
  $( "#onlinePlayers" ).load( "onlineplayers",
    function(data)
    {
      var obj = JSON.parse(data);
      $("#onlinePlayers").html(obj.section);
      $(".nbPlayers").each(function(){$(this).text(obj.nb)});
    }
);
}

reloadPlayers();
setInterval(function(){
    reloadPlayers() // this will run after every 1.5 second
}, 1500);

