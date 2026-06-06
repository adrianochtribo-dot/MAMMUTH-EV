"""
MAMMUTH•EVENTS™ — Safety Engine
Module: risk_calculator.py
Scenario: A (Deterministico)
Version: 1.0.0
Author: KREATIO UNIVERSAL SYSTEM™

Implementa la valutazione deterministica del rischio crowd crush
basata sugli standard internazionali di John J. Fruin (Pedestrian
Planning and Design, 1971) e SFPE Handbook of Fire Protection Engineering.

Filosofia: INFORMARE, CONSIGLIARE, MITIGARE — mai vietare o censurare.
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

# Soglie densità (persone/m²) — Fruin Level of Service (LoS)
DENSITY_LOS_A = 0.5    # LoS A: libera circolazione, comfort massimo
DENSITY_LOS_B = 1.0    # LoS B: movimento agevole
DENSITY_LOS_C = 2.0    # LoS C: movimento limitato — ATTENZIONE
DENSITY_LOS_D = 3.0    # LoS D: contatto fisico frequente — ALLERTA
DENSITY_LOS_E = 4.0    # LoS E: immobilità parziale — CRITICO
DENSITY_LOS_F = 6.0    # LoS F: pressione fisica — EMERGENZA (Piazza San Carlo: 6.2)

# Capacità deflusso standard (persone/metro/minuto) — UK Guide to Safety at Sports Grounds
FLOW_RATE_NORMAL = 82        # p/m/min — flusso normale in corridoio
FLOW_RATE_BOTTLENECK = 60    # p/m/min — riduzione in strozzatura
FLOW_RATE_PANIC = 25         # p/m/min — flusso in panico (crowd crush imminente)

# Pesi per il calcolo del risk score composito (somma = 1.0)
WEIGHT_DENSITY = 0.40
WEIGHT_BOTTLENECK = 0.30
WEIGHT_HISTORICAL = 0.20
WEIGHT_MODIFIERS = 0.10


# ---------------------------------------------------------------------------
# ENUMERAZIONI
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    BASSO    = "BASSO"
    MEDIO    = "MEDIO"
    ALTO     = "ALTO"
    CRITICO  = "CRITICO"
    EMERGENZA = "EMERGENZA"


class RiskColor(str, Enum):
    BASSO    = "#2ECC71"   # verde
    MEDIO    = "#F39C12"   # arancio
    ALTO     = "#E67E22"   # arancio scuro
    CRITICO  = "#E74C3C"   # rosso
    EMERGENZA = "#8E1A0E"  # rosso scuro


# ---------------------------------------------------------------------------
# DATACLASS DI INPUT
# ---------------------------------------------------------------------------

@dataclass
class Bottleneck:
    """Rappresenta un collo di bottiglia geometrico nell'area evento."""
    id: str
    label: str
    width_m: float                      # larghezza netta in metri
    is_bidirectional: bool = False      # flusso bidirezionale?
    is_obstructed: bool = False         # ostruzione prevista/rilevata?

    def effective_flow_rate(self) -> float:
        """
        Calcola la portata effettiva in persone/minuto.
        Dimezza se bidirezionale (controflusso = fattore critico).
        """
        base = self.width_m * FLOW_RATE_BOTTLENECK
        if self.is_bidirectional:
            base *= 0.5
        if self.is_obstructed:
            base *= 0.4
        return base


@dataclass
class EventModifiers:
    """Fattori contestuali che amplificano il rischio base."""
    alcohol_expected: bool = False
    fireworks_planned: bool = False
    live_music: bool = False
    low_lighting: bool = False
    no_safety_plan: bool = False
    mobility_impaired_percent: float = 0.0   # % pubblico a mobilità ridotta
    temperature_c: float = 20.0
    humidity_percent: float = 50.0

    def composite_modifier(self) -> float:
        """
        Restituisce un moltiplicatore [1.0 — 1.55] da applicare al score base.
        Calibrato su analisi post-incidente Piazza San Carlo + letteratura SFPE.
        """
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

        # Stress termico — heat index semplificato
        if self.temperature_c > 28 and self.humidity_percent > 65:
            modifier += 0.10
        elif self.temperature_c > 32:
            modifier += 0.08

        return min(modifier, 1.55)   # cap al 55% di amplificazione


@dataclass
class HistoricalIncident:
    """
    Vettore di features di un incidente storico verificato.
    Usato per Cosine Similarity matching.
    """
    id: str
    name: str
    # Feature vector: [densità_picco, n_bottleneck, area_chiusa, alcol, fuochi]
    feature_vector: list[float]
    risk_score_retrospective: float     # score 0.0–1.0 calcolato ex-post


@dataclass
class VenueGeometry:
    """Geometria certificata dell'area evento."""
    name: str
    area_sqm: float
    bottlenecks: list[Bottleneck] = field(default_factory=list)
    is_enclosed: bool = True            # area chiusa (piazza con imbuti)?
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


# ---------------------------------------------------------------------------
# DATACLASS DI OUTPUT
# ---------------------------------------------------------------------------

