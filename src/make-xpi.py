#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
import shutil
import argparse

sys.path.insert(0, "./build")

import console
import addonconf
from themebuilder import ThemeBuilder
from extensionbuilder import ExtensionBuilder
from packagebuilder import PackageBuilder

def main():
    console.start_timer()

    config = addonconf.load("config.json")
    if not config:
        sys.exit(1)

    available_actions = []
    package_is_avaliable = True
    for t in ["theme", "extension"]:
        if t in config:
            available_actions = available_actions + [t]
        else:
            package_is_avaliable = False
    if package_is_avaliable and "package" in config:
        available_actions = available_actions + ["package"]

    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs='?', default="all",
                        choices=["all"] + available_actions + ["clean"],
                        help="build theme, extension, package or clean sources")
    parser.add_argument("--version",
                        help="override version from config.json")
    parser.add_argument("--target-version", type=int,
                        help="build for a certain version only")
    parser.add_argument("--force-rebuild", action="store_true",
                        help="regenerate all needed files")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="increase output verbosity")
    args = parser.parse_args()

    action = args.action

    # Override preferences from config.json
    if "VERSION" in os.environ:
        config["version"] = os.environ.get("VERSION")
        config["override-version"] = True
    if args.version:
        config["version"] = args.version
        config["override-version"] = True

    if args.target_version:
        config["target-version"] = args.target_version

    config["force-rebuild"] = args.force_rebuild
    config["verbose"] = args.verbose

    config = addonconf.validate(config)
    if not config:
        sys.exit(1)

    # Clean up
    if action == "clean":
        clean_paths = []
        if os.path.isdir(".build"):
            for base, dirs, files in os.walk(".build", topdown=False):
                for name in files:
                    clean_paths.append(os.path.join(base, name))
                for name in dirs:
                    clean_paths.append(os.path.join(base, name))
            clean_paths.append(".build")

        for base, dirs, files in os.walk("build"):
            for name in files:
                if name.endswith(".pyc"):
                    clean_paths.append(os.path.join(base, name))
        clean_paths.append("build/__pycache__")

        for i in available_actions:
            clean_paths.append(config[i]["xpi"])

        for path in clean_paths:
            path = os.path.abspath(path)
            if not os.path.exists(path):
                continue
            console.log("removing", path)
            if os.path.isfile(path):
                os.remove(path)
            else:
                os.rmdir(path)

        sys.exit(0)

    # Theme building
    if action in ["theme", "all"] and "theme" in available_actions:
        builder = ThemeBuilder(config)
        print(":: Starting build theme...")
        builder.build()

    # Extension building
    if action in ["extension", "all"] and "extension" in available_actions:
        builder = ExtensionBuilder(config)
        print(":: Starting build extension...")
        builder.build()

    # Package building
    if action in ["package", "all"] and "package" in available_actions:
        builder = PackageBuilder(config)
        print(":: Starting make package...")
        builder.build()

if __name__ == "__main__":
    main()

