import simplejson
from dataclasses import dataclass
from fuzzingbook.Fuzzer import Runner
from fuzzingbook.Coverage import Coverage


@dataclass
class JsonParserExecution:
    inp: str
    out: dict | None
    err: Exception | None
    status: str
    cov: Coverage


class ParseJsonRunner(Runner):
    def run(self, inp: str) -> JsonParserExecution:
        with Coverage() as cov:
            try:
                res = simplejson.loads(inp)
                return JsonParserExecution(inp, res, None, Runner.PASS, cov)
            except Exception as e:
                return JsonParserExecution(inp, None, e, Runner.FAIL, cov)
