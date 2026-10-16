# Piano full paper – Federated Cloud Continuum per Smart-City CPS (i-Cities 2026)

Oct 16, 2026 · @Fabio

## Obiettivo e contributi

Il full paper trasforma il position paper in un lavoro **architettura + validazione sperimentale**: i quattro principi diventano un'architettura di riferimento, un modello di experiment descriptor e una proof-of-concept misurata su un caso di **controllo adattivo del traffico urbano** distribuito nel continuum.

**Titolo di lavoro:** *Reproducible Smart-City CPS Experimentation over Federated Cloud Continuum Infrastructures: Architecture, Experiment Descriptors, and an Urban Traffic-Control Case Study*

Contributi da dichiarare in introduzione:

1. **Requisiti** (R1–R6) per la sperimentazione CPS smart-city nel continuum, ricavati dalle sez. II–III dell'abstract.
2. **Analisi comparativa** di testbed e framework esistenti rispetto ai requisiti, con una tabella che evidenzia il gap.
3. **Architettura di riferimento** a livelli, allineata al SLICES Cloud Continuum Blueprint, e un **modello di experiment descriptor** che cattura l'intent (topologia, placement, timing, workload, osservabilità, provenance).
4. **Proof-of-concept e valutazione** su un workload di controllo del traffico distribuito edge–fog–cloud: ripetibilità e sensibilità a placement e degrado di rete; costo dell'osservabilità solo come misura indicativa.

Requisiti proposti:

| ID | Requisito | Principio dell'abstract |
| --- | --- | --- |
| R1 | Separazione tra capability d'infrastruttura e logica applicativa | Separate layers |
| R2 | Intent sperimentale esplicito e versionato, non solo script | Reproducible programmability |
| R3 | Composizione di risorse eterogenee multi-sito senza nasconderne l'eterogeneità | Federation |
| R4 | Variazione controllata di placement, rete, capacità | Need for continuum |
| R5 | Osservabilità cross-layer con base temporale comune | Continuum-aware observability |
| R6 | Provenance e gestione dell'incertezza fisica tra run | Open directions |

## Scaletta (target 14 pagine CCIS, \~5.000–5.500 parole)

Figure, tabelle e listing occupano spazio: il conteggio parole tiene conto di questo. Circa il 70% del testo è nuovo rispetto all'abstract; le sez. 4.1 e 7 riusano e ampliano il materiale esistente.

1. **Introduction** (1,5 pp.)
   - Contesto: CPS smart-city distribuiti nel continuum (riuso sez. I).
   - Problema: sperimentazione frammentata e non riproducibile.
   - Contributi 1–4 e struttura del paper.
2. **Background and Motivation** (1,5 pp.)
   - Il continuum come parte della semantica CPS (riuso sez. II).
   - Tre fonti di frammentazione: interfacce, osservabilità, descrizione degli esperimenti (riuso sez. III).
   - Requisiti R1–R6 in tabella.
3. **Related Work** (2 pp.)
   - Testbed IoT/smart-city, testbed cloud/rete, framework di sperimentazione edge-to-cloud, simulatori, standard di provenance.
   - Tabella di confronto testbed × R1–R6, poi il gap in un paragrafo.
4. **Reference Architecture** (3 pp.)
   - 4.1 Principi di design (riuso sez. IV, ristretto).
   - 4.2 Livelli: federated resources, experiment control plane, observability plane, provenance/archival, workload layer.
   - 4.3 Mappatura sul SLICES Blueprint e sui servizi del nodo usato.
   - Figura architetturale dettagliata (evoluzione della Fig. 1).
5. **Experiment Descriptor Model** (1,5 pp.)
   - Schema e semantica dei campi; esempio compatto in listing.
   - Ciclo di vita: reservation → configuration → execution → measurement → provenance → archival.
   - Come il descriptor gestisce l'incertezza: condizioni controllate vs registrate (carico di fondo, RTT WAN reale, offset di clock).
6. **Case Study: Urban Traffic Control** (2,5 pp.)
   - Workload, testbed, scenari, metriche, risultati (2–3 grafici + 1 tabella).
7. **Discussion and Open Challenges** (1 p.)
   - Lezioni apprese, limiti (scala, una sola classe di workload misurata, domanda di traffico simulata), minacce alla validità. Future work dichiarato in modo esplicito: monitoraggio urbano con dati reali, digital twin con HPC, confronto con E2Clab/EnOSlib, federazione su più siti, rilascio pubblico del descriptor.
   - Open directions riformulate alla luce dei dati (riuso sez. VII).
8. **Conclusion** (0,5 pp.) + **References** (\~1,5 pp., 30–40 voci).

## Bozza experiment descriptor

Il descriptor separa ciò che l'infrastruttura offre (`infrastructure`) da ciò che l'esperimento fa (`application`), e distingue le condizioni **controllate** da quelle solo **registrate** (carico di fondo, latenza WAN reale, deriva di clock). Questa distinzione è il punto nuovo rispetto a TOSCA o ai file di E2Clab. Attenzione: la domanda di traffico in SUMO è simulata e quindi completamente controllata; la parte "registrata" riguarda le condizioni reali dell'infrastruttura, e il paper deve dirlo apertamente.

