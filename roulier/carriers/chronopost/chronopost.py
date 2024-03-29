# -*- coding: utf-8 -*-
"""Implementation for Dpd."""

from .chronopost_decoder import ChronopostDecoder
from .chronopost_encoder import ChronopostEncoder
from .chronopost_transport import ChronopostTransport
from roulier.carrier import Carrier


class Chronopost(Carrier):
    """Implementation for Dpd."""

    encoder = ChronopostEncoder()
    decoder = ChronopostDecoder()
    ws = ChronopostTransport()

    def api(self):
        """Expose how to communicate with a Chronopost."""
        return self.encoder.api()

    def get(self, data, action):
        """Run an action with data against Chronopost WS."""
        request = self.encoder.encode(data, action)
        response = self.ws.send(request)
        return self.decoder.decode(
            response['body'],
            request['output_format'])


#    def get(self, data, action):
#        """Run an action with data against Dpd WS."""
#        request = self.encoder.encode(data, action)
#        response = self.ws.send(request)

#    # shortcuts
    def get_label(self, data):
        """Genereate a shipping label."""
        return self.get(data, 'shipping')


    def cancel_skybill(self, data):
        """Cancel a skybill."""

        action = "cancelSkybill"
        tracking_data = {
            "accountNumber": data["login"],
            "password": data["password"],
            "skybillNumber": data["skybillNumber"],
            "language": data["language"],
        }
        response = self.ws.send_tracking_request(tracking_data, action)
        return self.decoder.decode_tracking(response['body'], action)

    def track_skybill(self, data):
        """Track a skybill."""

        action = "trackSkybillV2"
        tracking_data = {
            "skybillNumber": data["skybillNumber"],
            "language": data["language"]
        }
        response = self.ws.send_tracking_request(tracking_data, action)
        return self.decoder.decode_tracking(response['body'], action)
