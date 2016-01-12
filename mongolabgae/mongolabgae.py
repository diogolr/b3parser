"""
:mod:`mongolabgae`
==================
.. module:: mongolabgae
   :platform: Unix, Windows
   :synopsis: A MongoLab REST API connection module using Python standard library modules.
.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>
Created on 2013-12-04, 23:06
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import urllib
import http.client
import json


class MongoLabRestClient(object):
    """A MongoLab connection client using the RESTful API for communication.
     Furthermore, the :py:class:`MongoLabRestClient` uses only :py:mod:`urllib`
     and :py:mod:`httplib`, making it possible to use on Google App Engine.
    """

    def __init__(self, api_key, api_version=1, debug=False):
        """Constructor for :py:class:`MongoLabRestClient`.
        :param api_key: The MongoLab API Key
        :type api_key: unicode or str
        :param api_version: The integer version of the REST API. Default is 1.
        :type api_version: int
        :param debug: If set to ``True``, then :py:mod:`httplib` prints out debug
         information for all requests made.
        :type debug: bool
        """
        self._URL = 'api.mongolab.com'
        self._BASE_URL = 'api.mongolab.com/api'
        self._API_VERSION = api_version
        self._API_KEY = api_key

        self._header = {'Content-type': 'application/json;charset=utf-8',
                        'Accept': 'application/json',
                        'Accept-Language': 'en'}

        self._https_connection = http.client.HTTPSConnection(self._URL, timeout=10.0)
        self._https_connection.set_debuglevel(int(debug))

    def get_databases(self):
        """Obtain a list of names of all databases present for this account.
        :return: List of all databases for this account.
        :rtype: list
        """
        return self._request('GET', ['databases', ])

    def get_collections(self, db_name):
        """Obtain a list of names of all collections present in specified database.
        :param db_name: The name of the database to get collections from.
        :type db_name: unicode or str
        :return: All collections in this database.
        :rtype: list
        """
        return self._request('GET', ['databases', db_name, 'collections'])

    # --- MongoDB methods ---

    def find(self, db_name, collection_name, query=None, fields=None, sort=None, skip=None, limit=None):
        """Make a MongoDB ``find`` query.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param query: Restrict results by the specified JSON query.
        :type query: dict
        :param fields: Specify the set of fields to include or
         exclude in each document (1 - include; 0 - exclude).
        :type fields: dict
        :param sort: Specify the order in which to sort each specified
         field (1- ascending; -1 - descending).
        :type sort: dict
        :param skip: Specify the number of results to skip in the result set; useful for paging.
        :type skip: int
        :param limit: Specify the limit for the number of results (default on server is 1000).
        :type limit: int
        :return: The request JSON result parsed to a list of dicts.
        :rtype: list
        """
        parameters = {}
        for key, value in zip(('q', 'f', 's', 'sk', 'l'), (query, fields, sort, skip, limit)):
            if value:
                parameters[key] = value
        return self._request('GET',
                             ['databases', db_name, 'collections', collection_name],
                             parameters)

    def find_one(self, db_name, collection_name, query=None, fields=None):
        """Make a MongoDB ``findOne`` query.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param query: Restrict results by the specified JSON query.
        :type query: dict
        :param fields: Specify the set of fields to include or
         exclude in each document (1 - include; 0 - exclude).
        :type fields: dict
        :return: The request JSON result parsed to a dict or a list.
        :rtype: dict
        """
        parameters = {'fo': True}
        for key, value in zip(('q', 'f'), (query, fields)):
            if value:
                parameters[key] = value
        return self._request('GET',
                             ['databases', db_name, 'collections', collection_name],
                             parameters)

    def count(self, db_name, collection_name, query=None):
        """Make a MongoDB ``count`` query.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param query: Restrict results by the specified JSON query.
        :type query: dict
        :return: The number of entries found by query.
        :rtype: int
        """
        parameters = {'c': True}
        if query:
            parameters['q'] = query
        return self._request('GET',
                             ['databases', db_name, 'collections', collection_name],
                             parameters=parameters)

    def insert(self, db_name, collection_name, docs):
        """Create new document/documents in the specified collection.
        If you POST a document that contains an _id field, the effect will be to overwrite any
        existing document with that _id.  When your document already includes an _id value,
        think of POST like "save" or "upsert" (discussed below) rather than "create" or "insert".
        One consequence of this behavior: for a document with an _id specified, there is no
        straightforward way in the API to realize a pure "insert" — that is, an operation that
        refuses to modify a pre-existing document with that _id.  POST will save over the old document;
        PUT will modify it.  If this property is problematic for your application, consider using
        a field other than "_id", with its own index to enforce uniqueness.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param docs: The document to insert or list of documents to insert.
        :type docs: dict or list
        :return: The inserted document or a dict with information about multiple successful inserts.
        :rtype: dict
        """
        return self._request('POST',
                             ['databases', db_name, 'collections', collection_name],
                             body=docs)

    save = insert

    def update(self, db_name, collection_name, update_doc, query=None, multi=True, upsert=True):
        """Perform an ``update`` MongoDB operation.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param update_doc: The update specification(s) to apply.
        :type update_doc: dict or list
        :param query: A MongoDB query, matching which documents to update.
        :type query: dict
        :param multi: ``True`` means that all matching documents will be updated with
         ``update_doc``, ``False`` will update only the first matching document.
        :type multi: bool
        :param upsert: If ``True``, perform a "update or insert" operation.
        :type upsert: bool
        :return: Returns a dictionary stating the number of successful update operations.
        :rtype: dict
        """
        parameters = {'m': multi, 'u': upsert}
        if query:
            parameters['q'] = query
        return self._request('PUT',
                             ['databases', db_name, 'collections', collection_name],
                             parameters=parameters,
                             body=update_doc)

    def remove(self, db_name, collection_name, query=None):
        """Perform an ``remove`` MongoDB operation.
        Identical to calling the :py:meth:`update` method with empty list input.
        To remove all elements in the collection::
            mongolab_rest_client.remove('db_name', 'collection_name')
        To remove all elements which have a specific field present:
            mongolab_rest_client.remove('db_name', 'collection_name', {'field': {'$exists': 1}})
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param query: A MongoDB query, matching which documents to remove.
        :type query: dict
        :return: Returns a dictionary stating the number of successful remove operations.
        :rtype: dict
        """
        return self.update(db_name, collection_name, update_doc=[], query=query)

    # --- Single document methods ---

    def find_one_by_id(self, db_name, collection_name, _id):
        """Returns the document with the specified ``_id``.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param _id: Key to the MongoDB document to obtain.
        :type _id: unicode or str
        :return: The document or dict stating that specified ``_id`` was not found.
        :rtype: dict
        """
        return self._request('GET', ['databases', db_name, 'collections', collection_name, _id])

    def update_by_id(self, db_name, collection_name, _id, update_doc):
        """Modifies the document matching the specified ``_id``. If no document matching the
        specified _id already exists, it creates a new document.  The modification document should
        contain a replacement document or update modifiers.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param _id: Key to the MongoDB document to obtain.
        :type _id: unicode or str
        :param update_doc: The update specification(s) to apply.
        :type update_doc: dict or list
        :return: The upserted document.
        :rtype: dict
        """
        return self._request('PUT',
                             ['databases', db_name, 'collections', collection_name, _id],
                             body=update_doc)

    def remove_by_id(self, db_name, collection_name, _id):
        """Deletes the document with the specified ``_id``.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param _id: Key to the MongoDB document to obtain.
        :type _id: unicode or str
        :return: The deleted document or dict stating that specified ``_id`` was not found.
        :rtype: dict
        """
        return self._request('DELETE', ['databases', db_name, 'collections', collection_name, _id])

    def run_command(self, db_name, command_to_run, cmd_value=None, **kwargs):
        """Run database and collection-level commands.
        To run a MongoDB database command, send a POST request to the runCommand endpoint.
        Only certain MongoDB commands are exposed through the REST API.  If there are other
        commands you need to run, you can always use the mongo shell or a standard MongoDB
        driver instead.  The available commands are:
            * getLastError
            * getPrevError
            * ping
            * profile
            * repairDatabase
            * resetError
            * whatsmyuri
            * convertToCapped
            * distinct
            * findAndModify
            * geoNear
            * reIndex
            * collStats
            * dbStats
        POST /databases/{database}/runCommand
        Content-Type: application/json
        Body: <JSON data>
        Example (using jQuery):
        The following returns a list of distinct values for 'account' in
        the 'users' collection matching ``{"active": true}``.
        .. code-block:: jQuery
            $.ajax( { url: "https://api.mongolab.com/api/1/databases/my-db/runCommand?apiKey=myAPIKey",
                      data: JSON.stringify( {"distinct": "users","key": "account","query": {"active":true}} ),
                      type: "POST",
                      contentType: "application/json",
                      success: function(msg) {
                           alert( msg );
                      } } )
        :param db_name: The name of the database to run command on.
        :type db_name: str or unicode
        :param command_to_run: The name of the command to run.
        :type command_to_run: str or unicode
        :param cmd_value: The value to set to this command. Most often ``1`` or the name of a collection.
        :type cmd_value: anything
        :return: Results of the command.
        :rtype: dict
        """

        payload = {command_to_run: cmd_value if cmd_value else {}}
        for k in kwargs:
            payload[k] = kwargs[k]
        return self._request('POST', ['databases', db_name, 'runCommand'], body=payload)

    # --- Convenience methods for available runCommand tasks ---

    def get_last_error(self, db_name, w=1, wtimeout=10):
        """Method calling the ``getLastError`` command.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param w: The write concern
        :type w: int or str
        :param wtimeout:
        :type wtimeout:
        :return:
        :rtype:
        """
        return self.run_command(db_name, 'getLastError', 1, w=w, timeout=wtimeout)

    def get_prev_error(self, db_name, w=1, wtimeout=10):
        return self.run_command(db_name, 'getPrevError', 1, w=w, timeout=wtimeout)

    def ping(self, db_name):
        return self.run_command(db_name, 'ping', 1)

    def profile(self, db_name, profile_level_to_set=0, slowms=None):
        return self.run_command(db_name, 'profile', profile_level_to_set, slowms=slowms)

    def whats_my_uri(self, db_name):
        return self.run_command(db_name, 'whatsmyuri', 1)

    def db_stats(self, db_name):
        return self.run_command(db_name, 'dbStats', 1)

    def coll_stats(self, db_name, collection_name):
        return self.run_command(db_name, 'collStats', collection_name)

    def reindex(self, db_name, collection_name):
        return self.run_command(db_name, 'reIndex', collection_name)

    def convert_to_capped(self, db_name, collection_name, size):
        return self.run_command(db_name, 'convertToCapped', collection_name, size=size)

    def repair_database(self, db_name):
        return self.run_command(db_name, 'repairDatabase', 1)

    def reset_error(self, db_name):
        return self.run_command(db_name, 'resetError', 1)

    def distinct(self, db_name, collection_name, key, query):
        return self.run_command(db_name, 'distinct', collection_name, key=key, query=query)

    def find_and_modify(self, db_name, collection_name, query, sort, remove, update, new, fields, upsert):
        """Performs a findAndModify MongoDB command.
        The findAndModify command takes the following fields:
        Fields:
            findAndModify (string) – Required. The collection against which to run the command.
            query (document) – Optional. Specifies the selection criteria for the modification. The query
                field employs the same query selectors as used in the find() method. Although the query may
                match multiple documents, findAndModify will only select one document to modify.
            sort (document) – Optional. Determines which document the operation will modify if the query selects
                multiple documents. findAndModify will modify the first document in the sort order specified
                by this argument.
            remove (boolean) – Must specify either the remove or the update field in the findAndModify
                command. When true, removes the selected document. The default is false.
            update (document) – Must specify either the remove or the update field in the findAndModify
                command. The update field employs the same update operators or field: value
                specifications to modify the selected document.
            new (boolean) – Optional. When true, returns the modified document rather than the original.
                The findAndModify method ignores the new option for remove operations. The default is false.
            fields (document) – Optional. A subset of fields to return. The fields document
                specifies an inclusion of a field with 1, as in the following:
                    fields: { <field1>: 1, <field2>: 1, ... }
            upsert (boolean) – Optional. Used in conjunction with the update field. When true, the
                findAndModify command creates a new document if the query returns no documents.
                The default is false.
        :param db_name: The name of the database to query.
        :type db_name: str or unicode
        :param collection_name: The name of the collection to query.
        :type collection_name: str or unicode
        :param query:
        :type query:
        :param sort:
        :type sort:
        :param remove:
        :type remove:
        :param update:
        :type update:
        :param new:
        :type new:
        :param fields:
        :type fields:
        :param upsert:
        :type upsert:
        :return: A operation report document.
        :rtype: dict
        """
        raise NotImplementedError('To be done...')

    def geonear(self,  db_name, collection_name, near, limit, num, max_distance,
                query, spherical, distance_multiplier, include_locs, unique_docs):
        raise NotImplementedError('To be done...')

    # --- Request method ---

    def _request(self, type_of_request, dir_strings=(), parameters='', body=None):
        """Perform an HTTPS request.
        :param type_of_request: String with value 'GET', 'PUT', 'POST' or 'DELETE'.
        :type type_of_request: unicode
        :param dir_strings: List of strings or string of folders in url. Default is ``[]``
        :type dir_strings: list of unicode or unicode
        :param parameters: The dictionary of parameters to send.
        :type parameters: dict
        :returns: Dictionary of parsed response.
        :rtype: List or dict
        :raises: py:exc:`nExtConnectionError`, py:exc:`nExtSessionExpiredError`.
        """
        try:
            self._https_connection.request(method=type_of_request,
                                           url=self._build_request_url(dir_strings, parameters),
                                           body=json.dumps(body) if body is not None else None,
                                           headers=self._header)
        except Exception as e:
            parsed_response = {'error': "Request error: {0}".format(str(e))}
        else:
            # Request was successfully sent. Now, try to get the response.
            try:
                request_response = self._https_connection.getresponse()
            except Exception as e:
                # General error handler. Request failed somehow, so return an error with information.
                parsed_response = {'error': "Request error: {0}".format(e)}
            else:
                # HTTP response was successfully retrieved. Now read the information and
                # deserialize the JSON document returned into a dict.
                try:
                    parsed_response = json.loads(request_response.read())
                except Exception as e:
                    # Some error occurred, stack information into error output and return it.
                    parsed_response = {'error': "Request error: {0}, Response: {1} - {2}".format(
                        e, request_response.status, request_response.reason)}
                finally:
                    # Finally, try to close the request if it has not been closed properly yet.
                    if not request_response.isclosed():
                        request_response.close()
        finally:
            self._https_connection.close()
        return parsed_response
    # --- Internal help functions ---
    def _build_request_url(self, dir_strings, parameters=None):
        """Returns the `https` url to use, complete with encoded parameters in URL.
        :param dir_strings: List of extra folders in the URL or simply a string.
        :type dir_strings: list, tuple, unicode or str
        :param parameters: The dictionary of parameters to send.
        :type parameters: dict
        :return: The URL to use.
        :rtype: unicode
        """
        url_string = ['https://{0}/{1}'.format(self._BASE_URL, self._API_VERSION), ]
        if isinstance(dir_strings, (list, tuple)):
            for s in dir_strings:
                url_string.append(str(s))
        elif isinstance(dir_strings, basestring):
            url_string.append(dir_strings)
        if parameters:
            parameters['apiKey'] = self._API_KEY
        else:
            parameters = {'apiKey': self._API_KEY}
        return "{0}?{1}".format("/".join(url_string), urllib.parse.urlencode(parameters))
