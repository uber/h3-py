'''
 Copyright (c) 2018 Uber Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import os
import re
import unittest

from h3 import h3
from h3_version import h3_version


def camelTo_snake(funcName):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', funcName)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class TestParity(unittest.TestCase):
    def start_test_parity(self):
        os.system('bash ./.test_parity.sh {}'.format(h3_version))

    def cleanup_test_parity(self):
        os.system('bash ./.test_parity_cleanup.sh')

    def parse_h3api(self):
        os.system('bash ./h3c/scripts/binding_functions.sh')
        with open('./binding-functions', 'r') as binding_functions:
            methods = list(map(camelTo_snake, binding_functions))
        return [method.rstrip('\r\n') for method in methods]

    def test_parity(self):
        self.start_test_parity()
        required_methods = self.parse_h3api()
        all_methods = set(dir(h3))
        for method in required_methods:
            self.assertTrue(method in all_methods,
                            'Missing method {}'.format(method))
        #self.cleanup_test_parity()
