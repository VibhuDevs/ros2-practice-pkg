#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from my_robot_interfaces.action import TargetAngle
from rclpy.action import ActionServer
from rclpy.action import CancelResponse
from rclpy.action.server import ServerGoalHandle, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

class ArmControllerServer(Node):
    def __init__(self):
        super().__init__('controller_server')
        self.action_server = ActionServer(self, TargetAngle, 'angle_carrier',
            goal_callback = self.goal_angle_callback, execute_callback = self.goal_execution_callback, cancel_callback = self.cancel_goal)
        self.initial_angles = [20, -130, -50]


    def goal_angle_callback(self, goal_request: TargetAngle.Goal): # This callback handles the goals that are to be accepted/rejected
        for angle in goal_request.target_angles:
            if angle > 180 or angle < -180:
                self.get_logger().warn('Cannot accept an angle like such')
                return GoalResponse.REJECT
        
        return GoalResponse.ACCEPT
        
            
    def goal_execution_callback(self, goal_handle: ServerGoalHandle):
        target_angles = goal_handle.request.target_angles
        result = TargetAngle.Result()
        feedback = TargetAngle.Feedback()
        while self.initial_angles != list(target_angles):

            feedback.current_angles = self.initial_angles
            feedback.feed = f"Current angles: {self.initial_angles}"
            self.get_logger().info(f"{feedback.feed}")
            goal_handle.publish_feedback(feedback)

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.final_angles = self.initial_angles
                result.message = 'The goal has been cancelled'
                self.get_logger().info(f'{result.message} and current joint angles are: {result.final_angles}')
                return result
            
            for i in range(3):
                if self.initial_angles[i] < target_angles[i]:
                    self.initial_angles[i] += 10
                elif self.initial_angles[i] > target_angles[i]:
                    self.initial_angles[i] -= 10
                time.sleep(1)

        goal_handle.succeed()
        result.final_angles = self.initial_angles
        result.message = 'Goal achieved'
        return result
    
    def cancel_goal(self, goal_handle: ServerGoalHandle):
        self.get_logger().info(f'Received a cancel goal request from the client. Halted at {self.initial_angles}')
        return CancelResponse.ACCEPT
    
def main(args = None):
    rclpy.init(args = args)
    node = ArmControllerServer()
    executor = MultiThreadedExecutor()
    rclpy.spin(node, executor)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

            



