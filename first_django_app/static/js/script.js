

async function sendMessage() {
    if (message.value.length > 0) {
        console.log(message.value.length);
        renderClientMessage(message.value);
        let url = new URL(window.location.href);
        let userId = url.searchParams.get("user_id");
        userId = parseInt(userId, 10);
        let form = new FormData();
        form.append('text_message', message.value);
        form.append('chat_id', chat_id.value);
        form.append('csrfmiddlewaretoken', token.value)
        try {
            let response = await fetch(`/chat_view/?user_id=${userId}`, {
                method: 'POST',
                body: form
            })
            let json_response = await response.json();
            document.getElementById('client_messsage').remove()
            renderBackendMessage(json_response)
        } catch (error) {
            console.log('Error sending message');
        }
        message.value = '';
        scrollDown();
    }
}


function scrollDown() {
    let scrollingDiv = document.getElementById("message_main");
    scrollingDiv.scrollTop = scrollingDiv.scrollHeight;
    scrollingDiv.scrollTop = scrollingDiv.scrollHeight;

}


function renderClientMessage(message) {
    let div = document.getElementById('message_main')
    div.innerHTML += `<span id="client_messsage">${message}</span>`;
}


function renderBackendMessage(message) {
    let div = document.getElementById('message_main')
    div.innerHTML += `  <div class="author_message" id="backend_messsage">
                            <span class="date"> ${message.created_at}</span>
                            ${message.text}  
                        </div>`;
}


function formatData(time) {
    const months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];
    const date = new Date(time);
    const month = months[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();
    const hour = date.getHours();
    const minute = date.getMinutes();
    const period = (hour >= 12) ? "p.m." : "a.m.";
    const formattedMinute = (minute < 10) ? `0${minute}` : minute;
    const formattedHour = (hour % 12 === 0) ? 12 : hour % 12;
    const formattedDate = `${month} ${day}, ${year}, ${formattedHour}:${String(formattedMinute).padStart(2, '0')} ${period}`;
    return formattedDate;
}