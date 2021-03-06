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

from ..utils import classname
from collections import OrderedDict

class Issue(object):
    PLATFORM = 0
    """
    Platform error (e.g. I/O, hardware, a bug in ARIA)
    """
    
    SYNTAX = 1
    """
    Syntax and format (e.g. YAML, XML, JSON)
    """
    
    FIELD = 2
    """
    Single field
    """
    
    BETWEEN_FIELDS = 3
    """
    Relationships between fields within the type (internal grammar)
    """
    
    BETWEEN_TYPES = 4
    """
    Relationships between types (e.g. inheritance, external grammar)
    """
    
    BETWEEN_INSTANCES = 5
    """
    Topology (e.g. static requirements and capabilities)
    """
    
    EXTERNAL = 6
    """
    External (e.g. live requirements and capabilities)
    """
    
    ALL = 100

    def __init__(self, message=None, exception=None, location=None, line=None, column=None, locator=None, snippet=None, level=0):
        if message is not None:
            self.message = str(message)
        elif exception is not None:
            self.message = str(exception)
        else:
            self.message = 'unknown issue'
            
        self.exception = exception
        
        if locator is not None:
            self.location = locator.location
            self.line = locator.line
            self.column = locator.column
        else:
            self.location = location
            self.line = line
            self.column = column
            
        self.snippet = snippet
        self.level = level

    @property
    def as_raw(self):
        return OrderedDict((
            ('level', self.level),
            ('message', self.message),
            ('location', self.location),
            ('line', self.line),
            ('column', self.column),
            ('snippet', self.snippet),
            ('exception', classname(self.exception) if self.exception else None)))
            
    @property
    def locator_as_str(self):
        if self.location is not None:
            if self.line is not None:
                if self.column is not None:
                    return '"%s":%d:%d' % (self.location, self.line, self.column)
                else: 
                    return '"%s":%d' % (self.location, self.line)
            else:
                return '"%s"' % self.location
        else:
            return None
    
    @property
    def heading_as_str(self):
        return '%d: %s' % (self.level, self.message)

    @property
    def details_as_str(self):
        r = ''
        locator = self.locator_as_str
        if locator is not None:
            r += '@%s' % locator
        if self.snippet is not None:
            r += '\n%s' % self.snippet
        return r

    def __str__(self):
        r = self.heading_as_str
        details = self.details_as_str
        if details:
            r += ', ' + details
        return r
