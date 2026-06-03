#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.action import TargetAngle
from rclpy.action import ActionClient
from  rclpy.action.client import ClientGoalHandle, GoalStatus

class ArmControllerClient(Node):
    def __init__(self):
        super().__init__('arm_client')
        self.action_client = ActionClient(self, TargetAngle, 'angle_carrier')
        self.cancel_timer = self.create_timer(4.0, self.cancel_goal)

    def send_goal(self, target_angles):
        self.action_client.wait_for_server()
        goal = TargetAngle.Goal()
        goal.target_angles = target_angles # This just means that we are telling them that goal of target_angles is whatever that is inside target_angles
        future = self.action_client.send_goal_async(goal)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        self.goal_handle: ClientGoalHandle = future.result()
        if self.goal_handle.accepted:
            self.get_logger().info('Goal got accepted')
            self.goal_handle.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().info('Goal got rejected')

    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Success')
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info('Aborted')
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info(f'Cancelled at {result.final_angles}')
        self.get_logger().info(f'Goal achieved. Final angles: {result.final_angles}')

    def cancel_goal(self):
        self.get_logger().info('Send a cancel goal request')
        self.goal_handle.cancel_goal_async()

def main(args = None):
    rclpy.init(args = args)
    node = ArmControllerClient()
    node.send_goal([90.0, -40.0, 120.0])
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


