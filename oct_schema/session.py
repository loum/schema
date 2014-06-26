import ming

bind = ming.create_datastore('mim://localhost:27018/tutorial')
SESSION = ming.Session(bind)
