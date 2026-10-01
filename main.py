
from __future__ import annotations

import os
from pathlib import Path
from time import sleep
import threading

from isaac_core.devkit import Sim
from isaac_core.devkit.recording import video_recorder
from isaac_core.contracts.pose import Lla
from isaac_core.devkit import PoseBot

CENTER_POINT = (32.22481, 35.25619, 516.827)
MOVEMENTS = [
    (0, 5),
    (4, 6),
    (-4, 6),
    (8, 7),
    (-8, 7),
    (12, 8),
    (-12, 8),
    (6, 10),
    (-6, 10),
    (0, 12),
]
REPO_ROOT = Path(__file__).resolve().parent

def main() -> None:
    """Record both regular and segmented videos with movement using the custom config."""
    
    # Set the config file path via environment variable
    os.environ["ISAAC_CORE_CONFIG"] = str(REPO_ROOT / "config" / "config.toml")
    
    with Sim.launch() as session:
        print("capabilities:", session.get_capabilities())

        for i, (right_left, up_down) in enumerate(MOVEMENTS):
            with PoseBot(start=Lla(lat_deg=32.224800, lon_deg=35.256100, alt_m=519.00)) as bot:
                bot.turn_to_point(*CENTER_POINT, duration_s=0.1)

                bot.move_right_left(right_left, duration_s=0.1)
                bot.move_up_down(up_down, duration_s=0.1)

                bot.turn_to_point(*CENTER_POINT, duration_s=0.1)

            camera = video_recorder()
            camera.start()
            threading.Thread(target=camera.spin, daemon=True).start()

            print(f"session state: {session.state()}")
            session.start_segmentation_recording()

            sleep(4.0)


            data_dir = REPO_ROOT / "isaac_core_out" / f"pov{i}"
            data_dir.mkdir(parents=True, exist_ok=True)

            session.stop_segmentation_recording(str(data_dir / f"seg_.mp4"))
            camera.stop()
            camera.save_video(str(data_dir / f"vis_.mp4"))

            sleep(0.2)

            camera.shutdown()

    for text_file in (REPO_ROOT / "isaac_core_out").rglob("*.txt"):
        if text_file.is_file():
            text_file.unlink()

if __name__ == "__main__":
    main()
