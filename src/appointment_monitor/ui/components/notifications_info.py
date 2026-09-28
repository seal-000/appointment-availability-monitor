"""Notification channels and their enabled states."""

from pathlib import Path

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QSizePolicy,
	QVBoxLayout,
	QWidget,
)

from .notification_channel import NotificationChannel
from .status_tag import StatusTag


class NotificationsInfo(QFrame):
	"""Show configured notification channels and enabled indicators."""

	def __init__(self, parent: QWidget | None = None) -> None:
		"""Build the notification summary card using the supplied SVG assets."""
		super().__init__(parent)
		self.setObjectName("panel")
		self.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Maximum,
		)
		layout = QVBoxLayout(self)
		layout.setContentsMargins(16, 14, 16, 16)
		layout.setSpacing(10)

		icons_dir = Path(__file__).parents[1] / "resources" / "imgs"
		heading = QHBoxLayout()
		heading.setSpacing(10)
		heading.addWidget(
			self._icon_tile(icons_dir / "notifications_icon.svg", "notificationHeaderIcon")
		)

		title = QLabel("Notifications")
		title.setObjectName("notificationTitle")
		heading.addWidget(title)
		heading.addStretch()

		self.enabled_badge = StatusTag("Enabled")
		heading.addWidget(self.enabled_badge)
		layout.addLayout(heading)

		layout.addSpacing(4)
		layout.addWidget(
			NotificationChannel(
				"Email",
				"your@email.com",
				(icons_dir / "alternate_email_icon.svg",),
			)
		)
		layout.addWidget(
			NotificationChannel(
				"SMS",
				"+1 (516) XXX-XXXX",
				(icons_dir / "sms_enabled_icon.svg",),
			)
		)

	@staticmethod
	def _icon_tile(icon_source: Path | str, object_name: str) -> QLabel:
		"""Create a consistent icon tile from an SVG path or short text symbol."""
		icon = QLabel()
		icon.setObjectName(object_name)
		icon.setFixedSize(32, 32)
		icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
		if isinstance(icon_source, Path):
			icon.setPixmap(QIcon(str(icon_source)).pixmap(QSize(18, 18)))
		else:
			icon.setText(icon_source)
		return icon
