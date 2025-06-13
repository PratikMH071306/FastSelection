


### MANUAL DB CREATION SO NOT NEEDED  ###





# src/api/db.py
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "mssql+pyodbc://sa:Velotech*1@pc1:1434/pumpManagement_v5_server?driver=ODBC+Driver+17+for+SQL+Server"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)

# def get_all_tables_data():
#     with engine.connect() as conn:
#        # Table tbl_01_pumptype
#        pump_data = conn.execute(text("SELECT * FROM tbl_01_pumptype")).mappings().all()
#         #pump_data = conn.execute(text("SELECT * FROM pump_table")).mappings().all()
#         fluid_data = conn.execute(text("SELECT * FROM fluid_table")).mappings().all()
#         curve_data = conn.execute(text("SELECT * FROM curve_table")).mappings().all()
#         material_data = conn.execute(text("SELECT * FROM material_table")).mappings().all()
#         application_data = conn.execute(text("SELECT * FROM application_table")).mappings().all()

#     if __name__ == "__main__":
#         pump_types = get_pump_types()
#         for row in pump_types[:5]:  # Only the first 5 rows
#             print(row)


#     return {
#         "pumps": [dict(row) for row in pump_data[:5]],
#         #"fluids": [dict(row) for row in fluid_data],
#         #"curves": [dict(row) for row in curve_data],
#         #"materials": [dict(row) for row in material_data],
#         #"applications": [dict(row) for row in application_data],
#     }
