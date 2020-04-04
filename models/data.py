import common.constants as constants

class Data:

  def __init__(self, data, version_check=True):
    self.__data = data
    self.__version_check = version_check
    self.__validate()
    self.__schema = self.__data[constants.DATA_KEY_SCHEMA]
    self.__values = self.__data[constants.DATA_KEY_VALUES]
    self.__row = constants.DATA_KEY_VALUES_ROW
    self.__name = constants.DATA_KEY_NAME

  def __validate(self):
    for key in constants.DATA_KEYS:
      if key not in self.__data:
        raise ValueError("Invalid Data file. Key " + key + " not present")

    if self.__version_check:
      if constants.VERSION_KEY not in self.__data:
        raise ValueError("Key " + constants.VERSION_KEY + " not present")
      if self.__data[constants.VERSION_KEY] != constants.VERSION_1:
        raise ValueError("Version " + self.__data[constants.VERSION_KEY] + " not supported.")
    
    schema_length = len(self.__data[constants.DATA_KEY_SCHEMA])

    for val in self.__data[constants.DATA_KEY_VALUES]:
      if len(val[constants.DATA_KEY_VALUES_ROW]) != schema_length:
        raise ValueError("Row length doesnot matches to schema length for " + self.__data[constants.DATA_KEY_NAME])

    if constants.DATE_KEY_OUTPUT_FORMATING in self.__data:
      schema = self.__data[constants.DATA_KEY_SCHEMA]
      output_formating = self.__data[constants.DATE_KEY_OUTPUT_FORMATING]

      for val in output_formating:
        present = False
        for schema_val in schema:
          if schema_val == val:
            present =True
        if not present:
          raise ValueError(val + " not present in data schema.")

  def get_all_row_values(self):
    values = []
    for value in self.__values:
      values.append(value[self.__row])
    return values

  def get_output_formating(self):
    if constants.DATE_KEY_OUTPUT_FORMATING in self.__data:
      return self.__data[constants.DATE_KEY_OUTPUT_FORMATING]
    return {}
  
  def get_schema(self):
    return self.__schema
  
  def get_name(self):
    return self.__data[self.__name]
