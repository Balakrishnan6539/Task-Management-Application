from enum import Enum

class TeamRole(str, Enum):
    ADMIN="Admin"
    PM="Project Manager"
    TM="Team Member"