
from __future__ import annotations

import os
import threading

from isaac_core.devkit import Sim
from isaac_core.devkit.recording import bbox_recorder, video_recorder
from isaac_core.devkit.transport import UdpPoseTransport, pace

from time import sleep


def main() -> None:
    """Record a full orbit with the camera and the bounding boxes."""

    # Set the config file path via environment variable
    os.environ["ISAAC_CORE_CONFIG"] = "./config/config.toml"
    with Sim.launch() as session:
        print("capabilities:", session.get_capabilities())

        session.set_pose(lat_deg=32.224640, lon_deg=35.256210, alt_m=525.00, roll_deg=0.0, pitch_deg=-30.0, yaw_deg=-20.0)

        # # Two recorders, each on its own thread. Start them before the flight so nothing is missed.
        # camera = video_recorder()
        # boxes = bbox_recorder()
        # for recorder in (camera, boxes):
        #     recorder.start()
        #     threading.Thread(target=recorder.spin, daemon=True).start()

        # # Change the simulation two ways: a control call, and a runtime config patch.
        # session.set_gimbal(pitch_deg=-40.0)                     # aim the camera down at the ground
        # session.config.patch("vehicles.drone_0.gimbal.max_rate_deg_s", 10.0)     # slow later gimbal moves down

        # # Poses arrive over UDP, independently of the control plane.
        # transport = UdpPoseTransport(port=33333)
        # flight = threading.Thread(target=fly, args=(transport,), daemon=True)
        # flight.start()

        # # Part way round, swing the camera and let the slew rate we just patched take effect.
        # session.step(count=900)
        # session.set_gimbal(yaw_deg=90.0)

        # flight.join(timeout=90.0)
        # transport.close()

        # for recorder in (camera, boxes):
        #     recorder.stop()
        # print("video:", camera.save_video("orbit.mp4"))
        # print("boxes:", boxes.save_to("orbit_bboxes.pkl"))
        # for recorder in (camera, boxes):
        #     recorder.shutdown()

        # print("final pose:", session.get_pose())
        sleep(20)


if __name__ == "__main__":
    main()

