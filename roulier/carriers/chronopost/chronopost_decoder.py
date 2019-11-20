# -*- coding: utf-8 -*-
"""Dpd XML -> Python."""
from lxml import objectify
from roulier.codec import Decoder
from .chronopost_api import CHRONOPOST_LABEL_FORMAT


class ChronopostDecoder(Decoder):
    """Chronopost XML -> Python."""

    def decode(self, body, output_format):
        """Chronopost XML -> Python."""

        def create_shipment_with_labels(msg, output_format):
            """Understand a CreateShipmentWithLabelsResponse."""
            result = msg.getchildren()[0]
            tracking_ref = result.skybillNumber.text
            data = result.skybill.text.encode()
            x = {
                "parcels": [{
                    "id": 1,  # no multi parcel management for now.
                    "reference": "",
                    "tracking": {
                        'number': tracking_ref,
                        "url": "",
                    },
                    "label": {
                        "data": data,
                        "name": "label_%s" % tracking_ref,
                        "type": CHRONOPOST_LABEL_FORMAT.get(output_format,
                                                            output_format),
                    },
                }],
                "annexes": [],
            }
            return x
        xml = objectify.fromstring(body)
        return create_shipment_with_labels(xml, output_format)

    def decode_tracking(self, body, action):
        xml = objectify.fromstring(body)
        if action == "cancelSkybill":
            result = xml.getchildren()[0]
            success = result.errorCode.text == "0"
            x = {"result": success}
            return x
        if action == "trackSkybillV2":
            result = xml.getchildren()[0]
            x = {"events": [],
                 "skybillNumber": result.listEventInfoComp.skybillNumber}
            if hasattr(result.listEventInfoComp, "events"):
                for event in result.listEventInfoComp.events:
                    ev = {"code": event.code,
                          "eventDate": event.eventDate,
                          "eventLabel": event.eventLabel,
                          }
                    if hasattr(event, "infoCompList"):
                        ev["infoCompList"] = []
                        for info in event.infoCompList:
                            inf = {"name": info.name,
                                   "value": info.value}
                            ev["infoCompList"].append(inf)

                    x["events"].append(ev)
            return x