```yaml
experiment:
  id: traffic-placement-v1
  version: 1.0.0
  hypothesis: "Fog placement of state estimation reduces control-loop latency vs cloud"
  owner: unime-mdslab

infrastructure:            # R1, R3: capability, non tecnologie
  sites:
    - {id: edge-me,  tier: edge,  site: slices-it-messina, nodes: 4, arch: arm64}
    - {id: fog-me,   tier: fog,   site: slices-it-messina, nodes: 2, cpu: 16, mem: 32Gi}
    - {id: cloud-x,  tier: cloud, site: <secondo-sito-slices>, nodes: 2}
  links:
    - {from: edge-me, to: fog-me,  profile: lan}
    - {from: fog-me,  to: cloud-x, profile: wan}
  impairments:             # R4: variabili controllate
    wan: {delay_ms: [10, 50, 100], jitter_ms: 5, loss_pct: [0, 1]}

application:               # workload layer
  class: control-cps       # control | monitoring | digital-twin
  components:
    - {name: detector-gw,       placement: edge}    # flussi/code da SUMO (hardware-in-the-loop)
    - {name: state-estimator,   placement: [fog, cloud]}   # fattore sperimentale
    - {name: signal-controller, placement: fog}
    - {name: actuator,          placement: edge}    # cambio fase semaforica
  dataflows:
    - {from: detector-gw, to: state-estimator, rate_hz: 1}
  timing:
    control_period_s: 5
    deadline_ms: 500
  workload_profile: sumo-scenario-v1   # rete, domanda e seed versionati

observability:             # R5
  clock_sync: ptp          # o chrony; errore registrato
  metrics: [infra.cpu, net.rtt, app.e2e_latency, cps.avg_wait_time, cps.queue_length]
  traces: opentelemetry
  sampling_s: 1

conditions:                # R6: non controllate, solo registrate
  recorded: [background_load, wan_rtt_baseline, clock_offset]

execution:
  repetitions: 10
  duration_min: 30
  warmup_min: 5
  termination: {on: [duration, deadline_miss_rate > 0.2]}

provenance:                # R2, R6
  capture: [descriptor_hash, image_digests, node_inventory, impairment_log, sumo_seed]
  format: ro-crate
```

Da decidere: se implementare un piccolo parser/orchestratore proprio (YAML → risorse SLICES + Kubernetes/K3s + tc/netem + lancio SUMO) o estendere un tool esistente come EnOSlib/E2Clab. Per i tempi conviene un **thin layer proprio** sopra strumenti esistenti, citando gli altri come related work.

## Caso di studio: controllo adattivo del traffico, disegno sperimentale

Due domande di ricerca principali (RQ1, RQ2) con circa 85 run automatizzate; RQ3 resta come misura indicativa e la sua versione completa va alla rivista. Le domande servono a dimostrare l'infrastruttura, non a ottimizzare il controllo del traffico.

**Workload.** Pipeline di controllo: gateway di rilevamento (edge) → stima dello stato del traffico/code (fog o cloud) → controllore delle fasi semaforiche (fog) → comando di attuazione (edge). Il traffico è generato da uno scenario SUMO con rete, domanda e seed versionati, eseguito a velocità controllata e collegato ai nodi edge (hardware-in-the-loop).

| RQ | Domanda | Fattori variati | Metriche | Run |
| --- | --- | --- | --- | --- |
| RQ1 Ripetibilità (R2, R6) | Lo stesso descriptor produce risultati stabili su run ripetute, e su un secondo sito? | Nessuno; poi sito A vs sito B | Coefficiente di variazione di latenza e KPI CPS; intervalli di confidenza; deviazione tra siti | 10 × 2 siti |
| RQ2 Sensibilità al continuum (R4) | Quanto contano placement e rete per il comportamento CPS? | Placement dello state-estimator {fog, cloud} × ritardo WAN {10, 50, 100 ms} × perdita {0, 1%} | Latenza end-to-end del ciclo, deadline miss rate, tempo medio di attesa, lunghezza delle code | 12 config × 5 rip. |
| RQ3 Costo dell'osservabilità (R5), versione ridotta | Quanto costa l'osservabilità cross-layer e quanto è accurata? | Osservabilità {minima, completa}; NTP vs PTP rimandato alla rivista | Overhead CPU, rete e latenza; errore di sincronizzazione; completezza delle tracce | 2 config × 3 rip. |

Grafici previsti: box plot della latenza per configurazione (RQ1–RQ2), heatmap placement × ritardo sul deadline miss rate (RQ2), valore di overhead in tabella (RQ3). In più, una tabella di effort: righe di descriptor vs righe di script equivalenti, tempo di setup.

Risultato chiave da mostrare: lo **stesso codice applicativo** esibisce comportamento CPS diverso al variare delle sole condizioni di continuum, ed è il descriptor a renderlo ripetibile e confrontabile.

## Related work da coprire

