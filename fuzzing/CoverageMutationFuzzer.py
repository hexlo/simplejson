from typing import Set

from ParseJsonRunner import ParseJsonRunner, JsonParserExecution
from MutationFuzzer import MutationFuzzer


class CoverageMutationFuzzer(MutationFuzzer):
    def __init__(self, seed=None, min_mutations=1, max_mutations=5):
        """Constructor.
        `seed` - a list of (input) strings to mutate.
        `min_mutations` - the minimum number of mutations to apply.
        `max_mutations` - the maximum number of mutations to apply.
        """
        super().__init__(seed=seed, min_mutations=min_mutations, max_mutations=max_mutations)
        self.coverages_seen: Set[frozenset] = set()
        self.population = []

    def run(self, runner: ParseJsonRunner) -> JsonParserExecution:
        """Run function(inp).
           If we reach new coverage, add inp to population and its coverage to coverages_seen.
        """
        result = super().run(runner)
        new_coverage = frozenset(result.cov.coverage())
        if new_coverage not in self.coverages_seen:
            self.population.append(self.inp)
            self.coverages_seen.add(new_coverage)

        return result
