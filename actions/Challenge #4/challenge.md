# Challenge: ROS 2 Inspection Action Server with Feedback and Cancellation

## Objective

Create a ROS 2 Action Server named **Inspector** that simulates inspection of checkpoints and supports:

* Goal acceptance
* Continuous feedback during execution
* Goal cancellation
* Final result reporting

## Requirements

### Goal

The client sends the number of checkpoints to inspect.

### Execution

* Start from checkpoint `0`.
* Simulate movement between checkpoints using a delay.
* Continue until all requested checkpoints have been inspected.

### Feedback

During execution, publish feedback containing:

* Current checkpoint reached
* Status message indicating movement to the next checkpoint

### Cancellation

* Allow the client to cancel the inspection at any time.
* If cancellation is requested:

  * Stop execution immediately.
  * Return the last completed checkpoint.
  * Report that the action was cancelled.

### Result

When all checkpoints are inspected successfully:

* Return the total number of completed checkpoints.
* Return a success message confirming completion of the inspection mission.

## Expected Concepts Practiced

* ROS 2 Actions
* Action Server implementation
* Goal handling
* Feedback publishing
* Result generation
* Goal cancellation handling
* Multi-threaded execution using `MultiThreadedExecutor`
* Logging and execution monitoring

