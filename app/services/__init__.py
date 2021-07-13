from app.exc import DataTypeError, DataKeyError



class CreateAndUpdateBaseService:
    def __init__(self, input_template: list, request_data: dict, optional_keys: list) -> None:
        self.mandatory_keys = [*input_template]
        self.input_template = input_template
        self.request_data = request_data
        self.optional_keys = optional_keys

    def _clear_request_data_keys(self):
        for k in self.request_data.copy():
            if k not in self.mandatory_keys + self.optional_keys:
                self.request_data.pop(k)

    def check_request_data_keys(self):
        self._clear_request_data_keys()
        for mk in self.mandatory_keys:
            if mk not in self.request_data:
                raise DataKeyError({'error': f'missing key {mk}'})

    def check_request_data_types(self):
        invalid_types = {k: type(self.request_data[k]).__name__ for k in self.request_data if self.input_template[k] != type(self.request_data[k])}
        expected_types = {k: self.input_template[k].__name__ for k in self.request_data if self.input_template[k] != type(self.request_data[k])}
        if invalid_types:
            raise DataTypeError({'error': {'invalid_types': invalid_types, 'expected_types': expected_types}})
