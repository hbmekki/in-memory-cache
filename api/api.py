import json
from flask_restful import Resource, request, reqparse, abort

# For parsing query paramters
parser = reqparse.RequestParser()
parser.add_argument('ttl', type=int)

class  CacheApi(Resource):
    
    # A class proprty used to hold the cached items
    cache = None

    @classmethod
    def initialize_cache(cls, cache_instance):
        """This class method is used to initialize the cache with an instance
        created using the parameters provided in the app config.  
        """

        cls.cache = cache_instance


    def get(self, key):
        """Returns the object stored at {key} if the object is not expired.
        ---
        path:
            /object/{key}
        parameters:
            - name: key
                in: path
                type: string
                required: true
        responses:
            200:
                description: JSON object
                examples:
                    {"first": "Steve", "last": "Moody"}
            404:
                description: An error message
                exapmples:
                    {"message": "Object at {key} is not found or expired"}
        """

        entry = self.cache.get_entry(key)
        if entry:
            return json.loads(entry.json_str), 200
        abort(404, message=f"Object at {key} is not found or expired")


    def _update(self, key):
        """This private method implemets inserting and updating items in 
        the cache. Both post and put methods call it.
        """
        ttl = parser.parse_args().get('ttl', None)
        obj_json_str  = json.dumps(request.get_json())
        cached = self.cache.set_entry(key, obj_json_str, ttl)
        if cached:
            return {"message": "success"}, 200
        return {"message": "The server has no storage"}, 507


    def post(self, key):
        """Inserts the {object} provided in the body of the request into a slot
        in memory at {key}. If {ttl} is not specified it will use server’s 
        default TTL from the config, if ttl=0 it means store indefinitely
        ---
        path:
            /object/{key}
        parameters:
            - name: key
                in: path
                type: string
                required: true
            - name: ttl
                in: query
                type: integer
                required: false
            - name: body
                in: body
                type: object
                required: true
        responses:
            200:
                description: JSON object
                examples:
                    {"message": "success"}
            507:
                description: An error message
                exapmples:
                    {"message": "The server has no storage"}
            400:
                description: An error message if ttl is not an integer
        """

        return self._update(key)
        
    def put(self, key):
        """Inserts the {object} provided in the body of the request into a slot
        in memory at {key}. If {ttl} is not specified it will use server’s 
        default TTL from the config, if ttl=0 it means store indefinitely
        ---
        path:
            /object/{key}
        parameters:
            - name: key
                in: path
                type: string
                required: true
            - name: ttl
                in: query
                type: integer
                required: false
            - name: body
                in: body
                type: object
                required: true
        responses:
            200:
                description: JSON object
                examples:
                    {"message": "success"}
            507:
                description: An error message
                exapmples:
                    {"message": "The server has no storage"}
        """

        return self._update(key)


    def delete(self, key):
        """Deletes the object stored at slot {key}
        ---
        path:
            /object/{key}
        parameters:
            - name: key
                in: path
                type: string
                required: true
        responses:
            200:
                description: JSON object
                examples:
                    {"message": "success"}
            404:
                description: An error message
                exapmples:
                    {"message": "Object at {key} is not found or expired"}
        """
        deleted = self.cache.delete_entry(key)
        if deleted:
            return {"message": "success"}, 200
        abort(404, message=f"Object at {key} is not found or expired")

    def patch(self, key):
        return {
            "content": [(k,v.json_str, v._ttl) for k,v in self.cache._container.items()],
            "params": [self.cache._max_slots, self.cache.default_ttl]
        }