#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import subprocess

from addonbuilder import AddonBuilder

class ExtensionBuilder(AddonBuilder):
    def __init__(self, config=None, build_dir=".build", extension_dir="extension"):
        AddonBuilder.__init__(self, config=config, build_dir=build_dir)

        self.extension_dir = os.path.normpath(extension_dir)
        self.build_extension_dir = os.path.join(
                                 self.build_dir,
                                 os.path.basename(self.extension_dir))

    def build(self):
        self._archive(self.extension_dir, self.config["xpi"]["extension"])

    def _archive(self, source, target):
        saved_path = os.getcwd()
        zip_archive = os.path.abspath(target)
        os.chdir(source)
        subprocess.call("zip -FS -r " + zip_archive + " *", shell=True)
        os.chdir(saved_path)

