#!/usr/bin/env python
#
# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Enables dalvik vm asserts in the android device."""

import argparse
import sys

import devil_chromium
from devil.android import device_blacklist
from devil.android import device_utils


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument('--blacklist-file', help='Device blacklist JSON file.')

  set_asserts_group = parser.add_mutually_exclusive_group(required=True)
  set_asserts_group.add_argument(
      '--enable_asserts', dest='set_asserts', action='store_true',
      help='Sets the dalvik.vm.enableassertions property to "all"')
  set_asserts_group.add_argument(
      '--disable_asserts', dest='set_asserts', action='store_false',
      help='Removes the dalvik.vm.enableassertions property')

  args = parser.parse_args()

  devil_chromium.Initialize()

  blacklist = (device_blacklist.Blacklist(args.blacklist_file)
               if args.blacklist_file
               else None)

  # TODO(jbudorick): Accept optional serial number and run only for the
  # specified device when present.
  devices = device_utils.DeviceUtils.parallel(
      device_utils.DeviceUtils.HealthyDevices(blacklist))

  def set_java_asserts_and_restart(device):
    if device.SetJavaAsserts(args.set_asserts):
      device.RunShellCommand(['stop'], check_return=True)
      device.RunShellCommand(['start'], check_return=True)

  devices.pMap(set_java_asserts_and_restart)
  return 0


if __name__ == '__main__':
  sys.exit(main())
