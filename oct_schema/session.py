__all__ = [
    'SESSION'
]
import ming
import ming.odm

bind = ming.create_datastore('mim://localhost:27018/tutorial')
doc_session = ming.Session(bind)
SESSION = ming.odm.ThreadLocalODMSession(doc_session=doc_session)
