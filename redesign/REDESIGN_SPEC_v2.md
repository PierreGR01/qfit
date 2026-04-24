# qfit — Implementation spec for PR "Wizard-style dock widget (Option B)"
**Version** : 2.0 — corrections techniques intégrées  
**Auteur de la correction** : revue ingénierie QGIS (voir §ADDENDUM pour le détail des écarts corrigés par rapport à la v1)
 
> **Audience** : AI coding agent ou contributeur humain implémentant le redesign dans `ebelo/qfit`.  
> **Scope** : remplacer `qfit_dockwidget_base.ui` (panneau monolithique à scroll) par un dock widget wizard en 5 étapes, conformément à l'Option B de l'audit UX.  
> **Source de vérité** : ce document. Ne pas réinterpréter. Si une valeur ou un comportement n'est pas spécifié ici, appliquer le comportement idiomatique Qt/QGIS et laisser un commentaire `# TODO(design)`.
 
Ce document est auto-suffisant : chaque chaîne, chaque widget, chaque signal et chaque comportement nécessaires pour correspondre à la maquette sont listés ci-dessous. Suivre de haut en bas.
 
---
 
## 0. Architecture générale
 
### 0.1 Fichiers à créer
 
| Chemin | Rôle |
|---|---|
| `ui/dockwidget/qfit_dockwidget_base.ui` | **RÉÉCRITURE** — squelette minimaliste (voir §0.4). Tout le contenu des pages est construit en Python. |
| `ui/dockwidget/stepper_bar.py` | Widget composite custom rendant le stepper cliquable en 5 étapes. |
| `ui/dockwidget/footer_status_bar.py` | Widget footer persistant (pills + chemin gpkg). |
| `ui/dockwidget/step_page.py` | Classe de base commune aux 5 pages (header + nav + contenu). |
| `ui/dockwidget/pages/step1_connect.py` | Page 1 — Connexion. |
| `ui/dockwidget/pages/step2_sync.py` | Page 2 — Synchronisation. |
| `ui/dockwidget/pages/step3_map.py` | Page 3 — Carte & filtres. |
| `ui/dockwidget/pages/step4_analyze.py` | Page 4 — Analyse. |
| `ui/dockwidget/pages/step5_atlas.py` | Page 5 — Atlas PDF. |
| `ui/widgets/pill.py` | Widget Pill réutilisable (bg/fg par tone). |
| `ui/widgets/tokens.py` | Constantes de design (couleurs, QSS fragments). |
| `ui/qss/qfit.qss` | Feuille de style scopée au dock widget (voir §9). |
| `qfit_config_dialog.py` | **MODIFIER** — unique point d'édition des credentials OAuth. |
| `qfit_dockwidget.py` | **REFACTORER** — contrôleur fin : câble StepperBar, QStackedWidget, FooterStatusBar, et chaque StepXPage. La logique métier reste dans les packages features existants. |
 
### 0.2 Widgets existants à supprimer du dock
 
Les widgets suivants **ne doivent plus apparaître dans le dock** — ils migrent vers la config dialog ou disparaissent :
 
- `clientIdLineEdit`, `clientIdLabel`
- `clientSecretLineEdit`, `clientSecretLabel`
- `redirectUriLineEdit`, `redirectUriLabel`
- `authCodeLineEdit`, `authCodeLabel`
- `refreshTokenLineEdit`, `refreshTokenLabel`
- `openAuthorizeButton`, `exchangeCodeButton`
- `authHelpLabel`
- `titleLabel`, `workflowLabel`
- `activitiesIntroLabel`, `outputIntroLabel`, `analysisHelpLabel`, `backgroundHelpLabel`, `temporalHelpLabel`, `publishHelpLabel`, `atlasPdfHelpLabel`
- `connectionStatusLabel`, `querySummaryLabel`, `countLabel`, `statusLabel` (remplacés par les pills du footer)
Déplacés dans `qfit_config_dialog.py` :
- Tous les champs OAuth + `openAuthorizeButton` + `exchangeCodeButton`.
- Les champs Mapbox (`mapboxAccessTokenLineEdit`, `mapboxStyleOwnerLineEdit`, `mapboxStyleIdLineEdit`) — affichés en lecture seule dans la Step 3 via un hint "ⓘ Token configuré" et édités uniquement dans la config dialog.
### 0.3 Arbre de widgets principal
 
```
QDockWidget "qfit" (windowTitle="qfit")
└─ QWidget dockWidgetContents
   └─ QVBoxLayout outerLayout (margins 0,0,0,0, spacing 0)
      ├─ StepperBar stepperBar           # custom widget promoted, hauteur fixe 36 px
      ├─ QFrame hLine                    # HLine separator, 1 px
      ├─ QScrollArea contentScroll       # widgetResizable=true, frameShape=NoFrame
      │  └─ QStackedWidget pagesStack    # 5 pages : step1…step5, vide dans le .ui
      └─ FooterStatusBar footerBar       # custom widget promoted, hauteur fixe 28 px
```
 
Largeur minimale du dock : **440 px**. Largeur initiale recommandée : **460 px**. Redimensionnable horizontalement.
 
### 0.4 Contenu du fichier `.ui` (squelette minimal)
 
> ⚠️ **IMPORTANT** : Le fichier `qfit_dockwidget_base.ui` ne contient QUE le squelette ci-dessous.  
> Tout le contenu des pages est construit **programmatiquement en Python** dans chaque `StepXPage`.  
> `StepperBar` et `FooterStatusBar` sont déclarés comme **promoted widgets** dans Qt Designer.
 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>QfitDockWidgetBase</class>
 <widget class="QDockWidget" name="QfitDockWidgetBase">
  <property name="windowTitle"><string>qfit</string></property>
  <property name="minimumWidth"><number>440</number></property>
  <widget class="QWidget" name="dockWidgetContents">
   <layout class="QVBoxLayout" name="outerLayout">
    <property name="margin"><number>0</number></property>
    <property name="spacing"><number>0</number></property>
    <item>
     <widget class="StepperBar" name="stepperBar">
      <property name="minimumHeight"><number>36</number></property>
      <property name="maximumHeight"><number>36</number></property>
     </widget>
    </item>
    <item>
     <widget class="QFrame" name="hLine">
      <property name="frameShape"><enum>QFrame::HLine</enum></property>
      <property name="frameShadow"><enum>QFrame::Plain</enum></property>
      <property name="lineWidth"><number>1</number></property>
     </widget>
    </item>
    <item>
     <widget class="QScrollArea" name="contentScroll">
      <property name="widgetResizable"><bool>true</bool></property>
      <property name="frameShape"><enum>QFrame::NoFrame</enum></property>
      <widget class="QStackedWidget" name="pagesStack"/>
     </widget>
    </item>
    <item>
     <widget class="FooterStatusBar" name="footerBar">
      <property name="minimumHeight"><number>28</number></property>
      <property name="maximumHeight"><number>28</number></property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <customwidgets>
  <customwidget>
   <class>StepperBar</class>
   <extends>QWidget</extends>
   <header>ui.dockwidget.stepper_bar</header>
  </customwidget>
  <customwidget>
   <class>FooterStatusBar</class>
   <extends>QWidget</extends>
   <header>ui.dockwidget.footer_status_bar</header>
  </customwidget>
 </customwidgets>
