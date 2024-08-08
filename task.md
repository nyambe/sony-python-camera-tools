# TASK
# TASK: Test-Driven CRUD in Python

## Objective
Implement a test-driven CRUD (Create, Read, Update, Delete) functionality in Python.

## Requirements
1. Create a class called `Task` with the following attributes:
	- `id` (integer): unique identifier for each task
	- `title` (string): title of the task
	- `description` (string): description of the task
	- `completed` (boolean): indicates whether the task is completed or not

2. Implement the following methods in the `Task` class:
	- `__init__(self, title: str, description: str)`: constructor method to initialize the task with a title and description
	- `get_id(self) -> int`: method to get the task's ID
	- `get_title(self) -> str`: method to get the task's title
	- `get_description(self) -> str`: method to get the task's description
	- `is_completed(self) -> bool`: method to check if the task is completed
	- `mark_as_completed(self)`: method to mark the task as completed
	- `update_title(self, new_title: str)`: method to update the task's title
	- `update_description(self, new_description: str)`: method to update the task's description
	- `delete(self)`: method to delete the task

3. Write unit tests for each method using a testing framework of your choice (e.g., `unittest`, `pytest`).

4. Create a separate file called `test_task.py` to write and run the unit tests.

## Example Usage