"""Refactored workflow section coordinator using design system VisibilityCoordinator."""

from __future__ import annotations

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QToolButton, QVBoxLayout, QWidget

from ..design_system import VisibilityCoordinator, VisibilityRule
from ..mapbox_config import preset_requires_custom_style


class WorkflowSectionCoordinatorV2:
    """Coordinate dock-widget workflow sections with declarative visibility rules."""

    def __init__(self, dock_widget):
        self.dock_widget = dock_widget
        self._visibility_coordinator = None

    def configure_starting_sections(self) -> None:
        """Configure initial sections and layout."""
        dock = self.dock_widget
        dock.workflowLabel.setText("Workflow: Fetch & store → Visualize → Analyze → Publish")
        dock.credentialsGroupBox.hide()
        dock.activitiesGroupBox.setTitle("")
        dock.activitiesIntroLabel.setText(
            "Fetch your activities from Strava using the credentials saved in qfit → Configuration. "
            "Store or clear the local GeoPackage here too. Filters are applied later in the Visualize step — no re-fetch needed."
        )
        self._move_store_section_under_fetch()
        self._move_load_layers_to_visualize()
        self._move_temporal_controls_to_visualize()
        dock.outputGroupBox.setTitle("Store / database")
        dock.publishGroupBox.setCheckable(False)
        dock.publishSettingsWidget.setVisible(True)
        self.install_collapsible_section(
            dock.activitiesGroupBox,
            "activitiesGroupLayout",
            "1. Fetch and store activities",
            "activities",
        )
        self.install_collapsible_section(dock.styleGroupBox, "styleGroupLayout", "2. Visualize", "style")
        self.install_collapsible_section(
            dock.analysisWorkflowGroupBox,
            "analysisWorkflowLayout",
            "3. Analyze",
            "analysis",
        )
        self.install_collapsible_section(
            dock.publishGroupBox,
            "publishGroupLayout",
            "4. Publish / atlas",
            "publish",
        )
        dock.mapboxAccessTokenLabel.hide()
        dock.mapboxAccessTokenLineEdit.hide()

    def install_collapsible_section(self, group_box, layout_attr: str, title: str, key: str) -> None:
        """Install a collapsible section with toggle button."""
        dock = self.dock_widget
        layout = getattr(dock, layout_attr, None)
        toggle_attr = f"{key}SectionToggleButton"
        content_attr = f"{key}SectionContentWidget"

        if layout is None or hasattr(dock, toggle_attr):
            return

        group_box.setTitle("")

        # Create content container
        content_widget = QWidget(group_box)
        content_widget.setObjectName(f"{key}SectionContentWidget")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(layout.spacing())

        # Move existing widgets into content container
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            spacer = item.spacerItem()
            if widget is not None:
                content_layout.addWidget(widget)
            elif child_layout is not None:
                content_layout.addLayout(child_layout)
            elif spacer is not None:
                content_layout.addItem(spacer)

        # Create toggle button
        toggle = QToolButton(group_box)
        toggle.setObjectName(f"{key}SectionToggleButton")
        toggle.setText(title)
        toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toggle.setArrowType(Qt.DownArrow)
        toggle.setCheckable(True)
        toggle.setChecked(True)
        toggle.setStyleSheet("QToolButton { border: none; font-weight: bold; }")
        toggle.toggled.connect(lambda expanded, section_key=key: self.set_section_expanded(section_key, expanded))

        setattr(dock, toggle_attr, toggle)
        setattr(dock, content_attr, content_widget)
        layout.addWidget(toggle)
        layout.addWidget(content_widget)

    def set_section_expanded(self, key: str, expanded: bool) -> None:
        """Toggle section expansion."""
        dock = self.dock_widget
        toggle = getattr(dock, f"{key}SectionToggleButton", None)
        content = getattr(dock, f"{key}SectionContentWidget", None)
        if toggle is not None:
            toggle.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
        if content is not None:
            content.setVisible(expanded)

    def configure_workflow_sections(self) -> None:
        """Configure visibility rules for workflow sections."""
        dock = self.dock_widget

        # Build declarative visibility rules
        visibility_rules = [
            # Detailed streams toggle
            VisibilityRule(
                trigger_widget=dock.detailedStreamsCheckBox,
                target_widgets=[
                    dock.detailedRouteStrategyLabel,
                    dock.detailedRouteStrategyComboBox,
                    dock.maxDetailedActivitiesLabel,
                    dock.maxDetailedActivitiesSpinBox,
                ] + self._get_optional_widgets(dock, [
                    "backfillMissingDetailedRoutesButton",
                    "detailedRouteStrategyComboBoxContextHelpLabel",
                    "detailedRouteStrategyComboBoxHelpField",
                    "maxDetailedActivitiesSpinBoxContextHelpLabel",
                    "maxDetailedActivitiesSpinBoxHelpField",
                ]),
                condition=lambda w: w.isChecked(),
            ),
            # Point sampling toggle
            VisibilityRule(
                trigger_widget=dock.writeActivityPointsCheckBox,
                target_widgets=[
                    dock.pointSamplingStrideLabel,
                    dock.pointSamplingStrideSpinBox,
                ] + self._get_optional_widgets(dock, [
                    "pointSamplingStrideSpinBoxContextHelpLabel",
                    "pointSamplingStrideSpinBoxHelpField",
                ]),
                condition=lambda w: w.isChecked(),
            ),
            # Advanced fetch settings
            VisibilityRule(
                trigger_widget=dock.advancedFetchGroupBox,
                target_widgets=self._get_optional_widgets(dock, ["advancedFetchSettingsWidget"]),
                condition=lambda w: w.isChecked(),
            ),
            # Mapbox advanced settings
            VisibilityRule(
                trigger_widget=dock.backgroundPresetComboBox,
                target_widgets=[
                    dock.mapboxStyleOwnerLabel,
                    dock.mapboxStyleOwnerLineEdit,
                    dock.mapboxStyleIdLabel,
                    dock.mapboxStyleIdLineEdit,
                ] + self._get_optional_widgets(dock, [
                    "mapboxStyleOwnerLineEditContextHelpLabel",
                    "mapboxStyleIdLineEditContextHelpLabel",
                    "mapboxStyleIdLineEditHelpField",
                ]),
                condition=lambda w: preset_requires_custom_style(w.currentText()),
            ),
        ]

        # Initialize visibility coordinator
        self._visibility_coordinator = VisibilityCoordinator(visibility_rules)
        self._visibility_coordinator.apply_all()

    def _get_optional_widgets(self, dock, widget_names: list[str]) -> list:
        """Get widgets if they exist, skip if not."""
        widgets = []
        for name in widget_names:
            widget = getattr(dock, name, None)
            if widget is not None:
                widgets.append(widget)
        return widgets

    def _move_store_section_under_fetch(self) -> None:
        """Move store section under fetch section."""
        dock = self.dock_widget
        outer_layout = getattr(dock, "verticalLayout", None)
        activities_layout = getattr(dock, "activitiesGroupLayout", None)
        if outer_layout is None or activities_layout is None:
            return
        if dock.outputGroupBox.parent() is dock.activitiesGroupBox:
            return
        outer_layout.removeWidget(dock.outputGroupBox)
        dock.outputGroupBox.setParent(dock.activitiesGroupBox)
        activities_layout.addWidget(dock.outputGroupBox)

    def _move_load_layers_to_visualize(self) -> None:
        """Move load layers button to visualize section."""
        dock = self.dock_widget
        output_layout = getattr(dock, "outputGroupLayout", None)
        style_layout = getattr(dock, "styleGroupLayout", None)
        if output_layout is None or style_layout is None:
            return
        if dock.loadLayersButton.parent() is dock.styleGroupBox:
            return
        output_layout.removeWidget(dock.loadLayersButton)
        dock.loadLayersButton.setParent(dock.styleGroupBox)
        style_layout.insertWidget(0, dock.loadLayersButton)

    def _move_temporal_controls_to_visualize(self) -> None:
        """Move temporal controls to visualize section."""
        dock = self.dock_widget
        analysis_layout = getattr(dock, "analysisWorkflowLayout", None)
        style_layout = getattr(dock, "styleGroupLayout", None)
        temporal_row = getattr(dock, "analysisTemporalModeRow", None)
        temporal_help = getattr(dock, "temporalHelpLabel", None)
        if analysis_layout is None or style_layout is None or temporal_row is None or temporal_help is None:
            return
        if temporal_row.parent() is dock.styleGroupBox:
            return
        analysis_layout.removeWidget(temporal_row)
        analysis_layout.removeWidget(temporal_help)
        temporal_row.setParent(dock.styleGroupBox)
        temporal_help.setParent(dock.styleGroupBox)
        style_layout.addWidget(temporal_row)
        style_layout.addWidget(temporal_help)
