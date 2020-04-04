from models.data import Data

class DataService():

  def __init__(self, data, check_version=True):
    self.__data = Data(data, check_version)

  def generate_query(self):
    values = self.__data.get_all_row_values()
    schema = self.__data.get_schema()
    name = self.__data.get_name()

    output_formating = self.__data.get_output_formating()
    output_formating_keys = list(output_formating.keys())
    query_list = []
    for i in range(len(values)):
      _ql = []
      for j in range(len(schema)):
        value = str(values[i][j])
        substitute_value = None
        if schema[j] in output_formating_keys:
          substitute_value = output_formating[schema[j]]
          value = substitute_value.replace("#[value]", value)

        _ql.append(value + " AS " + str(schema[j]))
      query = ", ".join(_ql)
      query = "SELECT " + query
      query_list.append(query)
    query = " UNION ALL ".join(query_list)
    query = name + " AS ( " + query + " )"
    return query

  def get_name(self):
    return self.__data.get_name()

  def get_schema(self):
    return self.__data.get_schema()
