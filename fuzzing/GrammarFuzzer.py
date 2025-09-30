from fuzzingbook.GrammarFuzzer import FasterGrammarFuzzer
from fuzzingbook.Grammars import Grammar

from BaseFuzzer import BaseFuzzer


class GrammarFuzzer(BaseFuzzer):
    """A grammar-based fuzzer for generating JSON strings"""
    JSON_GRAMMAR: Grammar = {
        "<start>": ["<json>"],
        "<json>": ["<object>", "<array>", "<value>"],
        "<object>": ["{<members>}", "{}"],
        "<members>": ["<pair>", "<pair>,<members>"],
        "<pair>": ["<string>:<value>"],
        "<array>": ["[<elements>]", "[]"],
        "<elements>": ["<value>", "<value>,<elements>"],
        "<value>": ["<string>", "<number>", "<object>", "<array>", "true", "false", "null"],
        "<string>": ['"<chars>"'],
        "<chars>": ["", "<char><chars>"],
        "<char>": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                   "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                   "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                   "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                   "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_", "-", "+", ".",
                   " ", "\\\\", "\\/", "\\\"", "\\b", "\\f", "\\n", "\\r", "\\t"],
        "<number>": ["<integer>", "<integer>.<digits>", "<integer>e<integer>", "<integer>E<integer>",
                     "<integer>.<digits>e<integer>", "<integer>.<digits>E<integer>"],
        "<integer>": ["<digit>", "<onenine><digits>", "-<digit>", "-<onenine><digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
        "<digit>": ["0", "<onenine>"],
        "<onenine>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    }

    def __init__(self, min_nonterminals=0, max_nonterminals=10, disp=False):
        """Constructor.
        `min_nonterminals` - the minimum number of nonterminals to expand
        `max_nonterminals` - the maximum number of nonterminals to expand
        `disp` - whether to display the production tree
        """
        self.impl = FasterGrammarFuzzer(
            grammar=self.JSON_GRAMMAR,
            min_nonterminals=min_nonterminals,
            max_nonterminals=max_nonterminals,
            disp=disp
        )

    def fuzz(self):
        """Generate a random JSON string based on the grammar"""
        return self.impl.fuzz()

    def get_seed_pool(self, n):
        """Generate a pool of valid JSON strings to use as seeds for mutation testing"""
        return [self.fuzz() for _ in range(n)]
