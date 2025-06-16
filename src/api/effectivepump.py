# src/api/effectivepump.py
from fastapi import APIRouter
from pydantic import BaseModel, Extra
from typing import List, Optional
from jinja2 import Template
# from src.models.selectionBaseModel import PumpDataBase


router = APIRouter()

class PumpData(BaseModel):  # PumpDataBase

    id: Optional[int]
    pumpModel: Optional[str]
    pumpTypeUuid: Optional[str]
    pumpModelUuid: Optional[str]
    primeMoverUuid: Optional[str]
    perfCurvNo: Optional[str]
    pumpModelId: Optional[int]
    perfCurvNoId: Optional[int]
    series: Optional[str]
    pumpTypeId: Optional[int]
    dpFlow: str
    dpHead: str
    stgType: Optional[str]
    stg: Optional[int]

    trimDia: Optional[float]
    maxDia: Optional[float]
    minDia: Optional[float]
    diaList: Optional[str]
    diaList2: Optional[str]
    suction: Optional[str]
    discharge: Optional[str]
    pumpShaftDia: Optional[str]
    shaftGroup: Optional[str]
    impellerDia2: Optional[str]
    recommendedPipeSuc: Optional[int]
    recommendedPipeDis: Optional[int]

    speed: Optional[int]
    pole: Optional[int]
    trimRatio: Optional[float]
    bepPerPumpWater: Optional[str]
    bepPerPump: Optional[str]
    bepWater: Optional[str]
    bepPump: Optional[str]
    bepEff: float
    bepFlowPercentage: Optional[float]
    minContinuousFlow: Optional[float]
    operatingRange: Optional[str]

    efficiencyDp: Optional[str]
    npshrDp: Optional[str]
    powerDp: Optional[str]
    powerDpMax: Optional[str]
    soh: Optional[str]

    primeMoverID: Optional[int]
    primeMoverPower: Optional[str]
    primeMoverFrame: Optional[str]
    primeMoverPowerHP: Optional[str]
    primemoverSpeed: Optional[str]

    system: Optional[str]
    noOfPumps: Optional[int]
    staticHead: Optional[int]
    verticalLogic: Optional[bool]
    genericBom: Optional[bool] = None
    patternAvl: Optional[bool] = None
    discontinued: Optional[bool] = None

    specificSpeed: Optional[float]
    suctionSpecificSpeed: Optional[float]
    tipSpeedCal: Optional[float]
    sysPreCal: Optional[str]

# Template for the message
template = Template(
    "Most effective Pump Model will be {{ model }} at efficiency of {{ efficiency }}%."
)

@router.post("/")  # effectivepump
def effectivepump(data: List[PumpData]):
    if not data:
        return {"text": "No data provided."}

    # Filter out items that don't have a pumpModel or bepEff
    valid_data = [item for item in data if item.pumpModel and item.bepEff is not None]
    if not valid_data:
        return {"text": "No valid pump model with efficiency found."}

    # Find the item with the maximum bepEff
    max_eff_item = max(valid_data, key=lambda x: x.bepEff)

     # Calculate and format efficiency with 2 decimal places
    efficiency_value = max_eff_item.bepEff * 100
    efficiency_str = f"{efficiency_value:.2f}"

    # Generate the summary message
    summary_text = template.render(
        model= max_eff_item.pumpModel,
        efficiency= efficiency_str
    )

    # Return in desired JSON format
    return {summary_text}
