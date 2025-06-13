document.addEventListener("DOMContentLoaded", function () {
    const socket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + chatConfig.otherUserId + '/'
    );

    const chatBox = document.getElementById('chat-box');
    const chatForm = document.getElementById('chat-form');
    const messageInput = chatForm.querySelector('textarea');
    const typingStatus = document.getElementById('typing-status');

    chatBox.scrollTop = chatBox.scrollHeight;

    socket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.typing) {
            typingStatus.innerText = `${data.sender} is typing...`;
            setTimeout(() => {
                typingStatus.innerText = '';
            }, 1500);
            return;
        }

        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message');
        msgDiv.classList.add(data.sender === chatConfig.currentUsername ? 'sent' : 'received');

        msgDiv.innerHTML = `
            <p class="meta">
                <strong>${data.sender}</strong>
                <span>${data.timestamp}</span>
            </p>
            <p class="content">${data.message}</p>
        `;

        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    chatForm.onsubmit = function (e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message.length === 0) return;

        socket.send(JSON.stringify({
            message: message,
            sender: chatConfig.currentUsername,
            timestamp: new Date().toLocaleString()
        }));

        messageInput.value = '';
    };

    messageInput.addEventListener('input', () => {
        socket.send(JSON.stringify({
            typing: true,
            sender: chatConfig.currentUsername
        }));
    });
});
