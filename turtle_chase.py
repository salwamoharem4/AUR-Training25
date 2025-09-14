#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from std_msgs.msg import Int32
from turtlesim.srv import Spawn, Kill
import random
import math


class TurtleChase(Node):
    def __init__(self):
        super().__init__('turtle_chase')

        self.score = 0
        self.score_pub = self.create_publisher(Int32, '/score', 10)

        self.player_pose = None
        self.create_subscription(Pose, '/turtle1/pose', self.player_callback, 10)

        self.enemy_pose = {}
        for i in range(1, 4):
            name = f"enemy{i}"
            self.spawn_enemy(name)
            self.create_subscription(Pose, f"/{name}/pose",lambda msg, n=name: self.enemy_callback(msg, n), 10) #we used lamda as we need here 2 strings

        # Timer to check collisions
        self.create_timer(0.1, self.check_collision)

    def player_callback(self, msg):
        self.player_pose = msg

    def enemy_callback(self, msg, name):
        self.enemy_pose[name] = msg

    def check_collision(self):
        if not self.player_pose:
            return #to exit if player node isnot available

        for name, pose in list(self.enemy_pose.items()):
            dist = self.find_dist(self.player_pose, pose)
            if dist < 0.5:
                self.get_logger().info(f"{name} hit")
                self.score += 1
                self.score_pub.publish(Int32(data=self.score))
                self.kill_enemy(name)

    def find_dist(self, pos1, pos2):
        return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)

    def spawn_enemy(self, name):
        client = self.create_client(Spawn, '/spawn')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for spawn service")
        req = Spawn.Request()
        req.x = random.uniform(1.0, 10.0)
        req.y = random.uniform(1.0, 10.0)
        req.theta = 0.0
        req.name = name
        future = client.call_async(req)
        future.add_done_callback(lambda f: self.get_logger().info(f"{name} spawned!"))

    def kill_enemy(self, name):
        client = self.create_client(Kill, '/kill')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for kill service")
        req = Kill.Request()
        req.name = name
        future = client.call_async(req)

        def respawn_callback(fut):
            self.get_logger().info(f"{name} killed, respawning")
            self.spawn_enemy(name)

        future.add_done_callback(respawn_callback)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleChase()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()


