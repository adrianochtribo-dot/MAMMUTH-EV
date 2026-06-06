"""
MAMMUTH•EVENTS™ — Safety Engine
Module: api/v1/routes/predict.py
Scenario: A (Deterministico)
Version: 1.0.0

Endpoint FastAPI per la valutazione predittiva del rischio crowd crush.
Validazione input con Pydantic v2.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator, model_validator

from core.risk_calculator import (
    EventInput,
    EventModifiers,
    VenueGeometry,
    Bottleneck,
    calculate_risk,
    RiskAssessment,
)

router = APIRouter(prefix="/safety", tags=["Safety Engine"])


# ---------------------------------------------------------------------------
# PYDANTIC SCHEMAS — Request
# ---------------------------------------------------------------------------

class BottleneckSchema(BaseModel):
    id: str = Field(..., description="Identificativo univoco del bottleneck")
    label: str = Field(..., description="Descrizione leggibile (es. 'Vicolo Nord — arco')")
    width_m: float = Field(..., gt=0, le=50, description="Larghezza netta in metri")
    is_bidirectional: bool = Field(False, description="Flusso bidirezionale?")
    is_obstructed: bool = Field(False, description="Ostruzione prevista o rilevata?")


class VenueGeometrySchema(BaseModel):
    name: str = Field(..., description="Nome dell'area/piazza")
    area_sqm: float = Field(..., gt=0, description="Superficie in m²")
    bottlenecks: list[BottleneckSchema] = Field(
        default_factory=list,
        description="Colli di bottiglia identificati"
    )
    is_enclosed: bool = Field(True, description="Area chiusa con accessi limitati?")
    escape_routes_count: int = Field(2, ge=0, description="Numero vie di fuga")
    escape_routes_obstructed: int = Field(0, ge=0, description="Vie di fuga ostruite")

    @model_validator(mode="after")
    def validate_escape_routes(self) -> "VenueGeometrySchema":
        if self.escape_routes_obstructed > self.escape_routes_count:
            raise ValueError(
                "escape_routes_obstructed non può superare escape_routes_count"
            )
        return self


class EventModifiersSchema(BaseModel):
    alcohol_expected: bool = False
    fireworks_planned: bool = False
    live_music: bool = False
    low_lighting: bool = False
    no_safety_plan: bool = False
    mobility_impaired_percent: float = Field(0.0, ge=0, le=100)
    temperature_c: float = Field(20.0, ge=-10, le=50)
    humidity_percent: float = Field(50.0, ge=0, le=100)


class PredictRequest(BaseModel):
    event_id: str = Field(..., description="ID univoco evento (es. EVT-2026-LT-SRM-001)")
    event_name: str = Field(..., min_length=3, description="Nome dell'evento")
    expected_attendance: int = Field(..., gt=0, le=500_000, description="Presenze attese")
    istat_comune: str = Field(..., pattern=r"^\d{6}$", description="Codice ISTAT 6 cifre")
    event_date: str = Field(..., description="Data evento (YYYY-MM-DD)")
    venue: VenueGeometrySchema
    modifiers: EventModifiersSchema = Field(default_factory=EventModifiersSchema)
    has_safety_plan: bool = Field(False, description="Piano sicurezza depositato in Prefettura?")

    @field_validator("event_date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("event_date deve essere in formato YYYY-MM-DD")
        return v


# ---------------------------------------------------------------------------
# PYDANTIC SCHEMAS — Response
# ---------------------------------------------------------------------------

class DensityAnalysisResponse(BaseModel):
    persons_per_sqm: float
    los_label: str
    threshold_margin_percent: float
    status: str
    projected_peak_risk: bool


class BottleneckAnalysisResponse(BaseModel):
    bottleneck_id: str
    label: str
    effective_flow_ppm: float
    time_to_clear_min: float
    is_critical: bool
    recommendation: str


class HistoricalMatchResponse(BaseModel):
    incident_id: str
    incident_name: str
    similarity_score: float
    matched_factors: list[str]


class RecommendationResponse(BaseModel):
    priority: str
    code: str
    message: str
    action_type: str


class PredictResponse(BaseModel):
    request_id: str
    computed_at: str
    scenario_used: str = "A"
    event_id: str
    event_name: str
    global_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: str
    risk_color: str
    confidence: float
    modifier_factor: float
    density_analysis: DensityAnalysisResponse
    bottleneck_analyses: list[BottleneckAnalysisResponse]
    historical_match: Optional[HistoricalMatchResponse]
    recommendations: list[RecommendationResponse]
    legal_disclaimer: str


# ---------------------------------------------------------------------------
# MAPPING helpers
# ---------------------------------------------------------------------------

def _map_request_to_domain(req: PredictRequest) -> EventInput:
    bottlenecks = [
        Bottleneck(
            id=b.id,
            label=b.label,
            width_m=b.width_m,
            is_bidirectional=b.is_bidirectional,
            is_obstructed=b.is_obstructed,
        )
        for b in req.venue.bottlenecks
    ]

    venue = VenueGeometry(
        name=req.venue.name,
        area_sqm=req.venue.area_sqm,
        bottlenecks=bottlenecks,
        is_enclosed=req.venue.is_enclosed,
        escape_routes_count=req.venue.escape_routes_count,
        escape_routes_obstructed=req.venue.escape_routes_obstructed,
    )

    modifiers = EventModifiers(
        alcohol_expected=req.modifiers.alcohol_expected,
        fireworks_planned=req.modifiers.fireworks_planned,
        live_music=req.modifiers.live_music,
        low_lighting=req.modifiers.low_lighting,
        no_safety_plan=req.modifiers.no_safety_plan,
        mobility_impaired_percent=req.modifiers.mobility_impaired_percent,
        temperature_c=req.modifiers.temperature_c,
        humidity_percent=req.modifiers.humidity_percent,
    )

    return EventInput(
        event_id=req.event_id,
        event_name=req.event_name,
        expected_attendance=req.expected_attendance,
        venue=venue,
        modifiers=modifiers,
        has_safety_plan=req.has_safety_plan,
    )


def _map_assessment_to_response(
    assessment: RiskAssessment,
    request_id: str,
) -> PredictResponse:
    return PredictResponse(
        request_id=request_id,
        computed_at=datetime.utcnow().isoformat() + "Z",
        event_id=assessment.event_id,
        event_name=assessment.event_name,
        global_score=assessment.global_score,
        risk_level=assessment.risk_level.value,
        risk_color=assessment.risk_color,
        confidence=assessment.confidence,
        modifier_factor=assessment.modifier_factor,
        density_analysis=DensityAnalysisResponse(
            persons_per_sqm=assessment.density_analysis.persons_per_sqm,
            los_label=assessment.density_analysis.los_label,
            threshold_margin_percent=assessment.density_analysis.threshold_margin_percent,
            status=assessment.density_analysis.status,
            projected_peak_risk=assessment.density_analysis.projected_peak_risk,
        ),
        bottleneck_analyses=[
            BottleneckAnalysisResponse(
                bottleneck_id=b.bottleneck_id,
                label=b.label,
                effective_flow_ppm=b.effective_flow_ppm,
                time_to_clear_min=b.time_to_clear_min,
                is_critical=b.is_critical,
                recommendation=b.recommendation,
            )
            for b in assessment.bottleneck_analyses
        ],
        historical_match=HistoricalMatchResponse(
            incident_id=assessment.historical_match.incident_id,
            incident_name=assessment.historical_match.incident_name,
            similarity_score=assessment.historical_match.similarity_score,
            matched_factors=assessment.historical_match.matched_factors,
        ) if assessment.historical_match else None,
        recommendations=[
            RecommendationResponse(
                priority=r.priority,
                code=r.code,
                message=r.message,
                action_type=r.action_type,
            )
            for r in assessment.recommendations
        ],
        legal_disclaimer=assessment.legal_disclaimer,
    )


# ---------------------------------------------------------------------------
# ENDPOINT
# ---------------------------------------------------------------------------

import uuid

@router.post(
    "/predict",
    response_model=PredictResponse,
    status_code=status.HTTP_200_OK,
    summary="Calcola indice di rischio crowd crush per un evento pianificato",
    description=(
        "Scenario A — Deterministico. Valuta densità (Fruin LoS), "
        "colli di bottiglia, similarità storica e fattori contestuali. "
        "Output: score 0.0–1.0, livello rischio, raccomandazioni prioritizzate."
    ),
)
def predict_risk(payload: PredictRequest) -> PredictResponse:
    try:
        event_input = _map_request_to_domain(payload)
        assessment = calculate_risk(event_input)
        request_id = f"REQ-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8].upper()}"
        return _map_assessment_to_response(assessment, request_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Errore interno Safety Engine: {str(exc)}",
        )
