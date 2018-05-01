# Copyright 2018 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import datetime
import unittest

from soundwave import tables


class TestAlerts(unittest.TestCase):
  def testDataFrameFromJson(self):
    data = {
        'anomalies': [
            {
                'key': 'abc123',
                'timestamp': '2009-02-13T23:31:30.000',
                'testsuite': 'loading.mobile',
                'test': 'timeToFirstInteractive/Google',
                'master': 'ChromiumPerf',
                'bot': 'android-nexus5',
                'start_revision': 12345,
                'end_revision': 12543,
                'median_before_anomaly': 2037.18,
                'median_after_anomaly': 2135.540,
                'units': 'ms',
                'improvement': False,
                'bug_id': 55555,
                'bisect_status': 'started',
            },
            {
                'key': 'xyz567',
                'timestamp': '2009-02-13T23:31:30.000',
                'testsuite': 'loading.mobile',
                'test': 'timeToFirstInteractive/Wikipedia',
                'master': 'ChromiumPerf',
                'bot': 'android-nexus5',
                'start_revision': 12345,
                'end_revision': 12543,
                'median_before_anomaly': 2037.18,
                'median_after_anomaly': 2135.540,
                'units': 'ms',
                'improvement': False,
                'bug_id': None,
                'bisect_status': 'started',
            }
        ]
    }
    alerts = tables.alerts.DataFrameFromJson(data)
    self.assertEqual(len(alerts), 2)

    alert = alerts.loc['abc123']  # Get alert by key.
    self.assertEqual(alert['timestamp'], datetime.datetime(
        year=2009, month=2, day=13, hour=23, minute=31, second=30))
    self.assertEqual(alert['bot'], 'ChromiumPerf/android-nexus5')
    self.assertEqual(alert['test_suite'], 'loading.mobile')
    self.assertEqual(alert['test_case'], 'Google')
    self.assertEqual(alert['measurement'], 'timeToFirstInteractive')
    self.assertEqual(alert['bug_id'], 55555)
    self.assertEqual(alert['status'], 'triaged')

    # We expect bug_id's to be integers.
    self.assertEqual(alerts['bug_id'].dtype, int)

    # Missing bug_id's become 0.
    self.assertEqual(alerts.loc['xyz567']['bug_id'], 0)


if __name__ == '__main__':
  unittest.main()