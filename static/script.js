function listen(event) {
    event.preventDefault();
    var element = event.currentTarget;
    var state = element.innerText;

    var synth = speechSynthesis;
    var article = document.getElementById('article');
    var utterance = new SpeechSynthesisUtterance();
    utterance.text = article.textContent;
    utterance.pitch = 1;
    utterance.rate = 1.25;
    utterance.onend = function() {
        element.innerText = "listen";
    };

    if (state == "listen") {
        synth.cancel();
        synth.speak(utterance);
        element.innerText = "pause";
    }

    if (state == "pause") {
        synth.pause();
        element.innerText = "resume";
    }

    if (state == "resume") {
        synth.resume();
        element.innerText = "pause";
    }
}