Il gap da argomentare: i testbed coprono bene uno o due livelli del continuum, i framework edge-to-cloud automatizzano il deployment, ma nessuno tratta come artefatti di prima classe sia l'intent sperimentale sia le condizioni fisiche non controllabili (R2, R6). I riferimenti sotto vengono da memoria e vanno **verificati tutti** su DBLP o Google Scholar prima della citazione.

| Categoria | Lavori da citare (da verificare) | Cosa coprono | Cosa manca rispetto a R1–R6 |
| --- | --- | --- | --- |
| Testbed IoT/smart-city | SmartSantander (Sanchez et al., Computer Networks 2014); FIT IoT-LAB (Adjih et al., WF-IoT 2015) | Sensori reali su larga scala | Integrazione con cloud/HPC, intent sperimentale |
| Testbed cloud/rete | Chameleon (Keahey et al., USENIX ATC 2020); FABRIC (Baldin et al., IEEE Internet Computing 2019); Grid'5000; Fed4FIRE+ | Risorse programmabili, federazione | Semantica CPS, osservabilità fisica |
| Testbed wireless/edge | Colosseum (Bonati et al., 2021); EdgeNet (Şenel et al., 2021) | Emulazione RF, edge multi-tenant | Continuum completo, provenance |
| Federazione europea | SLICES Blueprint (Sabbioni et al., IFIP Networking 2025) + altri documenti SLICES | Reference model federato | È la base: il contributo è istanziarlo per i CPS |
| Framework edge-to-cloud | E2Clab (Rosendo et al., IEEE Cluster 2020); EnOSlib (Cherrueau et al., IEEE TCC 2022) | Deployment riproducibile, layer e servizi | Condizioni fisiche registrate, KPI CPS |
| Simulatori | iFogSim (Gupta et al., 2017); EdgeCloudSim; SUMO (Lopez et al., 2018) | Esplorazione rapida, simulazione del traffico | Realismo, eterogeneità reale |
| Orchestrazione/IoT cloud | Stack4Things (Longo et al.); TOSCA | Gestione dei dispositivi, modelli dichiarativi | Esperimento come artefatto |
| Riproducibilità e provenance | National Academies 2019; W3C PROV; RO-Crate (Soiland-Reyes et al., 2022); Popper | Modelli di provenance e packaging | Specializzazione per i CPS |
| Domain | Digital twin urbani (Li et al., 2021); controllo adattivo dei semafori e edge computing per ITS | Motivazione dei workload | — |

Da aggiungere: lavori recenti del gruppo (2024–2026) su SLICES-IT e sul cloud continuum, se pertinenti, e 2–3 survey sul computing continuum per dare ampiezza.

## Piano di lavoro

Il percorso critico è l'orchestratore: deve girare entro fine ottobre perché gli esperimenti si chiudano il 10 novembre e restino cinque giorni per i grafici prima della revisione interna.

&#91;embedded content: piano di lavoro · 5 settimane\]

- [ ] Compilare il Google Form entro Oct 28, 2026
- [ ] Confermare i siti SLICES (secondo sito per RQ1) e prenotare le risorse
- [ ] Definire lo scenario SUMO (rete, domanda, seed) e l'interfaccia hardware-in-the-loop con i nodi edge
- [ ] Scaricare il template Springer CCIS (LaTeX) e impostare il repository del paper
- [ ] Sottomettere entro Nov 20, 2026

## Roadmap verso la rivista

Il paper CCIS fissa architettura, descriptor e primi risultati; la versione su rivista Q1/Q2 (2027) aggiunge ampiezza sperimentale e conta per l'indicatore articoli dell'ASN, che invece non considera i conference paper.

| Contenuto | CCIS (20 nov 2026) | Rivista (2027) |
| --- | --- | --- |
| Requisiti R1–R6 e related work | Completi | Ampliati, con survey sistematica |
| Architettura di riferimento | Completa | Raffinata con le lezioni del CCIS |
| Experiment descriptor | Schema ed esempio | Schema formale, tool e dataset pubblici (RO-Crate) |
| Classi di workload misurate | 1 (controllo traffico) | 2–3 (+ monitoraggio ambientale urbano con dati reali, digital twin con HPC) |
| Federazione | 2 siti | 3+ siti, analisi dell'eterogeneità |
| RQ1 Ripetibilità | Sì | Sì, con test statistici |
| RQ2 Placement e rete | Sì | Sì, spazio dei fattori ampliato |
| RQ3 Osservabilità | Indicativa | Completa (NTP vs PTP, overhead, completezza) |
| Confronto con E2Clab/EnOSlib o script manuali | No | Sì: effort ed espressività |

Regole per la versione estesa:

- Citare il paper CCIS e dichiarare nella cover letter che si tratta di un'estensione.
- Garantire una quota sostanziale di contenuto nuovo: molte riviste chiedono almeno il 30–50%, ma va verificata la policy della rivista scelta.
- Riscrivere testo e figure riusate, senza copia diretta.

Riviste candidate, da confrontare su Scimago (quartile della categoria pertinente) e per tempi di revisione: *Future Generation Computer Systems*, *Computer Networks*, *Internet of Things* (Elsevier), *Journal of Grid Computing*, *Future Internet*, *IEEE Access*.
