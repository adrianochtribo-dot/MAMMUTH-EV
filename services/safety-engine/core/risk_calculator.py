"""
MAMMUTH•EVENTS™ — Safety Engine
Module: risk_calculator.py
Scenario: A (Deterministico)
Version: 1.1.0
Author: KREATIO UNIVERSAL SYSTEM™

Implementa la valutazione deterministica del rischio crowd crush
basata sugli standard internazionali di John J. Fruin (Pedestrian
Planning and Design, 1971) e SFPE Handbook of Fire Protection Engineering.

Filosofia: INFORMARE, CONSIGLIARE, MITIGARE — mai vietare o censurare.
v1.1.0: aggiunto DataInconsistencyError + OSM validation layer
Ref: SYSTEM-ANTI-FRAGILE-V1.0 — Pattern "Synapse Collapse"
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from numpy import dot
from numpy.linalg import norm


# ---------------------------------------------------------------------------
# COSTANTI — Standard Fruin + letteratura crowd safety internazionale
# ---------------------------------------------------------------------------

DENSITY_LOS_A = 0.5
DENSITY_LOS_B = 1.0
DENSITY_LOS_C = 2.0
DENSITY_LOS_D = 3.0
DENSITY_LOS_E = 4.0
DENSITY_LOS_F = 6.0

FLOW_RATE_NORMAL = 82
FLOW_RATE_BOTTLENECK = 60
FLOW_RATE_PANIC = 25

WEIGHT_DENSITY = 0.40
WEIGHT_BOTTLENECK = 0.30
WEIGHT_HISTORICAL = 0.20
WEIGHT_MODIFIERS = 0.10

OSM_VARIANCE_THRESHOLD = 15.0


# ---------------------------------------------------------------------------
# ECCEZIONE CUSTOM — DataInconsistencyError
# ---------------------------------------------------------------------------

class DataInconsistencyError(Exception):
    """
    Sollevata quando i dati inseriti dall'utente differiscono di oltre
    il 15% rispetto alla misurazione geometrica OSM verificata.

    Blocca il calcolo del risk score per proteggere la difendibilità
    legale del sistema. Un risk score calcolato su dati errati è
    peggio di nessun risk score.

    Filosofia: MAMMUTH genera Decision Intelligence per operatori
    qualificati. Un dato inconsistente non è Decision Intelligence.
    """
    def __init__(
        self,
        field: str,
        declared_value: float,
        osm_value: float,
        variance_percent: float,
    ):
        self.field = field
        self.declared_value = declared_value
        self.osm_value = osm_value
        self.variance_percent = variance_percent
        super().__init__(
            f"DataInconsistencyError: campo '{field}' — "
            f"valore dichiarato {declared_value} differisce del "
            f"{variance_percent:.1f}% dal dato OSM verificato {osm_value}. "
            f"Soglia massima consentita: {OSM_VARIANCE_THRESHOLD}%. "
            f"Correggere il dato prima di procedere al calcolo del rischio."
        )


# ---------------------------------------------------------------------------
# OSM VALIDATOR
# ---------------------------------------------------------------------------

@dataclass
class OSMValidationResult:
    field: str
    declared_value: float
    osm_value: float
    variance_percent: float
    is_consistent: bool
    message: str


def validate_against_osm(
    field: str,
    declared_value: float,
    osm_value: float,
    threshold_percent: float = OSM_VARIANCE_THRESHOLD,
) -> OSMValidationResult:
    """
    Confronta un valore dichiarato con il dato OSM verificato.
    Raises DataInconsistencyError se varianza > soglia.
    """
    if osm_value <= 0:
        return OSMValidationResult(
            field=field,
            declared_value=declared_value,
            osm_value=osm_value,
            variance_percent=0.0,
            is_consistent=True,
            message=f"Dato OSM per '{field}' non disponibile — validazione saltata.",
        )

    variance = abs(declared_value - osm_value) / osm_value * 100

    if variance > threshold_percent:
        raise DataInconsistencyError(
            field=field,
            declared_value=declared_value,
            osm_value=osm_value,
            variance_percent=variance,
        )

    return OSMValidationResult(
        field=field,
        declared_value=declared_value,
        osm_value=osm_value,
        variance_percent=round(variance, 2),
        is_consistent=True,
        message=(
            f"'{field}' validato: varianza {variance:.1f}% "
            f"< soglia {threshold_percent}% — dato coerente con OSM."
        ),
    )


def validate_venue_geometry(
    venue: "VenueGeometry",
    osm_area_sqm: float = 0.0,
) -> list[OSMValidationResult]:
    """
    Valida la geometria del venue contro i dati OSM.
    Raises DataInconsistencyError al primo campo inconsistente.
    """
    results = []
    if osm_area_sqm > 0:
        result = validate_against_osm(
            field="area_sqm",
            declared_value=venue.area_sqm,
            osm_value=osm_area_sqm,
        )
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# ENUMERAZIONI
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    BASSO     = "BASSO"
    MEDIO     = "MEDIO"
    ALTO      = "ALTO"
    CRITICO   = "CRITICO"
    EMERGENZA = "EMERGENZA"


class RiskColor(str, Enum):
    BASSO     = "#2ECC71"
    MEDIO     = "#F39C12"
    ALTO      = "#E67E22"
    CRITICO   = "#E74C3C"
    EMERGENZA = "#8E1A0E"


# ---------------------------------------------------------------------------
# DATACLASS DI INPUT
# ---------------------------------------------------------------------------

@dataclass
class Bottleneck:
    id: str
    label: str
    width_m: float
    is_bidirectional: bool = False
    is_obstructed: bool = False

    def effective_flow_rate(self) -> float:
        base = self.width_m * FLOW_RATE_BOTTLENECK
        if self.is_bidirectional:
            base *= 0.5
        if self.is_obstructed:
            base *= 0.4
        return base


@dataclass
class EventModifiers:
    alcohol_expected: bool = False
    fireworks_planned: bool = False
    live_music: bool = False
    low_lighting: bool = False
    no_safety_plan: bool = False
    mobility_impaired_percent: float = 0.0
    temperature_c: float = 20.0
    humidity_percent: float = 50.0

    def composite_modifier(self) -> float:
        modifier = 1.0
        if self.alcohol_expected:
            modifier += 0.10
        if self.fireworks_planned:
            modifier += 0.08
        if self.live_music:
            modifier += 0.05
        if self.low_lighting:
            modifier += 0.12
        if self.no_safety_plan:
            modifier += 0.15
        if self.mobility_impaired_percent > 5:
            modifier += 0.05
        if self.temperature_c > 28 and self.humidity_percent > 65:
            modifier += 0.10
        elif self.temperature_c > 32:
            modifier += 0.08
        return min(modifier, 1.55)


@dataclass
class HistoricalIncident:
    id: str
    name: str
    feature_vector: list[float]
    risk_score_retrospective: float


@dataclass
class VenueGeometry:
    name: str
    area_sqm: float
    bottlenecks: list[Bottleneck] = field(default_factory=list)
    is_enclosed: bool = True
    escape_routes_count: int = 2
    escape_routes_obstructed: int = 0


@dataclass
class EventInput:
    """Input completo per la valutazione di rischio Scenario A."""
    event_id: str
    event_name: str
    expected_attendance: int
    venue: VenueGeometry
    modifiers: EventModifiers = field(default_factory=EventModifiers)
    has_safety_plan: bool = False
    osm_area_sqm: float = 0.0    # area OSM verificata — 0 = non disponibile


# ---------------------------------------------------------------------------
# DATACLASS DI OUTPUT
# ---------------------------------------------------------------------------

@dataclass
class DensityAnalysis:
    persons_per_sqm: float
    los_label: str
    threshold_margin_percent: float
    status: str
    projected_peak_risk: bool


@dataclass
class BottleneckAnalysis:
    bottleneck_id: str
    label: str
    effective_flow_ppm: float
    time_to_clear_min: float
    is_critical: bool
    recommendation: str


@dataclass
class HistoricalMatch:
    incident_id: str
    incident_name: str
    similarity_score: float
    matched_factors: list[str]


@dataclass
class Recommendation:
    priority: str
    code: str
    message: str
    action_type: str


@dataclass
class RiskAssessment:
    event_id: str
    event_name: str
    global_score: float
    risk_level: RiskLevel
    risk_color: RiskColor
    confidence: float
    density_analysis: DensityAnalysis
    bottleneck_analyses: list[BottleneckAnalysis]
    historical_match: Optional[HistoricalMatch]
    recommendations: list[Recommendation]
    modifier_factor: float
    osm_validation: list[OSMValidationResult] = field(default_factory=list)
    legal_disclaimer: str = (
        "Output a carattere esclusivamente informativo e consultivo. "
        "Non sostituisce la valutazione di un tecnico della sicurezza "
        "certificato (RSPP) né l'autorizzazione prefettizia."
    )


# ---------------------------------------------------------------------------
# DATABASE STORICO SEED
# ---------------------------------------------------------------------------

HISTORICAL_INCIDENTS_DB: list[HistoricalIncident] = [
    HistoricalIncident(
        id="INC-2017-IT-TO-001",
        name="Piazza San Carlo, Torino 2017",
        feature_vector=[6.2, 3, 1, 0.5, 0],
        risk_score_retrospective=0.87,
    ),
    HistoricalIncident(
        id="INC-1989-GB-SHF-001",
        name="Hillsborough Stadium, Sheffield 1989",
        feature_vector=[7.1, 2, 1, 0.3, 0],
        risk_score_retrospective=0.95,
    ),
    HistoricalIncident(
        id="INC-2010-DE-DUI-001",
        name="Love Parade, Duisburg 2010",
        feature_vector=[5.8, 1, 1, 0.6, 0],
        risk_score_retrospective=0.91,
    ),
    HistoricalIncident(
        id="INC-1985-BE-BRU-001",
        name="Heysel Stadium, Bruxelles 1985",
        feature_vector=[4.5, 2, 1, 0.4, 0],
        risk_score_retrospective=0.78,
    ),
]


# ---------------------------------------------------------------------------
# FUNZIONI CORE
# ---------------------------------------------------------------------------

def _classify_density(density: float) -> tuple[str, str]:
    if density <= DENSITY_LOS_A:
        return "LoS A", "Circolazione libera — nessun vincolo"
    elif density <= DENSITY_LOS_B:
        return "LoS B", "Movimento agevole — monitoraggio ordinario"
    elif density <= DENSITY_LOS_C:
        return "LoS C", "Movimento limitato — ATTENZIONE consigliata"
    elif density <= DENSITY_LOS_D:
        return "LoS D", "Contatto fisico frequente — ALLERTA"
    elif density <= DENSITY_LOS_E:
        return "LoS E", "Immobilità parziale — CRITICO: ridurre accessi"
    else:
        return "LoS F", "Pressione fisica — EMERGENZA: evacuazione immediata"


def _analyze_density(event: EventInput) -> DensityAnalysis:
    density = event.expected_attendance / event.venue.area_sqm
    los_label, status = _classify_density(density)
    margin = ((DENSITY_LOS_E - density) / DENSITY_LOS_E) * 100
    peak_risk = density >= DENSITY_LOS_D
    return DensityAnalysis(
        persons_per_sqm=round(density, 3),
        los_label=los_label,
        threshold_margin_percent=round(margin, 1),
        status=status,
        projected_peak_risk=peak_risk,
    )


def _analyze_bottlenecks(event: EventInput) -> list[BottleneckAnalysis]:
    analyses = []
    for bn in event.venue.bottlenecks:
        flow = bn.effective_flow_rate()
        time_to_clear = event.expected_attendance / flow if flow > 0 else 999.0
        is_critical = (
            time_to_clear > 15
            or bn.is_obstructed
            or (bn.is_bidirectional and bn.width_m < 5)
        )
        if is_critical:
            rec = (
                f"ATTENZIONE: '{bn.label}' — deflusso stimato "
                f"{round(time_to_clear, 1)} min per {event.expected_attendance} "
                f"persone. Valutare senso unico o ampliamento a "
                f"≥{math.ceil(bn.width_m * 1.5)}m."
            )
        elif time_to_clear > 8:
            rec = (
                f"ATTENZIONE: '{bn.label}' — valutare presidio steward dedicato. "
                f"Deflusso stimato {round(time_to_clear, 1)} min."
            )
        else:
            rec = f"'{bn.label}' — deflusso adeguato ({round(time_to_clear, 1)} min)."
        analyses.append(BottleneckAnalysis(
            bottleneck_id=bn.id,
            label=bn.label,
            effective_flow_ppm=round(flow, 1),
            time_to_clear_min=round(time_to_clear, 2),
            is_critical=is_critical,
            recommendation=rec,
        ))
    return analyses


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    a = [float(x) for x in vec_a]
    b = [float(x) for x in vec_b]
    denom = norm(a) * norm(b)
    if denom == 0:
        return 0.0
    return float(dot(a, b) / denom)


def _find_historical_match(
    event: EventInput,
    density: float,
) -> Optional[HistoricalMatch]:
    query_vector = [
        density,
        len(event.venue.bottlenecks),
        1.0 if event.venue.is_enclosed else 0.0,
        1.0 if event.modifiers.alcohol_expected else 0.0,
        1.0 if event.modifiers.fireworks_planned else 0.0,
    ]
    best_match = None
    best_score = 0.0
    for incident in HISTORICAL_INCIDENTS_DB:
        score = _cosine_similarity(query_vector, incident.feature_vector)
        if score > best_score:
            best_score = score
            best_match = incident
    if best_match is None or best_score < 0.40:
        return None
    matched_factors = []
    qv = query_vector
    iv = best_match.feature_vector
    if qv[0] >= DENSITY_LOS_D and iv[0] >= DENSITY_LOS_D:
        matched_factors.append("alta_densità")
    if qv[1] >= 2 and iv[1] >= 2:
        matched_factors.append("colli_di_bottiglia_multipli")
    if qv[2] == iv[2] == 1.0:
        matched_factors.append("area_chiusa")
    if qv[3] == iv[3] == 1.0:
        matched_factors.append("presenza_alcol")
    if qv[4] == iv[4] == 1.0:
        matched_factors.append("fuochi_artificiali")
    return HistoricalMatch(
        incident_id=best_match.id,
        incident_name=best_match.name,
        similarity_score=round(best_score, 3),
        matched_factors=matched_factors,
    )


def _build_recommendations(
    event: EventInput,
    density_analysis: DensityAnalysis,
    bottleneck_analyses: list[BottleneckAnalysis],
    global_score: float,
) -> list[Recommendation]:
    recs: list[Recommendation] = []
    if density_analysis.persons_per_sqm >= DENSITY_LOS_E:
        max_safe = int(event.venue.area_sqm * DENSITY_LOS_D)
        recs.append(Recommendation(
            priority="CRITICA",
            code="REC-CAP-01",
            message=(
                f"Densità prevista {density_analysis.persons_per_sqm} p/m² supera "
                f"soglia Fruin LoS E ({DENSITY_LOS_E} p/m²). "
                f"Si suggerisce di valutare riduzione a max {max_safe} presenze "
                f"o espansione area evento."
            ),
            action_type="CAPACITY_REDUCTION",
        ))
    elif density_analysis.persons_per_sqm >= DENSITY_LOS_D:
        recs.append(Recommendation(
            priority="ALTA",
            code="REC-CAP-02",
            message=(
                f"Densità {density_analysis.persons_per_sqm} p/m² — Fruin LoS D. "
                f"Si suggerisce sistema di contingentamento con counter fisici."
            ),
            action_type="CAPACITY_MONITORING",
        ))
    for bn in bottleneck_analyses:
        if bn.is_critical:
            recs.append(Recommendation(
                priority="ALTA",
                code=f"REC-BN-{bn.bottleneck_id}",
                message=bn.recommendation,
                action_type="FLOW_MANAGEMENT",
            ))
    if not event.has_safety_plan:
        recs.append(Recommendation(
            priority="CRITICA",
            code="REC-LEG-01",
            message=(
                "Nessun piano di sicurezza certificato risulta allegato. "
                "Si raccomanda il deposito in Prefettura prima dell'autorizzazione "
                "(D.M. 18/03/1996 e successive modifiche)."
            ),
            action_type="COMPLIANCE",
        ))
    if event.venue.escape_routes_obstructed > 0:
        recs.append(Recommendation(
            priority="CRITICA",
            code="REC-ESC-01",
            message=(
                f"{event.venue.escape_routes_obstructed}/"
                f"{event.venue.escape_routes_count} vie di fuga risultano ostruite. "
                f"Si raccomanda rimozione ostruzioni prima dell'apertura."
            ),
            action_type="EVACUATION",
        ))
    if event.modifiers.temperature_c > 28 and event.modifiers.humidity_percent > 65:
        recs.append(Recommendation(
            priority="ALTA",
            code="REC-MED-01",
            message=(
                f"Heat index elevato (T={event.modifiers.temperature_c}°C, "
                f"U={event.modifiers.humidity_percent}%). "
                f"Si suggerisce min. 3 punti idratazione e 1 unità medica dedicata."
            ),
            action_type="MEDICAL_PREPAREDNESS",
        ))
    if event.modifiers.fireworks_planned and density_analysis.persons_per_sqm >= DENSITY_LOS_C:
        recs.append(Recommendation(
            priority="ALTA",
            code="REC-FUO-01",
            message=(
                "Fuochi artificiali pianificati con densità ≥ LoS C. "
                "Si suggerisce zona buffer di 50m con barriere fisiche permeabili."
            ),
            action_type="BARRIER_MANAGEMENT",
        ))
    priority_order = {"CRITICA": 0, "ALTA": 1, "MEDIA": 2, "BASSA": 3}
    recs.sort(key=lambda r: priority_order.get(r.priority, 9))
    return recs


def _score_to_level(score: float) -> tuple[RiskLevel, RiskColor]:
    if score < 0.25:
        return RiskLevel.BASSO, RiskColor.BASSO
    elif score < 0.50:
        return RiskLevel.MEDIO, RiskColor.MEDIO
    elif score < 0.70:
        return RiskLevel.ALTO, RiskColor.ALTO
    elif score < 0.85:
        return RiskLevel.CRITICO, RiskColor.CRITICO
    else:
        return RiskLevel.EMERGENZA, RiskColor.EMERGENZA


# ---------------------------------------------------------------------------
# ENTRY POINT PUBBLICO
# ---------------------------------------------------------------------------

def calculate_risk(event: EventInput) -> RiskAssessment:
    """
    Calcola il rischio crowd crush per un evento pianificato.
    Entry point principale del Safety Engine — Scenario A.

    BLOCCO OSM: se osm_area_sqm > 0 e differisce > 15% dal dato
    dichiarato, solleva DataInconsistencyError prima di qualsiasi calcolo.
    """
    # --- 0. Validazione OSM obbligatoria — blocca su dato inconsistente ---
    osm_validation = []
    if event.osm_area_sqm > 0:
        osm_validation = validate_venue_geometry(
            event.venue,
            osm_area_sqm=event.osm_area_sqm,
        )

    # --- 1. Density Score ---
    density_analysis = _analyze_density(event)
    density = density_analysis.persons_per_sqm
    density_score = min(density / DENSITY_LOS_F, 1.0)

    # --- 2. Bottleneck Score ---
    bottleneck_analyses = _analyze_bottlenecks(event)
    if bottleneck_analyses:
        critical_count = sum(1 for b in bottleneck_analyses if b.is_critical)
        max_clear_time = max(b.time_to_clear_min for b in bottleneck_analyses)
        bottleneck_score = min(
            (critical_count / max(len(bottleneck_analyses), 1)) * 0.6
            + min(max_clear_time / 30, 1.0) * 0.4,
            1.0
        )
    else:
        bottleneck_score = 0.0

    # --- 3. Historical Similarity Score ---
    historical_match = _find_historical_match(event, density)
    historical_score = historical_match.similarity_score * 0.8 if historical_match else 0.0

    # --- 4. Modifier Score ---
    modifier_factor = event.modifiers.composite_modifier()
    modifier_score = min((modifier_factor - 1.0) / 0.55, 1.0)

    # --- 5. Score Composito ---
    base_score = (
        density_score    * WEIGHT_DENSITY
        + bottleneck_score * WEIGHT_BOTTLENECK
        + historical_score * WEIGHT_HISTORICAL
        + modifier_score   * WEIGHT_MODIFIERS
    )
    final_score = min(base_score * modifier_factor, 1.0)

    # --- 6. Confidence ---
    confidence = 0.65
    if event.venue.bottlenecks:
        confidence += 0.10
    if historical_match and historical_match.similarity_score > 0.7:
        confidence += 0.10
    if event.venue.area_sqm > 0 and event.expected_attendance > 0:
        confidence += 0.05
    if osm_validation:
        confidence += 0.05
    confidence = min(round(confidence, 2), 0.95)

    risk_level, risk_color = _score_to_level(final_score)
    recommendations = _build_recommendations(
        event, density_analysis, bottleneck_analyses, final_score
    )

    return RiskAssessment(
        event_id=event.event_id,
        event_name=event.event_name,
        global_score=round(final_score, 3),
        risk_level=risk_level,
        risk_color=risk_color.value,
        confidence=confidence,
        density_analysis=density_analysis,
        bottleneck_analyses=bottleneck_analyses,
        historical_match=historical_match,
        recommendations=recommendations,
        modifier_factor=round(modifier_factor, 3),
        osm_validation=osm_validation,
    )
