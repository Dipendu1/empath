$(document).ready(function () {
    $('.text').textillate({
        loop: true,
        sysn: true,
        in: {
            effect: "bounceIn",

        },
        out: {
            effect: "bounceOut",
        }
    });
    //siri cogf
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
    });

    function displaySiriMessage() {
        $('.siri-message').text(messages[messageIndex]);
        $('.siri-message').textillate({
            loop: true,
            sync: true,
            in: {
                effect: "fadeIn",
                sync: true,
                callback: function () {
                    setTimeout(() => {
                        $('.siri-message').textillate('out');
                    }, 2000); // Display each point for 2 seconds
                }
            },
            out: {
                effect: "fadeOut",
                sync: true,
                callback: function () {
                    messageIndex = (messageIndex + 1) % messages.length; // Loop through points
                    $('.siri-message').text(messages[messageIndex]); // Update message text
                    $('.siri-message').textillate('in');
                }
            }
        });
    }
    //mic button click event
    $('#MicBtn').click(function () {
        eel.playAssistantSound()
        $('#Oval').attr("hidden", true);
        $('#SiriWave').attr("hidden", false);
        eel.allCommands()()
    });

    function doc_keyUp(e) {
        // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // to play assisatnt 
    function PlayAssistant(message) {

        if (message != "") {

            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);

        }

    }

    // toogle fucntion to hide and display mic and send button 
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // key up event handler on text box
    $("#chatbox").keyup(function () {

        let message = $("#chatbox").val();
        ShowHideButton(message)

    });

    // send button event handler
    $("#SendBtn").click(function () {

        let message = $("#chatbox").val()
        PlayAssistant(message)

    });


    // enter press event handler on chat box
    $("#chatbox").keypress(function (e) {
        const key = e.which; // Declare key here
        if (key == 13) {
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });
    
    
    $(document).ready(function () {
        const chatbox = document.getElementById("chatbox");
        const sendButton = document.getElementById("SendBtn");
        const chatCanvasBody = document.getElementById("chat-canvas-body");

        // Function to send message to Python backend
        async function sendMessage() {
            const userMessage = chatbox.value.trim();
            if (!userMessage) return;

            // Append user's message to chat display
            addChatMessage("User", userMessage);

            // Clear the input field
            chatbox.value = "";

            try {
                // Send the message to Python backend and get the response
                const botResponse = await eel.generate_cohere_response(userMessage)();
                console.log("Bot Response:", botResponse);  // Log the response
                if (botResponse) {
                    addChatMessage("Bot", botResponse);
                } else {
                    addChatMessage("Bot", "No response from the bot.");
                }
            } catch (error) {
                console.error("Error in fetching bot response:", error);
                addChatMessage("Bot", "Error retrieving response. Please try again.");
            }
        }

        // Function to add messages to chat canvas body
        function addChatMessage(sender, message) {
            const messageDiv = document.createElement("div");
            messageDiv.className = sender === "User" ? "user-message" : "bot-message";
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatCanvasBody.appendChild(messageDiv);
            chatCanvasBody.scrollTop = chatCanvasBody.scrollHeight; // Auto-scroll to the bottom
        }

        // Send message when clicking the Send button
        sendButton.addEventListener("click", sendMessage);

        //

        async function sendMessage() {
            const userMessage = chatbox.value.trim();
            if (!userMessage) return;
        
            addChatMessage("User", userMessage);
            chatbox.value = "";
        
            try {
                const botResponse = await eel.chat(userMessage)(); // Make sure this matches your Python function
                console.log("Bot Response:", botResponse);
                if (botResponse) {
                    addChatMessage("Bot", botResponse);
                } else {
                    addChatMessage("Bot", "No response from the bot.");
                }
            } catch (error) {
                console.error("Error in fetching bot response:", error);
                addChatMessage("Bot", "Error retrieving response. Please try again.");
            }
        }
        


    });
});
