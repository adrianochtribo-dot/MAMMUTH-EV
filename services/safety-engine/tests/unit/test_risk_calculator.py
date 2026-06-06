"""
MAMMUTH•EVENTS™ — Safety Engine
Module: tests/unit/test_risk_calculator.py
Version: 1.0.0

Unit test per il modulo risk_calculator.py — Scenario A Deterministico.
Calibrati su incidenti storici verificati (Piazza San Carlo 2017).

Run: pytest tests/unit/test_risk_calculator.py -v
"""

import pytest
from core.risk_calculator import (
    Bottleneck,
    EventInput,
    EventModifiers,
    VenueGeometry,
    RiskLevel,
    calculate_risk,
    _analyze_density,
    _analyze_bottlenecks,
    _cosine_similarity,
    _find_historical_match,
    _score_to_level,
    DENSITY_LOS_C,
    DENSITY_LOS_D,
    DENSITY_LOS_E,
    DENSITY_LOS_F,
)


# ---------------------------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------------------------

@pytest.fixture
def sermoneta_safe() -> EventInput:
    """Evento a basso rischio — Sermoneta, piccola sagra."""
    return EventInput(
        event_id="TEST-LOW-001",
        event_name="Sagra del Carciofo — Sermoneta",
        expected_attendance=800,
        venue=VenueGeometry(
            name="Piazza del Comune, Sermoneta",
            area_sqm=1200,
            bottlenecks=[
                Bottleneck("BN-01", "Ingresso principale", width_m=8.0)
            ],
            is_enclosed=True,
            escape_routes_count=3,
            escape_routes_obstructed=0,
        ),
        modifiers=EventModifiers(temperature_c=22, humidity_percent=55),
        has_safety_plan=True,
    )


@pytest.fixture
def sermoneta_high_risk() -> EventInput:
    """Evento ad alto rischio — sovraffollamento + nessun piano sicurezza."""
    return EventInput(
        event_id="TEST-HIGH-001",
        event_name="Concerto Piazza — Sermoneta",
        expected_attendance=4500,
        venue=VenueGeometry(
            name="Piazza del Comune, Sermoneta",
            area_sqm=1200,
            bottlenecks=[
                Bottleneck("BN-01", "Vicolo nord — arco medievale",
                           width_m=3.2, is_bidirectional=True),
                Bottleneck("BN-02", "Uscita est — scalinata",
                           width_m=2.5, is_obstructed=True),
            ],
            is_enclosed=True,
            escape_routes_count=2,
            escape_routes_obstructed=1,
        ),
        modifiers=EventModifiers(
            alcohol_expected=True,
            live_music=True,
            fireworks_planned=True,
            temperature_c=31,
            humidity_percent=72,
            no_safety_plan=True,
        ),
        has_safety_plan=False,
    )


@pytest.fixture
def piazza_san_carlo_reconstruction() -> EventInput:
    """
    Ricostruzione parametrica di Piazza San Carlo 2017.
    Il sistema deve restituire score >= 0.80 (CRITICO/EMERGENZA).
    """
    return EventInput(
        event_id="TEST-PSC-2017",
        event_name="Champions League Final — Piazza San Carlo 2017",
        expected_attendance=30000,
        venue=VenueGeometry(
            name="Piazza San Carlo, Torino",
            area_sqm=19000,
            bottlenecks=[
                Bottleneck("BN-01", "Via Roma — ingresso nord",
                           width_m=14.0, is_bidirectional=True),
                Bottleneck("BN-02", "Portici lato ovest — colonnato",
                           width_m=6.0, is_bidirectional=False),
                Bottleneck("BN-03", "Via Carlo Alberto — uscita est",
                           width_m=9.0, is_bidirectional=True,
                           is_obstructed=True),
            ],
            is_enclosed=True,
            escape_routes_count=3,
            escape_routes_obstructed=1,
        ),
        modifiers=EventModifiers(
            alcohol_expected=True,
            temperature_c=24,
            humidity_percent=58,
            no_safety_plan=True,
        ),
        has_safety_plan=False,
    )


# ---------------------------------------------------------------------------
# TEST: DENSITY ANALYSIS
# ---------------------------------------------------------------------------

