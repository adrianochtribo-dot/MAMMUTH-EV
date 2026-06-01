# Calendario Liturgico Cistercense
> Riferimento per seed di tipo heritage/abbazia — cluster LAZ-02 Monti Lepini

## Scopo
Questo file mappa le ricorrenze liturgiche rilevanti per l'Abbazia di Valvisciolo 
e il calendario cistercense. Usato per compilare il campo `connessione_liturgica` 
nei seed di tipo `festa_religiosa`.

## Primo semestre 2025

| Data | Ricorrenza | Rilevanza cistercense |
|------|-----------|----------------------|
| 5 Mar | Mercoledì delle Ceneri | Inizio Quaresima — apertura ciclo penitenziale |
| 20 Apr | Pasqua | Solennità principale |
| 29 Mag | Ascensione | Festa liturgica |
| 22 Giu | Corpus Domini | Processioni, eventi comunitari monastici |

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
