const { constructDadaSaying } = require('./proziceri.logic');

// Helpers – build a proverb array from its three parts.
const saying = (part1, sep, part2) => [part1, sep, part2];

describe('constructDadaSaying', () => {
    describe('dada output', () => {
        test('combines part1+separator of first proverb with part2 of second proverb', () => {
            const first  = saying('Omul sfințește locul',  ',', 'nu locul omul');
            const second = saying('Graba strică treaba',   ',', 'dar răbdarea o drege');

            const { dada } = constructDadaSaying(first, second);

            expect(dada).toBe('Omul sfințește locul, dar răbdarea o drege');
        });

        test('does NOT add a space before a comma separator', () => {
            const first  = saying('Cine se scoală de dimineață', ',', 'departe ajunge');
            const second = saying('Capul plecat',               ',', 'sabia nu-l taie');

            const { dada } = constructDadaSaying(first, second);

            // "Cine se scoală de dimineață," — no extra space before the comma
            expect(dada).toMatch(/locul de dimineață, sabia nu-l taie|Cine se scoală de dimineață, sabia nu-l taie/);
            expect(dada).not.toMatch(/ ,/);
        });

        test('adds a space before a word separator', () => {
            const first  = saying('Vorba lungă',  'este', 'sărăcia omului');
            const second = saying('Ochii sunt',   'este', 'oglinda sufletului');

            const { dada } = constructDadaSaying(first, second);

            // space before and after the word separator
            expect(dada).toBe('Vorba lungă este oglinda sufletului');
        });

        test('uses a space when the separator field is empty', () => {
            const first  = saying('Un om',               '', 'de treabă');
            const second = saying('Prietenul la nevoie', '', 'se cunoaște');

            const { dada } = constructDadaSaying(first, second);

            // empty separator defaults to ' '; padding is also ' ' → three spaces total
            expect(dada).toBe('Un om   se cunoaște');
        });
    });

    describe('original sayings preserved', () => {
        test('first field reconstructs the first original proverb', () => {
            const first  = saying('Omul sfințește locul', ',', 'nu locul omul');
            const second = saying('Graba strică treaba',  ',', 'dar răbdarea o drege');

            const { first: firstOut } = constructDadaSaying(first, second);

            expect(firstOut).toBe('Omul sfințește locul, nu locul omul');
        });

        test('second field reconstructs the second original proverb', () => {
            const first  = saying('Omul sfințește locul', ',', 'nu locul omul');
            const second = saying('Graba strică treaba',  ',', 'dar răbdarea o drege');

            const { second: secondOut } = constructDadaSaying(first, second);

            expect(secondOut).toBe('Graba strică treaba, dar răbdarea o drege');
        });

        test('second field uses its own separator, not the first proverb\'s', () => {
            const first  = saying('Vorba lungă',        ',',   'sărăcia omului');
            const second = saying('Lupu-și schimbă părul', 'dar', 'năravul ba');

            const { first: firstOut, second: secondOut } = constructDadaSaying(first, second);

            expect(firstOut).toBe('Vorba lungă, sărăcia omului');
            expect(secondOut).toBe('Lupu-și schimbă părul dar năravul ba');
        });
    });

    describe('return shape', () => {
        test('returns an object with dada, first, and second string fields', () => {
            const first  = saying('A', ',', 'B');
            const second = saying('C', ',', 'D');

            const result = constructDadaSaying(first, second);

            expect(result).toHaveProperty('dada');
            expect(result).toHaveProperty('first');
            expect(result).toHaveProperty('second');
            expect(typeof result.dada).toBe('string');
            expect(typeof result.first).toBe('string');
            expect(typeof result.second).toBe('string');
        });
    });
});
