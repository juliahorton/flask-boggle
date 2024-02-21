const $form = $("#guess-form");
const $input = $("#guess");
const $submitBtn = $("#guess-form button")
const $message = $(".msg");
const $score = $("#score");
const $countdown = $("#countdown");
const $startBtn = $("#start");
const $gamesPlayed = $("#games-played");
const $highScore = $("#high-score");
let timerIntervId;
// let gameOver = null;

// prevents user from submitting a guess before the timer has been started
$form.on("submit", function(e){e.preventDefault()});

$startBtn.on("click", startGame);

function startGame(){
    $startBtn.off();
    $startBtn.text("New Game");
    $startBtn.on("click", newGameHandler);
    $form.on("submit", getGuess);
    // after 60 seconds, stop allowing user to submit new guesses
    setTimeout(gameOver, 10000);
    // update UI to show 60-second countdown once timer has started
    timerIntervId = setInterval(showCountdown, 1000);
}

function newGameHandler(){
    location.reload();
}

async function getGuess(e){
    e.preventDefault();
    const guess = $input.val();
    $form.trigger("reset");

    // if (!guess) return;

    const response = await axios.get("/check-guess", { params: {guess} });
    
    if (response.data.result === "not-word"){
        showMessage(`"${guess}" is not a valid English word`, "err")
    } else if (response.data.result === "not-on-board"){
        showMessage(`"${guess}" is not a valid word on this board`, "err")
    } else {
        showMessage(`Added: ${guess}`, "ok");
        updateScore(guess.length);
    }
}

function showMessage(msg, cls){
    $message.text(msg).removeClass().addClass(`msg ${cls}`)
}

function updateScore(lengthOfGuess){
    let currScore = Number($score.text());
    let newScore = currScore + lengthOfGuess;
    $score.text(newScore)
}

function showCountdown(){
    let currNum = Number($countdown.text());
    $countdown.text(`${currNum - 1}`);
}

function gameOver(){
    $form.off();
    $form.on("submit", function(e){e.preventDefault()});
    clearInterval(timerIntervId);
    $("#timer-container span").empty().append("<p>GAME OVER</p>");
    // let gameOver = true;
    let finalScore = Number($score.text());
    updateStats(finalScore);
}

async function updateStats(score){
    const response = await axios.get("/update-stats", { params: {score} });
    $highScore.text(response.data.high_score);
    $gamesPlayed.text(response.data.games_played);
}