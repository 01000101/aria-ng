#
# Copyright (c) 2016 GigaSpaces Technologies Ltd. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

from aria.deployment import Type, RelationshipType, DeploymentTemplate, NodeTemplate, RelationshipTemplate, CapabilityTemplate, GroupTemplate, PolicyTemplate, SubstitutionTemplate, MappingTemplate, Interface, Operation, Artifact, Requirement, Metadata, Parameter
from .data_types import coerce_value
import re

def get_deployment_template(context, presenter):
    r = DeploymentTemplate()

    r.description = presenter.service_template.description.value if presenter.service_template.description is not None else None

    metadata = presenter.service_template.metadata
    if metadata is not None:
        rr = Metadata()
        rr.values['template_name'] = metadata.template_name
        rr.values['template_author'] = metadata.template_author
        rr.values['template_version'] = metadata.template_version
        custom = metadata.custom
        if custom:
            for name, value in custom.iteritems():
                rr.values[name] = value
        r.metadata = rr

    normalize_types(context, context.deployment.node_types, presenter.node_types)
    normalize_types(context, context.deployment.group_types, presenter.group_types)
    normalize_types(context, context.deployment.capability_types, presenter.capability_types)
    normalize_types(context, context.deployment.relationship_types, presenter.relationship_types, normalize_relationship_type)
    normalize_types(context, context.deployment.policy_types, presenter.policy_types)
    normalize_types(context, context.deployment.artifact_types, presenter.artifact_types)
    normalize_types(context, context.deployment.interface_types, presenter.interface_types)
    
    topology_template = presenter.service_template.topology_template
    if topology_template is not None:
        normalize_property_values(r.inputs, topology_template._get_input_values(context))
        normalize_property_values(r.outputs, topology_template._get_output_values(context))

    node_templates = presenter.node_templates
    if node_templates:
        for node_template_name, node_template in node_templates.iteritems():
            r.node_templates[node_template_name] = normalize_node_template(context, node_template)

    groups = presenter.groups
    if groups:
        for group_name, group in groups.iteritems():
            r.group_templates[group_name] = normalize_group(context, group)

    policies = presenter.policies
    if policies:
        for policy_name, policy in policies.iteritems():
            r.policy_templates[policy_name] = normalize_policy(context, policy)

    substitution_mappings = topology_template.substitution_mappings if topology_template is not None else None
    if substitution_mappings is not None:
        rr = SubstitutionTemplate(substitution_mappings.node_type)
        capabilities = substitution_mappings.capabilities
        if capabilities:
            for mapped_capability_name, capability in capabilities.iteritems():
                rr.capabilities[mapped_capability_name] = MappingTemplate(mapped_capability_name, capability.node_template, capability.capability)
        requirements = substitution_mappings.requirements
        if requirements:
            for mapped_requirement_name, requirement in requirements.iteritems():
                rr.requirements[mapped_requirement_name] = MappingTemplate(mapped_requirement_name, requirement.node_template, requirement.requirement)
        r.substitution_template = rr

    return r

def normalize_node_template(context, node_template):
    r = NodeTemplate(name=node_template._name, type_name=node_template.type)

    normalize_property_values(r.properties, node_template._get_property_values(context))
    normalize_interfaces(context, r.interfaces, node_template._get_interfaces(context))

    artifacts = node_template._get_artifacts(context)
    if artifacts:
        for artifact_name, artifact in artifacts.iteritems():
            r.artifacts[artifact_name] = normalize_artifact(context, artifact)

    requirements = node_template._get_requirements(context)
    if requirements:
        for _, requirement in requirements:
            r.requirements.append(normalize_requirement(context, requirement))

    capabilities = node_template._get_capabilities(context)
    if capabilities:
        for capability_name, capability in capabilities.iteritems():
            r.capabilities[capability_name] = normalize_capability(context, capability)

    normalize_node_filter(context, node_template.node_filter, r.target_node_template_constraints)
    
    return r

def normalize_interface(context, interface):
    the_type = interface._get_type(context)
    
    r = Interface(name=interface._name, type_name=the_type._name)

    inputs = interface.inputs
    if inputs:
        for input_name, the_input in inputs.iteritems():
            r.inputs[input_name] = Parameter(the_input.value.type, the_input.value.value, None) # TODO: description

    operations = interface.operations
    if operations:
        for operation_name, operation in operations.iteritems():
            r.operations[operation_name] = normalize_operation(context, operation)
    
    return r if r.operations else None

