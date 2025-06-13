# src/api/effectivepump.py
from fastapi import APIRouter
from pydantic import BaseModel, Extra
from typing import List, Optional
from jinja2 import Template

router = APIRouter()

class PumpData(BaseModel):
    id: int
    pumpModel: str
    pumpTypeUuid: str
    pumpModelUuid: str
    primeMoverUuid: str
    perfCurvNo: str
    pumpModelId: int
    perfCurvNoId: int
    series: str
    pumpTypeId: int
    stgType: str
    stg: int

    trimDia: float
    maxDia: float
    minDia: float
    diaList: str
    diaList2: str
    suction: str
    discharge: str
    pumpShaftDia: str
    shaftGroup: str
    impellerDia2: str
    recommendedPipeSuc: int
    recommendedPipeDis: int

    speed: int
    pole: int
    trimRatio: float
    bepPerPumpWater: str
    bepPerPump: str
    bepWater: str
    bepPump: str
    bepEff: float
    bepFlowPercentage: float
    minContinuousFlow: float
    operatingRange: str

    efficiencyDp: str
    npshrDp: str
    powerDp: str
    powerDpMax: str
    soh: str

    primeMoverID: int
    primeMoverPower: str
    primeMoverFrame: str
    primeMoverPowerHP: str
    primemoverSpeed: str

    system: str
    noOfPumps: int
    staticHead: int
    verticalLogic: bool
    genericBom: Optional[bool] = None
    patternAvl: Optional[bool] = None
    discontinued: Optional[bool] = None

    specificSpeed: float
    suctionSpecificSpeed: float
    tipSpeedCal: float
    sysPreCal: str

    class Config:
        extra = Extra.allow  # Allow unexpected fields

# Template for the message
template = Template(
    "Most effective Pump Model will be {{ model }} at efficiency of {{ efficiency }}%."
)

@router.post("/")  # effectivepump
def effectivepump(data: List[PumpData]):
    if not data:
        return {"text": "No data provided."}

    # Find the item with the maximum bepEff
    max_eff_item = max(data, key=lambda x: x.bepEff)

    # Generate the summary message
    summary_text = template.render(
        model=max_eff_item.pumpModel,
        efficiency=round(max_eff_item.bepEff * 100, 2)
    )

    # Return in desired JSON format
    return {summary_text}
