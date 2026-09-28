"""Appointment-monitor table widget and row rendering."""

from collections.abc import Mapping, Sequence

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem

from .status_tag import StatusTag


MonitorRecord = Mapping[str, str | int]


class MonitorTable(QTableWidget):
	"""Display monitor records and expose checked row indices to its owner."""

	def __init__(self, parent=None) -> None:
		"""Create a configured, read-only table with a checkbox column."""
		super().__init__(0, 7, parent)
		self.setHorizontalHeaderLabels(
			["", "NAME", "URL", "INTERVAL", "STATUS", "LAST CHECKED", "LAST RESULT"]
		)
		self.verticalHeader().setVisible(False)
		self.setAlternatingRowColors(True)
		self.setShowGrid(False)
		self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
		self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
		self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
		self.setMinimumHeight(250)

		header = self.horizontalHeader()
		header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
		header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
		header.resizeSection(0, 44)
		for column in (1, 3, 4, 5):
			header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)

	def set_monitors(self, monitors: Sequence[MonitorRecord]) -> None:
		"""Replace the visible rows with the supplied monitor records."""
		self.setRowCount(len(monitors))
		for row_index, monitor in enumerate(monitors):
			checkbox = QTableWidgetItem()
			checkbox.setFlags(
				Qt.ItemFlag.ItemIsEnabled
				| Qt.ItemFlag.ItemIsUserCheckable
				| Qt.ItemFlag.ItemIsSelectable
			)
			checkbox.setCheckState(Qt.CheckState.Unchecked)
			checkbox.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
			self.setItem(row_index, 0, checkbox)

			values = (
				(1, monitor["name"]),
				(2, monitor["url"]),
				(3, f'{monitor["interval"]} s'),
				(5, monitor["checked"]),
				(6, monitor["result"]),
			)
			for column, value in values:
				item = QTableWidgetItem(str(value))
				item.setToolTip(str(value))
				if column == 6 and str(value).startswith(("503", "404")):
					item.setForeground(QColor("#A34B43"))
				self.setItem(row_index, column, item)

			status = str(monitor["status"])
			variant = "success" if status == "Active" else "warning"
			self.setCellWidget(row_index, 4, StatusTag(status, variant))
			self.setRowHeight(row_index, 42)

	def checked_rows(self) -> list[int]:
		"""Return row indices whose checkbox is checked."""
		return [
			row
			for row in range(self.rowCount())
			if self.item(row, 0).checkState() == Qt.CheckState.Checked
		]