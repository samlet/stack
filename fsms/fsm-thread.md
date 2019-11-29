# fsm-thread.md
## thread
* idle, running-task, suspending-task, shutting-down, idle-shutdown, shutdown-complete

♤ idle
    [run-task] running-task, startTask()
    [task-created] running-task, startTask() 
    [task-unblocked] running-task, startTask()
♤ running-task
    [timeout] suspending-task, suspendTask()
    [task-suspended] idle
    [task-blocked] idle
    [task-deleted] idle
    [task-done] idle

## task
* suspended, running, blocked, stopping, stopped-state, deleted

♤ suspended
    [start] running
♤ running
    [suspend] suspended
    [done] stopped-state
♤ blocked
    [unblock] suspended
    [block] nil
♤ stopping
    [stopped] stopped-state
    [delete] nil


