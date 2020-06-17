
from src.synchronous.expeditions.repository.repository import ExpeditionsRepository


class ExpeditionsRepositoryPSQL(ExpeditionsRepository):
    def __init__(self, db):
        self.db = db
        super(ExpeditionsRepositoryPSQL, self).__init__()

    def get_all(self, filters):
        query = self.db.table('bc_expedition').offset(0).limit(10)

        return query.get()

    def get_total(self, request_objects):
        query = self.db.table('bc_expedition')

        return query.count()

    def get_by_id(self, id):
        query = self.db.table('bc_expedition').where('id', '=', id)

        return query.first()
