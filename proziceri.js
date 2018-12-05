// All the sayings generated in the session.
var sayings_in_session = [];
// All the sayings, parsed from the CSV file.
var allParsedSayings;
// The saying currently on display.
var currentSaying;

$(document).ready(function() {
    openCSVFile();

    $("#originalSayingsContainer").css("top", function() {
        return $("#dadaSaying").offset().top - 100;
    });

    $("#dadaSaying").hover(
        function() {
            $("#originalSayingsContainer").show();
        },
        function() {
            $("#originalSayingsContainer").hide();
        });

    $("#newSaying").click(function() {
        getDadaSaying();
    });

    $("#previousSaying").click(function() {
        if (sayings_in_session.length > 1) {
            var indexes = $.map(sayings_in_session, function(obj, index) {
                if (obj.dada == currentSaying.dada) {
                    return index;
                }
            })
            var indexOfCurrentSession = indexes[0]

            if (indexOfCurrentSession > 0) {
                var previousSaying = sayings_in_session[indexOfCurrentSession - 1];
                displaySaying(previousSaying.dada, previousSaying.first, previousSaying.second);
            }
        }
    });

    $("#nextSaying").click(function() {
        if (sayings_in_session.length > 1) {
            var indexes = $.map(sayings_in_session, function(obj, index) {
                if (obj.dada == currentSaying.dada) {
                    return index;
                }
            })
            var indexOfCurrentSession = indexes[0]

            if (indexOfCurrentSession < sayings_in_session.length - 1) {
                var nextSaying = sayings_in_session[indexOfCurrentSession + 1];
                displaySaying(nextSaying.dada, nextSaying.first, nextSaying.second);
            }
        }
    });

    $("#about").click(function() {
        if (this.innerText == "despre") {
            this.innerText = "înapoi";
            $("#sayingsContainer").hide();
            $("#aboutContainer").show();
        } else {
            this.innerText = "despre";
            $("#sayingsContainer").show();
            $("#aboutContainer").hide();
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

    $("#dadaSaying").html(dada_saying);
    $("#oSaying1").html(first_saying);
    $("#oSaying2").html(second_saying);
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
        var separatorFirstSaying = firstSaying[1] ? firstSaying[1] : ' ';
        var separatorSecondSaying = secondSaying[1] ? secondSaying[1] : ' ';

        // Return the part1 and separator from the first saying and the part2 from the second saying
        // if the separator is a comma, don't add an extra space before it
        var part1Padding = separatorFirstSaying == ',' ? '' : ' ';
        var part2Padding = separatorSecondSaying == ',' ? '' : ' ';

        // Create the dada saying.
        var dadaSaying = firstSaying[0] + part1Padding + separatorFirstSaying + ' ' + secondSaying[2]

        // Add the saying to the session and display it.
        var firstSayingString = firstSaying[0] + part1Padding + separatorFirstSaying + ' ' + firstSaying[2];
        var secondSayingString = secondSaying[0] + part2Padding + separatorSecondSaying + ' ' + secondSaying[2];

        addSayingToSession(dadaSaying, firstSayingString, secondSayingString);
        displaySaying(dadaSaying, firstSayingString, secondSayingString);
    }
}

function openCSVFile() {
    $.ajax({
        type: "GET",
        url: "Proziceri.csv",
        dataType: "text",
        success: function(data) { processData(data); }
    });
}

function processData(data) {
    Papa.parse(data, {
        complete: function(results) {
            allParsedSayings = results.data
            getDadaSaying()
        }
    });
}