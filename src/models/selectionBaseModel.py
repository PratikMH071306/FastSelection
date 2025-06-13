
from pydantic import BaseModel
from typing import Optional

class PumpDataBase(BaseModel):
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

#   class Config:
#       extra = Extra.allow  # Allow unexpected fields