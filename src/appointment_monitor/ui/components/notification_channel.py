"""A notification channel row with icons, contact detail, and state."""

from collections.abc import Sequence
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


class NotificationChannel(QFrame):
	"""Show a notification method and its configured contact information."""

	def __init__(
		self,
		name: str,
		contact: str,
		icons: Sequence[Path] | str,
		parent: QWidget | None = None,
		*,
		enabled: bool = True,
	) -> None:
		"""Build one compact row from its icon files, label, and contact value."""
		super().__init__(parent)
		self.setObjectName("notificationChannel")
		self.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Fixed,
		)
		self.setFixedHeight(68)

		layout = QHBoxLayout(self)
		layout.setContentsMargins(0, 4, 0, 4)
		layout.setSpacing(12)

		icon_group = QWidget()
		icon_group.setObjectName("notificationIconGroup")
		icon_layout = QHBoxLayout(icon_group)
		icon_layout.setContentsMargins(0, 0, 0, 0)
		icon_layout.setSpacing(5)
		icon_items = (icons,) if isinstance(icons, str) else tuple(icons)
		icon_group.setFixedWidth(max(32, 32 * len(icon_items) + 5 * (len(icon_items) - 1)))
		for icon_source in icon_items:
			icon = QLabel()
			icon.setObjectName("notificationIconTile")
			icon.setFixedSize(32, 32)
			icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
			if isinstance(icon_source, Path):
				icon.setPixmap(QIcon(str(icon_source)).pixmap(QSize(17, 17)))
			else:
				icon.setText(icon_source)
			icon_layout.addWidget(icon)
		layout.addWidget(icon_group)

		text_layout = QVBoxLayout()
		text_layout.setContentsMargins(0, 0, 0, 0)
		text_layout.setSpacing(1)
		channel_name = QLabel(name)
		channel_name.setObjectName("notificationChannelName")
		text_layout.addWidget(channel_name)
		contact_label = QLabel(contact)
		contact_label.setObjectName("notificationContact")
		text_layout.addWidget(contact_label)
		layout.addLayout(text_layout, 1)

		status_icon_name = "check_icon.svg" if enabled else "close_icon.svg"
		status_icon_path = Path(__file__).parents[1] / "resources" / "imgs" / status_icon_name
		status_icon = QLabel()
		status_icon.setObjectName("notificationIndicator")
		status_icon.setAccessibleName(
			f"{name} {'enabled' if enabled else 'disabled'}"
		)
		status_icon.setToolTip("Enabled" if enabled else "Disabled")
		status_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
		status_icon.setFixedSize(22, 22)
		status_icon.setPixmap(QIcon(str(status_icon_path)).pixmap(QSize(18, 18)))
		layout.addWidget(status_icon)