from ParseJsonRunner import ParseJsonRunner, JsonParserExecution


class BaseFuzzer:
    def fuzz(self) -> str:
        ...

    def run(self, runner: ParseJsonRunner) -> JsonParserExecution:
        inp = self.fuzz()
        return runner.run(inp)

    def runs(self, runner: ParseJsonRunner, trials: int) -> list[JsonParserExecution]:
        runs = []
        for i in range(trials):
            res = self.run(runner)
            runs.append(res)
            if i % 100 == 0:
                print(f"Run {i:4} of {self.__class__.__name__} | Input: {repr(res.inp)}")

        return runs
