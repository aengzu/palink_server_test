from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import SessionLocal
from models import Scenario

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ScenarioBase(BaseModel):
    scenario_name: str
    scenario_description: str

class ScenarioCreate(ScenarioBase):
    category_id: int

class ScenarioRead(ScenarioBase):
    scenario_id: int
    category_id: int

    class Config:
        orm_mode = True

# Scenario 생성 API
@router.post("/", response_model=ScenarioRead, status_code=201)
async def create_scenario(scenario_data: ScenarioCreate, db: Session = Depends(get_db)):
    new_scenario = Scenario(**scenario_data.dict())
    db.add(new_scenario)
    db.commit()
    db.refresh(new_scenario)
    return new_scenario

# 모든 Scenario 조회 API
@router.get("/", response_model=List[ScenarioRead])
async def read_scenarios(db: Session = Depends(get_db)):
    scenarios = db.query(Scenario).all()
    return scenarios

# 특정 Scenario 조회 API
@router.get("/{scenario_id}", response_model=ScenarioRead)
async def read_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

# Scenario 수정 API
@router.put("/{scenario_id}", response_model=ScenarioRead)
async def update_scenario(scenario_id: int, scenario_data: ScenarioBase, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    for var, value in vars(scenario_data).items():
        setattr(scenario, var, value)
    db.commit()
    return scenario

# Scenario 삭제 API
@router.delete("/{scenario_id}", status_code=204)
async def delete_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
    if scenario is None:
        raise HTTPException(status_code=404, detail="Scenario not found")
    db.delete(scenario)
    db.commit()
    return {"detail": "Scenario deleted successfully"}
