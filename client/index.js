function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}


setTimeout(function(){
    phrases = ["You're awesome and an amazing person!"] //List of phrases to send. 
    
    try{
        //Set the text box to a random phrase.
        document.getElementById("question").value = phrases[0, getRandomInt(0, phrases.length -1)]; 
        
        setTimeout(function(){
            document.getElementById("ask_button").click(); //Click submit
        }, 100)
        
    } catch(err) {
        console.info("Timed out");
        
        //We've run out of submits, refresh the page every five minutes and try again.
        setTimeout(function(){
            window.location.reload();
        }, 300000)
    }
    
}, 200)