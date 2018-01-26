var sock = new SockJS('http://localhost:9999/echo');
sock.onopen = function() {
    console.log('open');
    sock.send(JSON.stringify({"action": "open_connect"}));
};

sock.onmessage = function(e) {
    console.log('message', e.data);
    sock.close();
};

sock.onclose = function() {
    console.log('close');
};