</ui>
```
 
### 0.5 Classe de base du dock — vérification préalable obligatoire
 
> ⚠️ **VÉRIFIER AVANT D'IMPLÉMENTER** : inspecter `qfit_dockwidget.py` existant pour déterminer la classe de base réelle (`QDockWidget` vs `QgsDockWidget`). Ne pas changer la classe de base sans justification explicite — un changement entraîne une erreur MRO si le `FORM_CLASS` généré par `uic.loadUiType` ne s'y attend pas.
 
```python
# Pattern attendu — à conserver tel quel :
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'ui/dockwidget/qfit_dockwidget_base.ui'))
 
class QfitDockWidget(QDockWidget, FORM_CLASS):   # ← ne pas changer QDockWidget en QgsDockWidget
    ...
```
 
---
 
## 1. Composants partagés
 
### 1.1 `StepperBar` (`ui/dockwidget/stepper_bar.py`)
 
Widget `QWidget` custom rendant 5 étapes cliquables en layout horizontal.
 
```
ÉTAPE 1 ─── ÉTAPE 2 ─── [ÉTAPE 3] ─── ÉTAPE 4 ─── ÉTAPE 5
Connexion   Sync        Carte         Analyse     Atlas
   ✓           ✓          (pill)        (dim)      (dim)
```
 
**Labels des étapes (ordre, index 0-based)** :
0. "Connexion"
1. "Synchronisation"
2. "Carte"
3. "Analyse"
4. "Atlas"
**États** : `done`, `current`, `upcoming`, `locked`.  
- Une étape est `locked` tant que son prérequis n'est pas `done` ET que l'utilisateur ne l'a pas encore visitée (voir §7).
- Cliquer une étape non-locked émet `stepRequested(int index)`.
**Style par état** (stylesheets — utiliser les tokens de §1.4) :
- `done` : chip cercle vert rempli avec glyphe ✓, label `#202124` regular.
- `current` : fond pill `#589632` (vert QGIS), texte blanc gras, compteur dans un cercle blanc translucide.
- `upcoming` : cercle gris `#d0d3d8`, label `#6b6f76`.
- `locked` : identique à `upcoming` mais `setEnabled(False)` et curseur `Qt.ForbiddenCursor`.
Connecteurs entre chips : `QFrame HLine` de 8 px, hauteur 1 px, couleur `#589632` si l'étape précédente est `done`, sinon `#d0d3d8`.
 
**API publique** :
```python
class StepperBar(QWidget):
    stepRequested = pyqtSignal(int)          # l'utilisateur a cliqué une étape
    def set_state(self, states: list[str])   # len=5, chaque valeur dans {done, current, upcoming, locked}
    def set_current(self, index: int)        # raccourci : marque index current, les autres dim
```
 
Hauteur fixe **36 px**. Padding interne `4 2 10 2`.
 
**État initial** :
- Premier lancement (pas de clé `qfit/ui/wizard_version` dans `QgsSettings`) : step 0 = `current`, steps 1–4 = `locked`.
- Lancements suivants : restaurer `qfit/ui/last_step_index`, puis recalculer les états via §7.
### 1.2 `FooterStatusBar` (`ui/dockwidget/footer_status_bar.py`)
 
Barre fine persistante en bas du dock.
 
**Contenu (gauche → droite)** :
- Pill `● Strava` — vert `#dcefd0 / #2e6318` si connecté, rouge `#f6d4d4 / #8a121b` si non connecté.
- Pill `{N} activités` — bleu `#d6e7f7 / #124c8c`. N = comptage live depuis `activity_registry`. Si pas de gpkg chargé, afficher `— activités` en gris.
- Pill `{M} couches` — neutre `#eef0f2 / #6b6f76`. M = nombre de couches qfit dans `QgsProject`.
- Stretch.
- Chemin en police mono : `qfit.gpkg` (basename uniquement, chemin complet en tooltip). Police `monospace`, 10.5 pt, couleur `#6b6f76`.
Fond `#f7f7f7`, bordure haute 1 px `#dcdcdc`. Padding `4 10 4 10`. Hauteur **28 px**.
 
**API publique** :
```python
class FooterStatusBar(QWidget):
    def set_strava(self, connected: bool): ...
    def set_activity_count(self, n: int | None): ...
    def set_layer_count(self, m: int): ...
    def set_gpkg_path(self, path: str | None): ...
```
 
Les Pills sont réutilisables — créer `ui/widgets/pill.py` avec `Pill(text, tone)` où `tone ∈ {ok, info, muted, warn, danger}`. Utilisé aussi dans les pages.
 
### 1.3 Classe de base `StepPage` (`ui/dockwidget/step_page.py`)
 
Chrome commun dont héritent toutes les pages.
 
```
┌───────────────────────────────────────────────────┐
│ ÉTAPE 2/5     Synchronisation des activités   [●] │  ← StepHeader
│ Récupération depuis Strava vers un GeoPackage…    │
├───────────────────────────────────────────────────┤
│                                                   │
│  (contenu spécifique à la page)                   │
│                                                   │
├───────────────────────────────────────────────────┤
│ [← Précédent]            [extra] [Primary CTA →] │  ← StepNav
└───────────────────────────────────────────────────┘
```
 
```python
class StepPage(QWidget):
    backRequested = pyqtSignal()
    nextRequested = pyqtSignal()
    def __init__(self, step_num: int, step_total: int, title: str, subtitle: str, status_pill=None): ...
    def set_status(self, text: str | None, tone: str = "muted"): ...
    def set_next(self, label: str, icon: str = "→", primary: bool = True, enabled: bool = True): ...
    def set_back(self, label: str = "Précédent", enabled: bool = True): ...
    def add_extra_button(self, btn: QPushButton, align: str = "right"): ...
    def content_layout(self) -> QVBoxLayout: ...   # les sous-classes placent leurs QGroupBox ici
```
 
Typographie du header : `ÉTAPE n/5` en `font-size 10.5pt, weight 600, letter-spacing .5px, color #6b6f76` ; titre en `font-size 14pt, weight 600` ; sous-titre en `11pt, #6b6f76, word-wrap, margin-top 3px, line-height 1.45`.
 
Nav : marge haute 10 px. Bouton Back ton `ghost` (plat, bordure `#b0b4ba` 1 px). Bouton primary next : fond vert QGIS `#589632`, texte blanc, weight 600.
 
### 1.4 Tokens de couleur (`ui/widgets/tokens.py`)
 
