
import tosca, tosca.interfaces
	
class Standard(tosca.interfaces.Root):
	"""
	This lifecycle interface defines the essential, normative operations that TOSCA nodes may support. 
	
	`TOSCA Simple Profile v1.0 <http://docs.oasis-open.org/tosca/TOSCA-Simple-Profile-YAML/v1.0/csprd02/TOSCA-Simple-Profile-YAML-v1.0-csprd02.html#>` (wrong anchor)
	"""
	
	DESCRIPTION = 'This lifecycle interface defines the essential, normative operations that TOSCA nodes may support.'

    SHORTHAND_NAME = 'Standard'
    TYPE_QUALIFIED_NAME = 'tosca:Standard'
    TYPE_URI = 'tosca.interfaces.node.lifecycle.Standard'
