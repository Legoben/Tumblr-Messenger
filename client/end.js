setTimeout(function(){
    
    $.ajax({"url":"http://localhost:9009/nextblog", success: function(d){
        //Get (and crawl) the next blog from the server.
        window.location = d //Go to the next blog.
    }, error:function(){
        console.error("error"); window.location.reload() //On error, refresh
    }})
}, 500)