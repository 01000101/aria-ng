
from .definitions import PropertyDefinition, AttributeDefinition, InterfaceDefinitionForType, RequirementDefinition, CapabilityDefinition, ArtifactDefinition
from .misc import ConstraintClause
from aria import dsl_specification
from aria.presentation import Presentation, has_fields, primitive_field, primitive_list_field, object_field, object_dict_field, field_validator, derived_from_validator
from tosca import Version

@has_fields
@dsl_specification('3.6.3', 'tosca-simple-profile-1.0')
class ArtifactType(Presentation):
    """
    An Artifact Type is a reusable entity that defines the type of one or more files that are used to define implementation or deployment artifacts that are referenced by nodes or relationships on their operations.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_ARTIFACT_TYPE>`__
    """

    @field_validator(derived_from_validator('artifact_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        An optional parent Artifact Type name the Artifact Type derives from.
        
        :rtype: str
        """

    @object_field(Version)
    def version(self):
        """
        An optional version for the Artifact Type definition.
        
        :rtype: :class:`Version`
        """

    @primitive_field(str)
    def description(self):
        """
        An optional description for the Artifact Type.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @primitive_field(str)
    def mime_type(self):
        """
        The required mime type property for the Artifact Type.
        
        :rtype: str
        """

    @primitive_list_field(str)
    def file_ext(self):
        """
        The required file extension property for the Artifact Type.
        
        :rtype: list of str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        An optional list of property definitions for the Artifact Type.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """
    
    def _get_parent(self, consumption_context):
        return consumption_context.presentation.artifact_types.get(self.derived_from)

    def _get_properties(self, consumption_context):
        return self._inherit_and_get_dict_field(consumption_context, 'properties', 'derived_from', 'artifact_types')

@has_fields
@dsl_specification('3.6.5', 'tosca-simple-profile-1.0')
class DataType(Presentation):
    """
    A Data Type definition defines the schema for new named datatypes in TOSCA.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_DATA_TYPE>`__
    """

    @field_validator(derived_from_validator('data_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        The optional key used when a datatype is derived from an existing TOSCA Data Type.
        
        :rtype: str
        """

    @object_field(Version)
    def version(self):
        """
        An optional version for the Data Type definition.
        
        :rtype: :class:`Version`
        """

    @primitive_field(str)
    def description(self):
        """
        The optional description for the Data Type.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(ConstraintClause)
    def constraints(self):
        """
        The optional list of sequenced constraint clauses for the Data Type.
        
        :rtype: dict of str, :class:`ConstraintClause`
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        The optional list property definitions that comprise the schema for a complex Data Type in TOSCA.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    def _get_parent(self, consumption_context):
        return consumption_context.presentation.data_types.get(self.derived_from)

    def _get_properties(self, consumption_context):
        return self._inherit_and_get_dict_field(consumption_context, 'properties', 'derived_from', 'data_types')

@has_fields
@dsl_specification('3.6.6', 'tosca-simple-profile-1.0')
class CapabilityType(Presentation):
    """
    A Capability Type is a reusable entity that describes a kind of capability that a Node Type can declare to expose. Requirements (implicit or explicit) that are declared as part of one node can be matched to (i.e., fulfilled by) the Capabilities declared by another node.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_CAPABILITY_TYPE>`__
    """

    @field_validator(derived_from_validator('capability_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        An optional parent capability type name this new Capability Type derives from.
        
        :rtype: str
        """

    @object_field(Version)
    def version(self):
        """
        An optional version for the Capability Type definition.
        
        :rtype: :class:`Version`
        """

    @primitive_field(str)
    def description(self):
        """
        An optional description for the Capability Type.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        An optional list of property definitions for the Capability Type.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @object_dict_field(AttributeDefinition)
    def attributes(self):
        """
        An optional list of attribute definitions for the Capability Type.
        
        :rtype: dict of str, :class:`AttributeDefinition`
        """

    @primitive_list_field(str)
    def valid_source_types(self):
        """
        An optional list of one or more valid names of Node Types that are supported as valid sources of any relationship established to the declared Capability Type.
        
        :rtype: list of str
        """
        
    def _get_parent(self, consumption_context):
        return consumption_context.presentation.capability_types.get(self.derived_from)

    def _get_properties(self, consumption_context):
        return self._inherit_and_get_dict_field(consumption_context, 'properties', 'derived_from', 'capability_types')

@has_fields
@dsl_specification('3.6.4', 'tosca-simple-profile-1.0')
class InterfaceType(Presentation):
    """
    An Interface Type is a reusable entity that describes a set of operations that can be used to interact with or manage a node or relationship in a TOSCA topology.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_INTERFACE_TYPE>`__
    """

    @field_validator(derived_from_validator('interface_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        An optional parent Interface Type name this new Interface Type derives from.
        
        :rtype: str
        """

    @object_field(Version)
    def version(self):
        """
        An optional version for the Interface Type definition.
        
        :rtype: :class:`Version`
        """

    @primitive_field(str)
    def description(self):
        """
        An optional description for the Interface Type.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def inputs(self):
        """
        The optional list of input parameter definitions.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    def _get_parent(self, consumption_context):
        return consumption_context.presentation.interface_types.get(self.derived_from)

    def _get_inputs(self, consumption_context):
        return self._inherit_and_get_dict_field(consumption_context, 'inputs', 'derived_from', 'interface_types')

@has_fields
@dsl_specification('3.6.9', 'tosca-simple-profile-1.0')
class RelationshipType(Presentation):
    """
    A Relationship Type is a reusable entity that defines the type of one or more relationships between Node Types or Node Templates.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_RELATIONSHIP_TYPE>`__
    """

    @field_validator(derived_from_validator('relationship_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        An optional parent Relationship Type name the Relationship Type derives from.
        
        :rtype: str
        """

    @object_field(Version)
    def version(self):
        """
        An optional version for the Relationship Type definition.
        
        :rtype: :class:`Version`
        """

    @primitive_field(str)
    def description(self):
        """
        An optional description for the Relationship Type.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        An optional list of property definitions for the Relationship Type.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @object_dict_field(AttributeDefinition)
    def attributes(self):
        """
        An optional list of attribute definitions for the Relationship Type.
        
        :rtype: dict of str, :class:`AttributeDefinition`
        """

    @object_dict_field(InterfaceDefinitionForType)
    def interfaces(self):
        """
        An optional list of interface definitions interfaces supported by the Relationship Type.
        
        :rtype: dict of str, :class:`InterfaceDefinitionForType`
        """

    @primitive_list_field(str)
    def valid_target_types(self):
        """
        An optional list of one or more names of Capability Types that are valid targets for this relationship.
        
        :rtype: list of str
        """

    def _get_parent(self, consumption_context):
        return consumption_context.presentation.relationship_types.get(self.derived_from)

    def _get_properties(self, consumption_context):
        return self._inherit_and_get_dict_field(consumption_context, 'properties', 'derived_from', 'relationship_types')

@has_fields
@dsl_specification('3.6.8', 'tosca-simple-profile-1.0')
class NodeType(Presentation):
    """
    A Node Type is a reusable entity that defines the type of one or more Node Templates. As such, a Node Type defines the structure of observable properties via a Properties Definition, the Requirements and Capabilities of the node as well as its supported interfaces.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_NODE_TYPE>`__
    """

    @field_validator(derived_from_validator('node_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        An optional parent Node Type name this new Node Type derives from.
        
        :rtype: str
        """

    @object_field(Version)
    def version(self):
        """
        An optional version for the Node Type definition.
        
        :rtype: :class:`Version`
        """

    @primitive_field(str)
    def description(self):
        """
        An optional description for the Node Type.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        An optional list of property definitions for the Node Type.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @object_dict_field(AttributeDefinition)
    def attributes(self):
        """
        An optional list of attribute definitions for the Node Type.
        
        :rtype: dict of str, :class:`AttributeDefinition`
        """

    @object_dict_field(RequirementDefinition)
    def requirements(self):
        """
        An optional sequenced list of requirement definitions for the Node Type.
        
        :rtype: dict of str, :class:`RequirementDefinition`
        """

    @object_dict_field(CapabilityDefinition)
    def capabilities(self):
        """
        An optional list of capability definitions for the Node Type.
        
        :rtype: dict of str, :class:`CapabilityDefinition`
        """

    @object_dict_field(InterfaceDefinitionForType)
    def interfaces(self):
        """
        An optional list of interface definitions supported by the Node Type.
        
        :rtype: dict of str, :class:`InterfaceDefinitionForType`
        """

    @object_dict_field(ArtifactDefinition)
    def artifacts(self):
        """
        An optional list of named artifact definitions for the Node Type.
        
        :rtype: dict of str, :class:`ArtifactDefinition`
        """

    def _get_parent(self, consumption_context):
        return consumption_context.presentation.node_types.get(self.derived_from)

    def _get_properties(self, consumption_context):
        return self._inherit_and_get_dict_field(consumption_context, 'properties', 'derived_from', 'node_types')

@has_fields
@dsl_specification('3.6.10', 'tosca-simple-profile-1.0')
class GroupType(Presentation):
    """
    A Group Type defines logical grouping types for nodes, typically for different management purposes. Groups can effectively be viewed as logical nodes that are not part of the physical deployment topology of an application, yet can have capabilities and the ability to attach policies and interfaces that can be applied (depending on the group type) to its member nodes.

    Conceptually, group definitions allow the creation of logical "membership" relationships to nodes in a service template that are not a part of the application's explicit requirement dependencies in the topology template (i.e. those required to actually get the application deployed and running). Instead, such logical membership allows for the introduction of things such as group management and uniform application of policies (i.e., requirements that are also not bound to the application itself) to the group's members.
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_GROUP_TYPE>`__
    """

    @field_validator(derived_from_validator('group_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        An optional parent Group Type name the Group Type derives from.
        
        :rtype: str
        """

    @object_field(Version)
    def version(self):
        """
        An optional version for the Group Type definition.
        
        :rtype: :class:`Version`
        """

    @primitive_field(str)
    def description(self):
        """
        The optional description for the Group Type.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        An optional list of property definitions for the Group Type.
        
        :rtype: dict of str, :class:`PropertyDefinition`
        """

    @primitive_list_field(str)
    def members(self):
        """
        An optional list of one or more names of Node Types that are valid (allowed) as members of the Group Type. 

        Note: This can be viewed by TOSCA Orchestrators as an implied relationship from the listed members nodes to the group, but one that does not have operational lifecycle considerations. For example, if we were to name this as an explicit Relationship Type we might call this "MemberOf" (group).
        
        :rtype: list of str
        """

    @object_dict_field(InterfaceDefinitionForType)
    def interfaces(self):
        """
        An optional list of interface definitions supported by the Group Type.
        
        :rtype: dict of str, :class:`InterfaceDefinitionForType`
        """

    def _get_parent(self, consumption_context):
        return consumption_context.presentation.group_types.get(self.derived_from)

    def _get_properties(self, consumption_context):
        return self._inherit_and_get_dict_field(consumption_context, 'properties', 'derived_from', 'group_types')

@has_fields
@dsl_specification('3.6.11', 'tosca-simple-profile-1.0')
class PolicyType(Presentation):
    """
    A Policy Type defines a type of requirement that affects or governs an application or service's topology at some stage of its lifecycle, but is not explicitly part of the topology itself (i.e., it does not prevent the application or service from being deployed or run if it did not exist).
    
    See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ENTITY_POLICY_TYPE>`__
    """

    @field_validator(derived_from_validator('policy_types'))
    @primitive_field(str)
    def derived_from(self):
        """
        An optional parent Policy Type name the Policy Type derives from.
        
        :rtype: str
        """

    @object_field(Version)
    def version(self):
        """
        An optional version for the Policy Type definition.
        
        :rtype: :class:`Version`
        """

    @primitive_field(str)
    def description(self):
        """
        The optional description for the Policy Type.
        
        See the `TOSCA Simple Profile v1.0 specification <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#DEFN_ELEMENT_DESCRIPTION>`__
        
        :rtype: str
        """

    @object_dict_field(PropertyDefinition)
    def properties(self):
        """
        An optional list of property definitions for the Policy Type.
        
        :rtype: :class:`PropertyDefinition`
        """

    @primitive_list_field(str)
    def targets(self):
        """
        An optional list of valid Node Types or Group Types the Policy Type can be applied to.

        Note: This can be viewed by TOSCA Orchestrators as an implied relationship to the target nodes, but one that does not have operational lifecycle considerations. For example, if we were to name this as an explicit Relationship Type we might call this "AppliesTo" (node or group).
        
        :rtype: list of str
        """

    def _get_parent(self, consumption_context):
        return consumption_context.presentation.policy_types.get(self.derived_from)

    def _get_properties(self, consumption_context):
        return self._inherit_and_get_dict_field(consumption_context, 'properties', 'derived_from', 'policy_types')
