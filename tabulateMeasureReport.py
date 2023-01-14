from pathlib import Path
from phdi.tabulation import load_schema, write_data
from phdi.fhir.tabulation import extract_data_from_schema, tabulate_data
import pandas as pd
import requests
import json

schema = load_schema(Path("MeasureReportSchema.yaml"))  # Path to a schema config file.
output_path = "./"  # Path to directory where tables will be written
output_format = "csv"  # File format of tables
fhir_url = 'https://fhir.agg-data.connectathon.dev.cirg.uw.edu/fhir'  # The URL for a FHIR server
# cred_manager = AzureCredentialManager(fhir_url)   # Credential manager for authentication with the FHIR server.

# output_params = {
#     "CDC Patient Impact and Hospital Capacity": {
#         "output_type": output_format,
#         "directory": output_path,
#         "filename": filename,
#     }
# }
# generate_tables(schema, output_params, fhir_url)

results = extract_data_from_schema(schema, fhir_url)

tabulated_results = {}
for table_name, data in results.items():
    filename = table_name + ".csv"
    tabulated_results[table_name] = tabulate_data(data, schema, table_name)
    print(tabulated_results[table_name][0])
    print(tabulated_results[table_name][1])
    df = pd.DataFrame(data=tabulated_results[table_name][1:], columns=tabulated_results[table_name][0])
    df = df.sort_values(by=['Subject','Reporter','Period Start','Period End'], ascending=True, ignore_index=True)
    df.to_csv(output_path+filename)
    # write_data(tabulated_results[table_name], output_path, output_format, filename) # Removed in favor of DataFrame.to_csv
    print("Wrote " + table_name + " table to " + output_path + filename)

# print(tabulated_results)

