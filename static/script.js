function utterThis(synth, p) {
    var initial = p.innerText;
    var utterance = new SpeechSynthesisUtterance();
    utterance.text = p.innerText;
    utterance.pitch = 1;
    utterance.rate = 1.25;
    utterance.onend = function() {
        p.innerHTML = initial;
    };
    utterance.onboundary = function(e) {
        if (e.charLength) {
            before = initial.slice(0, e.charIndex);
            inner = initial.slice(e.charIndex, e.charIndex + e.charLength);
            after = initial.slice(e.charIndex + e.charLength);
            p.innerHTML = before + '<u>' + inner + '</u>' + after;
        }
    }
    synth.speak(utterance);
}

function listen(event) {
    event.preventDefault();
    var button = event.currentTarget;
    var state = button.innerText;
    var synth = speechSynthesis;
    var article = document.getElementById('article');
    if (state == "listen") {
        synth.cancel();
        button.innerText = "pause";
        article.childNodes.forEach(p => {
            if (p.innerText && !p.children.length) {
                utterThis(synth, p);
            }
        })
    }
    if (state == "pause") {
        synth.pause();
        button.innerText = "resume";
    }
    if (state == "resume") {
        synth.resume();
        button.innerText = "pause";
    }
}