@dataclass
class DensityAnalysis:
    persons_per_sqm: float
    los_label: str                  # Fruin Level of Service (A–F)
    threshold_margin_percent: float
    status: str
    projected_peak_risk: bool


@dataclass
class BottleneckAnalysis:
    bottleneck_id: str
    label: str
    effective_flow_ppm: float       # persone/minuto
    time_to_clear_min: float        # minuti per evacuare l'intera folla
    is_critical: bool
    recommendation: str


@dataclass
class HistoricalMatch:
    incident_id: str
    incident_name: str
    similarity_score: float         # 0.0–1.0
    matched_factors: list[str]


@dataclass
class Recommendation:
    priority: str                   # CRITICA / ALTA / MEDIA / BASSA
    code: str
    message: str
    action_type: str


@dataclass
class RiskAssessment:
    """Output strutturato completo della valutazione Scenario A."""
    event_id: str
    event_name: str
    global_score: float             # 0.0–1.0
    risk_level: RiskLevel
    risk_color: RiskColor
    confidence: float               # 0.0–1.0
    density_analysis: DensityAnalysis
    bottleneck_analyses: list[BottleneckAnalysis]
    historical_match: Optional[HistoricalMatch]
    recommendations: list[Recommendation]
    modifier_factor: float
    legal_disclaimer: str = (
        "Output a carattere esclusivamente informativo e consultivo. "
        "Non sostituisce la valutazione di un tecnico della sicurezza "
        "certificato (RSPP) né l'autorizzazione prefettizia."
    )


# ---------------------------------------------------------------------------
# DATABASE STORICO SEED — Scenario A (subset verificato)
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
                f"CRITICO: '{bn.label}' — deflusso stimato {round(time_to_clear, 1)} min "
                f"per {event.expected_attendance} persone. "
                f"Imporre senso unico o ampliare a ≥{math.ceil(bn.width_m * 1.5)}m."
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
                f"la soglia critica Fruin LoS E ({DENSITY_LOS_E} p/m²). "
                f"Ridurre il contingentamento a max {max_safe} presenze "
                f"o espandere l'area evento."
            ),
            action_type="CAPACITY_REDUCTION",
        ))
    elif density_analysis.persons_per_sqm >= DENSITY_LOS_D:
        recs.append(Recommendation(
            priority="ALTA",
            code="REC-CAP-02",
            message=(
                f"Densità {density_analysis.persons_per_sqm} p/m² — Fruin LoS D. "
                f"Istituire sistema di contingentamento con counter fisici agli ingressi."
            ),
            action_type="CAPACITY_MONITORING",
        ))
    for bn in bottleneck_analyses:
        if bn.is_critical:
            recs.append(Recommendation(
                priority="CRITICA",
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
                "L'evento non è autorizzabile senza deposito in Prefettura "
                "(D.M. 18/03/1996 e successive modifiche)."
            ),
            action_type="COMPLIANCE",
        ))
    obstructed = event.venue.escape_routes_obstructed
    total = event.venue.escape_routes_count
    if obstructed > 0:
        recs.append(Recommendation(
            priority="CRITICA",
            code="REC-ESC-01",
            message=(
                f"{obstructed}/{total} vie di fuga risultano ostruite. "
                f"Rimozione ostruzioni obbligatoria prima dell'apertura."
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
                f"Prevedere min. 3 punti idratazione gratuita e 1 unità medica dedicata."
            ),
            action_type="MEDICAL_PREPAREDNESS",
        ))
    if event.modifiers.fireworks_planned and density_analysis.persons_per_sqm >= DENSITY_LOS_C:
        recs.append(Recommendation(
            priority="ALTA",
            code="REC-FUO-01",
            message=(
                "Fuochi artificiali pianificati con densità ≥ LoS C. "
                "Istituire zona buffer di 50m attorno al punto di lancio "
                "con barriere fisiche permeabili."
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
    """
    density_analysis = _analyze_density(event)
    density = density_analysis.persons_per_sqm
    density_score = min(density / DENSITY_LOS_F, 1.0)

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

    historical_match = _find_historical_match(event, density)
    if historical_match:
        historical_score = historical_match.similarity_score * 0.8
    else:
        historical_score = 0.0

    modifier_factor = event.modifiers.composite_modifier()
    modifier_score = min((modifier_factor - 1.0) / 0.55, 1.0)

    base_score = (
        density_score    * WEIGHT_DENSITY
        + bottleneck_score * WEIGHT_BOTTLENECK
        + historical_score * WEIGHT_HISTORICAL
        + modifier_score   * WEIGHT_MODIFIERS
    )

    final_score = min(base_score * modifier_factor, 1.0)

    confidence = 0.65
    if event.venue.bottlenecks:
        confidence += 0.10
    if historical_match and historical_match.similarity_score > 0.7:
        confidence += 0.10
    if event.venue.area_sqm > 0 and event.expected_attendance > 0:
        confidence += 0.05
    confidence = min(round(confidence, 2), 0.90)

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
    )