def normalize_operation(context, operation):
    r = Operation(name=operation._name)

    implementation = operation.implementation
    if implementation is not None:
        r.implementation = implementation.primary
        dependencies = implementation.dependencies
        if dependencies is not None:
            r.dependencies = dependencies

    inputs = operation.inputs
    if inputs:
        for input_name, the_input in inputs.iteritems():
            r.inputs[input_name] = Parameter(the_input.value.type, the_input.value.value, None) # TODO: description
    
    return r

def normalize_artifact(context, artifact):
    r = Artifact(name=artifact._name, type_name=artifact.type, source_path=artifact.file)

    r.target_path = artifact.deploy_path

    repository = artifact._get_repository(context)
    if repository is not None:
        r.repository_url = repository.url
        credential = repository._get_credential(context)
        if credential:
            for k, v in credential.iteritems():
                r.repository_credential[k] = v

    normalize_property_values(r.properties, artifact._get_property_values(context))
    
    return r

def normalize_requirement(context, requirement):
    r = {'name': requirement._name}

    node, node_variant = requirement._get_node(context)
    if node is not None:
        if node_variant == 'node_type':
            r['target_node_type_name'] = node._name
        else:
            r['target_node_template_name'] = node._name

    capability, capability_variant = requirement._get_capability(context)
    if capability is not None:
        if capability_variant == 'capability_type':
            r['target_capability_type_name'] = capability._name
        else:
            r['target_capability_name'] = capability._name

    r = Requirement(**r)

    normalize_node_filter(context, requirement.node_filter, r.target_node_template_constraints)

    relationship = requirement.relationship
    if relationship is not None:
        r.relationship_template = normalize_relationship(context, relationship)
        
    return r

def normalize_relationship_type(context, relationship_type):
    return RelationshipType(relationship_type._name)

def normalize_relationship(context, relationship):
    relationship_type, relationship_type_variant = relationship._get_type(context)
    if relationship_type_variant == 'relationship_type':
        r = RelationshipTemplate(type_name=relationship_type._name)
    else:
        r = RelationshipTemplate(template_name=relationship_type._name)

    normalize_properties(r.properties, relationship.properties)
    normalize_interfaces(context, r.source_interfaces, relationship.interfaces)
    
    return r

def normalize_capability(context, capability):
    capability_type = capability._get_type(context)
    r = CapabilityTemplate(name=capability._name, type_name=capability_type._name)
    
    capability_definition = capability._get_definition(context)
    occurrences = capability_definition.occurrences
    if occurrences is not None:
        r.min_occurrences = occurrences.value[0]
        if occurrences.value[1] != 'UNBOUNDED':
            r.max_occurrences = occurrences.value[1]
    
    valid_source_types = capability_definition.valid_source_types
    if valid_source_types:
        r.valid_source_node_type_names = valid_source_types

    normalize_properties(r.properties, capability.properties)
    
    return r

def normalize_group(context, group):
    group_type = group._get_type(context)
    r = GroupTemplate(name=group._name, type_name=group_type._name)

    normalize_property_values(r.properties, group._get_property_values(context))
    normalize_interfaces(context, r.interfaces, group._get_interfaces(context))
    
    members = group.members
    if members:
        for member in members:
            r.member_node_template_names.append(member)
    
    return r

def normalize_policy(context, policy):
    policy_type = policy._get_type(context)
    r = PolicyTemplate(name=policy._name, type_name=policy_type._name)

    normalize_property_values(r.properties, policy._get_property_values(context))
    
    node_templates, groups = policy._get_targets(context)
    for node_template in node_templates:
        r.target_node_template_names.append(node_template._name)
    for group in groups:
        r.target_group_template_names.append(group._name)
    
    return r

#
# Utils
#

def normalize_types(context, root, types, normalize=None):
    if types is None:
        return
    
    def added_all():
        for name in types:
            if root.get_descendant(name) is None:
                return False
        return True

    while not added_all():    
        for name, the_type in types.iteritems():
            if root.get_descendant(name) is None:
                parent_type = the_type._get_parent(context)
                if normalize:
                    r = normalize(context, the_type)
                else:
                    r = Type(the_type._name)
                if parent_type is None:
                    root.children.append(r)
                else:
                    container = root.get_descendant(parent_type._name)
                    if container is not None:
                        container.children.append(r)

def normalize_property_values(properties, source_properties):
    if source_properties:
        for property_name, prop in source_properties.iteritems():
            properties[property_name] = Parameter(prop.type, prop.value, None) # TODO: description