class TestDensityAnalysis:

    def test_low_density_los_a(self, sermoneta_safe):
        """800 persone / 1200m2 = 0.67 p/m2 — LoS A."""
        result = _analyze_density(sermoneta_safe)
        assert result.persons_per_sqm == pytest.approx(0.667, abs=0.01)
        assert "LoS A" in result.los_label
        assert result.projected_peak_risk is False

    def test_critical_density_los_d(self, sermoneta_high_risk):
        """4500 / 1200 = 3.75 p/m2 — LoS D, peak_risk=True."""
        result = _analyze_density(sermoneta_high_risk)
        assert result.persons_per_sqm == pytest.approx(3.75, abs=0.01)
        assert result.projected_peak_risk is True
        assert result.persons_per_sqm >= DENSITY_LOS_D

    def test_piazza_san_carlo_density(self, piazza_san_carlo_reconstruction):
        """30000 / 19000 = 1.578 p/m2."""
        result = _analyze_density(piazza_san_carlo_reconstruction)
        assert result.persons_per_sqm == pytest.approx(1.578, abs=0.01)

    def test_density_minimal_area(self):
        """Area minima non deve causare crash."""
        event = EventInput(
            event_id="ERR-001",
            event_name="Test",
            expected_attendance=100,
            venue=VenueGeometry(name="Test", area_sqm=0.001),
        )
        result = _analyze_density(event)
        assert result.persons_per_sqm > 0


# ---------------------------------------------------------------------------
# TEST: BOTTLENECK ANALYSIS
# ---------------------------------------------------------------------------

class TestBottleneckAnalysis:

    def test_no_bottlenecks_returns_empty(self, sermoneta_safe):
        """Venue senza bottleneck restituisce lista vuota."""
        sermoneta_safe.venue.bottlenecks = []
        result = _analyze_bottlenecks(sermoneta_safe)
        assert result == []

    def test_critical_bottleneck_obstructed(self, sermoneta_high_risk):
        """BN-02 ostruito deve essere marcato is_critical=True."""
        results = _analyze_bottlenecks(sermoneta_high_risk)
        bn02 = next(b for b in results if b.bottleneck_id == "BN-02")
        assert bn02.is_critical is True

    def test_bidirectional_halves_flow(self):
        """Flusso bidirezionale dimezza la portata effettiva."""
        bn_uni = Bottleneck("A", "Test", width_m=10.0, is_bidirectional=False)
        bn_bi  = Bottleneck("B", "Test", width_m=10.0, is_bidirectional=True)
        assert bn_bi.effective_flow_rate() == pytest.approx(
            bn_uni.effective_flow_rate() * 0.5, rel=0.01
        )

    def test_obstructed_reduces_flow(self):
        """Ostruzione riduce la portata al 40%."""
        bn_clear = Bottleneck("A", "Test", width_m=5.0, is_obstructed=False)
        bn_obstr = Bottleneck("B", "Test", width_m=5.0, is_obstructed=True)
        assert bn_obstr.effective_flow_rate() == pytest.approx(
            bn_clear.effective_flow_rate() * 0.4, rel=0.01
        )

    def test_time_to_clear_calculation(self):
        """Verifica calcolo tempo di deflusso: 1800 / (5*60) = 6.0 min."""
        event = EventInput(
            event_id="T-001",
            event_name="Test",
            expected_attendance=1800,
            venue=VenueGeometry(
                name="Test venue",
                area_sqm=2000,
                bottlenecks=[Bottleneck("BN-1", "Uscita", width_m=5.0)]
            ),
        )
        results = _analyze_bottlenecks(event)
        assert results[0].time_to_clear_min == pytest.approx(6.0, abs=0.1)


# ---------------------------------------------------------------------------
# TEST: COSINE SIMILARITY
# ---------------------------------------------------------------------------

class TestCosineSimilarity:

    def test_identical_vectors_score_one(self):
        v = [1.0, 2.0, 3.0, 4.0]
        assert _cosine_similarity(v, v) == pytest.approx(1.0, abs=0.001)

    def test_orthogonal_vectors_score_zero(self):
        assert _cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0, abs=0.001)

    def test_zero_vector_returns_zero(self):
        assert _cosine_similarity([0, 0, 0], [1, 2, 3]) == pytest.approx(0.0)

    def test_similarity_always_in_range(self):
        """La similarity deve essere sempre in [0, 1]."""
        import random
        for _ in range(50):
            v1 = [random.uniform(0, 10) for _ in range(5)]
            v2 = [random.uniform(0, 10) for _ in range(5)]
            score = _cosine_similarity(v1, v2)
            assert 0.0 <= score <= 1.0


# ---------------------------------------------------------------------------
# TEST: HISTORICAL MATCHING
# ---------------------------------------------------------------------------

class TestHistoricalMatching:

    def test_piazza_san_carlo_matches(self, piazza_san_carlo_reconstruction):
        """Evento simile a PSC 2017 deve matchare con score > 0.7."""
        density = 30000 / 19000
        match = _find_historical_match(piazza_san_carlo_reconstruction, density)
        assert match is not None
        assert match.similarity_score > 0.7

    def test_low_risk_event_weak_match(self, sermoneta_safe):
        """Evento a bassa densità deve avere match debole o assente."""
        density = 800 / 1200
        match = _find_historical_match(sermoneta_safe, density)
        if match:
            assert match.similarity_score < 0.8

    def test_match_has_factors_list(self, sermoneta_high_risk):
        """Se matcha, matched_factors deve essere una lista."""
        density = 4500 / 1200
        match = _find_historical_match(sermoneta_high_risk, density)
        if match:
            assert isinstance(match.matched_factors, list)


