# Calendario Liturgico Cistercense
> Riferimento per seed di tipo heritage/abbazia — cluster LAZ-02 Monti Lepini

## Scopo
Questo file mappa le ricorrenze liturgiche rilevanti per l'Abbazia di Valvisciolo 
e il calendario cistercense. Usato per compilare il campo `connessione_liturgica` 
nei seed di tipo `festa_religiosa`.

## Primo semestre 2025

| Data | Ricorrenza | Rilevanza cistercense |
|------|-----------|----------------------|
| 6 Gen | Epifania del Signore | Chiusura ciclo natalizio |
| 12 Gen | Battesimo del Signore | Chiusura tempo natalizio |
| 5 Mar | Mercoledì delle Ceneri | Inizio Quaresima — ciclo penitenziale |
| 9 Mar | I Domenica di Quaresima | |
| 16 Mar | II Domenica di Quaresima | |
| 23 Mar | III Domenica di Quaresima | |
| 30 Mar | IV Domenica di Quaresima | |
| 13 Apr | Domenica delle Palme | Inizio Settimana Santa |
| 18 Apr | Venerdì Santo | |
| 20 Apr | Pasqua | Solennità principale |
| 21 Apr | Lunedì dell'Angelo | |
| 29 Mag | Ascensione | Festa liturgica |
| 8 Giu | Pentecoste | |
| 15 Giu | SS. Trinità | |
| 22 Giu | Corpus Domini | Processioni, eventi comunitari monastici |
| 27 Giu | Sacro Cuore di Gesù | Devozione cistercense |

## Secondo semestre 2025

| Data | Ricorrenza | Rilevanza cistercense |
|------|-----------|----------------------|
| 15 Ago | Assunzione B.V. Maria | Festa mariana principale — ordine cistercense |
| 8 Set | Natività B.V. Maria | Ricorrenza mariana |
| 4 Ott | S. Francesco d'Assisi | Feste patronali area Monti Lepini |
| 1 Nov | Ognissanti | Commemorazione liturgica |
| 21 Nov | Presentazione B.V. Maria | Calendario monastico cistercense |
| 8 Dic | Immacolata Concezione | Solennità cistercense — aperture straordinarie |
| 25 Dic | Natale del Signore | Ciclo natalizio |

## Utilizzo nei seed

Nel campo `connessione_liturgica` di ogni seed, riferirsi alle date di questa 
tabella. Esempio:
connessione_liturgica: Assunzione B.V. Maria (15 Ago) — festa cistercense principale
## Integrazione Dynamic Island

Queste date sono i trigger consigliati per push notifiche via APNs 
(ActivityKit + pushType: .token) senza App Store review.
Ogni ricorrenza può attivare un aggiornamento del ContentState 
con contenuto tematico stagionale.
## Primo semestre 2026

| Data | Ricorrenza | Rilevanza cistercense |
|------|-----------|----------------------|
| 6 Gen | Epifania del Signore | Chiusura ciclo natalizio |
| 11 Gen | Battesimo del Signore | Chiusura tempo natalizio |
| 18 Feb | Mercoledì delle Ceneri | Inizio Quaresima — ciclo penitenziale |
| 1 Mar | II Domenica di Quaresima | |
| 8 Mar | III Domenica di Quaresima | |
| 15 Mar | IV Domenica di Quaresima | |
| 22 Mar | V Domenica di Quaresima | |
| 29 Mar | Domenica delle Palme | Inizio Settimana Santa |
| 3 Apr | Venerdì Santo | |
| 5 Apr | Pasqua | Solennità principale |
| 6 Apr | Lunedì dell'Angelo | |
| 25 Apr | Liberazione | Ponte — eventi culturali |
| 14 Mag | Ascensione | Festa liturgica |
| 24 Mag | Pentecoste | |
| 31 Mag | SS. Trinità | |
| 7 Giu | Corpus Domini | Processioni, eventi comunitari monastici |
| 12 Giu | Sacro Cuore di Gesù | Devozione cistercense |
| 2 Giu | Festa della Repubblica | Ponte — eventi heritage |
