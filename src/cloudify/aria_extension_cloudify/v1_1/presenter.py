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

from ..v1_0 import CloudifyPresenter1_0
from .templates import ServiceTemplate
from .functions import Concat
from aria.utils import cachedmethod

class CloudifyPresenter1_1(CloudifyPresenter1_0):
    """
    ARIA presenter for the `Cloudify DSL v1.1 specification <http://getcloudify.org/guide/3.2/dsl-spec-general.html>`__.
    
    Changes over v1.0:
    
    * `concat` `intrinsic function <http://getcloudify.org/guide/3.2/dsl-spec-intrinsic-functions.html#concat>`__.
    * Addition of `max_retries` and `retry_interval` to `operation definitions <http://getcloudify.org/guide/3.2/dsl-spec-interfaces.html>`__.
    * Addition of `install_arguments` to `plugin definitions <http://getcloudify.org/guide/3.2/dsl-spec-plugins.html>`__.
    """

    @property
    @cachedmethod
    def service_template(self):
        return ServiceTemplate(raw=self._raw)

    @property
    @cachedmethod
    def functions(self):
        functions = super(CloudifyPresenter1_1, self).functions
        functions.update({
            'concat': Concat})
        return functions

    # Presenter

    @staticmethod
    def can_present(raw):
        dsl = raw.get('tosca_definitions_version')
        return dsl == 'cloudify_dsl_1_1'
