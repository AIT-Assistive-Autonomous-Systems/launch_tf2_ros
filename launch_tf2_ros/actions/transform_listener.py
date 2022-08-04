# Copyright 2022 AIT Austrian Institute of Technology GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
from launch.logging import get_logger
from launch.action import Action
from launch import LaunchContext
from launch_ros.ros_adapters import get_ros_node
from rclpy.time import Time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener as ROSTransformListener
from launch_tf2_ros.events import TimeOut, OnTransformAvailable


class TransformListener(Action):
    """Action to listens for a TF transformation and emit an event when it is available."""

    def __init__(
        self,
        *,
        target_frame: str,
        source_frame: str,
        timeout=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.__logger = get_logger(__name__)
        self.__target_frame = target_frame
        self.__source_frame = source_frame
        self.__timeout = timeout
        self.__buffer = None
        self.__tf_listener = None
        self.__wait_task = None

    async def __execute_async(self, context):
        latest_t = Time(seconds=0, nanoseconds=0)
        tf_task = self.__buffer.wait_for_transform_async(
            self.__target_frame, self.__source_frame, latest_t)
        try:
            has_transform = await asyncio.wait_for(tf_task, self.__timeout)
            assert(has_transform)
        except asyncio.TimeoutError:
            await context.emit_event(TimeOut())
            return

        self.__logger.debug(
            f'transform {self.__source_frame} to {self.__target_frame} available')
        await context.emit_event(OnTransformAvailable())

    def get_asyncio_future(self):
        return self.__wait_task

    def execute(self, context: LaunchContext):
        node = get_ros_node(context)

        self.__buffer = Buffer()
        self.__tf_listener = ROSTransformListener(self.__buffer, node)

        self.__wait_task = context.asyncio_loop.create_task(
            self.__execute_async(context))

        return super().execute(context)
