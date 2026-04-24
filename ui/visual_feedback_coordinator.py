"""Coordinator for visual feedback components (phase, progress, result indicators)."""

from __future__ import annotations

from qgis.PyQt.QtWidgets import QVBoxLayout

from ..design_system import (
    PhaseIndicator,
    ProgressFeedback,
    ResultIndicator,
    WorkflowPhase,
    WorkflowState,
)


class VisualFeedbackCoordinator:
    """Manages integration of visual feedback components into the dock."""

    def __init__(self, dock_widget):
        self.dock_widget = dock_widget
        self.phase_indicator: PhaseIndicator | None = None
        self.progress_feedback: ProgressFeedback | None = None
        self.result_indicator: ResultIndicator | None = None

    def setup_visual_components(self) -> None:
        """Initialize and insert visual feedback components into dock layout."""
        dock = self.dock_widget

        # Find the main layout
        main_layout = getattr(dock, "verticalLayout", None)
        if main_layout is None:
            return

        # Create phase indicator
        self.phase_indicator = PhaseIndicator(1, 6, "Connect to Strava")
        main_layout.insertWidget(0, self.phase_indicator)

        # Create progress feedback
        self.progress_feedback = ProgressFeedback()
        main_layout.insertWidget(1, self.progress_feedback)

        # Create result indicator
        self.result_indicator = ResultIndicator()
        main_layout.insertWidget(2, self.result_indicator)

    def on_state_changed(self, new_state: WorkflowState) -> None:
        """Handle workflow state changes."""
        if self.phase_indicator is None:
            return

        # Update phase indicator
        phase_num = new_state.phase.phase_number()
        phase_name = str(new_state.phase)
        self.phase_indicator.set_phase(phase_num, phase_name)

        # Update color based on phase
        phase_colors = {
            WorkflowPhase.CONNECT: "#E74C3C",  # Red
            WorkflowPhase.FETCH: "#3498DB",   # Blue
            WorkflowPhase.STORE: "#27AE60",   # Green
            WorkflowPhase.VISUALIZE: "#9B59B6",  # Purple
            WorkflowPhase.ANALYZE: "#E67E22",  # Orange
            WorkflowPhase.PUBLISH: "#2C3E50",  # Dark gray
        }
        color = phase_colors.get(new_state.phase, "#3498DB")
        self.phase_indicator.set_color(color)

        # Update progress feedback
        if self.progress_feedback is not None:
            if new_state.is_processing:
                self.progress_feedback.show_progress(new_state.processing_message)
            else:
                self.progress_feedback.hide_progress()

        # Update result indicator
        if self.result_indicator is not None:
            self.result_indicator.clear()
            if new_state.last_error:
                self.result_indicator.set_error(new_state.last_error)
            elif new_state.last_message:
                self.result_indicator.set_success(new_state.last_message)

    def show_processing(self, message: str) -> None:
        """Show processing feedback."""
        if self.progress_feedback:
            self.progress_feedback.show_progress(message)

    def hide_processing(self, final_message: str = "") -> None:
        """Hide processing feedback."""
        if self.progress_feedback:
            self.progress_feedback.hide_progress(final_message)

    def show_error(self, message: str, suggestion: str = "") -> None:
        """Display error result."""
        if self.result_indicator:
            self.result_indicator.set_error(message, suggestion)

    def show_success(self, message: str) -> None:
        """Display success result."""
        if self.result_indicator:
            self.result_indicator.set_success(message)

    def show_warning(self, message: str) -> None:
        """Display warning result."""
        if self.result_indicator:
            self.result_indicator.set_warning(message)

    def clear_feedback(self) -> None:
        """Clear all feedback displays."""
        if self.progress_feedback:
            self.progress_feedback.reset()
        if self.result_indicator:
            self.result_indicator.clear()
