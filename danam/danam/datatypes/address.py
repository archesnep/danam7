from arches.app.datatypes.base import BaseDataType

details = {
    'datatype': 'address',
    'iconclass': 'fa fa-location-arrow',
    'modulename': 'datatypes.py',
    'classname': 'AddressDataType',
    'defaultwidget': None,
    'defaultconfig': None,
    'configcomponent': None,
    'configname': None,
    'isgeometric': False,
    'issearchable': False
}


class AddressDataType(BaseDataType):

    def validate(self, value, source=None):
        errors = []
        message = 'datatype: address, value: {1} {2} - missing required properties. This data was not imported.'
        try:
            value['address']
            value['x']
            value['y']
        except KeyError:
            errors.append({
                'type': 'ERROR',
                'message': message.format(value, source)
            })

        return errors

    def append_to_document(self, document, nodevalue, nodeid, tile):
        document['strings'].append({
            'string': nodevalue['address'],
            'nodegroup_id': tile.nodegroup_id
        })

    def get_search_terms(self, nodevalue, nodeid=None):
        return [
            nodevalue['address']
        ]
