from django.contrib import admin

# Register your models here.
from webapp.models import (
    Game,
    AgentTable,
    State,
    Agent,
    Node
)

admin.site.register(Game)
admin.site.register(AgentTable)
admin.site.register(State)
admin.site.register(Agent)
admin.site.register(Node)
