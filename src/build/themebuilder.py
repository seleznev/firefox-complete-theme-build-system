#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
import time
import json
import subprocess
import zipfile

from addonbuilder import AddonBuilder

class ThemeBuilder(AddonBuilder):
    def __init__(self, config=None, build_dir=".build", theme_dir="theme"):
        AddonBuilder.__init__(self, config=config, build_dir=build_dir)

        self.theme_dir = os.path.normpath(theme_dir)
        self.build_theme_dir = os.path.join(
                             self.build_dir,
                             os.path.basename(self.theme_dir))

        self.shared_dir = self.config["directory-structure"]["shared-dir"]

        self.default_dependencies = {
            os.path.join(self.theme_dir, "install.rdf.in"): ["config.json"],
            os.path.join(self.theme_dir, "chrome.manifest.in"): ["config.json"]
        }

    def _validate_config(self, config):
        config = AddonBuilder._validate_config(self, config)

        if not "directory-structure" in config:
            config["directory-structure"] = {}
            config["directory-structure"]["shared-dir"] = "shared"

        return config

    def build(self):
        self.app_versions = []
        for name in os.listdir(self.theme_dir):
            if name.startswith("chrome-"):
                version = int(name.replace("chrome-", ""))
                self.app_versions.append(version)

        self.dependencies = self._load_dependencies_cache()

        self.files_to_xpi = []

        for base, dirs, files in os.walk(self.theme_dir):
            for name in files:
                self._process_file(os.path.join(base, name))

        xpi = zipfile.ZipFile(self.config["xpi"]["theme"], "w")
        for i in self.files_to_xpi:
            xpi.write(i[0], i[1])
        xpi.close()
        del self.files_to_xpi

        self._save_dependencies_cache(self.dependencies)

    def _load_dependencies_cache(self):
        path = os.path.join(self.build_dir, "deps.cache")
        if not os.path.exists(path):
            return self.default_dependencies
        with open(path, "r") as cache_file:
            return json.load(cache_file)

    def _save_dependencies_cache(self, deps):
        with open(os.path.join(self.build_dir, "deps.cache"), "w") as cache_file:
            json.dump(deps, cache_file)

    def _generate_chrome_manifest(self, source, target):
        print("Convert " + source + " to " + target)

        os.makedirs(os.path.dirname(target), exist_ok=True)

        subprocess.call(["build/manifest.sh",
                        "-m", str(min(self.app_versions)),
                        "-M", str(max(self.app_versions)),
                        source, target])

    def _preprocess(self, source, target, current_version):
        print("Convert " + source + " to " + target)

        deps_tmp_file = os.path.join(self.build_dir, "deps.tmp")

        os.makedirs(os.path.dirname(target), exist_ok=True)
        a = subprocess.call(["python2", "build/preprocessor.py",
                         "--marker=%",
                         "--depend=" + deps_tmp_file,
                         "-D", "APP_VERSION="+str(current_version)+"",
                         "--output="+target, source])

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

    def _process_file(self, source):
        source_short = source[len(self.theme_dir)+1:]

        if source_short in ["chrome.manifest.in", "install.rdf.in"]:
            target = os.path.join(self.build_theme_dir, source_short[:-3])

            deps = [source]
            if source in self.dependencies:
                deps = deps + self.dependencies[source]

            if not self._is_need_update(target, deps):
                return

            if source_short == "chrome.manifest.in":
                self._generate_chrome_manifest(source, target)
            else:
                self._generate_install_manifest(source, target)
        elif source_short.endswith(".inc.css"):
            pass
        elif source_short.startswith(self.shared_dir + "/"):
            for app_version in self.app_versions:
                sub_path = re.sub(r"^"+self.shared_dir,
                                  "chrome-" + str(app_version),
                                  source_short)

                if os.path.exists(os.path.join(self.theme_dir, sub_path)):
                    continue

                target = sub_path

                deps = [source]
                if source in self.dependencies:
                    deps = deps + self.dependencies[source]

                if source_short.endswith(".css"):
                    source_res = os.path.join(self.build_theme_dir, sub_path)
                    if self._is_need_update(source_res, deps):
                        self._preprocess(source, source_res, app_version)
                    self.files_to_xpi.append([source_res, target])
                else:
                    self.files_to_xpi.append([source, target])
        else:
            target = source_short

            deps = [source]
            if source in self.dependencies:
                deps = deps + self.dependencies[source]

            if source_short.endswith(".css"):
                source_res = os.path.join(self.build_theme_dir, source_short)
                if self._is_need_update(source_res, deps):
                    if source_short.startswith("chrome-"):
                        app_version = re.sub(r"^chrome-", "", source_short)
                        app_version = re.sub(r"\/.*", "", app_version)
                        app_version = int(app_version)
                    self._preprocess(source, source_res, app_version)
                self.files_to_xpi.append([source_res, target])
            else:
                self.files_to_xpi.append([source, target])

