# my-python-robot/my_cool_arm.py

import asyncio
from typing import Any, Dict, Optional
from viam.components.arm import Arm, JointPositions, Pose
from viam.operations import run_with_operation


class MyCoolArm(Arm):
    # Subclass the Viam Arm component and implement the required functions

    def __init__(self, name: str):
        # Starting position
        self.position = Pose(
            x=0,
            y=0,
            z=0,
            o_x=0,
            o_y=0,
            o_z=0,
            theta=0,
        )

        # Starting joint positions
        self.joint_positions = JointPositions(values=[0, 0, 0, 0, 0, 0])
        self.is_stopped = True
        super().__init__(name)

    async def get_end_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Pose:
        return self.position

    @run_with_operation
    async def move_to_position(
        self,
        pose: Pose,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        operation = self.get_operation(kwargs)

        self.is_stopped = False
        self.position = pose

        # Simulate the length of time it takes for the arm to move to its new position
        for x in range(10):
            await asyncio.sleep(1)

            # Check if the operation is cancelled and, if it is, stop the arm's motion
            if await operation.is_cancelled():
                await self.stop()
                break

        self.is_stopped = True

    async def get_joint_positions(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> JointPositions:
        return self.joint_positions

    @run_with_operation
    async def move_to_joint_positions(self, positions: JointPositions, extra: Optional[Dict[str, Any]] = None, **kwargs):
        operation = self.get_operation(kwargs)

        self.is_stopped = False
        self.joint_positions = positions

        # Simulate the length of time it takes for the arm to move to its new joint position
        for x in range(10):
            await asyncio.sleep(1)

            # Check if the operation is cancelled and, if it is, stop the arm's motion
            if await operation.is_cancelled():
                await self.stop()
                break

        self.is_stopped = True

    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self.is_stopped = True

    async def is_moving(self) -> bool:
        return not self.is_stopped
