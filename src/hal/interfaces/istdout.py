# ---------------------------------------------------------------------------------------------------------------------

class IStdOut:

    def write(self, msg: str) -> 'Self':
        raise Exception('Not Implented!')

    def read(self) -> str:
        raise Exception('Not Implented!')

    pass
# ---------------------------------------------------------------------------------------------------------------------
