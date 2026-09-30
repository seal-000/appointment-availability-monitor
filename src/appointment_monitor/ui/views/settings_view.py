"""Settings for notification integrations."""

import keyring
from PyQt6.QtCore import QRegularExpression, QSettings
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (
	QCheckBox,
	QFormLayout,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QPushButton,
	QVBoxLayout,
	QWidget,
)


class SettingsView(QWidget):
	"""Configure Twilio SMS credentials and phone numbers."""

	_SERVICE_NAME = "appointment-availability-monitor"
	_TOKEN_USERNAME = "twilio-auth-token"

	def __init__(self, parent: QWidget | None = None) -> None:
		super().__init__(parent)
		settings = QSettings("Appointment Monitor", "Appointment Availability Monitor")

		layout = QVBoxLayout(self)
		layout.setContentsMargins(24, 24, 24, 24)
		layout.setSpacing(16)

		heading = QLabel("Settings")
		heading.setObjectName("pageHeading")
		layout.addWidget(heading)

		section_heading = QLabel("Twilio SMS")
		section_heading.setObjectName("notificationTitle")
		layout.addWidget(section_heading)

		description = QLabel(
			"Enter your Twilio account details and the phone numbers for SMS alerts."
		)
		description.setWordWrap(True)
		layout.addWidget(description)

		self.sms_enabled = QCheckBox("Enable phone (SMS) notifications")
		self.sms_enabled.setChecked(
			settings.value("notifications/sms_enabled", False, type=bool)
		)
		layout.addWidget(self.sms_enabled)
		self.email_enabled = QCheckBox("Enable email notifications")
		self.email_enabled.setChecked(
			settings.value("notifications/email_enabled", False, type=bool)
		)
		layout.addWidget(self.email_enabled)

		form = QFormLayout()
		form.setHorizontalSpacing(16)
		form.setVerticalSpacing(12)
		self.account_sid = QLineEdit(settings.value("twilio/account_sid", ""))
		self.account_sid.setPlaceholderText("AC...")
		form.addRow("Account SID", self.account_sid)

		self.auth_token = QLineEdit()
		self.auth_token.setEchoMode(QLineEdit.EchoMode.Password)
		self.auth_token.setPlaceholderText("Twilio Auth Token")
		try:
			self.auth_token.setText(
				keyring.get_password(self._SERVICE_NAME, self._TOKEN_USERNAME) or ""
			)
		except keyring.errors.KeyringError:
			pass
		form.addRow("Auth Token", self.auth_token)

		self.from_number = QLineEdit(settings.value("twilio/from_number", ""))
		self.from_number.setPlaceholderText("+15551234567")
		form.addRow("Twilio phone number", self.from_number)

		self.to_number = QLineEdit(settings.value("twilio/to_number", ""))
		self.to_number.setPlaceholderText("+15557654321")
		form.addRow("Alert recipient", self.to_number)

		self.email_address = QLineEdit(
			settings.value("notifications/email_address", "")
		)
		self.email_address.setPlaceholderText("your@email.com")
		self.email_address.setValidator(
			QRegularExpressionValidator(
				QRegularExpression(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
			)
		)
		form.addRow("Alert recipient email", self.email_address)
		layout.addLayout(form)

		actions = QHBoxLayout()
		self.save_button = QPushButton("Save settings")
		self.save_button.setObjectName("startMonitoringButton")
		self.save_button.clicked.connect(self._save_settings)
		actions.addWidget(self.save_button)
		self.status = QLabel("")
		self.status.setObjectName("settingsStatus")
		actions.addWidget(self.status, 1)
		layout.addLayout(actions)
		layout.addStretch()

	def _save_settings(self) -> None:
		"""Persist the phone details and store the token in the OS keyring."""
		account_sid = self.account_sid.text().strip()
		auth_token = self.auth_token.text().strip()
		from_number = self.from_number.text().strip()
		to_number = self.to_number.text().strip()
		email_address = self.email_address.text().strip()
		if self.sms_enabled.isChecked() and not all(
			(account_sid, auth_token, from_number, to_number)
		):
			self.status.setText("Complete all four fields to save Twilio settings.")
			return
		if self.email_enabled.isChecked() and not self.email_address.hasAcceptableInput():
			self.status.setText("Enter a valid alert recipient email address.")
			return

		if self.sms_enabled.isChecked():
			try:
				keyring.set_password(
					self._SERVICE_NAME, self._TOKEN_USERNAME, auth_token
				)
			except keyring.errors.KeyringError:
				self.status.setText("Could not access the system credential store.")
				return

		settings = QSettings("Appointment Monitor", "Appointment Availability Monitor")
		settings.setValue("notifications/sms_enabled", self.sms_enabled.isChecked())
		settings.setValue("notifications/email_enabled", self.email_enabled.isChecked())
		settings.setValue("twilio/account_sid", account_sid)
		settings.setValue("twilio/from_number", from_number)
		settings.setValue("twilio/to_number", to_number)
		settings.setValue("notifications/email_address", email_address)
		self.status.setText("Notification preferences saved.")
