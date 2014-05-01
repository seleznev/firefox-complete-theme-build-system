#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
import time
import subprocess
import zipfile

class AddonBuilder():
    def __init__(self, config=None, build_dir=".build"):
        self.config = self._validate_config(config)
        self.build_dir = os.path.normpath(build_dir)
        os.makedirs(self.build_dir, exist_ok=True)

    def _validate_config(self, config):
        if "version" in config:
            version = config["version"]

            for i in ["theme", "extension", "package"]:
                config["xpi"][i] = config["xpi"][i].replace("@VERSION@", version)

        return config

    def _is_need_update(self, target, dependencies=None):
        if not os.path.exists(target):
            return True

        target_mtime = os.path.getmtime(target)
        for source in dependencies:
            if os.path.getmtime(source) > target_mtime:
                return True

        return False

    def _archive(self, source, target):
        saved_path = os.getcwd()
        zip_archive = os.path.abspath(target)
        os.chdir(source)
        subprocess.call("zip -FS -r " + zip_archive + " *", shell=True)
        os.chdir(saved_path)

    def _generate_install_manifest(self, source, target):
        print("Convert " + source + " to " + target)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        cmd = "sed"
        cmd = cmd + " -e s,[@]VERSION[@]," + self.config["version"] + ",g"
        cmd = cmd + " -e s,[@]MIN_VERSION[@]," + self.config["min-version"] + ",g"
        cmd = cmd + " -e s,[@]MAX_VERSION[@]," + self.config["max-version"] + ",g"
        cmd = cmd + " < '" + source + "' > '" + target + "'"
        subprocess.call(cmd, shell=True)

    def _preprocess(self, source, target, current_version=None):
        print("Convert " + source + " to " + target)

        deps_tmp_file = os.path.join(self.build_dir, "deps.tmp")

        os.makedirs(os.path.dirname(target), exist_ok=True)

        variables = []
        if current_version:
            variables.append(["-D", "APP_VERSION="+str(current_version)])

        cmd = []
        cmd.append(["python2", "build/preprocessor.py", "--marker=%"])
        cmd.append(["--depend="+deps_tmp_file])
        cmd.append(variables)
        cmd.append(["--output="+target, source])

        subprocess.call(cmd)

        line = open(deps_tmp_file, "r").readline()
        line = re.sub(r"^[^:]*:", "", line)
        line = line.replace(os.path.abspath(self.theme_dir), self.theme_dir)
        line = line.replace(source, "")
        line = line.strip()

        if line:
            deps = line.split(" ")
            self._update_dependencies(source, deps)

        #os.remove(deps_tmp_file)

    def _update_dependencies(self, source, deps):
        if len(deps) == 0 and source in self.dependencies:
            del self.dependencies[source]
        elif len(deps) > 0:
            self.dependencies[source] = deps

