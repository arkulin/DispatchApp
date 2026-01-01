from kivy.uix.screenmanager import Screen
import json
import os


class AirportScreen(Screen):
    """Screen for displaying airport information."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'airports.json')
        with open(file_path, 'r') as f:
            self.data = json.load(f)

    def search_airport(self, *_):
        icao = self.ids.input_icao.text.upper()
        if icao in self.data:
            info = self.data[icao]
            output = (
                f"{info['name']}\nCurfew: {info['curfew']}\n"
                f"Slot Required: {info['slot_required']}\n"
                f"PPR Required: {info['ppr_required']}\n"
                f"Flight Permit Needed: {info['flight_permit_needed']}\n"
                f"Notes: {info['notes']}"
            )
            self.ids.result_label.text = output
        else:
            self.ids.result_label.text = "Airport not found"

    def go_home(self, *_):
        self.manager.current = 'home'
