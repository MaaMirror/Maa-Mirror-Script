import argparse


class Argparser:
    parser = argparse.ArgumentParser()

    def __init__(self):
        self._add_argument()
        self.args = self.parser.parse_args()

    def _add_argument(self):
        self.parser.add_argument("--check", action="store_true", default=False)
        self.parser.add_argument("--check_res", action="store_true", default=False)
        self.parser.add_argument("--issue", action="store_true", default=False)
        self.parser.add_argument("--issue_res", action="store_true", default=False)
        self.parser.add_argument("--token", type=str, help="Github Token", default=None)
        self.parser.add_argument("--CF", type=bool, action="store_true", default=False)
        self.parser.add_argument(
            "--build", type=bool, action="store_true", default=False
        )
