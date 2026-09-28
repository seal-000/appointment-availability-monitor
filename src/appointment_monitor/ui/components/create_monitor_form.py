"""Form for adding an appointment page to the monitor list."""

from pathlib import Path

from PyQt6.QtCore import QSize, Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
	QComboBox,
	QFrame,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QPushButton,
	QSizePolicy,
	QVBoxLayout,
)


class CreateMonitorForm(QFrame):
	"""Collect monitor details and emit a validated demo monitor record."""

	monitor_created = pyqtSignal(dict)

	def __init__(self, parent=None) -> None:
		"""Build the name, URL, interval, and start-monitoring controls."""
		super().__init__(parent)
		self.setObjectName("panel")
		self.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Maximum,
		)
		layout = QVBoxLayout(self)
		layout.setContentsMargins(16, 14, 16, 16)
		layout.setSpacing(8)

		title = QLabel("CREATE MONITOR")
		title.setObjectName("sectionLabel")
		layout.addWidget(title)

		self.name_input = self._add_text_field(
			layout,
			"Name",
			"e.g. Primary Clinic",
		)
		self.url_input = self._add_text_field(
			layout,
			"URL",
			"https://example.com/appointments",
		)

		bottom_row = QHBoxLayout()
		bottom_row.setSpacing(12)

		interval_column = QVBoxLayout()
		interval_column.setSpacing(5)
		interval_label = QLabel("Check interval")
		interval_label.setObjectName("formLabel")
		interval_column.addWidget(interval_label)
		self.interval_combo = QComboBox()
		for minutes in (5, 10, 15, 30):
			self.interval_combo.addItem(f"{minutes} minutes", minutes * 60)
		interval_column.addWidget(self.interval_combo)
		bottom_row.addLayout(interval_column, 1)

		self.start_button = QPushButton("Start Monitoring")
		self.start_button.setObjectName("startMonitoringButton")
		play_icon = Path(__file__).parents[1] / "resources" / "imgs" / "play-arrow-icon.svg"
		self.start_button.setIcon(QIcon(str(play_icon)))
		self.start_button.setIconSize(QSize(18, 18))
		self.start_button.setMinimumHeight(44)
		self.start_button.clicked.connect(self._submit)
		bottom_row.addWidget(
			self.start_button,
			2,
			alignment=Qt.AlignmentFlag.AlignBottom,
		)
		layout.addLayout(bottom_row)

		self.error_label = QLabel()
		self.error_label.setObjectName("formError")
		self.error_label.setWordWrap(True)
		layout.addWidget(self.error_label)

	@staticmethod
	def _add_text_field(layout: QVBoxLayout, label_text: str, placeholder: str) -> QLineEdit:
		"""Add a labeled single-line text input and return the input widget."""
		label = QLabel(label_text)
		label.setObjectName("formLabel")
		layout.addWidget(label)
		field = QLineEdit()
		field.setObjectName("formInput")
		field.setPlaceholderText(placeholder)
		field.setClearButtonEnabled(True)
		layout.addWidget(field)
		return field

	def _submit(self) -> None:
		"""Validate the entered details and emit a monitor record."""
		name = self.name_input.text().strip()
		url_text = self.url_input.text().strip()
		url = QUrl(url_text)

		if not name:
			self.error_label.setText("Enter a name for this monitor.")
			self.name_input.setFocus()
			return
		if url.scheme().lower() not in ("http", "https") or not url.host():
			self.error_label.setText("Enter a valid HTTP or HTTPS URL.")
			self.url_input.setFocus()
			return

		self.error_label.clear()
		self.monitor_created.emit(
			{
				"name": name,
				"url": url.toString(),
				"interval": int(self.interval_combo.currentData()),
				"status": "Active",
				"checked": "Just now",
				"result": "Waiting for first check",
			}
		)
		self.name_input.clear()
		self.url_input.clear()