# ARCHITECTURE-DESIGN

## Overview
BodyVision è composto da frontend (Next.js + Shadcn/UI), backend (FastAPI + Strawberry GraphQL), motore di elaborazione immagini e uno storage esterno (Supabase Object Storage). L'obiettivo è valutare la composizione corporea da fotografie standardizzate, mantenendo disaccoppiamento tra acquisizione, archiviazione ed elaborazione.

Il frontend gestisce la cattura delle immagini via fotocamera browser, effettua l'upload su un bucket dedicato su Supabase e comunica al backend solo le URL delle immagini. Il backend recupera le immagini direttamente dallo storage, eseguendo inferenza e generando i risultati.

## Componenti
- **Frontend Web (Next.js)**: acquisizione immagini, guida pose, upload su Supabase.
- **Supabase Storage**: archivio immagini raw e risultati derivati.
- **Backend API (FastAPI + Strawberry GraphQL)**:
  - REST per azioni (acquisizione, processing, export).
  - GraphQL per consultare misurazioni, storico, report.
- **Inference Engine (Python + PyTorch)**:
  - Estrazione pose e contorni.
  - Fitting modello corporeo (feature flag per modello utilizzato).
  - Stima misurazioni e metriche.
- **Database (PostgreSQL - Supabase)**: metadati, sessioni, risultati.

## Feature Flag Modelli
Il componente "Body Model Provider" è astratto e consente la selezione runtime di uno tra tre modelli parametrici tramite variabile d'ambiente:
```
BODYVISION_MODEL = smplx | star | ghum
```

## Diagramma Architetturale (ASCII)
```
[Browser / Frontend]
   |  cattura foto
   v
[Supabase Storage] <---------> [PostgreSQL]
   ^                              ^
   | URL immagini                 |
   |                              |
[Backend API (REST/GraphQL)] ---->
   |
   | scarica immagini
   v
[Inference Engine]
   |
   v
[Risultati -> Storage + Database]
```

## Sequence Diagram (Acquisizione & Processamento)
```
Utente -> Frontend: acquisisce foto
Frontend -> Supabase: upload file
Frontend -> Backend REST: invia URL immagini
Backend -> Supabase: scarica file
Backend -> Inference Engine: esegue analisi
Inference Engine -> Database: salva misurazioni
Inference Engine -> Storage: salva asset derivati (mesh/report)
Backend -> Frontend: conferma completamento
```

## Deployment (Docker)
Ogni componente è containerizzato:
- `frontend`: Next.js server
- `backend`: FastAPI + Strawberry
- `inference`: worker dedicato PyTorch
- `db`: gestito da Supabase (esterno)
- `storage`: Supabase bucket (esterno)

## Performance e Scalabilità
- Worker separato per inferenza (non blocca API)
- GPU opzionale, fallback CPU
- Pre-caching modelli al bootstrap
- Elaborazione asincrona tramite job queue
- Frontend statico distribuibile su CDN

## Sicurezza
- Backend riceve solo URL firmati
- Accesso storage regolato tramite policy Supabase
- Nessuna immagine sensibile salvata localmente

