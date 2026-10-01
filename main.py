
from __future__ import annotations

import os
from time import sleep
import threading

from isaac_core.devkit import Sim
from isaac_core.devkit.recording import video_recorder

def main() -> None:
    """Record both regular and segmented videos with movement using the custom config."""
    
    # Set the config file path via environment variable
    os.environ["ISAAC_CORE_CONFIG"] = "./config/config.toml"
    
    with Sim.launch() as session:
        print("capabilities:", session.get_capabilities())

        session.set_pose(lat_deg=32.224800, lon_deg=35.256100, alt_m=519.00, roll_deg=0.0, pitch_deg=0.0, yaw_deg=80.0)

        camera = video_recorder()
        camera.start()
        threading.Thread(target=camera.spin, daemon=True).start()

        session.start_segmentation_recording()

        sleep(4.0)

        camera.stop()

        print("video:", camera.save_video("/home/ofer/clones/construction_sim/isaac_core_out/POV1_vis.mp4"))
        print("segmented video:", session.stop_segmentation_recording("/home/ofer/clones/construction_sim/isaac_core_out/POV1_segmented.mp4"))
        

        camera.shutdown()

if __name__ == "__main__":
    main()