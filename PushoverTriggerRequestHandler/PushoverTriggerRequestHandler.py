#
#	PushoverTriggerRequestHandler.py
#
#	(c) 2026 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#
""" Pushover notification handler for TriggerRequest functionality. 
"""

from __future__ import annotations

from acmecse.runtime.PluginSupport import Service, plugin, endpoint, configure, validate, PluginConfigurationError
from acmecse.runtime.Logging import Logging as L
from acmecse.runtime.Configuration import Configuration
from acmecse.resources.TGR import TGR
from acmecse.etc.Types import TriggerStatus, TriggerPurpose
from acmecse.helpers.PushoverClient import PushoverClient, PushoverError

@plugin(tags=['triggerRequestHandler', 'pushover'])
class PushoverTriggerRequestHandler(Service):
	"""	Pushover notification handler for TriggerRequest functionality.

		This is a Pushover notification handler for TriggerRequest functionality. It sends notifications via the Pushover API
		to the assigned Pushover user or group key of the TriggerRequest resource. 

		The plugin can be configured via the *acme.ini* configuration file with the following settings:

			::

			[TriggerHandler.pushover]
			userKey=<Pushover user or group key>
			appToken=<Pushover application token>
			domain=<Domain for validating M2M-EXT-ID values, default: notification.example.com>
		
		These are only the default values. Individuel TriggerRequest resources can override these
		settings by providing the following labels in the TriggerRequest resource:

			- *userKey* : The Pushover user or group key to send the notification to.
			- *appToken* : The Pushover application token to use for sending the notification.

		Additionally, the following labels can be provided to customize the notification message:

			- *message* : The message to send in the notification. If not provided, a default message will be used based on the TriggerPurpose of the TriggerRequest resource.
			- *title* : The title of the notification. If not provided, a default title will be used.
	"""

	_message: dict[TriggerPurpose, str] = {
		None: "Establish connection",
		TriggerPurpose.establishConnection: "Establish connection",
		TriggerPurpose.registrationRequest: "Registration request",
		TriggerPurpose.executeCRUD: "Execute CRUD operation",
		TriggerPurpose.enrolmentRequest: "Enrolment request",
	}
	""" Internal dictionary to map TriggerPurpose values to default messages for Pushover notifications. """

	_configSection = 'TriggerHandler.pushover'
	""" Configuration section for the PushoverTriggerRequestHandler plugin.
	"""

	@configure
	def configure(self, config: Configuration) -> None:
		""" Configure the PushoverTriggerRequestHandler service. 

			Args:
				config: The configuration object for the PushoverTriggerRequestHandler service.
		"""
		parser = config.configParser
		self.userKey = parser.get(self._configSection, 'userKey', fallback=None)
		self.appToken = parser.get(self._configSection, 'appToken', fallback=None)
		self.domain = parser.get(self._configSection, 'domain', fallback='notification.example.com')


	@validate
	def validate(self, config: Configuration) -> None:
		""" Validate the PushoverTriggerRequestHandler service configuration.

			Args:
				config: The configuration object for the PushoverTriggerRequestHandler service.
		"""
		if not self.userKey:
			L.isWarn and L.logWarn(f'No userKey configured for PushoverTriggerRequestHandler. Provide it in the configuration or in the TriggerRequest resource labels.')
		if not self.appToken:
			L.isWarn and L.logWarn(f'No appToken configured for PushoverTriggerRequestHandler. Provide it in the configuration or in the TriggerRequest resource labels.')
		if not self.domain:
			raise PluginConfigurationError(f'No domain configured for PushoverTriggerRequestHandler. Provide it in the configuration in the section "[{self._configSection}]".')


	@endpoint('acceptsM2MExtID')
	def acceptsM2MExtID(self, m2mExtID: str) -> bool:
		""" Check whether the given m2mExtID is valid for this NSE handler, 
			that this handler can be used for triggering.
			
			Args:
				m2mExtID: The m2mExtID to check.
		"""
		return m2mExtID.endswith(f'@{self.domain}')


	@endpoint('sendTriggerRequest')
	def sendTriggerRequest(self, tgr: TGR) -> None:
		""" Send a TriggerRequest to the assigned NSE handler.

			Args:
				tgr: The TriggerRequest to send.
		"""
		L.isDebug and L.logDebug(f'Send Pushover notification for TriggerRequest {tgr.ri}')
		try:
			# Get optional values from the TriggerRequest resource's labels. 
			# If not provided, use the default values from the configuration.
			labels = dict(item.split(":", 1) for item in tgr.lbl) if tgr.lbl else {}

			userKey = labels.get('userKey', self.userKey)
			appToken = labels.get('appToken', self.appToken)
			message = labels.get('message', self._message.get(tgr.tpe, 'unknown purpose'))
			title = labels.get('title', f'TriggerRequest')

			if not userKey or not appToken:
				raise PushoverError('Missing userKey or appToken for Pushover notification. Provide them in the TriggerRequest resource labels or in the configuration.')

			# send the notification via the PushoverClient
			PushoverClient(token=appToken, user=userKey).sendNotification(message, title=title)
			tgr.setTriggerStatus(TriggerStatus.TRIGGER_DELIVERED)

			L.isDebug and L.logDebug(f'Successfully sent Pushover notification for TriggerRequest {tgr.ri}')
		except PushoverError as e:
			L.isWarn and L.logWarn(f'Failed to send Pushover notification for TriggerRequest {tgr.ri}: {e}')
			tgr.setTriggerStatus(TriggerStatus.TRIGGER_FAILED)


	@endpoint('checkTriggerRequestStatus')
	def checkTriggerRequestStatus(self, tgr: TGR) -> TriggerStatus:
		""" Check the status of a TriggerRequest.

			Args:
				tgr: The TriggerRequest to check.

			Returns:
				The current status of the TriggerRequest.
		"""
		# Just return the current triggerStatus attribute of the TriggerRequest resource.
		# The notification was already sent in the sendTriggerRequest method, and the status was set accordingly.
		return tgr.tst
	

	@endpoint('terminateTriggerRequest')
	def terminateTriggerRequest(self, tgr: TGR) -> None:
		""" Terminate a TriggerRequest.

			Args:
				tgr: The TriggerRequest to terminate.
		"""
		# Not much to do here for Pushover. """
		return

