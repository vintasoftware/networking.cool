
from django.conf import settings

from pytodoist import todoist


def export_to_todoist(username, password, project_name, attendees):
    user = todoist.login(username, password)

    projects = user.projects

    for _, p in projects.items():
        if p.name == project_name:
            project = p
            break
    else:
        project = user.add_project(project_name)


    for attendee in attendees:
        project.add_task(attendee.name)
