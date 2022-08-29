from src.config import CONFIG


DELETE_INPUT_FILE_ON_COMPLETION = CONFIG["DEFAULTS"]["delete_input_file_on_completion"]
DELETE_OUTPUT_FILE_ON_COMPLETION = CONFIG["DEFAULTS"][
    "delete_output_file_on_completion"
]


class GrouperParameter:
    def __init__(
        self,
        *args,
        delete_input: bool = DELETE_INPUT_FILE_ON_COMPLETION,
        delete_output: bool = DELETE_OUTPUT_FILE_ON_COMPLETION,
        **kwargs,
    ) -> None:
        self.delete_input_file: bool = delete_input
        self.delete_output_file: bool = delete_output

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __hash__(self):
        pass

    def __eq__(self, other) -> bool:
        pass