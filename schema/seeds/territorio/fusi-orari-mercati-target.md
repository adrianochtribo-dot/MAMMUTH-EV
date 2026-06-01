# Fusi Orari — Mercati Target MAMMUTH•EVENTS™
> Riferimento per timing push APNs e campagne crowdfunding 
> nei mercati europei e internazionali.

## Mercati target — offset GMT

| Paese | GMT offset | Note |
|-------|-----------|------|
| Italia | +1 | Base operativa MAMMUTH |
| Francia | +1 | Stesso fuso IT |
| Germania | +1 | Stesso fuso IT |
| Austria | +1 | Stesso fuso IT |
| Spagna | +1 | Stesso fuso IT |
| Svizzera | +1 | Stesso fuso IT |
| Lussemburgo | +1 | Stesso fuso IT |
| Paesi Bassi | +1 | Stesso fuso IT |
| Belgio | +1 | Stesso fuso IT |
| Gran Bretagna | GMT | -1h rispetto IT |
| Irlanda | GMT | -1h rispetto IT |
| Portogallo | GMT | -1h rispetto IT |
| Grecia | +2 | +1h rispetto IT |
| Romania | +2 | +1h rispetto IT |
| Turchia | +2 | +1h rispetto IT |
| Stati Uniti (Est) | -5 | -6h rispetto IT |
| Stati Uniti (Ovest) | -10 | -11h rispetto IT |
| Canada (Est) | -3/-8 | variabile |
| Argentina | -3 | -4h rispetto IT |
| Brasile | -2/-5 | variabile |

## Finestre orarie ottimali per push APNs

Base: ora italiana (CET = GMT+1)

| Finestra IT | GB/PT | GR/RO | US Est | Descrizione |
|-------------|-------|--------|--------|-------------|
| 08:00 | 07:00 | 09:00 | 02:00 | Morning push Europa |
| 12:00 | 11:00 | 13:00 | 06:00 | Pausa pranzo Europa |
| 18:00 | 17:00 | 19:00 | 12:00 | Fine giornata Europa + pranzo US |
| 20:00 | 19:00 | 21:00 | 14:00 | Sera Europa — picco engagement |

## Regola operativa per MAMMUTH

**Push ottimale per mercato europeo unificato:**
- Orario IT consigliato: **18:00–20:00 CET**
- Copre simultaneamente: IT, FR, DE, AT, ES, CH, NL, BE
- GB/PT ricevono 17:00–19:00 (ottimale)
- Grecia riceve 19:00–21:00 (ottimale)

**Push per diaspora italiana USA:**
- Orario IT: **20:00 CET** → US Est 14:00, US Ovest 09:00

## Note per ActivityKit

Quando si pianificano aggiornamenti ContentState via APNs:
- Usare sempre timestamp UTC nel payload
- IT = UTC+1 (inverno) / UTC+2 (estate — ora legale)
- Ora legale IT 2025: inizio 30 Mar, fine 26 Ott
- Ora legale IT 2026: inizio 29 Mar, fine 25 Ott
