# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Functions and classes to make testing easier."""

from perfkitbenchmarker import sample


class SamplesTestMixin(object):
  """A mixin for unittest.TestCase that adds a type-specific equality
  predicate for samples.
  """

  def __init__(self, *args, **kwargs):
    super(SamplesTestMixin, self).__init__(self, *args, **kwargs)

    self.addTypeEqualityFunc(sample.Sample, self.assertSamplesEqual)

  def assertSamplesEqualUpToTimestamp(self, a, b, msg=None):
    """Assert that two samples are equal, ignoring timestamp differences."""

    self.assertEqual(a.metric, b.metric,
                     msg or 'Samples %s and %s have different metrics' % (a, b))
    self.assertEqual(a.value, b.value,
                     msg or 'Samples %s and %s have different values' % (a, b))
    self.assertEqual(a.unit, b.unit,
                     msg or 'Samples %s and %s have different units' % (a, b))
    self.assertEqual(a.metadata, b.metadata,
                     msg or 'Samples %s and %s have different metadata' %
                     (a, b))
    # Deliberately don't compare the timestamp fields of the samples.

  def assertSampleListsEqualUpToTimestamp(self, a, b, msg=None):
    """Compare two lists of samples.

    Sadly, the builtin assertListsEqual will only use Python's
    built-in equality predicate for testing the equality of elements
    in a list. Since we compare lists of samples a lot, we need a
    custom test for that.
    """

    self.assertEqual(len(a), len(b),
                     msg or 'Lists %s and %s are not the same length' % (a, b))
    for i in xrange(len(a)):
      self.assertIsInstance(a[i], sample.Sample,
                            msg or ('%s (item %s in list) is '
                                    'not a sample.Sample object' %
                                    (a[i], i)))
      self.assertIsInstance(b[i], sample.Sample,
                            msg or ('%s (item %s in list) is '
                                    'not a sample.Sample object' %
                                    (b[i], i)))
      try:
        self.assertSamplesEqualUpToTimestamp(a[i], b[i], msg=msg)
      except self.failureException as ex:
        ex.message = ex.message + (' (was item %s in list)' % i)
        ex.args = (ex.message,)
        raise ex
