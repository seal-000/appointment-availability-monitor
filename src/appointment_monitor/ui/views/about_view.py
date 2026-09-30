"""Simple titled view used for sections that are not implemented yet."""

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class AboutView(QWidget):
	"""Display a page heading with an otherwise empty content area."""

	def __init__(self, title: str, parent: QWidget | None = None) -> None:
		super().__init__(parent)
		layout = QVBoxLayout(self)
		layout.setContentsMargins(24, 24, 24, 24)

		heading = QLabel(title)
		heading.setObjectName("pageHeading")
		layout.addWidget(heading)

		intro = QLabel(
			"Appointment Monitor checks configured appointment pages and can notify you "
			"when a slot opens."
		)
		intro.setObjectName("aboutIntro")
		intro.setWordWrap(True)
		intro.setMaximumWidth(900)
		layout.addWidget(intro)

		layout.addSpacing(12)
		setup_heading = QLabel("Required setup")
		setup_heading.setObjectName("aboutSectionTitle")
		layout.addWidget(setup_heading)

		setup_text = QLabel(
			"For SMS alerts, you need an active Twilio account. In Settings, enter your "
			"Account SID, Auth Token, Twilio phone number, and alert recipient number; "
			"then enable SMS and save. SMS alerts will not work without valid Twilio "
			"credentials and phone numbers.\n\n"
			"For email alerts, enter a valid recipient email address, enable email "
			"notifications, and save your settings."
		)
		setup_text.setObjectName("aboutBody")
		setup_text.setWordWrap(True)
		setup_text.setMaximumWidth(900)
		layout.addWidget(setup_text)

		layout.addSpacing(12)
		sections_heading = QLabel("Application sections")
		sections_heading.setObjectName("aboutSectionTitle")
		layout.addWidget(sections_heading)

		sections_text = QLabel(
			"Dashboard: manage appointment monitors.\n"
			"Settings: configure notification preferences.\n"
			"Logs: review recent application activity.\n"
			"About: application information and credits."
		)
		sections_text.setObjectName("aboutBody")
		sections_text.setWordWrap(True)
		sections_text.setMaximumWidth(900)
		layout.addWidget(sections_text)
		layout.addStretch()