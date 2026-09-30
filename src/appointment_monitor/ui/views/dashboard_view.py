"""Dashboard view for previewing appointment availability monitors."""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QVBoxLayout,
	QWidget,
)

from ..components import CreateMonitorForm, LastCheckText, MonitorTable, NotificationsInfo


MONITORS: list[dict[str, Any]] = [
	{
		"name": "Primary Clinic",
		"url": "https://clinic.example.com/appointments",
		"interval": 300,
		"status": "Running",
		"checked": "2 min ago",
		"result": "No availability at the moment",
	},
	{
		"name": "Dental Care",
		"url": "https://dental.example.com/bookings",
		"interval": 300,
		"status": "Appointment Found",
		"checked": "5 min ago",
		"result": "Appointment has been found at Dental Care",
	},
	{
		"name": "Lab Portal",
		"url": "https://lab.example.com/slots",
		"interval": 180,
		"status": "Error",
		"checked": "1 hr ago",
		"result": "HTTP 503 Service Unavailable",
	},
	{
		"name": "Urgent Care",
		"url": "https://urgent.example.com/appointments",
		"interval": 60,
		"status": "Running",
		"checked": "Just now",
		"result": "No availability at the moment",
	},
	{
		"name": "Specialist",
		"url": "https://specialist.example.com/visits",
		"interval": 3600,
		"status": "Stopped",
		"checked": "2 hr ago",
		"result": "Monitor has been stopped",
	},
]


class DashboardView(QWidget):
	"""Show the appointment monitor table, create form, and notification info."""

	def __init__(self, parent: QWidget | None = None) -> None:
		"""Build the dashboard and populate it with fictional monitor records."""
		super().__init__(parent)
		self.monitors = [monitor.copy() for monitor in MONITORS]
		self._build_ui()
		self._render_monitors()

	def _build_ui(self) -> None:
		"""Create the monitor table, action bar, form, and notification panel."""
		content_layout = QVBoxLayout(self)
		content_layout.setContentsMargins(24, 24, 24, 24)
		content_layout.setSpacing(16)

		heading_row = QHBoxLayout()
		heading = QLabel("Dashboard")
		heading.setObjectName("pageHeading")
		heading_row.addWidget(heading)
		heading_row.addStretch()
		self.summary_label = QLabel()
		self.summary_label.setObjectName("summaryLabel")
		heading_row.addWidget(self.summary_label)
		content_layout.addLayout(heading_row)

		subheading = QLabel("We'll check the web pages regularly and notify you when appointments become available.")
		subheading.setObjectName("sectionSubheading")
		content_layout.addWidget(subheading)

		monitor_panel = QFrame()
		monitor_panel.setObjectName("panel")
		monitor_layout = QVBoxLayout(monitor_panel)
		monitor_layout.setContentsMargins(16, 14, 16, 14)
		monitor_layout.setSpacing(10)

		table_title = QLabel("MONITORED APPOINTMENT PAGES")
		table_title.setObjectName("sectionLabel")
		monitor_layout.addWidget(table_title)

		self.table = MonitorTable()
		monitor_layout.addWidget(self.table)

		action_row = QHBoxLayout()
		action_row.setSpacing(8)
		self._add_action_button(action_row, "Remove", self._remove_selected)
		action_row.addStretch()
		self._add_action_button(action_row, "Start", lambda: self._set_selected_status("Running"))
		self._add_action_button(action_row, "Stop", lambda: self._set_selected_status("Stopped"))
		self._add_action_button(action_row, "Start All", lambda: self._set_all_status("Running"))
		self._add_action_button(action_row, "Stop All", lambda: self._set_all_status("Stopped"))
		monitor_layout.addLayout(action_row)
		content_layout.addWidget(monitor_panel)

		lower_row = QHBoxLayout()
		lower_row.setSpacing(16)
		self.create_monitor_form = CreateMonitorForm()
		self.create_monitor_form.monitor_created.connect(self._add_monitor)
		lower_row.addWidget(
			self.create_monitor_form,
			2,
			alignment=Qt.AlignmentFlag.AlignTop,
		)

		self.notifications_info = NotificationsInfo()
		lower_row.addWidget(
			self.notifications_info,
			1,
			alignment=Qt.AlignmentFlag.AlignTop,
		)
		content_layout.addLayout(lower_row, 1)

	def _add_action_button(
		self,
		layout: QHBoxLayout,
		text: str,
		callback: Any,
	) -> None:
		"""Add a compact action button."""
		button = QPushButton(text)
		button.clicked.connect(callback)
		layout.addWidget(button)

	def _render_monitors(self) -> None:
		"""Refresh table rows and the active-monitor summary from demo data."""
		self.table.set_monitors(self.monitors)
		running_count = sum(monitor["status"] == "Running" for monitor in self.monitors)
		self.summary_label.setText(f"{running_count} RUNNING  /  {len(self.monitors)} TOTAL")

	def _set_selected_status(self, status: str) -> None:
		"""Set the status for checked monitors, or the focused row if none are checked."""
		rows = self.table.checked_rows()
		if not rows and self.table.currentRow() >= 0:
			rows = [self.table.currentRow()]
		for row in rows:
			monitor = self.monitors[row]
			monitor["status"] = status
			monitor["checked"] = "Just now"
			monitor["result"] = self._status_detail(status, monitor["name"])
		self._render_monitors()

	def _add_monitor(self, monitor: dict[str, Any]) -> None:
		"""Add a monitor submitted by the create form to the demo table."""
		self.monitors.append(monitor)
		self._render_monitors()

	def _set_all_status(self, status: str) -> None:
		"""Set every demo monitor to the requested status."""
		for monitor in self.monitors:
			monitor["status"] = status
			monitor["checked"] = "Just now"
			monitor["result"] = self._status_detail(status, monitor["name"])
		self._render_monitors()

	@staticmethod
	def _status_detail(status: str, name: str) -> str:
		return LastCheckText.message_for(status, name)

	def _remove_selected(self) -> None:
		"""Remove checked demo monitors from the table."""
		selected = set(self.table.checked_rows())
		self.monitors = [
			monitor for index, monitor in enumerate(self.monitors) if index not in selected
		]
		self._render_monitors()
