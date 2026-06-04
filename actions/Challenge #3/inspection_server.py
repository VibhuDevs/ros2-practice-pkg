#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle, GoalResponse
from my_robot_interfaces.action import Inspector
from rclpy.action import CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

class InspectionServer(Node):
    def __init__(self):
        super().__init__('ins_serv_node')
        self.action_server = ActionServer(self, Inspector, 'checkpoints', 
                    goal_callback = self.checkpoints_goal_callback, execute_callback = self.goal_execution_callback,
                    cancel_callback = self.cancel_goal_callback)
        self.progress = 1
    
    def checkpoints_goal_callback(self, goal_request: Inspector.Goal):
        if goal_request.checkpoints <= 0:
            self.get_logger().info('Cannot accept a negative or a zero value')
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT
    
    def goal_execution_callback(self, goal_handle: ServerGoalHandle):
        checkpoints = goal_handle.request.checkpoints
        result = Inspector.Result()
        feedback = Inspector.Feedback()
        while self.progress < checkpoints:

            self.get_logger().info(f'Currently at checkpoint: {self.progress}')

            feedback.checked = self.progress
            feedback.feed = f'Travelling from checkpoint: {self.progress} to checkpoint: {self.progress + 1}'
            self.get_logger().info(f'{feedback.feed}')
            time.sleep(2)
            self.progress += 1

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.completed = self.progress
                result.message = f'Action cancelled. Completed checkpoint: {self.progress - 1}'
                self.get_logger().info(f'{result.message}')
                return result
        goal_handle.succeed()
        result.completed = self.progress
        result.message = f'Goal Achieved! All the {self.progress} checkpoints inspected properly'
        self.get_logger().info(f'{result.message}')
        return result
    
    def cancel_goal_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info('Cancelled')
        return CancelResponse.ACCEPT
    
def main(args = None):
    rclpy.init(args = args )
    node = InspectionServer()
    exec = MultiThreadedExecutor()
    rclpy.spin(node, exec)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    


        