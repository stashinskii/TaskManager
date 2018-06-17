#Task Manager (tman) for Command Line Interface (CLI)
## This application is designed to plan your daily activity throw bash terminal
**Some features:**

* Add new task and subtask
* Get tasks tree:
    * Showing task's title, its task ID (tid) and status (X- done, O-process)
    * Subtasks shown on their own level according to their height at tasks tree
* Edit task
* Delete task
* Task scheduler, task creates according to interval between last date and current date
* Order tasks by:
    * Tag (tag's title)
    * Priority (high, low, medium)
* Show tree of archieved tasks (marked as done)
* Make link between tasks
* Share tasks between users (using their login)
* Show full info of task, including:
    * Start and end date
    * Title and description
    * Current subtasks
    * Connected (linked) tasks
    * etc	

## Firstly, you need to clone this app:
```bash
$ git clone https://bitbucket.org/stashinskii/taskmanager/src/master/
```

## App installation:
Change current directory to ../TMan at your bash terminal and install your app:  
```bash
$ python3 -m pip install .
```

## Running tests:
```bash
$ cd tests
$ python3 -m unittest [TEST_FILE]
```

## Task usage: 
```bash
tman task [OPTIONS] COMMAND [ARGS]
```

## Examples:
```bash
$ tman task add -ti "Check my e-mail" -ed "2018-02-03" -sd "2018-02-05" -de "At GMail" -pr LOW -tg email
$ tman task edit --tid 6dad8f76-707f-11e8-8d1f-ec0ec42aa9f1 --title "Looks good" --priority HIGH
$ tman task delete_task --tid 6dad8f76-707f-11e8-8d1f-ec0ec42aa9f1
$ tman task make_link --first 6dad8f76-707f-11e8-8d1f-ec0ec42aa9f1 --second 1ac0fd16-707f-11e8-8d1f-ec0ec42aa9f1
$ tman task share --tid 6dad8f76-707f-11e8-8d1f-ec0ec42aa9f1 --observer user_login
$ tman task list 
$ tman task orderby tag "ИСП" 
$ tman task orderby priority LOW 
$ tman task status --tid 6dad8f76-707f-11e8-8d1f-ec0ec42aa9f1 --status done 
$ tman task archieve 
```

## Users actions:
```bash
tman users [OPTIONS] COMMAND [ARGS]
```

## Examples:
```bash
$ tman user change --login user_login 
$ tman user add_user --login user_login_1 
$ tman user current 
```

## Utils actions (scheduler, etc.):
```bash
$ tman util [OPTIONS] COMMAND [ARGS]
```

## Help:
```bash
$ tman [OPTIONS] COMMANDS --help
```

