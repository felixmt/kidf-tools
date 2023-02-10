import pandas as pd
from tools.file_helper import file_helper

df_test = pd.DataFrame({"name": ["gogo", "dudu", "fufu"]})
ar_test = ["toto", "nono", "juju"]
file_tools = file_helper()

# response = file_tools.write_dataframe_to_csv(df_test)
# print(response)
# print(type(response))

# response = file_tools.write_csv("name", ar_test)
# print(response)
# print(response.name)

response = file_tools.write_xlsx(["sheet1"], [["name"]], [[["toto"], ["dudu"], ["juju"]]])
print(response)
print(response.filename)