document.addEventListener("DOMContentLoaded", function() {
    // Open sign-up form when "Sign up" link is clicked
    document.querySelector("#signup a").addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default link action
        document.getElementById("signUpCard").style.display = "block"; 
        document.getElementById("effect").style.display = "block"; 
    });
    

    // Close sign-up form when "X" button is clicked
    document.getElementById("close").addEventListener("click", function() {
        document.getElementById("signUpCard").style.display = "none"; 
        document.getElementById("effect").style.display = "none"; 
    }); 
    
});  
document.addEventListener("DOMContentLoaded", function() {
    // Open verification form when "forget" link is clicked
    document.querySelector("#link1").addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default link action
        document.getElementById("verification").style.display = "block"; 
        document.getElementById("effect").style.display = "block"; 
    }); 
 
    // Close verification form when "X" button inside the div is clicked
    document.getElementById("close2").addEventListener("click", function() {
        document.getElementById("verification").style.display = "none"; // Hide the verification form
        document.getElementById("effect").style.display = "none"; // Hide the overlay effect
    });
});  
