
from __future__ import annotations

import os
import threading
from time import sleep, time

from isaac_core.devkit import Sim
from isaac_core.devkit.recording import video_recorder
from requests import session

def main() -> None:
    """Record both regular and segmented videos with movement using the custom config."""
    
    # Set the config file path via environment variable
    os.environ["ISAAC_CORE_CONFIG"] = "./config/config.toml"
    
    with Sim.launch() as session:
        print("capabilities:", session.get_capabilities())

        session.set_pose(lat_deg=32.224800, lon_deg=35.256100, alt_m=519.00, roll_deg=0.0, pitch_deg=0.0, yaw_deg=80.0)
        
        session.start_segmentation_recording()

        sleep(10.0)

        session.stop_segmentation_recording("segmentation_check2.mp4")
        

if __name__ == "__main__":
    main()