def normalize_properties(properties, source_properties):
    if source_properties:
        for property_name, prop in source_properties.iteritems():
            properties[property_name] = Parameter(prop.value.type, prop.value.value, None) # TODO: description

def normalize_interfaces(context, interfaces, source_interfaces):
    if source_interfaces:
        for interface_name, interface in source_interfaces.iteritems():
            interface = normalize_interface(context, interface)
            if interface is not None:
                interfaces[interface_name] = interface

def normalize_node_filter(context, node_filter, node_type_constraints):
    if node_filter is None:
        return
    
    properties = node_filter.properties
    if properties is not None:
        for property_name, constraint_clause in properties:
            fn = normalize_constraint_clause(context, node_filter, constraint_clause, property_name, None)
            if fn is not None:
                node_type_constraints.append(fn)

    capabilities = node_filter.capabilities
    if capabilities is not None:
        for capability_name, capability in capabilities: 
            properties = capability.properties
            if properties is not None:
                for property_name, constraint_clause in properties:
                    fn = normalize_constraint_clause(context, node_filter, constraint_clause, property_name, capability_name)
                    if fn is not None:
                        node_type_constraints.append(fn)

def normalize_constraint_clause(context, node_filter, constraint_clause, property_name, capability_name):
    constraint_key = constraint_clause._raw.keys()[0]
    the_type = constraint_clause._get_type(context)

    def coerce_constraint(constraint, container):
        constraint = coerce_value(context, node_filter, the_type, None, None, constraint, constraint_key) if the_type is not None else constraint
        if hasattr(constraint, '_evaluate'):
            constraint = constraint._evaluate(context, container)
        return constraint
    
    def get_value(node_type):
        if capability_name is not None:
            capability = node_type.capabilities.get(capability_name)
            return capability.properties.get(property_name) if capability is not None else None
        value = node_type.properties.get(property_name)
        return value.value if value is not None else None

    if constraint_key == 'equal':
        def equal(node_type, container):
            constraint = coerce_constraint(constraint_clause.equal, container)
            value = get_value(node_type)
            return value == constraint
        
        return equal

    elif constraint_key == 'greater_than':
        def greater_than(node_type, container):
            constraint = coerce_constraint(constraint_clause.greater_than, container)
            value = get_value(node_type)
            return value > constraint
        
        return greater_than

    elif constraint_key == 'greater_or_equal':
        def greater_or_equal(node_type, container):
            constraint = coerce_constraint(constraint_clause.greater_or_equal, container)
            value = get_value(node_type)
            return value >= constraint
        
        return greater_or_equal

    elif constraint_key == 'less_than':
        def less_than(node_type, container):
            constraint = coerce_constraint(constraint_clause.less_than, container)
            value = get_value(node_type)
            return value < constraint
        
        return less_than

    elif constraint_key == 'less_or_equal':
        def less_or_equal(node_type, container):
            constraint = coerce_constraint(constraint_clause.less_or_equal, container)
            value = get_value(node_type)
            return value <= constraint
        
        return less_or_equal

    elif constraint_key == 'in_range':
        def in_range(node_type, container):
            lower, upper = constraint_clause.in_range
            lower, upper = coerce_constraint(lower, container), coerce_constraint(upper, container)
            value = get_value(node_type)
            if value < lower:
                return False
            if (upper != 'UNBOUNDED') and (value > upper):
                return False
            return True
        
        return in_range

    elif constraint_key == 'valid_values':
        def valid_values(node_type, container):
            constraint = tuple(coerce_constraint(v, container) for v in constraint_clause.valid_values)
            value = get_value(node_type)
            return value in constraint

        return valid_values

    elif constraint_key == 'length':
        def length(node_type, container):
            constraint = constraint_clause.length
            value = get_value(node_type)
            return len(value) == constraint

        return length

    elif constraint_key == 'min_length':
        def min_length(node_type, container):
            constraint = constraint_clause.min_length
            value = get_value(node_type)
            return len(value) >= constraint

        return min_length

    elif constraint_key == 'max_length':
        def max_length(node_type, container):
            constraint = constraint_clause.max_length
            value = get_value(node_type)
            return len(value) >= constraint

        return max_length

    elif constraint_key == 'pattern':
        def pattern(node_type, container):
            constraint = constraint_clause.pattern
            # Note: the TOSCA 1.0 spec does not specify the regular expression grammar, so we will just use Python's
            value = node_type.properties.get(property_name)
            return re.match(constraint, str(value)) is not None

        return pattern

    return None
