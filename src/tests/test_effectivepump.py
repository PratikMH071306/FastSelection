
#Unit/integration test files for all modules.




# from fastapi import APIRouter
# from pydantic import BaseModel
# import spacy
# from sqlalchemy.orm import Session
# from sqlalchemy import text
# #from db import get_db
# import re
# import json
# import os
# from src.services.spacy_init import load_custom_nlp


# router = APIRouter()
# nlp = load_custom_nlp()

# Use absolute path for value_field_map.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "../services/value_field_map.json")
with open(JSON_PATH, encoding="utf-8") as f:
    value_field_map = json.load(f)

class Query(BaseModel):
    text: str

@router.post("/") #extract
def extract_data(query: Query, db: Session = Depends(get_db)):
    text = query.text.lower()
    doc = nlp(text)

    flow = head = temperature = density = None
    fluid = None

    # Flow in LPM (liters per minute)
    flow_match = re.search(r"(\d+)\s*(lpm|liters?\s*per\s*minute)?", text)
    if flow_match:
        flow = int(flow_match.group(1))

     # Head in meters
    head_match = re.search(r"(\d+)\s*(meters?|m)\s*(head)?", text)
    if head_match:
        head = int(head_match.group(1))

    # Temperature in °C
    temp_match = re.search(r"(\d+)\s*°?\s*c", text)
    if temp_match:
        temperature = int(temp_match.group(1))

    # Density in kg/m3 
    density_match = re.search(r"density\s+of\s+(\d+)\s*kg/m3", text, re.IGNORECASE)
    density = int(density_match.group(1)) if density_match else None

    #primemover_type
    # First, try to match explicit primemover_type
    primemover_type_match = re.search(r"primemover[_\s]*type\s*(?:is\s*)?(\w+)", text, re.IGNORECASE)

    if primemover_type_match:
        primemover_type = primemover_type_match.group(1)
    else:
    # If not found, look for keywords like 'motor' or 'engine'
        keyword_match = re.search(r"\b(motor|engine)\b", text, re.IGNORECASE)
        primemover_type = keyword_match.group(1).capitalize() if keyword_match else None



    # Fluid keyword detection
    if "hot water" in text:
        fluid = "hot water"
    elif "chemical" in text or "chemicals" in text:
        fluid = "chemical"
    elif "water" in text:
        fluid = "water"

    # Add more rules as needed

    final_result = {
        "dp_flow": flow,
        "dp_head": head,
        "dp_fluid_name": "Clear water",
        "density": "1000",
        "dp_primemover_type": "Motor",
    }

    # Default full structure
    prior_result = {
        "CE_display": "1",
        "CH3_display": "1",
        "CQ_display": "1",
        "checkFlowMissTolerance": False,
        "checkHeadMissTolerance": True,
        "checkOperatingRange": True,
        "constant": "Flow",
        "dp_AddEff": "",
        "dp_temperature": "",
        "dp_EffModifierImpellerType": "on",
        "dp_EffModifierMOC": "on",
        "dp_EffModifierStages": "on",
        "dp_ViscosityCorrectionFactor": [1, 1, 1],
        "dp_ambientTemp": "All",
        "dp_application": "None",
        "dp_consistency": "0",
        "dp_driver_sizing": "Rated Power",
        "dp_driver_sizing_perOfdp": "",
        "dp_effClass": "All",
        "dp_frequency": 50,
        "dp_liquid_description": fluid or "",
        "dp_liquid_type": "Clear",
        "dp_manufacturer": "All",
        "dp_max_flow": "",
        "dp_max_soh": "",
        "dp_max_solid_dia": "",
        "dp_min_head": "",
        "dp_min_soh": "",
        "dp_mounting": "All",
        "dp_npsha": "",
        "dp_phValue": "0",
        "dp_pmSeries": "",
        "dp_pole": "",
        "dp_pump_qty_system": "1",
        "dp_searchCriteria": "Primemover speed",
        "dp_serviceFactor": "1",
        "dp_solid_concentration": "",
        "dp_solid_concentration_uom": "PPM",
        "dp_specification": "All",
        "dp_speed": "0",
        "dp_spgr": "1",
        "dp_suction_pressure": "1",
        "dp_system": "Standalone",
        "dp_tempClass": "All",
        "dp_testing_standard": "No Negative Tolerance",
        "dp_totalQty": "1",
        "dp_uom_flow": "m3/hr",
        "dp_uom_head": "m",
        "dp_uom_npsha": "m",
        "dp_uom_pressure": "bar",
        "dp_uom_solid_size": "mm",
        "dp_uom_temperature": "Deg C",
        "dp_uom_viscosity": "Cst",
        "dp_vapor_pressure": "",
        "dp_viscosity": "0",
        "flowMissToleranceMax": "0",
        "flowMissToleranceMin": "0",
        "headMissToleranceMax": "0",
        "headMissToleranceMin": "0",
        "isUserImpellerDia": False,
        "noOfSystem": "1",
        "primeMoverCoupled": True,
        "seriesSelected": [52],
        "slurryECF": "1",
        "slurryHCF": "1",
        "staticHead": "0",
        "suctionCondition": "Flooded",
        "textfield-1090-inputEl": "",
        "typeOfDriver": "DIRECT",
        "userImpellerDia": ""
    }

    # Merge the two
    final_result.update(prior_result)

    return final_result

# If not flow/head — check master query
    identified_fields = {}
    for token in text.split():
        token_upper = token.upper()
        if token_upper in value_field_map:
            info = value_field_map[token_upper]
            table = info["table"]
            field = info["field"]
            if table not in identified_fields:
                identified_fields[table] = {}
            identified_fields[table][field] = token_upper

    responses = []
    for table, filters in identified_fields.items():
        conditions = [f"{col} = '{val}'" for col, val in filters.items()]
        sql = f"SELECT * FROM {table} WHERE {' AND '.join(conditions)}"
        result = db.execute(sql).fetchall()
        responses.append({
            "table": table,
            "filters": filters,
            "available": bool(result),
            "match_count": len(result)
        })

    return {"master_query_result": responses}
