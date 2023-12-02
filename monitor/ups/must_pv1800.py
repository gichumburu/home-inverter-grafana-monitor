import json
from . import Sample, UPS


class MustPV1800(UPS):
    def __init__(self, device_path: str):
        super().__init__(device_path, 4, 19200)

    def sample(self) -> Sample:
        states = {
            0: "PowerOn",
            1: "SelfTest",
            2: "OffGrid",
            3: "GridTie",
            4: "ByPass",
            5: "Stop",
            6: "GridCharging"
        }

        soc = self.scc.read_registers(25200, 75)
        
 # Create a dictionary with SOC data
        soc_data = {
            "StateOfCharge": soc  # Update with the correct SOC array
        }

        # Save SOC data to a JSON file
        file_path = "soc_data.json"  # Choose a file path/name
        with open(file_path, 'w') as json_file:
            json.dump(soc_data, json_file)

        batVolts = soc[5] / 10.0
        inputVolts = soc[7] // 10
        batAmps = soc[74]
        if batAmps > 32768:
            batAmps = batAmps - 65536
        batCharge = 0
        discharge = soc[54]
        loadPercent = soc[16]
        outputVA = soc[19]
        outputW = soc[15]
        tempInt = soc[33]
        state = states[soc[1]]

        return Sample(
            batVolts,
            batAmps,
            batCharge,
            inputVolts,
            loadPercent,
            outputVA,
            outputW,
            tempInt,
            discharge,
            state)
