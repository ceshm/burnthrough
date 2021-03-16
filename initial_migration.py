from models.base import *

db.create_tables([User, UserNotes, UserTaskTree])
db.create_tables([UserExpandedNodes])
db.create_tables([UserDailyData])
db.create_tables([UserSession])
