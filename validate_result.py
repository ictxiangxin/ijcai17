import tool
import compute
from workflow import Work


def validate_result(validate_path: str, result_path: str):
    validate_reader = tool.Reader(validate_path)
    result_reader = tool.Reader(result_path)
    validate = validate_reader.read(True)
    result = result_reader.read(True)
    print('Loss: {}'.format(compute.loss(validate, result)))


class ValidateResult(Work):
    def function(self):
        return validate_result
