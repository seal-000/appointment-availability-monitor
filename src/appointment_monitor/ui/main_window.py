"""Top-level application window and view navigation."""

from pathlib import Path

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from .components import Sidebar
from .views.dashboard_view import DashboardView
from .views.about_view import AboutView
from .views.settings_view import SettingsView
from .views.logs_view import LogsView


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
		self.pages = {
			"Dashboard": self.dashboard,
			"Settings": SettingsView(),
			"Logs": LogsView("Logs"),
			"About": AboutView("About"),
		}
		for page in self.pages.values():
			self.views.addWidget(page)
		layout.addWidget(self.views, 1)
		self.setCentralWidget(shell)

		stylesheet_path = Path(__file__).parent / "resources" / "styles.qss"
		stylesheet = stylesheet_path.read_text(encoding="utf-8")
		arrow_path = (
			stylesheet_path.parent / "imgs" / "dropdown-chevron.svg"
		).resolve().as_posix()
		check_path = (
			stylesheet_path.parent / "imgs" / "check_icon.svg"
		).resolve().as_posix()
		stylesheet = stylesheet.replace(
			'url("imgs/dropdown-chevron.svg")',
			f'url("{arrow_path}")',
		)
		stylesheet = stylesheet.replace(
			'url("imgs/check_icon.svg")',
			f'url("{check_path}")',
		)
		self.setStyleSheet(stylesheet)

	def _show_view(self, name: str) -> None:
		"""Show the selected navigation view when it exists."""
		page = self.pages.get(name)
		if page is not None:
			self.views.setCurrentWidget(page)