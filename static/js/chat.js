document.getElementById("send-btn").addEventListener("click", function() {
    var messageInput = document.getElementById("message-input");
    var message = messageInput.value;
  
    if (message.trim() !== "") {
      var chatContainer = document.getElementById("chat-container");
      var messageElement = document.createElement("div");
      messageElement.classList.add("message", "my-message");
      messageElement.innerHTML = '<i class="fas fa-user-circle icon"></i>' + message;
      chatContainer.appendChild(messageElement);
  
      var response = getResponse(message);
      if (response !== "") {
        simulateTyping(chatContainer);
  
        setTimeout(function() {
          var typingElement = document.querySelector(".typing");
          if (typingElement) {
            chatContainer.removeChild(typingElement);
          }
  
          var responseElement = document.createElement("div");
          responseElement.classList.add("message", "other-message");
          responseElement.innerHTML = '<i class="fas fa-user-circle icon"></i>' + response;
          chatContainer.appendChild(responseElement);
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }, 2000);
      }
  
      messageInput.value = "";
      messageInput.focus();
    }
  });
  
  function getResponse(message) {
    message = message.toLowerCase();
    var response = "";
  
    if (message.includes("hello")) {
      response = "Hi!";
    } else if (message.includes("how are you")) {
      response = "I am fine.";
    }
  
    return response;
  }
  
  function simulateTyping(chatContainer) {
    var typingElement = document.createElement("div");
    typingElement.classList.add("message", "other-message", "typing");
    typingElement.innerHTML = '<i class="fas fa-user-circle me-1 icon"></i><span class="typing-indicator">......</span>';
    chatContainer.appendChild(typingElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }