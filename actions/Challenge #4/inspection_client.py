#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from my_robot_interfaces.action import Inspector

class InspectionClient(Node):
    def __init__(self):
        super().__init__('ins_cli_node')
        self.action_client = ActionClient(self, Inspector, 'checkpoints')
        # self.timer = self.create_timer(4.0, self.cancel_goal)
        
    def goal_sender_callback(self, checkpoints):
        self.action_client.wait_for_server()
        goal = Inspector.Goal()
        goal.checkpoints = checkpoints
        future = self.action_client.send_goal_async(goal)
        future.add_done_callback(self.response_handle_callback)

    def response_handle_callback(self, future):
        self.goal_handle: ClientGoalHandle = future.result()
        if self.goal_handle.accepted:
            self.get_logger().info('Goal got accepted')
        else:
            self.get_logger().info('Goal got rejected')

    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Succeeded')
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info('Aborted')
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info('Cancelled')
        self.get_logger().info(f'Goal achieved! Final angles: {result.completed}')
    
    def cancel_goal(self):
        self.get_logger().info('Sending a cancel goal request')
        self.goal_handle.cancel_goal_async()

def main(args = None):
    rclpy.init(args = args)
    node = InspectionClient()
    node.goal_sender_callback(5)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()