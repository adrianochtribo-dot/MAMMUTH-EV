# Temperature e Taglie Internazionali
> Riferimento per modulo predittivo abbigliamento eventi outdoor.
> La piattaforma suggerisce cosa indossare in base alla temperatura 
> prevista nel giorno dell'evento.

## Conversione Temperature

| Celsius | Fahrenheit | Réaumur | Kelvin |
|---------|-----------|---------|--------|
| -20 | -4 | -16 | 253 |
| -10 | 14 | -8 | 263 |
| 0 | 32 | 0 | 273 |
| 10 | 50 | 8 | 283 |
| 20 | 68 | 16 | 293 |
| 30 | 86 | 24 | 303 |
| 40 | 104 | 32 | 313 |

## Fasce di abbigliamento per eventi outdoor

| Temperatura (°C) | Fascia | Suggerimento abbigliamento |
|-----------------|--------|---------------------------|
| < 0 | ❄️ Gelido | Cappotto pesante, guanti, sciarpa |
| 0–10 | 🥶 Freddo | Cappotto, maglione pesante |
| 10–15 | 🧥 Fresco | Giacca, felpa |
| 15–20 | 🌤 Mite | Giacca leggera, maglietta |
| 20–25 | ☀️ Caldo | Maglietta, pantaloni leggeri |
| 25–30 | 🌞 Molto caldo | Abbigliamento estivo leggero |
| > 30 | 🔥 Caldo intenso | Abbigliamento minimal, protezione solare |

## Taglie Internazionali — Uomo

### Abiti e Soprabiti
| IT | GB | USA |
|----|-----|-----|
| 46 | 36 | 36 |
| 48 | 38 | 38 |
| 50 | 40 | 40 |
| 52 | 42 | 42 |
| 54 | 42 | 42 |
| 56 | 44 | 44 |

### Camicie
| IT | GB | USA |
|----|-----|-----|
| 36 | 14 | 14 |
| 37 | 14½ | 14½ |
| 38 | 15 | 15 |
| 39 | 15½ | 15½ |
| 40 | 16 | 16 |
| 41 | 16½ | 16½ |

### Scarpe Uomo
| IT | GB | USA |
|----|-----|-----|
| 40 | 7 | 7½ |
| 41 | 7½ | 8 |
| 42 | 8 | 8½ |
| 43 | 8½-9 | 9-9½ |
| 44 | 9½-10 | 10-10½ |
| 45 | 10½-11 | 11-11½ |

## Taglie Internazionali — Donna

### Abiti e Tailleur
| IT | GB | USA |
|----|-----|-----|
| 38 | 32 | 10 |
| 40 | 33 | 12 |
| 42 | 35 | 14 |
| 44 | 36 | 16 |
| 46 | 38 | 18 |
| 48 | 39 | 20 |

### Scarpe Donna
| IT | GB | USA |
|----|-----|-----|
| 36 | 4½ | 6 |
| 37 | 5 | 6½ |
| 38 | 6 | 7½ |
| 39 | 7 | 8½ |
| 40 | 7½ | 9 |
| 41 | 8 | 9½ |

## Utilizzo predittivo nella piattaforma

Per ogni evento seed con `data_o_periodo` definita:
1. Incrociare con dati `clima-mercati-target.md`
2. Determinare fascia temperatura prevista
3. Suggerire abbigliamento appropriato
4. Convertire taglie in base al mercato dell'utente (IT/GB/USA)

Esempio:
```
Evento: Sagra delle Fragole — Nemi (Mag-Giu)
Temperatura prevista: 18-22°C → fascia "Mite/Caldo"
Suggerimento: giacca leggera + maglietta
Taglia giacca utente IT 48 → GB 38 → USA 38
```
