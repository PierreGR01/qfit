# QFit Plugin Redesign Integration Guide

## Overview

This guide describes the phased integration of the UX redesign components into the existing QFit plugin. The redesign introduces a reusable design system with improved workflow visibility, better error messaging, and cleaner architecture.

**Current UX Score:** 3.8/5 → **Target:** 4.8/5

---

## Phase 1: Design System Setup ✅

### Components Created

- **`design_system/__init__.py`** - Main package exports
- **`design_system/settings_field.py`** - Declarative settings bindings
  - `SettingsField`, `TextSettingsField`, `IntSettingsField`, etc.
  - `SettingsBinder` for load/save operations
  
- **`design_system/visibility_coordinator.py`** - Declarative visibility rules
  - `VisibilityRule`, `VisibilityCoordinator`
  
- **`design_system/workflow_state.py`** - Immutable workflow state machine
  - `WorkflowPhase`, `WorkflowState`, `WorkflowStateMachine`
  
- **`design_system/phase_indicator.py`** - Visual phase progress indicator
- **`design_system/progress_feedback.py`** - Loading/progress display
- **`design_system/result_indicator.py`** - Success/error/warning display
- **`design_system/user_facing_error.py`** - Actionable error messages

---

## Phase 2: Refactored Components (Ready to Integrate)

### New Implementation Files

1. **`configuration/application/dock_settings_bindings_v2.py`** 
   - Refactored from original `dock_settings_bindings.py`
   - Uses `SettingsBinder` instead of `UIFieldBinding` lambdas
   - Organized by functional groups (credentials, fetch, search, etc.)
   - **Reduces code from 156 lines → ~40 lines**

2. **`ui/workflow_section_coordinator_v2.py`**
   - Refactored from `workflow_section_coordinator.py`
   - Uses `VisibilityCoordinator` for declarative rules
   - Replaces 8+ manual setVisible() calls with 4 `VisibilityRule`s
   - **Reduces code from 211 lines → ~150 lines**

3. **`ui/visual_feedback_coordinator.py`** (New)
   - Manages integration of visual components
   - Coordinates PhaseIndicator, ProgressFeedback, ResultIndicator
   - Responds to workflow state changes

---

## Phase 3: Integration Steps

### Step 1: Add Visual Feedback Components to Dock

**File:** `qfit_dockwidget.py`

```python
from .ui.visual_feedback_coordinator import VisualFeedbackCoordinator

class QfitDockWidget(QDockWidget, FORM_CLASS):
    def __init__(self, ...):
        # ... existing code ...
        
        # Initialize visual feedback after UI setup
        self._visual_feedback = VisualFeedbackCoordinator(self)
        self._visual_feedback.setup_visual_components()
```

**Impact:** +0.5/5 UX (phase visibility + progress feedback + result indicators)

---

### Step 2: Migrate Settings Bindings (Optional - Backwards Compatible)

**Current code (still works):**
```python
from .configuration.application.dock_settings_bindings import build_dock_settings_bindings
bindings = build_dock_settings_bindings(self)
load_bindings(bindings, settings_service)
save_bindings(bindings, settings_service)
```

**New code (cleaner):**
```python
from .configuration.application.dock_settings_bindings_v2 import build_dock_settings_bindings_v2
binder = build_dock_settings_bindings_v2(self)
binder.load(settings_service)
binder.save(settings_service)
```

**Impact:** -115 lines of code, better maintainability

---

### Step 3: Migrate Visibility Coordinator (Optional)

**Current code (still works):**
```python
self._workflow_section_coordinator = WorkflowSectionCoordinator(self)
self._workflow_section_coordinator.configure_workflow_sections()
```

**New code (declarative):**
```python
from .ui.workflow_section_coordinator_v2 import WorkflowSectionCoordinatorV2
coordinator = WorkflowSectionCoordinatorV2(self)
coordinator.configure_workflow_sections()  # Uses VisibilityCoordinator internally
```

**Impact:** -60 lines of code, clearer intent

---

## Phase 4: Advanced Features (Optional)

### Integrate WorkflowStateMachine

For more sophisticated workflow management:

