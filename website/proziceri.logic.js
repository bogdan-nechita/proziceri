// Pure logic for constructing dada sayings — no DOM or jQuery dependencies.
// Works as a global in browsers and as a CommonJS module in Node.js (for tests).

/**
 * Builds a dada saying by combining the first half of one proverb
 * with the second half of another.
 *
 * Each saying is an array: [part1, separator, part2]
 *
 * @param {string[]} firstSaying  - The saying that contributes part1 + separator
 * @param {string[]} secondSaying - The saying that contributes part2
 * @returns {{ dada: string, first: string, second: string }}
 */
function constructDadaSaying(firstSaying, secondSaying) {
    var separatorFirst = firstSaying[1] ? firstSaying[1] : ' ';
    var separatorSecond = secondSaying[1] ? secondSaying[1] : ' ';

    // Comma separators attach directly to the preceding word (no leading space).
    var paddingFirst = separatorFirst === ',' ? '' : ' ';
    var paddingSecond = separatorSecond === ',' ? '' : ' ';

    return {
        dada:   firstSaying[0]  + paddingFirst  + separatorFirst  + ' ' + secondSaying[2],
        first:  firstSaying[0]  + paddingFirst  + separatorFirst  + ' ' + firstSaying[2],
        second: secondSaying[0] + paddingSecond + separatorSecond + ' ' + secondSaying[2],
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { constructDadaSaying };
}
