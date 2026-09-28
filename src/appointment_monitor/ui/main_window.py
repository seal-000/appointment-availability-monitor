"""Top-level application window and view navigation."""

from pathlib import Path

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from .components import Sidebar
from .views.dashboard_view import DashboardView


class MainWindow(QMainWindow):
	"""Compose the app sidebar and active view in the top-level window."""

	def __init__(self) -> None:
		"""Create the main window and load its initial dashboard view."""
		super().__init__()
		self.setWindowTitle("Appointment Monitor")
		self.resize(1260, 790)
		self.setMinimumSize(940, 640)

		shell = QWidget()
		layout = QHBoxLayout(shell)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		self.sidebar = Sidebar()
		self.sidebar.navigation_requested.connect(self._show_view)
		layout.addWidget(self.sidebar)

		self.views = QStackedWidget()
		self.dashboard = DashboardView()
		self.views.addWidget(self.dashboard)
		layout.addWidget(self.views, 1)
		self.setCentralWidget(shell)

		stylesheet_path = Path(__file__).parent / "resources" / "styles.qss"
		stylesheet = stylesheet_path.read_text(encoding="utf-8")
		arrow_path = (
			stylesheet_path.parent / "imgs" / "dropdown-chevron.svg"
		).resolve().as_posix()
		stylesheet = stylesheet.replace(
			'url("imgs/dropdown-chevron.svg")',
			f'url("{arrow_path}")',
		)
		self.setStyleSheet(stylesheet)

	def _show_view(self, name: str) -> None:
		"""Show the dashboard until the other navigation views are implemented."""
		if name == "Dashboard":
			self.views.setCurrentWidget(self.dashboard)
		else:
			self.sidebar.set_active_page("Dashboard")