```python
COLOR_BG           = "#f3f3f3"
COLOR_PANEL        = "#fafafa"
COLOR_GROUP_BORDER = "#c4c4c4"
COLOR_TEXT         = "#202124"
COLOR_MUTED        = "#6b6f76"
COLOR_ACCENT       = "#589632"   # vert QGIS, action primaire
COLOR_ACCENT_DARK  = "#3f6e22"
COLOR_LINK         = "#1a5fb4"
COLOR_DANGER       = "#c01c28"
COLOR_WARN         = "#b67204"
COLOR_INPUT_BORDER = "#b0b4ba"
COLOR_INPUT_BG     = "#ffffff"
COLOR_SEPARATOR    = "#dcdcdc"
COLOR_HOVER        = "#e8e8e8"
COLOR_TITLE_BAR    = "#e4e4e7"
 
# Palettes Pill : (bg, fg)
PILL_TONES = {
    "ok":      ("#dcefd0", "#2e6318"),
    "info":    ("#d6e7f7", "#124c8c"),
    "warn":    ("#fbe7c3", "#7a4f00"),
    "danger":  ("#f6d4d4", "#8a121b"),
    "muted":   ("#eef0f2", "#6b6f76"),
    "neutral": ("#e4e4e7", "#3f3f46"),
}
 
PRIMARY_BTN_QSS = """
QPushButton[role="primary"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #68ad3e, stop:1 #4e8a2b);
    color: white; font-weight: 600;
    border: 1px solid #3f6e22; border-radius: 2px;
    padding: 4px 12px; min-height: 22px;
}
QPushButton[role="primary"]:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #72ba45, stop:1 #579530); }
QPushButton[role="primary"]:disabled { background: #b0c9a0; border-color: #8aaa78; }
"""
```
 
Tous les stylesheets sont appliqués via `setProperty("role", …)` + QSS global, jamais en inline dans la logique. Le QSS est dans `ui/qss/qfit.qss` et chargé dans `qfit_plugin.py::initGui` **scopé au dock widget** (voir §9).
 
### 1.5 Widgets QGIS natifs — règles de substitution et version guards
 
| Remplacer | Par | Condition |
|---|---|---|
| `QLineEdit` pour chemin fichier | `QgsFileWidget` | Toujours |
| `QLineEdit` pour recherche | `QgsFilterLineEdit` | Toujours |
| `QLineEdit` pour mot de passe | `QgsPasswordLineEdit` | Toujours |
| `QGroupBox` (collapsible) | `QgsCollapsibleGroupBox` | Toujours |
| Paire de `QDoubleSpinBox` distance | `QgsDoubleRangeSlider` si QGIS ≥ 3.38, sinon deux `QDoubleSpinBox` | Voir guard ci-dessous |
| Paire de `QDateEdit` | Deux `QgsDateTimeEdit` côte à côte | `QgsDateTimeRangeWidget` n'existe PAS dans l'API publique — ne pas utiliser |
| Help `QLabel` | `QToolTip` sur le contrôle le plus proche, ou bouton ⓘ `QToolButton` ouvrant `QWhatsThis` | Toujours |
 
> ⚠️ `QgsCheckableComboBox` n'existe pas dans l'API publique `qgis.gui`. Utiliser un `QListWidget` avec `Qt.ItemIsUserCheckable` sur chaque item. Voir §5.2 pour l'usage concret.
 
**Version guard obligatoire pour `QgsDoubleRangeSlider`** :
 
```python
# ui/widgets/compat.py
from qgis.core import Qgis
 
def make_range_slider(parent=None):
    """
    Retourne un QgsDoubleRangeSlider si QGIS >= 3.38,
    sinon un widget composite avec deux QDoubleSpinBox.
    """
    if Qgis.QGIS_VERSION_INT >= 33800:
        from qgis.gui import QgsDoubleRangeSlider
        return QgsDoubleRangeSlider(Qt.Horizontal, parent)
    else:
        return _FallbackRangeWidget(parent)
 
class _FallbackRangeWidget(QWidget):
    """Deux QDoubleSpinBox 'min ── max' avec le même signal rangeChanged(float, float)."""
    rangeChanged = pyqtSignal(float, float)
    # … implémentation minimale …
```
 
Utiliser `make_range_slider()` partout dans la spec où `QgsDoubleRangeSlider` est mentionné.
 
---
 
## 2. Étape 1 — Connexion
 
**Fichier** : `ui/dockwidget/pages/step1_connect.py`  
**En-tête de l'étape** :
- Compteur `ÉTAPE 1/5`
- Titre `Connexion Strava`
- Sous-titre `Lien avec votre compte Strava via OAuth. Une seule fois, puis oublié.`
- Pill de statut : ton `ok`, label `Connecté` si credentials présents & dernier échange de token réussi, sinon `Non connecté` (ton `danger`).
### 2.1 Carte hero — "Compte Strava lié"
 
Un `QFrame` avec bordure verte visible (1 px `#589632`) et fond en dégradé léger. Layout :
 
- `QLabel` 36×36 avec glyphe ✓ unicode, weight 700, font-size 18, centré, `border-radius: 18px`, fond `#589632`, couleur blanche.
- Bloc vertical :
  - Ligne 1 : **"Compte Strava lié"** (`12.5pt, weight 600`)
  - Ligne 2 : `App : <code>{client_id_display}</code> · scope <code>activity:read_all</code>` (11pt, `#6b6f76`). `client_id_display` = `qfit-local (client_id {client_id[:6]})` si connu, sinon `(à configurer)`.
  - Ligne 3 : `Refresh token actif · renouvelé automatiquement, expire le {date}` (11pt, `#6b6f76`). `date` provient d'un check du token toutes les 6 h, mis en cache dans `QgsSettings`.
Padding : 12 px. Border-radius : 3 px. Dégradé : `qlineargradient(0,0,0,1 stop:0 #f5fbee stop:1 #e4f0da)`.
 
Quand **non connecté** : remplacer ✓ par ✕ rouge, reborder en `#c01c28`, titre "Compte Strava non lié", supprimer lignes 2–3, afficher un bouton primaire "Configurer la connexion…" (aligné à droite) qui ouvre la config dialog.
 
### 2.2 `QgsCollapsibleGroupBox` "Statut de connexion" (ouvert par défaut)
 
