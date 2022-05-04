import os
# CONFIG SECTION
class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY")
    REGISTERED_USERS={
        'scarlettscoville@gmail.com':{"name":"Scarlett","password":"abc123"},
        'michael@dundermifflin.com':{"name":"Michael","password":"shesaid"},
        'dwight@dundermifflin.com':{"name":"Dwight", "password":"beets"}
    }