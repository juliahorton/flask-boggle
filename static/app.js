const $form = $("#guess-form");
const $input = $("#guess");
const $message = $(".msg");
const $score = $("#score");

$form.on("submit", getGuess);

async function getGuess(e){
    e.preventDefault();
    const guess = $input.val();
    $form.trigger("reset");

    if (!guess) return;

    const response = await axios.get("/check-guess", { params: {guess} });
    
    if (response.data.result === "not-word"){
        showMessage(`"${guess}" is not a valid English word`, "err")
    } else if (response.data.result === "not-on-board"){
        showMessage(`"${guess}" is not a valid word on this board`, "err")
    } else {
        showMessage(`Added: ${guess}`, "ok");
        updateScore(guess.length);
    };
    // return false
}

function showMessage(msg, cls){
    $message.text(msg).removeClass().addClass(`msg ${cls}`)
}

function updateScore(lengthOfGuess){
    let currScore = Number($score.text());
    let newScore = currScore + lengthOfGuess;
    $score.text(newScore)
}