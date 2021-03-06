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

from .consumer import Consumer, ConsumerChain
from ..utils import json_dumps, yaml_dumps

class Instantiate(Consumer):
    def consume(self):
        if self.context.deployment.template is None:
            self.context.validation.report('Plan consumer: missing deployment template')
            return

        self.context.deployment.template.instantiate(self.context, None)

class Validate(Consumer):
    def consume(self):
        self.context.deployment.plan.validate(self.context)

class SatisfyRequirements(Consumer):
    def consume(self):
        self.context.deployment.plan.satisfy_requirements(self.context)
        
class CoerceValues(Consumer):
    def consume(self):
        self.context.deployment.template.coerce_values(self.context, None, True)

class ValidateCapabilities(Consumer):
    def consume(self):
        self.context.deployment.plan.validate_capabilities(self.context)

class Plan(ConsumerChain):
    """
    Generates the deployment plan by instantiating the deployment template.
    """
    
    def __init__(self, context):
        super(Plan, self).__init__(context, (Instantiate, Validate, SatisfyRequirements, CoerceValues, ValidateCapabilities))

    def dump(self):
        if self.context.has_arg_switch('graph'):
            self.context.deployment.plan.dump_graph(self.context)
        elif self.context.has_arg_switch('yaml'):
            indent = self.context.get_arg_value_int('indent', 2)
            raw = self.context.deployment.plan_as_raw
            self.context.out.write(yaml_dumps(raw, indent=indent))
        elif self.context.has_arg_switch('json'):
            indent = self.context.get_arg_value_int('indent', 2)
            raw = self.context.deployment.plan_as_raw
            self.context.out.write(json_dumps(raw, indent=indent))
        else:
            self.context.deployment.plan.dump(self.context)
