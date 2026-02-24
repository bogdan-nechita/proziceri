// All the sayings generated in the session.
var sayings_in_session = [];
// All the sayings, parsed from the CSV file.
var allParsedSayings;
// The saying currently on display.
var currentSaying;

document.addEventListener('DOMContentLoaded', function() {
    openCSVFile();

    var dadaSaying = document.getElementById('dadaSaying');
    var originalSayingsContainer = document.getElementById('originalSayingsContainer');

    originalSayingsContainer.style.top = (dadaSaying.offsetTop - 100) + 'px';

    dadaSaying.addEventListener('mouseenter', function() {
        originalSayingsContainer.style.display = '';
    });
    dadaSaying.addEventListener('mouseleave', function() {
        originalSayingsContainer.style.display = 'none';
    });

    document.getElementById('newSaying').addEventListener('click', function() {
        getDadaSaying();
    });

    document.getElementById('previousSaying').addEventListener('click', function() {
        if (sayings_in_session.length > 1) {
            var indexes = sayings_in_session
                .map(function(obj, index) { return obj.dada == currentSaying.dada ? index : null; })
                .filter(function(i) { return i !== null; });
            var indexOfCurrentSession = indexes[0];

            if (indexOfCurrentSession > 0) {
                var previousSaying = sayings_in_session[indexOfCurrentSession - 1];
                displaySaying(previousSaying.dada, previousSaying.first, previousSaying.second);
            }
        }
    });

    document.getElementById('nextSaying').addEventListener('click', function() {
        if (sayings_in_session.length > 1) {
            var indexes = sayings_in_session
                .map(function(obj, index) { return obj.dada == currentSaying.dada ? index : null; })
                .filter(function(i) { return i !== null; });
            var indexOfCurrentSession = indexes[0];

            if (indexOfCurrentSession < sayings_in_session.length - 1) {
                var nextSaying = sayings_in_session[indexOfCurrentSession + 1];
                displaySaying(nextSaying.dada, nextSaying.first, nextSaying.second);
            }
        }
    });

    document.getElementById('about').addEventListener('click', function() {
        if (this.innerText == "despre") {
            this.innerText = "înapoi";
            document.getElementById('sayingsContainer').style.display = 'none';
            document.getElementById('aboutContainer').style.display = '';
        } else {
            this.innerText = "despre";
            document.getElementById('sayingsContainer').style.display = '';
            document.getElementById('aboutContainer').style.display = 'none';
        }
    });

});

// Add the dada saying and the original ones.
function addSayingToSession(dada_saying, first_saying, second_saying) {
    sayings_in_session.push({ 'dada': dada_saying, 'first': first_saying, 'second': second_saying });
}
// Display the dada sayings with its corresponding original sayings.
function displaySaying(dada_saying, first_saying, second_saying) {
    currentSaying = { 'dada': dada_saying, 'first': first_saying, 'second': second_saying };

    document.getElementById('dadaSaying').innerHTML = dada_saying;
    document.getElementById('oSaying1').innerHTML = first_saying;
    document.getElementById('oSaying2').innerHTML = second_saying;
}

function getDadaSaying() {
    if (allParsedSayings) {
        // Generate two random ids between 0 and the number of sayings in the file.
        var numberOfSayings = allParsedSayings.length;

        var firstSayingIndex = Math.floor((Math.random() * numberOfSayings) + 1);
        var secondSayingIndex = Math.floor((Math.random() * numberOfSayings) + 1);

        // Get the two sayings.
        var firstSaying = allParsedSayings[firstSayingIndex];
        var secondSaying = allParsedSayings[secondSayingIndex];

        // Build the dada saying and its source originals via the shared pure function.
        var constructed = constructDadaSaying(firstSaying, secondSaying);
        var dadaSaying = constructed.dada;
        var firstSayingString = constructed.first;
        var secondSayingString = constructed.second;

        addSayingToSession(dadaSaying, firstSayingString, secondSayingString);
        displaySaying(dadaSaying, firstSayingString, secondSayingString);
    }
}

function openCSVFile() {
    fetch('data/Proziceri.csv')
        .then(function(response) { return response.text(); })
        .then(function(data) { processData(data); });
}

function processData(data) {
    Papa.parse(data, {
        complete: function(results) {
            allParsedSayings = results.data
            getDadaSaying()
        }
    });
}