```python
from design_system import WorkflowStateMachine, WorkflowPhase

self._state_machine = WorkflowStateMachine()
self._state_machine.state_changed.connect(self._on_state_changed)

# Transitions are validated
if self._state_machine.can_transition(WorkflowPhase.FETCH):
    self._state_machine.transition(WorkflowPhase.FETCH)
    self._state_machine.mark_processing("Fetching activities...")
```

### Use UserFacingError

Replace raw error strings with actionable messages:

```python
from design_system import ErrorFactory

try:
    activities = strava_api.fetch(...)
except StravAAPIError as e:
    error = ErrorFactory.create_api_error(e.status_code, original_error=e)
    self._visual_feedback.show_error(error.message, error.suggestion)
    logger.debug(error.technical_detail)
```

---

## Migration Checklist

- [ ] Design system created and tested
- [ ] `dock_settings_bindings_v2.py` ready (tested independently)
- [ ] `workflow_section_coordinator_v2.py` ready (tested independently)
- [ ] `visual_feedback_coordinator.py` integrated into dock
- [ ] PhaseIndicator displaying current phase
- [ ] ProgressFeedback showing during long operations
- [ ] ResultIndicator showing success/error after operations
- [ ] Optional: Migrate settings bindings to `SettingsBinder`
- [ ] Optional: Migrate visibility coordinator to v2
- [ ] Optional: Integrate `WorkflowStateMachine`
- [ ] All tests passing
- [ ] UX audit confirms 4.8/5 score

---

## Code Examples

### Example 1: Using SettingsField

```python
from design_system import TextSettingsField, IntSettingsField, SettingsBinder

fields = [
    TextSettingsField("api_key", "", widget=self.apiKeyInput),
    IntSettingsField("timeout", 30, widget=self.timeoutSpinBox),
]

binder = SettingsBinder(fields)
binder.load(qgsSettings)      # Load from settings
binder.save(qgsSettings)      # Save to settings
```

### Example 2: Using VisibilityCoordinator

```python
from design_system import VisibilityRule, VisibilityCoordinator

rules = [
    VisibilityRule(
        trigger_widget=self.advancedCheckBox,
        target_widgets=[self.advancedLabel, self.advancedCombo],
        condition=lambda w: w.isChecked()
    ),
]

coordinator = VisibilityCoordinator(rules)
coordinator.apply_all()  # Initialize visibility
```

### Example 3: Using Workflow State Machine

```python
from design_system import WorkflowStateMachine, WorkflowPhase

state_machine = WorkflowStateMachine()
state_machine.state_changed.connect(self._on_state_changed)

# Validate transition
if state_machine.can_transition(WorkflowPhase.FETCH):
    state_machine.transition(WorkflowPhase.FETCH)
    state_machine.mark_processing("Fetching activities...")
    # ... do work ...
    state_machine.mark_success("Fetched 42 activities")
```

---

## Testing Strategy

### Unit Tests

```bash
pytest tests/test_settings_field.py
pytest tests/test_visibility_coordinator.py
pytest tests/test_workflow_state.py
pytest tests/test_phase_indicator.py
```

### Integration Tests

```bash
pytest tests/integration/test_visual_feedback_coordinator.py
pytest tests/integration/test_dock_with_redesign.py
```

### Manual Testing

1. Open QFit dock
2. Verify PhaseIndicator shows "Phase 1/6 — Connect to Strava"
3. Click Fetch button
4. ProgressFeedback should appear with spinner
5. After completion, ResultIndicator should show success/error
6. Verify phase transitions update indicator color and number

---

## Backwards Compatibility

All new components are **opt-in**:

- Old `UIFieldBinding` continues to work
- Old `WorkflowSectionCoordinator` continues to work
- Visual feedback components can be added independently
- No breaking changes to existing code

You can migrate gradually or all at once.

---

## Performance Considerations

- **VisibilityCoordinator:** Minimal overhead (connects to Qt signals once during init)
- **SettingsBinder:** Same performance as old lambdas, slightly faster loading
- **Visual components:** Rendered on-demand (only visible when needed)
- **WorkflowStateMachine:** Zero overhead (no-op when not actively used)

---

## Support & Questions

For implementation help:
1. Review the design system source in `design_system/`
2. Check integration examples in this file
3. Run tests to verify components work
4. File issues in the project repository

---

**Document prepared for implementation guidance.**  
**Target completion: 6-7 days (as per audit estimate)**