# ---------------------------------------------------------------------------
# TEST: RISK SCORE — INTEGRAZIONE
# ---------------------------------------------------------------------------

class TestCalculateRisk:

    def test_safe_event_low_score(self, sermoneta_safe):
        """Evento sicuro deve restituire score < 0.40."""
        result = calculate_risk(sermoneta_safe)
        assert result.global_score < 0.40
        assert result.risk_level in (RiskLevel.BASSO, RiskLevel.MEDIO)

    def test_high_risk_event_high_score(self, sermoneta_high_risk):
        """Evento ad alto rischio deve restituire score >= 0.65."""
        result = calculate_risk(sermoneta_high_risk)
        assert result.global_score >= 0.65
        assert result.risk_level in (
            RiskLevel.ALTO, RiskLevel.CRITICO, RiskLevel.EMERGENZA
        )

    def test_piazza_san_carlo_calibration(self, piazza_san_carlo_reconstruction):
        """
        TEST DI CALIBRAZIONE RETROSPETTIVA — CRITICO.
        PSC 2017 deve restituire score >= 0.80.
        Se fallisce: ricalibrate i pesi in risk_calculator.py.
        """
        result = calculate_risk(piazza_san_carlo_reconstruction)
        assert result.global_score >= 0.80, (
            f"CALIBRATION FAILURE: PSC 2017 score={result.global_score:.3f} < 0.80. "
            f"Ricalibrate WEIGHT_* o soglie densita in constants."
        )

    def test_score_always_in_range(self, sermoneta_safe, sermoneta_high_risk):
        """Score sempre in [0.0, 1.0]."""
        for event in [sermoneta_safe, sermoneta_high_risk]:
            result = calculate_risk(event)
            assert 0.0 <= result.global_score <= 1.0

    def test_confidence_always_in_range(self, sermoneta_high_risk):
        """Confidence sempre in [0.0, 1.0]."""
        result = calculate_risk(sermoneta_high_risk)
        assert 0.0 <= result.confidence <= 1.0

    def test_no_safety_plan_triggers_compliance_rec(self, sermoneta_high_risk):
        """Assenza piano sicurezza genera raccomandazione REC-LEG-01."""
        result = calculate_risk(sermoneta_high_risk)
        codes = [r.code for r in result.recommendations]
        assert "REC-LEG-01" in codes

    def test_critical_bottleneck_triggers_recommendation(self, sermoneta_high_risk):
        """Bottleneck critico genera almeno una raccomandazione CRITICA."""
        result = calculate_risk(sermoneta_high_risk)
        critical = [r for r in result.recommendations if r.priority == "CRITICA"]
        assert len(critical) >= 1

    def test_heat_index_triggers_medical_rec(self):
        """T=31 + U=72 genera raccomandazione REC-MED-01."""
        event = EventInput(
            event_id="TEST-HEAT-001",
            event_name="Evento Estivo",
            expected_attendance=2000,
            venue=VenueGeometry(name="Piazza Test", area_sqm=3000),
            modifiers=EventModifiers(temperature_c=31, humidity_percent=72),
        )
        result = calculate_risk(event)
        codes = [r.code for r in result.recommendations]
        assert "REC-MED-01" in codes

    def test_modifiers_amplify_score(self):
        """Score con modificatori massimi deve superare score base."""
        base = EventInput(
            event_id="BASE-001",
            event_name="Base",
            expected_attendance=3000,
            venue=VenueGeometry(name="Piazza", area_sqm=1000),
            modifiers=EventModifiers(),
        )
        amplified = EventInput(
            event_id="AMP-001",
            event_name="Amplified",
            expected_attendance=3000,
            venue=VenueGeometry(name="Piazza", area_sqm=1000),
            modifiers=EventModifiers(
                alcohol_expected=True,
                fireworks_planned=True,
                low_lighting=True,
                no_safety_plan=True,
                temperature_c=33,
                humidity_percent=80,
            ),
        )
        assert calculate_risk(amplified).global_score > calculate_risk(base).global_score

    def test_score_to_level_boundaries(self):
        """Mapping score -> livello corretto per tutti i range."""
        assert _score_to_level(0.10)[0] == RiskLevel.BASSO
        assert _score_to_level(0.35)[0] == RiskLevel.MEDIO
        assert _score_to_level(0.60)[0] == RiskLevel.ALTO
        assert _score_to_level(0.75)[0] == RiskLevel.CRITICO
        assert _score_to_level(0.90)[0] == RiskLevel.EMERGENZA

    def test_legal_disclaimer_present(self, sermoneta_safe):
        """Il disclaimer legale deve essere sempre presente nell'output."""
        result = calculate_risk(sermoneta_safe)
        assert len(result.legal_disclaimer) > 20
        assert "informativo" in result.legal_disclaimer
