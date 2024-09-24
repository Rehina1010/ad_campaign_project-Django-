 document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('image-form');
        const loadingContainer = document.getElementById('loading-container');
        const loadingMessage = document.getElementById('loading-message').querySelector('p');
        const loadingEmojis = document.getElementById('loading-emojis');

        form.onsubmit = function(event) {
            event.preventDefault();
            loadingContainer.style.display = 'block';

            let messages = [
                "We're drawing your picture... 🎨",
                "Creating magic... ✨",
                "Drawing your vision... 🖼️",
                "Art in progress... 🎨",
                "Making your image awesome... 🌟"
            ];

            let emojis = ["🎨", "✨", "🖼️", "🌟", "🚀"];
            let messageIndex = 0;
            let emojiIndex = 0;

            const intervalId = setInterval(() => {
                loadingMessage.textContent = messages[messageIndex];
                loadingEmojis.textContent = emojis[emojiIndex];

                messageIndex = (messageIndex + 1) % messages.length;
                emojiIndex = (emojiIndex + 1) % emojis.length;
            }, 5000);

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.text())
            .then(html => {
                document.open();
                document.write(html);
                document.close();
                clearInterval(intervalId);
            })
            .catch(error => {
                console.error('Error:', error);
                clearInterval(intervalId);
            });
        };
    });