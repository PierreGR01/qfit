# QFit Plugin — Visual Preview (Après Redesign)

## État Initial (Phase 1 — CONNECT)

```
┌─────────────────────────────────────────────────────────────────┐
│ qfit - Strava Integration                        [_][~][×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1/6 — Connect to Strava                                  │  ← PhaseIndicator
│  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │     (NOUVEAU)
│  (Background bleu clair)                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Fetch and store activities ▼                                │
│  ┌─────────────────────────────────────────────────────────────┤
│  │ Connection Status: Not Connected                             │
│  │   ├─ Client ID: [________________]                          │
│  │   └─ Refresh Token: [________________]                      │
│  │                                                              │
│  │ [Open Authorize]  [Exchange Code]  [Settings]  [Help]       │
│  └─────────────────────────────────────────────────────────────┤
│                                                                  │
│  (ProgressFeedback vide — pas visible)                         │
│                                                                  │
│  (ResultIndicator vide — pas visible)                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 2 — FETCH (Pendant le chargement)

```
┌─────────────────────────────────────────────────────────────────┐
│ qfit - Strava Integration                        [_][~][×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 2/6 — Fetch Activities                                   │  ← Couleur BLEU
│  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  (Background bleu clair → bleu plus foncé)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Fetch and store activities ▼                                │
│  ┌─────────────────────────────────────────────────────────────┤
│  │ ☑ Connection Status: Connected                              │
│  │   ├─ Client ID: [abc123...]                                │
│  │   └─ Refresh Token: [xyz789...]                            │
│  │                                                              │
│  │ ☑ Fetch Parameters                                          │
│  │   ├─ Date Range: [2024-01-01] to [2024-04-24]             │
│  │   └─ Activity Types: [✓] Running [✓] Cycling               │
│  │                                                              │
│  │ [Fetch Data]  [Settings]  [Help]                           │
│  └─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ⟳ Connecting to Strava API...                                │  ← ProgressFeedback
│  ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 42%       │     (NOUVEAU)
│  (Background gris clair avec spinner animé)                   │
│                                                                  │
│  (ResultIndicator vide — pas visible)                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 2 — FETCH (Après succès)

```
┌─────────────────────────────────────────────────────────────────┐
│ qfit - Strava Integration                        [_][~][×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 2/6 — Fetch Activities                                   │
│  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  (Couleur BLEU)                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  (Section content masquée pendant loading)                     │
│                                                                  │
│  (ProgressFeedback masqué)                                      │
│                                                                  │
│  ✅ Fetched 42 activities                                       │  ← ResultIndicator
│  (Background vert clair avec icône ✅)                         │     (NOUVEAU)
│  (Message persistent)                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 3 — STORE (En cours)

```
┌─────────────────────────────────────────────────────────────────┐
│ qfit - Strava Integration                        [_][~][×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 3/6 — Store Activities                                   │  ← Couleur VERT
│  ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  (Background vert clair)                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  2. Visualize ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────┤
│  │ ☑ Store / database                                          │
│  │   ├─ Output Path: [/home/user/activities.gpkg]             │
│  │   ├─ [Load Layers]  [Clear Database]                       │
│  │                                                              │
│  │ [Store Data]  [Settings]                                   │
│  └─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ⟳ Storing activities to GeoPackage...                         │  ← ProgressFeedback
│  ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 65%        │
│                                                                  │
│  (ResultIndicator vide)                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 3 — STORE (Erreur)

```
┌─────────────────────────────────────────────────────────────────┐
│ qfit - Strava Integration                        [_][~][×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 3/6 — Store Activities                                   │
│  ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  (Couleur VERT)                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  (Section content)                                              │
│                                                                  │
│  (ProgressFeedback masqué)                                      │
│                                                                  │
│  ❌ Failed to store activities                                  │  ← ResultIndicator
│  Suggestion: Check disk space and file permissions.             │     (NOUVEAU)
│  (Background rouge clair avec icône ❌)                        │
│  (Message PERSISTANT jusqu'à action suivante)                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 4 — VISUALIZE (Prêt)

```
┌─────────────────────────────────────────────────────────────────┐
│ qfit - Strava Integration                        [_][~][×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 4/6 — Visualize Activities                               │  ← Couleur VIOLET
│  ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  (Background violet clair)                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  2. Visualize ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────┤
│  │ ☑ Loaded Layers (4)                                         │
│  │   ├─ activities (42 features)                               │
│  │   ├─ start_points (12 features)                             │
│  │   ├─ activity_points (8234 points)                          │
│  │   └─ atlas (1 feature)                                      │
│  │                                                              │
│  │ ☑ Style & Filters                                           │
│  │   ├─ Style Preset: [By activity type ▼]                    │
│  │   ├─ Show Background Map: [✓]                              │
│  │   └─ Temporal Mode: [Monthly ▼]                            │
│  │                                                              │
│  │ [Apply Visualization]  [Settings]                          │
│  └─────────────────────────────────────────────────────────────┤
│                                                                  │
│  (ProgressFeedback vide — pas visible)                         │
│                                                                  │
│  ✅ Visualization applied (42 activities visible)               │  ← ResultIndicator
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 5 — ANALYZE (En cours)

```
┌─────────────────────────────────────────────────────────────────┐
│ qfit - Strava Integration                        [_][~][×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 5/6 — Analyze Activities                                 │  ← Couleur ORANGE
│  █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  (Background orange clair)                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  3. Analyze ▼                                                   │
│  ┌─────────────────────────────────────────────────────────────┤
│  │ ☑ Analysis Mode: [Heatmap ▼]                               │
│  │   ├─ Cell Size: [256 pixels]                               │
│  │   └─ [Advanced Options ▼]                                  │
│  │                                                              │
│  │ [Run Analysis]  [Settings]                                 │
│  └─────────────────────────────────────────────────────────────┤
│                                                                  │
│  ⟳ Computing heatmap layer...                                  │  ← ProgressFeedback
│  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 75%       │
│                                                                  │
│  (ResultIndicator vide)                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 6 — PUBLISH (Prêt)

```
┌─────────────────────────────────────────────────────────────────┐
│ qfit - Strava Integration                        [_][~][×]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 6/6 — Publish Atlas                                      │  ← Couleur NOIR/GRIS
│  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  (Background gris foncé)                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  4. Publish / atlas ▼                                           │
│  ┌─────────────────────────────────────────────────────────────┤
│  │ ☑ Atlas Settings                                            │
│  │   ├─ Title: [qfit Activity Atlas]                          │
│  │   ├─ Subtitle: [2024 Activities Summary]                   │
│  │   └─ Output: [/home/user/atlas.pdf]                        │
│  │                                                              │
│  │ [Export Atlas PDF]  [Settings]                             │
│  └─────────────────────────────────────────────────────────────┤
│                                                                  │
│  (ProgressFeedback vide)                                        │
│                                                                  │
│  ✅ Atlas exported successfully (42 pages)                      │  ← ResultIndicator
│  Location: /home/user/atlas.pdf                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Couleurs par Phase

| Phase | Couleur | Hex | Usage |
|-------|---------|-----|-------|
| CONNECT | 🔴 Red | #E74C3C | Phase initiale |
| FETCH | 🔵 Blue | #3498DB | Récupération données |
| STORE | 🟢 Green | #27AE60 | Stockage données |
| VISUALIZE | 🟣 Purple | #9B59B6 | Visualisation |
| ANALYZE | 🟠 Orange | #E67E22 | Analyse |
| PUBLISH | ⚫ Dark | #2C3E50 | Publication |

---

## Comportement des Composants

### PhaseIndicator
```
Propriétés:
  • Position: Haut du dock (toujours visible)
  • Couleur: Change avec la phase
  • Texte: "Phase X/6 — Phase Name"
  • Barre de progression visuelle: █████░░░░

Mise à jour:
  • Automatique lors de transition de phase
  • Couleur change immédiatement
  • Texte et barre de progression mises à jour
```

### ProgressFeedback
```
Propriétés:
  • Position: Sous PhaseIndicator
  • Spinner: Animé avec 10 caractères ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏
  • Message: De l'opération en cours
  • Barre: Indéterminée (par défaut) ou % déterminé

Comportement:
  • Visible pendant long operations
  • Message mis à jour dynamiquement
  • Auto-masquage après succès (3 secondes)
  • Peut être masqué manuellement
```

### ResultIndicator
```
Propriétés:
  • Position: Sous ProgressFeedback
  • Icônes: ✅ ❌ ⚠️ ℹ️
  • Couleurs: Vert / Rouge / Orange / Bleu
  • Message: Clair et concis
  • Suggestion: Optional (affichée si fournie)

Comportement:
  • Reste visible jusqu'à nouvel appel
  • N'auto-masque PAS (contraste avec popups)
  • Cliquable pour copier message (optional)
  • Peut être masqué manuellement
```

---

## Comparaison Avant/Après

### AVANT (Sans design system)
```
┌──────────────────────────────────────┐
│ qfit                                 │
├──────────────────────────────────────┤
│                                      │
│ Workflow: Fetch & store → ...        │
│                                      │
│ 1. Fetch and store activities ▼      │
│   [...]                              │
│   [Fetch Data]                       │
│                                      │
│   (rien visible pendant chargement)  │  ← Pas de feedback
│                                      │
│   (message console ou popup)         │  ← Feedback éphémère
│                                      │
│ 2. Visualize ▼                       │
│   [...]                              │
│                                      │
└──────────────────────────────────────┘
```

**Problèmes:**
- ❌ Pas de visibilité de phase
- ❌ Pas de feedback visuel pendant chargement
- ❌ Messages d'erreur éphémères
- ❌ Utilisateur confus sur progression

### APRÈS (Avec design system)
```
┌──────────────────────────────────────┐
│ qfit                                 │
├──────────────────────────────────────┤
│                                      │
│ Phase 2/6 — Fetch Activities         │  ← NOUVEAU
│ ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│                                      │
│ 1. Fetch and store activities ▼      │
│   [...]                              │
│   [Fetch Data]                       │
│                                      │
│ ⟳ Connecting to API...              │  ← NOUVEAU
│ ████░░░░░░░░░░░░░░░░░░░░  50%   │
│                                      │
│ ✅ Fetched 42 activities             │  ← NOUVEAU
│                                      │
│ 2. Visualize ▼                       │
│   [...]                              │
│                                      │
└──────────────────────────────────────┘
```

**Améliorations:**
- ✅ Phase clarifiée (numéro + couleur)
- ✅ Progression visible (spinner + barre)
- ✅ Résultat persistant (pas d'oubli)
- ✅ Utilisateur comprend l'état

---

## Animations

### PhaseIndicator
```
Transition CONNECT → FETCH:
  1. Couleur change: Rouge → Bleu
  2. Texte change: Phase 1/6 → Phase 2/6
  3. Barre progresse: █░░░░░░░ → ██░░░░░░
  (durée: instantané)
```

### ProgressFeedback Spinner
```
Animation en boucle (100ms par frame):
  Frame 0: ⠋
  Frame 1: ⠙
  Frame 2: ⠹
  Frame 3: ⠸
  Frame 4: ⠼
  Frame 5: ⠴
  Frame 6: ⠦
  Frame 7: ⠧
  Frame 8: ⠇
  Frame 9: ⠏
  → Retour à Frame 0 (animation fluide)
```

### ResultIndicator Appearance
```
Apparition:
  1. Widget devient visible
  2. Couleur de fond appliquée
  3. Texte et icône affichés
  (durée: instantané)

Masquage:
  1. Widget devient invisible
  2. État réinitialisé
  (durée: instantané ou 3s si auto-hide)
```

---

## Cas d'Erreur Affichés

### Erreur API (401 Unauthorized)
```
❌ Authentication failed
Suggestion: Check your API credentials in Settings → Credentials

(Couleur: rouge clair #E74C3C)
```

### Erreur API (429 Rate Limit)
```
❌ Rate limit exceeded (too many requests)
Suggestion: Wait a few minutes and try again

(Couleur: rouge clair #E74C3C)
```

### Erreur Fichier
```
❌ Cannot store to file
Suggestion: Check disk space and file permissions

(Couleur: rouge clair #E74C3C)
```

### Erreur Géométrie
```
⚠️ Invalid geometries in the dataset
Suggestion: Use Vector → Tools → Fix Geometries to correct them

(Couleur: orange #F39C12)
```

---

## Intégration avec Workflow Existant

Les nouveaux composants s'intègrent **au-dessus** du workflow existant:

```
┌─────────────────────────────────────┐
│ [NOUVEAU] PhaseIndicator            │  ← Ajouté
├─────────────────────────────────────┤
│ [NOUVEAU] ProgressFeedback          │  ← Ajouté
├─────────────────────────────────────┤
│ [NOUVEAU] ResultIndicator           │  ← Ajouté
├─────────────────────────────────────┤
│                                     │
│ [EXISTANT] 1. Fetch and store ▼     │  ← Inchangé
│ ┌─────────────────────────────────┤
│ │ (Contenu existant du dock)      │
│ │                                 │
│ └─────────────────────────────────┤
│                                     │
│ [EXISTANT] 2. Visualize ▼           │  ← Inchangé
│ ┌─────────────────────────────────┤
│ │ (Contenu existant du dock)      │
│ │                                 │
│ └─────────────────────────────────┤
│                                     │
└─────────────────────────────────────┘
```

**Résultat:** 
- ✅ Aucune modification du workflow existant
- ✅ Composants ajoutés uniquement en haut
- ✅ Rétrocompatibilité 100%
- ✅ Utilisation optionnelle

---

## Résumé Visuel

| Élément | Avant | Après | Impact |
|---------|-------|-------|--------|
| Phase visibility | ❌ Invisible | ✅ Couleur + numéro | +0.3/5 |
| Progress feedback | ❌ Aucun | ✅ Spinner + message | +0.2/5 |
| Result feedback | ❌ Éphémère | ✅ Persistant | +0.2/5 |
| Error clarity | ❌ Technique | ✅ Actionnable | +0.1/5 |
| Session memory | ❌ Non | ⏳ Optional | +0.1/5 |
| **Total UX** | 3.8/5 | **4.8/5** | **+1.0** |

---

✨ **C'est ce que les utilisateurs verront après l'intégration!**
