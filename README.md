## tdl_app
Advanced python app that simulates how to-do-list applications work
### Data
  Id : using cryptography.fernet library I've generated a unique id for each task.
  
  title: str -> the title/name of task.
  
  content: list -> for each task you can add several checkboxes for completion.

  completed: bool -> you can mark task as completed if wanted
### Database
   The data is stored in a local json file