Form layout, lecture seule :
- `Application :` → label mono `qfit-local (client_id {client_id[:6]})` + Pill `OAuth 2.0` (ton `info`).
- `Endpoint :` → label mono `https://www.strava.com/api/v3`.
- `Dernier test :` → `{yyyy-MM-dd · HH:mm} — 200 OK` (rouge `— {status_code} {reason}` en cas d'échec). Résultat mis en cache.
### 2.3 `QgsCollapsibleGroupBox` "Stockage des identifiants" (ouvert par défaut)
 
- Hint : **pas de `QLabel` complet** — utiliser un `QToolButton` ⓘ à droite du titre du groupe, dont le tooltip contient : *"Les identifiants OAuth (client_id, client_secret, refresh_token) sont stockés via QgsSettings et ne s'affichent plus ici. Pour les voir ou les modifier, ouvrez la fenêtre ⚙ Configuration."*
- Rangée de boutons (`QHBoxLayout`) :
  - `[⚙ Ouvrir la configuration…]` → ouvre `QfitConfigDialog`. Ton `ghost`.
  - `[↻ Tester la connexion]` → appel API no-op `GET /athlete`. Ton `ghost`. En succès, met à jour "Dernier test" et la pill. En échec, affiche un `QgsMessageBar` (jamais un `QMessageBox`).
  - Stretch.
  - `[Déconnecter]` → bouton destructif flat (`color: #c01c28; background: transparent; border: 0`). Confirmation via `QMessageBox.warning`. Efface les credentials dans `QgsSettings`.
### 2.4 StepNav
 
- Back : aucun (désactivé / masqué).
- Next : **"Synchroniser"**, `→`, primary, activé uniquement si `strava.connected == True`.
### 2.5 Signaux & état
 
```python
class Step1ConnectPage(StepPage):
    openConfig = pyqtSignal()
    testConnection = pyqtSignal()
    disconnect = pyqtSignal()
 
    def set_connected(
        self,
        connected: bool,
        client_id: str | None,
        expires_at: QDateTime | None,
        last_test: tuple[QDateTime, int, str] | None
    ): ...
```
 
---
 
## 3. Étape 2 — Synchronisation
 
**Fichier** : `ui/dockwidget/pages/step2_sync.py`  
**En-tête** :
- Compteur `ÉTAPE 2/5`
- Titre `Synchronisation des activités`
- Sous-titre `Récupération depuis Strava vers un GeoPackage local. Les filtres s'appliquent plus tard — pas besoin de re-fetch.`
- Pill : `{K} nouvelles` ton `info` (K = delta depuis dernière sync), ou `À jour` ton `ok` si K = 0.
### 3.1 Carte action primaire — "Récupérer les nouvelles activités"
 
Même conteneur visuel que §2.1 (carte à bordure verte et dégradé). Contenu :
 
- Bloc gauche :
  - Titre **"Récupérer les nouvelles activités"** (12.5pt, 600).
  - Sous-ligne : `Dernière sync : {yyyy-MM-dd · HH:mm} · ~{K} activités en attente sur Strava` (10.5pt `#6b6f76`). Si K inconnu : `Dernière sync : {…} · fetch pour rafraîchir`.
- Bouton droit : **`[⟳ Fetch]`** — primary. `objectName` : `fetchButton`.
Au clic sur `fetchButton` :
- Désactiver le bouton, afficher un `QgsMessageBar` avec barre de progression inline et action Annuler.
- Déléguer au workflow existant `activities/application/fetch_workflow.py` (ne pas dupliquer la logique).
- En succès, rafraîchir le tableau de preview (§3.4) et les pills du footer.
### 3.2 `QgsCollapsibleGroupBox` "GeoPackage de destination" (ouvert)
 
Form layout :
- `Fichier :` → `QgsFileWidget`, mode `QgsFileWidget.SaveFile`, filtre `GeoPackage (*.gpkg)`, valeur par défaut depuis `QgsSettings key qfit/output_path`.
- `Points échantillonnés :` → `QCheckBox` **"Générer activity_points (pour heatmap & analyse)"**, `objectName` : `writeActivityPointsCheckBox`, coché par défaut.
- `Pas d'échantillonnage :` → layout inline `un point sur` + `QSpinBox` (range 1–100, défaut 5, pas de suffix) + label `pts`. N'activer cette ligne que si `writeActivityPointsCheckBox` est coché. `objectName` spinbox : `pointSamplingStrideSpinBox`.
### 3.3 `QgsCollapsibleGroupBox` "Options avancées" (**replié par défaut**)
 
Form layout :
- `Activités / page :` → `QSpinBox` 1–200, défaut 200. `objectName` : `perPageSpinBox`.
- `Pages max :` → `QSpinBox` 0–9999, défaut 0. Tooltip : *"0 = récupérer toutes les pages disponibles."* `objectName` : `maxPagesSpinBox`.
- `Routes détaillées :` → `QCheckBox` **"Fetch quand disponible"**. `objectName` : `detailedStreamsCheckBox`.
- `Stratégie :` → `QComboBox` : `Priorité aux plus récentes`, `Priorité aux plus anciennes`, `Aléatoire`. `objectName` : `detailedRouteStrategyComboBox`.
- `Max détaillées / run :` → `QSpinBox` 1–500, défaut 25. Activé uniquement si `detailedStreamsCheckBox` est coché. `objectName` : `maxDetailedActivitiesSpinBox`.
### 3.4 `QgsCollapsibleGroupBox` "Preview — {K} activités récupérées" (ouvert)
 
- Pill `{K} nouvelles` (ton `ok`) dans le titre du groupe : implémenté en overlayant un `QLabel` stylisé en pill, positionné en absolu dans le titre-row du `QgsCollapsibleGroupBox` via un sous-classage léger (`QgsCollapsibleGroupBox` ne fournit pas un layout titre standard). Voir note §13.1.
- Contenu : `QTableView` + `QStandardItemModel`, colonnes :
  - `Date` (largeur 70, format `dd/MM`, alignement gauche, couleur `#6b6f76`)
  - `Nom` (stretch, alignement gauche, police normale)
  - `Dist` (largeur 70, alignement droite, format `{d:.1f} km`)
  - `Type` (largeur 60, alignement droite, couleur `#6b6f76`)
Style header : fond `#efefef`, bordure basse 1 px `#dcdcdc`, police 10.5pt bold uppercase letter-spacing 0.5 `#6b6f76`. Hauteur de ligne 22 px. Pas d'alternance de couleurs. Sélection : `SelectRows`, `SingleSelection`.
 
Afficher uniquement les **6 lignes les plus récentes** sans scroll. Double-clic sur une ligne émet `activityActivated(activity_id)` (câblage optionnel en v1 — émettre le signal, laisser le handler `# TODO`).
 
### 3.5 StepNav
 
- Back : **"Précédent"**, ghost.
- Extra (aligné à droite, avant primary) : **`[⌦ Réinitialiser…]`** — petit bouton ghost ouvrant un dialog de confirmation puis appelant le code "Clear database" existant. Conserver le comportement existant de `clearDatabaseButton`.
- Next : **"Visualiser sur la carte"**, `→`, primary, activé quand le GeoPackage existe et est non vide.
### 3.6 Signaux
 
```python
# Dataclasses à définir dans ui/dockwidget/pages/step2_sync.py
from dataclasses import dataclass
from datetime import datetime
 
@dataclass
class ActivityPreviewRow:
    activity_id: int
    date: datetime
    name: str
    distance_km: float
    activity_type: str
 
class Step2SyncPage(StepPage):
    fetchRequested = pyqtSignal()
    resetRequested = pyqtSignal()
    outputPathChanged = pyqtSignal(str)
    activityActivated = pyqtSignal(int)
 
    def set_preview_rows(self, rows: list[ActivityPreviewRow]): ...
    def set_last_sync(self, when: QDateTime | None, pending: int | None): ...
```
 
---
 
## 4. Étape 3 — Carte & filtres
 
**Fichier** : `ui/dockwidget/pages/step3_map.py`  
**En-tête** :
- Compteur `ÉTAPE 3/5`
- Titre `Carte & filtres`
- Sous-titre `Appliquer un fond de carte, filtrer les activités visibles et choisir un style de rendu.`
- Pill : `{M} couches` ton `ok` si couches qfit présentes, sinon `Aucune couche` ton `muted`.
### 4.1 `QgsCollapsibleGroupBox` **checkable** "Fond de carte" (ouvert, décoché par défaut)
 
Checkable = ancien comportement de `backgroundMapCheckBox`. Quand décoché, enfants désactivés.
 
Form layout :
- `Preset :` → `QComboBox` peuplé depuis `mapbox_config.PRESETS`. `objectName` : `backgroundPresetComboBox`.
- `Rendu :` → `QComboBox` avec `Raster tiles`, `Vector tiles`. `objectName` : `tileModeComboBox`.
- Dernière ligne (colspan 2) : `QHBoxLayout` :
  - `[▦ Charger le fond]` petit bouton. `objectName` : `loadBackgroundButton`.
  - Stretch.
  - Label 10.5pt muted : `Token Mapbox : pk.eyJ1… ⓘ` (tooltip : "Modifiable dans ⚙ Configuration").
### 4.2 `QgsCollapsibleGroupBox` "Filtres" (ouvert)
 
Form layout :
- `Type :` → `QComboBox` : `Toutes les activités`, `Ride`, `Run`, `Hike`, `Ski`, `Swim`, `Walk`, etc. `objectName` : `activityTypeComboBox`.
- `Nom contient :` → `QgsFilterLineEdit`, placeholder `gravel, morning, commute…`. `objectName` : `activitySearchLineEdit`.
- `Période :` → deux `QgsDateTimeEdit` côte à côte séparés par un label `→`. Défaut min `2000-01-01`, max `QDate.currentDate()`. `objectName` : `dateStartEdit`, `dateEndEdit`.  
  > ⚠️ Ne pas utiliser `QgsDateTimeRangeWidget` — ce widget n'existe pas dans l'API publique `qgis.gui`.
- `Distance (km) :` → `make_range_slider()` (voir §1.5), range 0–500, défaut `[10, 180]`. En dessous du slider, une ligne avec labels `{low} km` / `{high} km`. `objectName` : `distanceRangeSlider`.
- Dernière ligne (colspan 2) : `QCheckBox` **"Uniquement activités avec tracés détaillés"**. `objectName` : `detailedOnlyCheckBox`.
**Live-apply avec debounce** : chaque changement de filtre démarre (ou redémarre) un `QTimer.singleShot(300, self._emit_filters_changed)`. Ne jamais bloquer le thread principal — `time.sleep` est interdit.
 
### 4.3 `QgsCollapsibleGroupBox` "Style de rendu" (ouvert, pill droite `6 presets` ton `info`)
 
Grille **3×2 de cartes cliquables** (`QToolButton` checkable, `QButtonGroup` exclusive). Chaque carte :
- Taille fixe 96×52 px.
- Bordure 1 px : `#b0b4ba` non sélectionné, `#589632` sélectionné.
- Fond : `#ffffff` par défaut, `#e8f2dd` sélectionné.
- Contenu centré : glyphe unicode (14pt) en haut, label (10.5pt) en dessous. Sélectionné : label weight 600.
Cartes (ordre, label, glyphe, clé preset) :
1. `Lignes simples` — `━` → `simple_lines`
2. `Par type` — `╳` → `by_activity_type`
3. `Points de tracé` — `·` → `track_points`
4. `Heatmap` — `⬢` → `heatmap`
5. `Points de départ` — `●` → `start_points`
6. `Starts groupés` — `◎` → `clustered_starts`
Sélection par défaut : `by_activity_type`.
 
### 4.4 StepNav
 
- Back : **"Précédent"**, ghost.
- Extra (aligné droite, avant primary) : **`[↻ Appliquer]`** — petit bouton non-primary, déclenche le comportement existant de `applyFiltersButton`.
- Next : **"Passer à l'analyse"**, `→`, primary, toujours activé.
### 4.5 Signaux
 
```python
from dataclasses import dataclass
 
@dataclass
class FilterRequest:
    """Reuse or extend the existing FilterRequest dataclass from visualization/application/.
    If it already exists there, import it instead of redefining."""
    activity_type: str | None = None
    name_contains: str | None = None
    date_start: QDate | None = None
    date_end: QDate | None = None
    distance_min_km: float = 0.0
    distance_max_km: float = 500.0
    detailed_only: bool = False
 
class Step3MapPage(StepPage):
    backgroundToggled = pyqtSignal(bool)
    loadBackgroundRequested = pyqtSignal()
    filtersChanged = pyqtSignal(FilterRequest)   # debounced 300 ms via QTimer
    applyFiltersRequested = pyqtSignal()
    styleChanged = pyqtSignal(str)               # clé preset
```
 
---
 
## 5. Étape 4 — Analyse
 
**Fichier** : `ui/dockwidget/pages/step4_analyze.py`  
**En-tête** :
- Compteur `ÉTAPE 4/5`
- Titre `Analyse spatiale`
- Sous-titre `Lancer une analyse sur les couches qfit chargées. Le résultat s'ajoute au projet comme nouvelle couche.`
- Pill : aucune par défaut ; **après un run** afficher `Terminée · {yyyy-MM-dd HH:mm}` ton `ok`.
### 5.1 `QgsCollapsibleGroupBox` "Choisir une analyse" (ouvert)
 
Grille 2 colonnes de 4 cartes d'analyse (`QToolButton` checkable, exclusive dans `QButtonGroup`). Chaque carte :
- Hauteur fixe 56 px, largeur = colonne.
- Bordure/fond : même schéma de sélection que §4.3.
- Layout horizontal : tile icône 24×24 (glyphe unicode, `#1a5fb4` sur `#eef0f2` non sélectionné, blanc sur `#589632` sélectionné) + bloc texte 2 lignes (titre 12pt 600 / description 10.5pt `#6b6f76`).
Cartes (titre, description, glyphe, clé) :
1. `Points de départ fréquents` · `Clusters DBSCAN sur les starts` · `●` → `frequent_starting_points`
2. `Heatmap d'activités` · `Densité sur grille hexagonale` · `⬢` → `activity_heatmap`
3. `Couloirs récurrents` · `Segments de tracé partagés` · `╳` → `recurrent_corridors`
4. `Statistiques par zone` · `Agrégats sur polygones` · `▦` → `stats_by_zone`
Sélection par défaut : `frequent_starting_points`.
 
### 5.2 `QgsCollapsibleGroupBox` "Paramètres — {titre analyse courante}" (ouvert)
 
Le titre **se met à jour dynamiquement** avec la carte sélectionnée.
 
Le layout interne est un **`QStackedWidget`** avec une page par clé d'analyse.
 
- `frequent_starting_points` :
  - `Rayon de cluster :` → `QSpinBox` 10–5000, défaut 250, `setSuffix(" m")`.
  - `Taille minimum :` → `QSpinBox` 2–200, défaut 3, `setSuffix(" pts")`.
  - `Couche source :` → `QComboBox` peuplé avec les couches qfit de points du projet, défaut `activity_starts`.
- `activity_heatmap` :
  - `Résolution :` → `QSpinBox` 50–5000, défaut 500, `setSuffix(" m")`.
  - `Grille :` → `QComboBox` : `Hexagones`, `Carrés`.
  - `Pondération :` → `QComboBox` : `Nombre d'activités`, `Distance cumulée`, `Durée cumulée`.
- `recurrent_corridors` :
  - `Tolérance spatiale :` → `QSpinBox` 5–200, défaut 15, `setSuffix(" m")`.
  - `Longueur min :` → `QSpinBox` 100–10000, défaut 500, `setSuffix(" m")`.
- `stats_by_zone` :
  - `Couche de zones :` → `QComboBox` peuplé depuis les couches polygones du projet, placeholder `Sélectionner…`.
  - `Agrégats :` → `QListWidget` avec items checkables (`Qt.ItemIsUserCheckable | Qt.ItemIsEnabled`) :
    `Nombre d'activités`, `Distance totale`, `Durée totale`.  
    > ⚠️ `QgsCheckableComboBox` n'existe pas dans l'API publique — utiliser `QListWidget` avec items checkables.
Ligne partagée (toutes les analyses) :
- `Portée :` → `QCheckBox` **"Appliquer les filtres actifs de l'étape 3"**, coché par défaut. `objectName` : `applyStep3FiltersCheckBox`.
### 5.3 `QgsCollapsibleGroupBox` "Lecture temporelle" (**replié par défaut**)
 
- `Mode :` → `QComboBox` — mêmes options que le `temporalModeComboBox` actuel.
- Tooltip sur le ⓘ du titre : *"Active la barre temporelle QGIS et mappe les timestamps locaux ou UTC quand ils sont disponibles."*
### 5.4 StepNav
 
- Back : **"Précédent"**, ghost.
- Extra (avant primary) : **`[▶ Lancer]`** — bouton à gradient vert (`role="primary"`), taille standard, `objectName` : `runAnalysisButton`. C'est l'action principale de cette page.
- Next : **"Passer à l'atlas"**, `→`, ton ghost non-primary (`primary=False`) jusqu'à ce qu'au moins un run ait été effectué dans la session. Devient primary ensuite.
> **Rationale** : sur cette page l'action CTA principale est "Lancer", pas "Suivant". "Suivant" reste une affordance de navigation.
 
### 5.5 Signaux
 
```python
class Step4AnalyzePage(StepPage):
    analysisSelected = pyqtSignal(str)        # analysis_key
    runRequested = pyqtSignal(str, dict)      # key, params
    temporalModeChanged = pyqtSignal(str)
```
 
---
 
## 6. Étape 5 — Atlas PDF
 
**Fichier** : `ui/dockwidget/pages/step5_atlas.py`  
**En-tête** :
- Compteur `ÉTAPE 5/5`
- Titre `Atlas PDF`
- Sous-titre `Génère un PDF par activité (titre, date, stats, carte centrée sur l'extent).`
- Pill : `Prêt` ton `ok` si prérequis satisfaits (§7), sinon `{raison}` ton `warn`.
### 6.1 `QgsCollapsibleGroupBox` "Couverture" (ouvert)
 
- `Titre :` → `QLineEdit`, défaut `qfit Activity Atlas`. `objectName` : `atlasTitleLineEdit`.
- `Sous-titre :` → `QLineEdit`, placeholder `Optionnel…`. `objectName` : `atlasSubtitleLineEdit`.
### 6.2 `QgsCollapsibleGroupBox` "Mise en page" (**replié par défaut**)
 
- `Format :` → `QComboBox` : `A4 paysage`, `A4 portrait`, `A3 paysage`, `A3 portrait`, `Letter paysage`. Défaut `A4 paysage`. `objectName` : `pageFormatComboBox`.
- `Pages incluses :` → pile verticale de `QCheckBox` :
  - `Couverture` (coché)
  - `Table des matières` (coché)
  - `1 page par activité` (coché)
  - `Résumé final` (décoché)
### 6.3 `QgsCollapsibleGroupBox` "Export" (ouvert)
 
- `Fichier de sortie :` → `QgsFileWidget`, mode `SaveFile`, filtre `PDF (*.pdf)`, valeur par défaut depuis `QgsSettings key qfit/atlas_pdf_path`. `objectName` : `atlasPdfPathFileWidget`.
- `Couches :` (colspan 2, align `top`) → `QLabel` rich text, `#6b6f76`, line-height 1.6 :
  ```
  ✓ activity_atlas_pages (N pages)
  ✓ activity_tracks
  ✓ qfit_background (Mapbox Outdoors)
  ```
  ✓ vert si la couche est chargée, ✗ gris sinon. N = nombre de lignes de `activity_atlas_pages`. Bloc **informatif, non éditable**.
### 6.4 Carte CTA — "Prêt à exporter"
 
Même conteneur gradient vert que §2.1 / §3.1 :
 
- Gauche : titre **"Prêt à exporter"** (12pt 600) / sous-ligne `{N} pages · temps estimé ~{m} min · taille ≈ {s} MB` (10.5pt `#6b6f76`).
- Droite : **`[▤ Générer PDF]`** primary, `objectName` : `generateAtlasPdfButton`.
**Calcul des estimations** (configurable, ne pas hardcoder dans le widget) :
```python
# atlas/application/atlas_config.py
PAGES_PER_MINUTE = 150    # baseline, ajustable
KB_PER_PAGE = 28          # baseline, ajustable
 
def estimate_time_min(n: int) -> int:
    return max(1, round(n / PAGES_PER_MINUTE))
 
def estimate_size_mb(n: int) -> float:
    return round(n * KB_PER_PAGE / 1024, 1)
```
 
Le widget appelle ces fonctions — il ne recalcule pas lui-même.
 
Pendant la génération :
- Désactiver le bouton, remplacer son label par `Génération…` avec spinner indéterminé.
- Progression via `QgsMessageBar` avec % et action Annuler (réutiliser la tâche atlas existante).
- En succès : toast `QgsMessageBar` avec actions `[Ouvrir]` / `[Dossier]`.
### 6.5 StepNav
 
- Back : **"Précédent"**, ghost.
- Extra (aligné droite) : **`[↻ Recommencer]`** — ghost, remet à zéro l'état du wizard (pas les données) et retourne à l'étape 1. Confirmation `QMessageBox.question` requise.
- Next : **aucun** (étape terminale). Masquer complètement le bouton.
### 6.6 Signaux
 
```python
from dataclasses import dataclass
 
@dataclass
class AtlasRequest:
    """Reuse the existing AtlasRequest dataclass if it exists in atlas/application/.
    If so, import it instead of redefining."""
    title: str
    subtitle: str
    page_format: str
    include_cover: bool
    include_toc: bool
    include_activity_pages: bool
    include_summary: bool
    output_path: str
    apply_step3_filters: bool = True
 
class Step5AtlasPage(StepPage):
    generateRequested = pyqtSignal(AtlasRequest)
    restartRequested = pyqtSignal()
```
 
---
 
## 7. Machine à états du stepper (règles de progression)
 
Une étape est `done` quand sa condition d'activation est satisfaite. Évaluées en temps réel :
 
| Étape | Condition `done` |
|---|---|
| 1 Connexion | `strava.credentials_present AND strava.last_token_exchange_successful` |
| 2 Sync | `gpkg_exists AND activity_count > 0` |
| 3 Carte | `qfit_layers_loaded_in_project >= 3 AND style_preset_applied_at_least_once` |
| 4 Analyse | `at_least_one_analysis_run_this_session` (non-persistant — remet à zéro au rechargement du plugin). L'étape est `unlocked` (pas `done`) dès que l'étape 3 est `done`. Elle devient `done` uniquement après un run effectif. |
| 5 Atlas | Étape terminale, pas de condition. |
 
**Règle de verrouillage** :
- L'étape `i` est `locked` si l'étape `i-1` n'est pas `done` **et** que l'utilisateur n'a pas encore visité l'étape `i` dans cette session.
- Une fois visitée, l'étape reste `unlocked` pour toute la session.
**Si l'utilisateur clique une étape locked** : ne rien faire et animer brièvement la bordure de l'étape courante (`QPropertyAnimation` sur `border-color`, 400 ms).
 
---
 
## 8. Refactoring de `qfit_dockwidget.py`
 
```python
# Classe de base : conserver celle du fichier existant (QDockWidget ou QgsDockWidget)
# Ne pas changer sans vérification préalable — voir §0.5
 
class QfitDockWidget(QDockWidget, FORM_CLASS):   # adapter selon l'existant
    def __init__(self, iface, settings, deps):
        super().__init__()
        self.setupUi(self)
 
        # 1. Construire les pages (injection de dépendances)
        self.page1 = Step1ConnectPage(deps.strava_gateway)
        self.page2 = Step2SyncPage(deps.sync_workflow)
        self.page3 = Step3MapPage(deps.visualization_workflow)
        self.page4 = Step4AnalyzePage(deps.analysis_workflow)
        self.page5 = Step5AtlasPage(deps.atlas_workflow)
 
        for p in (self.page1, self.page2, self.page3, self.page4, self.page5):
            self.pagesStack.addWidget(p)
 
        # 2. Câbler stepper ↔ stack
        self.stepperBar.stepRequested.connect(self.pagesStack.setCurrentIndex)
        self.pagesStack.currentChanged.connect(self._on_step_changed)
 
        # 3. Câbler la navigation entre pages
        for i, p in enumerate(self._pages()):
            p.backRequested.connect(lambda i=i: self.pagesStack.setCurrentIndex(max(0, i - 1)))
            p.nextRequested.connect(lambda i=i: self.pagesStack.setCurrentIndex(min(4, i + 1)))
 
        # 4. Câbler le footer et le stepper sur le state store
        deps.state_store.stateChanged.connect(self._refresh_footer)
        deps.state_store.stateChanged.connect(self._refresh_stepper)
 
    def _pages(self):
        return [self.page1, self.page2, self.page3, self.page4, self.page5]
 
    def _on_step_changed(self, index: int):
        QgsSettings().setValue("qfit/ui/last_step_index", index)
        self._refresh_stepper()
 
    def _refresh_stepper(self):
        # Recalculer les états depuis deps.state_store et appeler stepperBar.set_state([...])
        ...
 
    def _refresh_footer(self):
        # Mettre à jour les pills du footer depuis deps.state_store
        ...
```
 
- Ne pas déplacer la logique métier dans les pages. Les pages émettent des signaux d'intention ; `qfit_dockwidget.py` les câble aux modules workflows existants.
- Conserver les dataclasses request/result existantes. N'en introduire de nouvelles que si une page émet un nouveau type d'intention.
- Objectif : `QfitDockWidget.__init__` < 120 lignes (actuellement > 300).
---
 
## 9. Feuille de style QSS (`ui/qss/qfit.qss`)
 
> ⚠️ **RÈGLE CRITIQUE** : Ne jamais appeler `QApplication.instance().setStyleSheet(...)`. Appliquer le QSS **uniquement sur le dock widget lui-même** pour éviter de polluer l'UI globale de QGIS et les autres plugins.
 
```python
# Dans qfit_plugin.py::initGui()
qss_path = os.path.join(os.path.dirname(__file__), 'ui', 'qss', 'qfit.qss')
with open(qss_path, encoding='utf-8') as f:
    self.dockWidget.setStyleSheet(f.read())
```
 
Extrait non-exhaustif du fichier `qfit.qss` (toutes les règles doivent être préfixées par `QfitDockWidgetBase` via le `objectName` du `QDockWidget`) :
 
```css
/* Fond général */
QfitDockWidgetBase { background: #f3f3f3; }
 
/* Bouton primaire */
QfitDockWidgetBase QPushButton[role="primary"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #68ad3e, stop:1 #4e8a2b);
    color: white; border: 1px solid #3f6e22;
    border-radius: 2px; padding: 4px 12px; font-weight: 600;
}
QfitDockWidgetBase QPushButton[role="primary"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #72ba45, stop:1 #579530);
}
QfitDockWidgetBase QPushButton[role="primary"]:disabled {
    background: #b0c9a0; border-color: #8aaa78;
}
 
/* Bouton ghost */
QfitDockWidgetBase QPushButton[role="ghost"] {
    background: transparent; border: 1px solid #b0b4ba;
    border-radius: 2px; padding: 4px 10px; color: #202124;
}
QfitDockWidgetBase QPushButton[role="ghost"]:hover { background: #e8e8e8; }
 
/* Bouton lien destructif */
QfitDockWidgetBase QPushButton[role="link-danger"] {
    background: transparent; border: 0;
    color: #c01c28; text-decoration: underline;
}
 
/* GroupBox */
QfitDockWidgetBase QGroupBox {
    border: 1px solid #c4c4c4; border-radius: 2px;
    margin-top: 8px; padding-top: 10px; background: #fafafa;
}
QfitDockWidgetBase QGroupBox::title {
    subcontrol-origin: margin; left: 8px; padding: 0 4px;
    font-weight: 600; color: #202124;
}
 
/* Label hint secondaire */
QfitDockWidgetBase QLabel[role="section-hint"] {
    color: #6b6f76; font-size: 11pt;
}
 
/* … compléter pour Pill, StepperChip, StyleCard, AnalysisCard … */
```
 
Ne jamais inliner des stylesheets sur des widgets individuels. Utiliser `setProperty("role", value)` + `widget.style().polish(widget)` après chaque changement de propriété.
 
---
 
## 10. Internationalisation
 
Toutes les chaînes visibles dans cette spec sont en français et doivent être wrappées dans `self.tr(...)` à la création. Mettre à jour `i18n/qfit_fr.ts` et `i18n/qfit_en.ts`.
 
| FR | EN |
|---|---|
| Connexion | Connect |
| Synchronisation | Sync |
| Carte | Map |
| Analyse | Analyze |
| Atlas | Atlas |
| Connecté | Connected |
| Non connecté | Not connected |
| Compte Strava lié | Strava account linked |
| Compte Strava non lié | Strava account not linked |
| Récupérer les nouvelles activités | Fetch new activities |
| Visualiser sur la carte | View on map |
| Passer à l'analyse | Go to analysis |
| Passer à l'atlas | Go to atlas |
| Générer PDF | Generate PDF |
| Précédent | Back |
| Configurer la connexion… | Configure connection… |
| Ouvrir la configuration… | Open configuration… |
| Tester la connexion | Test connection |
| Déconnecter | Disconnect |
| Réinitialiser… | Reset… |
| Recommencer | Restart |
| Lancer | Run |
| Appliquer | Apply |
| Prêt à exporter | Ready to export |
| Génération… | Generating… |
| Uniquement activités avec tracés détaillés | Only activities with detailed tracks |
| Fetch quand disponible | Fetch when available |
| Appliquer les filtres actifs de l'étape 3 | Apply step 3 filters |
| Aucune couche | No layers |
| activités | activities |
| couches | layers |
 
Lancer `pylupdate5` après chaque modification. Le français est la traduction de référence.
 
---
 
## 11. Tests & CI
 
- `tests/test_wizard_dockwidget.py` :
  - Instancier chaque page en isolation avec des dépendances factices ; vérifier l'arbre de widgets (pas de crash, objectNames attendus présents).
  - Tester le gating du stepper (§7) avec une matrice `pytest.mark.parametrize`.
  - Tester que cliquer "Suivant" sur un gate désactivé ne fait rien.
- `tests/test_stepper_gating.py` : machine à états isolée, couverture complète des transitions.
- `tests/test_widget_compat.py` : vérifier que `make_range_slider()` retourne le bon type selon la version QGIS mockée.
- Conserver `tests/test_qgis_smoke.py` vert.
- Smoke screenshot visuel (gated par `SKIP_VISUAL_TESTS`) : ouvrir le dock, snapshoter chacune des 5 pages, stocker sous `validation_artifacts/wizard/step{1..5}.png`.
---
 
## 12. Migration & settings
 
- Conserver toutes les clés `QgsSettings` existantes sous `qfit/*`. Ajouter :
  - `qfit/ui/wizard_version = 1`
  - `qfit/ui/last_step_index` (int, 0–4) — restauré au prochain lancement.
  - `qfit/ui/collapsed_groups` (stringlist des objectNames de `QgsCollapsibleGroupBox` qui doivent démarrer repliés — mémoire utilisateur). **Les objectNames à persister sont** : `advancedOptionsGroup`, `layoutGroup`, `temporalGroup`. Tous les autres commencent dans leur état par défaut spécifié dans les sections précédentes.
- Ne pas supprimer les clés obsolètes des anciens widgets — les garder lisibles pour que les downgrades soient sûrs.
- Au premier lancement avec la nouvelle UI, migrer transparentement les valeurs OAuth existantes vers la config dialog.
---
 
## 13. Notes techniques complémentaires
 
### 13.1 Pill dans le titre d'un `QgsCollapsibleGroupBox`
 
`QgsCollapsibleGroupBox` n'expose pas son titre-row comme un layout Qt standard. L'approche retenue est un **sous-classage léger** :
 
```python
class PillGroupBox(QgsCollapsibleGroupBox):
    """QgsCollapsibleGroupBox avec un Pill optionnel dans la zone titre."""
    def __init__(self, title: str, parent=None):
        super().__init__(title, parent)
        self._pill = None
 
    def set_pill(self, text: str, tone: str):
        if self._pill is None:
            self._pill = Pill(text, tone, parent=self)
        else:
            self._pill.update_text(text, tone)
        self._reposition_pill()
 
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition_pill()
 
    def _reposition_pill(self):
        if self._pill:
            h = self._pill.sizeHint().height()
            self._pill.move(self.width() - self._pill.sizeHint().width() - 8, (20 - h) // 2)
```
 
Utiliser `PillGroupBox` partout où la spec demande un groupe avec pill dans le titre (§3.4, §4.3).
 
### 13.2 Debounce des filtres (§4.2)
 
```python
# Dans Step3MapPage.__init__
self._filter_timer = QTimer(self)
self._filter_timer.setSingleShot(True)
self._filter_timer.setInterval(300)
self._filter_timer.timeout.connect(self._emit_filters_changed)
 
# Sur chaque signal de changement de filtre :
def _on_any_filter_changed(self):
    self._filter_timer.start()   # restart si déjà en cours
 
def _emit_filters_changed(self):
    self.filtersChanged.emit(self._build_filter_request())
```
 
### 13.3 Estimations Atlas (§6.4)
 
Les constantes de calcul **ne sont jamais dans le widget**. Elles sont dans `atlas/application/atlas_config.py` et appelées depuis le widget :
 
```python
from qfit.atlas.application.atlas_config import estimate_time_min, estimate_size_mb
 
# Dans Step5AtlasPage._refresh_estimates(n_pages):
self._estimateLabel.setText(
    f"{n_pages} pages · temps estimé ~{estimate_time_min(n_pages)} min "
    f"· taille ≈ {estimate_size_mb(n_pages)} MB"
)
```
 
---
 
## 14. Définition of done
 
- [ ] Le dock widget correspond visuellement aux maquettes Option B de l'audit UX.
- [ ] Tous les signaux publics existants de `qfit_dockwidget.py` sont conservés — les consommateurs aval ne doivent pas casser.
- [ ] Pas de régression fonctionnelle : chaque ancien flux utilisateur reste accessible en ≤ 2 clics supplémentaires.
- [ ] `QfitDockWidget.__init__` réduit à < 120 lignes.
- [ ] `make_range_slider()` testé sur QGIS < 3.38 et ≥ 3.38.
- [ ] Aucun appel à `QApplication.instance().setStyleSheet(...)` — QSS scopé au dock uniquement.
- [ ] `QgsDateTimeRangeWidget` absent du code (widget inexistant dans l'API publique).
- [ ] `QgsCheckableComboBox` absent du code (remplacé par `QListWidget` checkable).
- [ ] Nouveaux tests passent ; tests existants toujours verts ; `ruff` + `black` + `codeql` verts.
- [ ] Docs mises à jour : screenshot dans `docs/images/` remplacé ; note d'une ligne dans `README.md`.
- [ ] i18n : `pylupdate5` propre ; les deux fichiers `.ts` à jour ; le français est la traduction de référence.
- [ ] `qfit/ui/wizard_version = 1` écrit dans `QgsSettings` au premier lancement.
---
 
*Fin de la spec v2.0.*
