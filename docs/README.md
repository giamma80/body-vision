# BodyVision

BodyVision è un sistema full-stack per la stima della composizione corporea tramite analisi di immagini standardizzate (fronte, lato, retro) o acquisizione da fotocamera in tempo reale.

## Obiettivo
- Guidare l’utente nell’assunzione di pose corrette.
- Estrarre struttura corporea tramite pose estimation.
- Approssimare volume, densità e body fat %.
- Generare una mesh 3D scaricabile.

## Input
- Tre foto: frontale, laterale, posteriore
- Metadati utente: altezza (cm), peso (kg), età, genere

## Output
- Body fat %
- Densità corporea
- Volume (litri)
- Mesh 3D scaricabile (.obj)

## Stack Tecnologico
- Backend: FastAPI + Python 3.11
- Worker: Dramatiq / Redis
- Modelli: SMPL-X / SMPL / GHUM / Light estimator
- Frontend: Next.js + Shadcn/UI (Radix + Tailwind)
- Storage: Supabase Object Storage
- Dependency management: uv
- Dev tools: black, ruff, mypy, pytest
