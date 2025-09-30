from pathlib import Path

from fuzzingbook.Fuzzer import Runner
import matplotlib.pyplot as plt
from typing import Dict

from ParseJsonRunner import JsonParserExecution

dest = Path("analytics")


def plot_successful_inputs(fuzzer_results: Dict[str, list[JsonParserExecution]]):
    """
    Plot the number of successful inputs (valid JSON) over runs for each fuzzer.

    Args:
        fuzzer_results: Dictionary mapping fuzzer names to their results (test_cases, runs)
    """
    plt.figure(figsize=(12, 8))

    for fuzzer_name, runs in fuzzer_results.items():
        # Count successful inputs over runs
        successful = [0]
        for run in runs:
            if run.status == Runner.PASS:
                successful.append(successful[-1] + 1)
            else:
                successful.append(successful[-1])

        # Plot
        plt.plot(range(len(successful)), successful, label=fuzzer_name)

    plt.xlabel('Number of Runs')
    plt.ylabel('Number of Successful Inputs')
    plt.title('Successful Inputs vs. Runs')
    plt.legend()
    plt.grid(True)
    plt.savefig(dest / 'successful_inputs.png')
    plt.close()


def plot_testcases(fuzzer_results: Dict[str, list[JsonParserExecution]]):
    """
    Plot the number of unique test cases (by coverage) over runs for each fuzzer.

    Args:
        fuzzer_results: Dictionary mapping fuzzer names to their results (test_cases, runs)
    """
    plt.figure(figsize=(12, 8))

    for fuzzer_name, runs in fuzzer_results.items():
        # Count unique coverages over runs
        unique_coverages = set()
        testcases = [0]

        for run in runs:
            coverage = frozenset(run.cov.coverage())
            if coverage not in unique_coverages:
                unique_coverages.add(coverage)
                testcases.append(testcases[-1] + 1)
            else:
                testcases.append(testcases[-1])

        # Plot
        plt.plot(range(len(testcases)), testcases, label=fuzzer_name)

    plt.xlabel('Number of Runs')
    plt.ylabel('Number of Unique Test Cases')
    plt.title('Unique Test Cases vs. Runs')
    plt.legend()
    plt.grid(True)
    plt.savefig(dest / 'testcases.png')
    plt.close()


def plot_total_coverage(fuzzer_results: Dict[str, list[JsonParserExecution]]):
    """
    Plot the total coverage over runs for each fuzzer.

    Args:
        fuzzer_results: Dictionary mapping fuzzer names to their results (test_cases, runs)
    """
    plt.figure(figsize=(12, 8))

    for fuzzer_name, runs in fuzzer_results.items():
        # Calculate cumulative coverage over runs
        all_coverage = set()
        coverage_size = [0]

        for run in runs:
            all_coverage.update(run.cov.coverage())
            coverage_size.append(len(all_coverage))

        # Plot
        plt.plot(range(len(coverage_size)), coverage_size, label=fuzzer_name)

    plt.xlabel('Number of Runs')
    plt.ylabel('Total Coverage')
    plt.title('Total Coverage vs. Runs')
    plt.legend()
    plt.grid(True)
    plt.savefig(dest / 'total_coverage.png')
    plt.close()


def analyze_all(fuzzer_results: Dict[str, list[JsonParserExecution]]):
    """
    Run all analytics functions and generate all plots.

    Args:
        fuzzer_results: Dictionary mapping fuzzer names to their results (test_cases, runs)
    """

    if not dest.exists():
        dest.mkdir()

    plot_total_coverage(fuzzer_results)
    plot_successful_inputs(fuzzer_results)
    plot_testcases(fuzzer_results)

    print(f"All plots generated successfully in {dest.absolute()}.")
