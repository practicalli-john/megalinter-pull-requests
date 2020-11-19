#!/usr/bin/env python3
"""
Updated Repository reporter
Creates a folder containing only files updated by the linters
"""
import logging
import os
import shutil

from megalinter import Reporter, utils


class UpdatedSourcesReporter(Reporter):
    name = "UPDATED_SOURCES"
    scope = "mega-linter"

    def __init__(self, params=None):
        # Activate update repository reporter by default
        self.is_active = True
        super().__init__(params)

    def manage_activation(self):
        if os.environ.get("UPDATED_SOURCES_REPORTER", "true") != "true":
            self.is_active = False

    def produce_report(self):
        logging.debug("Start updated Sources Reporter")
        # Copy updated files in report folder
        updated_files = utils.list_updated_files(self.master.github_workspace)
        logging.debug("Updated files :\n" + "\n -".join(updated_files))
        updated_dir = os.environ.get("UPDATED_SOURCES_REPORTER_DIR", "updated_sources")
        updated_sources_dir = f"{self.report_folder}{os.path.sep}{updated_dir}"
        for updated_file in updated_files:
            updated_file_clean = updated_file.replace("/tmp/lint/", "")
            if updated_file_clean in ["linter-helps.json", "linter-versions.json"]:
                continue
            target_file = f"{updated_sources_dir}{os.path.sep}{updated_file_clean}"
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            shutil.copy(
                utils.REPO_HOME_DEFAULT + os.path.sep + updated_file, target_file
            )
            logging.debug(f"Copied {updated_file} to {target_file}")
        # Log
        if len(updated_files) > 0:
            logging.info(
                f"Updated Sources Reporter: copied {str(len(updated_files))} fixed source files"
                f" in folder {updated_sources_dir}."
                f"Copy-paste it in your local repo to apply linters updates"
            )
        else:
            logging.info(
                "Updated Sources Reporter: No source file has been formatted or fixed"
            )