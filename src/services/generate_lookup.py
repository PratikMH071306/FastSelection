# # generate_lookup.py
# import json
# import os
# from sqlalchemy import create_engine, text

# # Use environment variables for sensitive info
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "mssql+pyodbc://sa:Velotech*1@pc1:1434/pumpManagement_v5_server?driver=ODBC+Driver+17+for+SQL+Server"
# )
# engine = create_engine(DATABASE_URL)

# # Define tables and their relevant fields
# TABLE_FIELDS = {
#     "tbl_01_pumptype": ["series", "mounting", "pumpType", "verticalLogic"],
#     "tbl_02_motor": ["power", "rpm", "mounting"],
#     # Add more as needed
# }

# value_field_map = {}

# try:
#     with engine.connect() as conn:
#         for table, fields in TABLE_FIELDS.items():
#             for field in fields:
#                 # Use parameterized query to avoid SQL injection
#                 query = text(f"SELECT DISTINCT [{field}] FROM [{table}]")
#                 try:
#                     result = conn.execute(query).fetchall()
#                     for row in result:
#                         val = str(row[0]).upper()
#                         if val and val != "NONE":
#                             value_field_map[val] = {"field": field, "table": table}
#                 except Exception as e:
#                     print(f"Error querying {table}.{field}: {e}")

#     # Write JSON to the same directory as this script
#     output_path = os.path.join(os.path.dirname(__file__), "value_field_map.json")
#     with open(output_path, "w") as f:
#         json.dump(value_field_map, f, indent=2)
# except Exception as e:
#     print(f"Database connection or file write failed: {e}")