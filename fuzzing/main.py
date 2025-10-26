import random
from typing import FrozenSet

from fuzzingbook.Coverage import Location

from ParseJsonRunner import ParseJsonRunner, JsonParserExecution
from MutationFuzzer import MutationFuzzer
from RandomFuzzer import RandomFuzzer
from CoverageMutationFuzzer import CoverageMutationFuzzer
from GrammarFuzzer import GrammarFuzzer
from analytics import analyze_all

NUM_TRIALS = 150

# TODO: Votre matricule
# RANDOM_SEED = 123456789
RANDOM_SEED = 1896074

MAX_DUPLICATES = 5

MUTATION_SEEDS = [
    '{"key": "value"}',
    '{"numbers": [1, 2, 3]}',
    '[true, false, null]',
    '42',
    '"test string"'
]


def part1():
    runner = ParseJsonRunner()
    fuzzer = RandomFuzzer()

    return {
        "Random Fuzzer": fuzzer.runs(runner, NUM_TRIALS)
    }


def part2():
    runner = ParseJsonRunner()
    random_fuzzer = RandomFuzzer()
    mutation_fuzzer = MutationFuzzer(seed=MUTATION_SEEDS)
    coverage_mutation_fuzzer = CoverageMutationFuzzer(seed=MUTATION_SEEDS)

    return {
        "Random Fuzzer": random_fuzzer.runs(runner, NUM_TRIALS),
        "Mutation Fuzzer": mutation_fuzzer.runs(runner, NUM_TRIALS),
        "Coverage Mutation Fuzzer": coverage_mutation_fuzzer.runs(runner, NUM_TRIALS)
    }


def part3():
    runner = ParseJsonRunner()
    random_fuzzer = RandomFuzzer()
    mutation_fuzzer = MutationFuzzer(seed=MUTATION_SEEDS)
    grammar_fuzzer = GrammarFuzzer(min_nonterminals=0, max_nonterminals=100)

    return {
        "Random Fuzzer": random_fuzzer.runs(runner, NUM_TRIALS),
        "Mutation Fuzzer": mutation_fuzzer.runs(runner, NUM_TRIALS),
        "Grammar Fuzzer": grammar_fuzzer.runs(runner, NUM_TRIALS)
    }


def part4():
    runner = ParseJsonRunner()
    random_fuzzer = RandomFuzzer()
    mutation_fuzzer = MutationFuzzer(seed=MUTATION_SEEDS)
    coverage_mutation_fuzzer = CoverageMutationFuzzer(seed=MUTATION_SEEDS)
    grammar_fuzzer = GrammarFuzzer(min_nonterminals=0, max_nonterminals=100)

    # TODO: Choose which fuzzers to use
    return {
        # "Random Fuzzer": random_fuzzer.runs(runner, NUM_TRIALS),
        # "Mutation Fuzzer": mutation_fuzzer.runs(runner, NUM_TRIALS),
        "Coverage Mutation Fuzzer": coverage_mutation_fuzzer.runs(runner, NUM_TRIALS),
        "Grammar Fuzzer": grammar_fuzzer.runs(runner, NUM_TRIALS)
    }


def produce_testcases(runs: list[JsonParserExecution]) -> dict[FrozenSet[Location], list[JsonParserExecution]]:
    """Produce a dictionary of test cases for each unique coverage obtained"""
    test_cases: dict[FrozenSet[Location], list[JsonParserExecution]] = {}

    for run in (runs):
        coverage = frozenset(run.cov.coverage())

        if test_cases.get(coverage, None):
            test_cases[coverage].append(run)
        else:
            test_cases[coverage] = [run]

    return test_cases


def filter_testcases(data: dict[str, list[JsonParserExecution]]) -> list[JsonParserExecution]:
    """Select the most interesting test cases from the data dictionary, avoiding duplicate or redundant inputs."""
    # TODO: Implement test case selection
    all_executions: list[JsonParserExecution] = []

    for fuzzer_name, runs in data.items():
        all_executions.extend(runs)

    # Keep only unique inputs
    unique_by_input = {}
    for exec in all_executions:
        if exec.inp not in unique_by_input:
            unique_by_input[exec.inp] = exec

    unique_executions = list(unique_by_input.values())

    # Within the unique inputs, keep only the ones that cover new lines
    selected_tests = []
    seen_coverage: set[Location] = set()

    for exec in unique_executions:
        cov = set(exec.cov.coverage())
        new_lines = cov - seen_coverage
        if new_lines:
            selected_tests.append(exec)
            seen_coverage |= cov

    return selected_tests



def stringify_testcase(execution: JsonParserExecution) -> str:
    output = f"Error: {execution.err}" if execution.err else str(execution.out)
    return f"{repr(execution.inp)} -> {output}"


def show_testcases_by_fuzzer(data: dict[str, list[JsonParserExecution]]):
    for runner, runs in data.items():
        print(f"Results for {runner}:")
        test_cases = produce_testcases(runs)
        for coverage, executions in test_cases.items():
            print(f"\tCoverage: {len(coverage):3}")
            for execution in executions[:MAX_DUPLICATES]:
                print(f"\t\t{stringify_testcase(execution)}")

            if len(executions) >= MAX_DUPLICATES:
                print(f"\t\t{len(executions) - MAX_DUPLICATES} more test cases not shown...")


if __name__ == "__main__":
    random.seed(RANDOM_SEED)

    # data = part1()
    # data = part2()
    # data = part3()
    data = part4()

    print("Generating analytics...")
    analyze_all(data)

    show_testcases_by_fuzzer(data)

    testcases = filter_testcases(data)

    print(f"Filtered testcases: {len(testcases)}")
    for testcase in testcases:
        print(f"\t{stringify_testcase(testcase)}")

    total_coverage = set()
    for testcase in testcases:
        total_coverage |= frozenset(testcase.cov.coverage())

    print(f"Filtered testcases cover a total of {len(total_coverage)} lines.")
