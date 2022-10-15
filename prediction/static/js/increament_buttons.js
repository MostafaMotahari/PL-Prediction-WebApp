// Increase the number in the number box
function increaseNumber(numberBoxId) {
    var numberBox = document.getElementById(numberBoxId);
    var number = parseInt(numberBox.value);
    if (number < 9) {
        numberBox.value = number + 1;
    }
}

// Deacrease the number in the number box
function decreaseNumber(numberBoxId) {
    var numberBox = document.getElementById(numberBoxId);
    var number = parseInt(numberBox.value);
    if (number > 0) {
        numberBox.value = number - 1;
    }
}