import uuid
import manifests
import utility


def extract_fr8_crate_contents(contents, manifest_id):
    manifest_id_str = str(manifest_id)
    if manifest_id_str not in manifests.manifest_extractors:
        raise 'Unsupported manifest_id, data extraction failed.'

    return manifests.manifest_extractors[manifest_id_str](contents)


TerminalStatus = utility.enum(ACTIVE=1, INACTIVE=0)

AuthenticationType = utility.enum(NONE=1, INTERNAL=2, EXTERNAL=3, INTERNAL_WITH_DOMAIN=4)

ActivityType = utility.enum(STANDARD=1, LOOP=2, SOLUTION=3)

AvailabilityType = utility.enum(NOTSET=0, CONFIGURATION=1, RUNTIME=2, ALWAYS=3)


class ActivityDTO(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.activity_template = kwargs.get('activity_template')
        self.root_plan_node_id = kwargs.get('root_plan_node_id')
        self.parent_plan_node_id = kwargs.get('parent_plan_node_id')
        self.current_view = kwargs.get('current_view')
        self.ordering = kwargs.get('ordering')
        self.id = kwargs.get('id')
        self.crate_storage = kwargs.get('crate_storage', CrateStorageDTO())
        self.children_activities = kwargs.get('children_activities', [])
        self.auth_token_id = kwargs.get('auth_token_id')
        self.auth_token = kwargs.get('auth_token')

    def to_fr8_json(self):
        return {
            'name': self.name,
            'label': self.label,
            'activityTemplate': self.activity_template.to_fr8_json(),
            'rootPlanNodeId': self.root_plan_node_id,
            'parentPlanNodeId': self.parent_plan_node_id,
            'currentView': self.current_view,
            'ordering': self.ordering,
            'id': self.id,
            'crateStorage': self.crate_storage.to_fr8_json(),
            'childrenActivities': [x.to_fr8_json() for x in self.children_activities],
            'authTokenId': self.auth_token_id,
            'authToken': self.auth_token.to_fr8_json() if self.auth_token else None,
        }

    @staticmethod
    def from_fr8_json(json_data):
        a = ActivityDTO(
            name=json_data.get('name'),
            label=json_data.get('label'),
            activity_template=ActivityTemplateDTO.from_fr8_json(json_data.get('activityTemplate')),
            root_plan_node_id=json_data.get('rootPlanNodeId'),
            parent_plan_node_id=json_data.get('parentPlanNodeId'),
            current_view=json_data.get('currentView'),
            ordering=json_data.get('ordering'),
            id=json_data.get('id'),
            crate_storage=CrateStorageDTO.from_fr8_json(json_data.get('crateStorage')) if json_data.get('crateStorage') else CrateStorageDTO(),
            children_activities=[ActivityDTO.from_fr8_json(x) for x in json_data.get('childrenActivities')]\
                if json_data.get('childrenActivities') else [],
            auth_token_id = json_data.get('authTokenId'),
            auth_token = AuthorizationTokenDTO.from_fr8_json(json_data.get('authToken')) if json_data.get('authToken') else None
        )
        return a


class ActivityResponseDTO(object):
    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.body = kwargs.get('body')

    def to_fr8_json(self):
        return {
            'type': self.type,
            'body': self.body
        }

    @staticmethod
    def from_fr8_json(json_data):
        dto = ActivityResponseDTO(
            type=json_data.get('type'),
            body=json_data.get('body')
        )

        return dto


class ActivityCategoryDTO(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.icon_path = kwargs.get('icon_path')

    def to_fr8_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'iconPath': self.icon_path
        }

    @staticmethod
    def from_fr8_json(json_data):
        if not json_data:
            return None

        ac = ActivityCategoryDTO(
            name=json_data.get('name'),
            icon_path=json_data.get('iconPath')
        )

        return ac


ActivityCategories = utility.enum(
    MONITORS=ActivityCategoryDTO(
        id='417DD061-27A1-4DEC-AECD-4F468013FD24',
        name='Triggers',
        icon_path='/Content/icons/monitor-icon-64x64.png'
    ),
    RECEIVERS=ActivityCategoryDTO(
        id='29EFB1D7-A9EA-41C5-AC60-AEF1F520E814',
        name='Get Data',
        icon_path='/Content/icons/get-icon-64x64.png'
    ),
    PROCESSORS=ActivityCategoryDTO(
        id='69FB6D2C-2083-4696-9457-B7B152D358C2',
        name='Process',
        icon_path='/Content/icons/process-icon-64x64.png'
    ),
    FORWARDERS=ActivityCategoryDTO(
        id='AFD7E981-A21A-4B05-B0B1-3115A5448F22',
        name='Ship Data',
        icon_path='/Content/icons/forward-icon-64x64.png'
    ),
    SOLUTION=ActivityCategoryDTO(
        id='F9DF2AC2-2F10-4D21-B97A-987D46AD65B0',
        name='Solution',
        icon_path='/Content/icons/solution-icon-64x64.png'
    )
)


class ActivityTemplateDTO(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.version = kwargs.get('version')
        self.terminal = kwargs.get('terminal')
        self.categories = kwargs.get('categories')
        self.needs_authentication = kwargs.get('needs_authentication', False)
        self.label = kwargs.get('label', '')
        self.activity_type = kwargs.get('activity_type', ActivityType.STANDARD)
        self.min_pane_width = kwargs.get('min_pane_width', 380)

    def to_fr8_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'terminal': self.terminal.to_fr8_json() if self.terminal else None,
            'categories': [x.to_fr8_json() for x in self.categories] if self.categories else None,
            'needsAuthentication': self.needs_authentication,
            'label': self.label,
            'type': self.activity_type,
            'minPaneWidth': self.min_pane_width
        }

    @staticmethod
    def from_fr8_json(json_data):
        a = ActivityTemplateDTO(
            id=json_data.get('id'),
            name=json_data.get('name'),
            label=json_data.get('label'),
            version=json_data.get('version'),
            web_service=WebServiceDTO.from_fr8_json(json_data.get('webService')) if json_data.get('webService') else None,
            terminal=TerminalDTO.from_fr8_json(json_data.get('terminal')) if json_data.get('terminal') else None,
            activity_category=json_data.get('category'),
            categories=[ActivityCategoryDTO.from_fr8_json(x) for x in json_data.get('categories')]\
                if json_data.get('categories') else [],
            activity_type=json_data.get('type'),
            min_pane_width=json_data.get('minPaneWidth'),
            needs_authentication=json_data.get('needsAuthentication')
        )
        return a


class AuthorizationTokenDTO(object):
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.token = kwargs.get('token')
        self.external_account_id = kwargs.get('external_account_id')
        self.external_state_token = kwargs.get('external_state_token')

    def to_fr8_json(self):
        return {
            'userId': self.user_id,
            'token': self.token,
            'externalAccountId': self.external_account_id,
            'externalStateToken': self.external_state_token
        }

    @staticmethod
    def from_fr8_json(json_data):
        dto = AuthorizationTokenDTO(
            user_id=json_data.get('userId'),
            token=json_data.get('token'),
            external_account_id=json_data.get('externalAccountId'),
            external_state_token=json_data.get('externalStateToken')
        )
        return dto


class CrateDTO(object):
    def __init__(self, **kwargs):
        self.manifest_type = kwargs.get('manifest_type')
        self.manifest_id = kwargs.get('manifest_id')
        self.manifest_registrar = kwargs.get('manifest_registrar')
        self.id = kwargs.get('id', uuid.uuid4())
        self.label = kwargs.get('label')
        self.contents = kwargs.get('contents')
        self.parent_crate_id = kwargs.get('parent_crate_id')
        self.create_time = kwargs.get('create_time', '')
        self.availability_type = kwargs.get('availability_type', AvailabilityType.NOTSET)

    def to_fr8_json(self):
        return {
            'manifestType': self.manifest_type,
            'manifestId': self.manifest_id,
            'manifestRegistrar': self.manifest_registrar,
            'id': self.id,
            'label': self.label,
            'contents': self.contents.to_fr8_json(),
            'createTime': self.create_time,
            'availability': self.availability_type
        }

    @staticmethod
    def from_fr8_json(json_data):
        c = CrateDTO(
            availability_type=json_data.get('availability'),
            contents=extract_fr8_crate_contents(json_data.get('contents'), json_data.get('manifestId')),
            create_time=json_data.get('createTime'),
            id=json_data.get('id'),
            label=json_data.get('label'),
            manifest_id=json_data.get('manifestId'),
            manifest_registrar=json_data.get('manifestRegistrar'),
            manifest_type=json_data.get('manifestType'),
            parent_crate_id=json_data.get('parentCrateId')
        )
        return c


class CrateStorageDTO(object):
    def __init__(self, **kwargs):
        self.crates = kwargs.get('crates', [])

    def first_crate_of_type(self, mt):
        for c in self.crates:
            if c.manifest_id == mt:
                return c
        return None

    def first_crate_contents_of_type(self, mt):
        crate = self.first_crate_of_type(mt)
        if not crate:
            return None

        return crate.contents

    def all_crates_of_type(self, mt):
        return [c for c in self.crates if c.manifest_id == mt]

    def to_fr8_json(self):
        return { 'crates': [x.to_fr8_json() for x in self.crates] }

    @staticmethod
    def from_fr8_json(json_data):
        dto = CrateStorageDTO(
            crates=[CrateDTO.from_fr8_json(c) for c in json_data.get('crates')]\
                if json_data.get('crates') else []
        )
        return dto


class ExternalAuthenticationDTO(object):
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.parameters = kwargs.get('parameters')

    @staticmethod
    def from_fr8_json(json_data):
        ea = ExternalAuthenticationDTO()
        ea.user_id = json_data.get('Fr8UserId')
        ea.parameters = dict()
        for x in json_data.get('RequestQueryString', '').split("&"):
            t = x.split('=')
            ea.parameters[t[0]] = t[1]
        return ea


class ExternalAuthUrlDTO(object):
    def __init__(self, **kwargs):
        self.state_token = kwargs.get('state_token')
        self.url = kwargs.get('url')

    def to_fr8_json(self):
        return {
            'ExternalStateToken': self.state_token,
            'Url': self.url
        }


class FieldDTO(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.field_type = kwargs.get('field_type')
        self.is_required = kwargs.get('is_required', False)
        self.tags = kwargs.get('tags')
        self.availability = kwargs.get('availability')
        self.data = kwargs.get('data', dict())

    def to_fr8_json(self):
        return {
            'key': self.name,
            'label': self.label,
            'fieldType': self.field_type,
            'isRequired': self.is_required,
            'tags': self.tags,
            'availability': self.availability,
            'data': self.data
        }

    @staticmethod
    def from_fr8_json(json_data):
        dto = FieldDTO(
            name=json_data.get('key'),
            label=json_data.get('label'),
            field_type=json_data.get('fieldType'),
            is_required=json_data.get('isRequired', False),
            tags=json_data.get('tags'),
            availability=json_data.get('availability', AvailabilityType.NOTSET),
            data=json_data.get('data', dict())
        )

        return dto


class Fr8DataDTO(object):
    def __init__(self, **kwargs):
        self.activity = kwargs.get('activity')
        self.container_id = kwargs.get('container_id')

    def get_user_id(self):
        return self.activity.auth_token.user_id

    def to_fr8_json(self):
        return {
            'ActivityDTO': self.activity.to_fr8_json() if self.activity else None,
            'ContainerId': self.container_id
        }

    @staticmethod
    def from_fr8_json(json_data):
        dto = Fr8DataDTO(
            activity=ActivityDTO.from_fr8_json(json_data.get('ActivityDTO')),
            container_id=json_data.get('ContainerId')
        )
        return dto


class KeyValueDTO(object):
    def __init__(self, **kwargs):
        self.key = kwargs.get('key')
        self.value = kwargs.get('value')
        self.tags = kwargs.get('tags')

    def to_fr8_json(self):
        return {
            'key': self.key,
            'value': self.value,
            'tags': self.tags
        }

    @staticmethod
    def from_fr8_json(json_data):
        dto = KeyValueDTO(
            key=json_data.get('key'),
            value=json_data.get('value'),
            tags=json_data.get('tags')
        )
        return dto


class PayloadDTO(object):
    def __init__(self, **kwargs):
        self.crate_storage = kwargs.get('crate_storage')
        self.container_id = kwargs.get('container_id')

    def success(self):
        crate = self.crate_storage.first_crate_of_type(manifests.ManifestType.OPERATIONAL_STATE)
        if not crate:
            cm = manifests.OperationalStateCM()
            crate = CrateDTO(contents=cm, availability_type=AvailabilityType.RUNTIME)
            self.crate_storage.crates.append(crate)

        crate.contents.set_success_response()

    def to_fr8_json(self):
        return {
            'container': self.crate_storage.to_fr8_json(),
            'containerId': self.container_id
        }

    @staticmethod
    def from_fr8_json(json_data):
        p = PayloadDTO(
            container_id=json_data.get('containerId'),
            crate_storage=CrateStorageDTO.from_fr8_json(json_data.get('container'))\
                if json_data.get('container') else []
        )
        return p


class PayloadObjectDTO(object):
    def __init__(self, **kwargs):
        self.payload_object = kwargs.get('payload_object', [])

    def to_fr8_json(self):
        return {
            'PayloadObject': [x.to_fr8_json() for x in self.payload_object]
        }

    @staticmethod
    def from_fr8_json(json_data):
        dto = PayloadObjectDTO(
            payload_object=[KeyValueDTO.from_fr8_json(x) for x in json_data.get('PayloadObject')]\
                if json_data.get('PayloadObject') else []
        )

        return dto


class TerminalDTO:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.version = kwargs.get('version')
        self.terminal_status = kwargs.get('terminal_status', TerminalStatus.ACTIVE)
        self.endpoint = kwargs.get('endpoint')
        self.description = kwargs.get('description')
        self.authentication_type = kwargs.get('authentication_type', AuthenticationType.NONE)

    def to_fr8_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'label': self.label,
            'version': self.version,
            'terminalStatus': self.terminal_status,
            'endpoint': self.endpoint,
            'description': self.description,
            'authenticationType': self.authentication_type
        }

    @staticmethod
    def from_fr8_json(json_data):
        t = TerminalDTO(
            id=json_data.get('id'),
            name=json_data.get('name'),
            label=json_data.get('label'),
            version=json_data.get('version'),
            terminal_status=json_data.get('terminalStatus'),
            endpoint=json_data.get('endpoint'),
            description=json_data.get('description'),
            authentication_type=json_data.get('authenticationType', AuthenticationType.NONE)
        )
        return t
