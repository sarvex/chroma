import time
from chroma.api import API

class LocalAPI(API):

    def __init__(self, settings, db):
        self._db = db


    def heartbeat(self):
        return int(1000 * time.time_ns())


    def add(self,
            embedding: list,
            input_uri: list,
            dataset: list = None,
            inference_class: list = None,
            label_class: list = None,
            model_spaces: list = None):

        number_of_embeddings = len(embedding)

        if isinstance(model_spaces, str):
            model_space = [model_spaces] * number_of_embeddings
        elif len(model_spaces) == 1:
            model_space = [model_spaces[0]] * number_of_embeddings
        else:
            model_space = model_spaces

        if isinstance(dataset, str):
            ds = [dataset] * number_of_embeddings
        elif len(dataset) == 1:
            ds = [dataset[0]] * number_of_embeddings
        else:
            ds = dataset

        self._db.add(
            model_space,
            embedding,
            input_uri,
            ds,
            inference_class,
            label_class
        )


    def fetch(self, where={}, sort=None, limit=None, offset=None, page=None, page_size=None):

        if page and page_size:
            offset = (page - 1) * page_size
            limit = page_size

        return self._db.fetch(where, sort, limit, offset)


    def delete(self, where={}):

        where = self.where_with_model_space(where)
        deleted_uuids = self._db.delete(where)
        return deleted_uuids


    def count(self, model_space=None):

        model_space = model_space or self._model_space
        return {"count": self._db.count(model_space=model_space)}


    def reset(self):

        self._db.reset()
        return True


    def get_nearest_neighbors(self, embedding, n_results, where):

        where = self.where_with_model_space(where)
        return self._db.get_nearest_neighbors(embedding, n_results, where)


    def raw_sql(self, raw_sql):

        return self._db.raw_sql(raw_sql)


    def create_index(self, model_space=None):

        self._db.create_index(model_space or self._model_space)
        return True


    def process(self, model_space=None):

        raise NotImplementedError("Cannot launch job: Celery is not configured")


    def get_status(self, task_id):

        raise NotImplementedError("Cannot get status of job: Celery is not configured")


    def get_results(self, model_space=None, n_results=100):

        raise NotImplementedError("Cannot get job results: Celery is not configured")