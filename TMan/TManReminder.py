#!/usr/bin/env python3
import DeamonLib, sys
import TManLibrary

def reload_data():
    users = TManLibrary.data_from_json("User", None)
    current = TManLibrary.set_current(users)
    tracked_tasks = TManLibrary.data_from_json("Task", current)
    return DeamonLib.TManReminder(tracked_tasks, '/tmp/daemon-reminders.pid')

if __name__=='__main__':
    
    if sys.argv[1] == "start":
        check_reminds = reload_data()
        check_reminds.start()
    elif sys.argv[1] == "restart":
        check_reminds = reload_data()
        check_reminds.restart()
    elif sys.argv[1] == "stop":
        check_reminds = reload_data()
        check_reminds.stop()

