#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ryan Brown <sb@ryansb.com>
#
# This file is part of pitted.
#
# pitted is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import dulwich.porcelain as git
from dulwich.errors import NotGitRepository

from IPython.utils.traitlets import Bool, Unicode
from IPython.html.services.notebooks.filenbmanager import FileNotebookManager

import os
from os import getcwd


class PittedConfigurationException(Exception):
    pass


class GitNotebookManager(FileNotebookManager):
    """Git-backed storage of ipython notebooks.
    """
    save_script = Bool(
        False, config=True,
        help="""Automatically create a Python script when saving the notebook.

        For easier use of import, %run and %load across notebooks, a
        <notebook-name>.py script will be created next to any
        <notebook-name>.ipynb on each save.  This can also be set with the
        short `--script` flag.
        """
    )
    notebook_dir = Unicode(getcwd(), config=True)
    committer_name = Unicode("Mr. Anonymous", config=True)
    committer_email = Unicode("anon@ymo.us", config=True)

    @property
    def committer_fullname(self):
        c = "{} <{}>".format(self.committer_name, self.committer_email)
        self.log.debug("Committing as " + c)
        return c

    _repo = None

    def __init__(self, **kwargs):
        super(GitNotebookManager, self).__init__(**kwargs)
        self._check_repo()

    def _check_repo(self):
        if self._repo is not None:
            return
        try:
            self._repo = git.Repo(self.notebook_dir)
        except NotGitRepository:
            git.Repo.init(self.notebook_dir)
            self._repo = git.Repo(self.notebook_dir)

    def _notebook_dir_changed(self, name, old, new):
        return super(GitNotebookManager, self)._notebook_dir_changed(name, old,
                                                                     new)

    def _copy(self, src, dest):
        return super(GitNotebookManager, self)._copy(src, dest)

    def get_notebook_names(self, path=''):
        return super(GitNotebookManager, self).get_notebook_names(path)

    def path_exists(self, path):
        return super(GitNotebookManager, self).path_exists(path)

    def is_hidden(self, path):
        return super(GitNotebookManager, self).is_hidden(path)

    def notebook_exists(self, name, path=''):
        return super(GitNotebookManager, self).notebook_exists(name, path)

    def list_dirs(self, path):
        return super(GitNotebookManager, self).list_dirs(path)

    def get_dir_model(self, name, path=''):
        return super(GitNotebookManager, self).get_dir_model(name, path)

    def list_notebooks(self, path):
        return super(GitNotebookManager, self).list_notebooks(path)

    def get_notebook(self, name, path='', content=True):
        return super(GitNotebookManager, self).get_notebook(name, path,
                                                            content)

    def save_notebook(self, model, name='', path=''):
        self._check_repo()

        model = super(GitNotebookManager, self).save_notebook(
            model, name, path)

        os_path = super(GitNotebookManager, self)._get_os_path(
            model['name'], model['path'])
        local_path = os_path[len(self.notebook_dir):].strip('/')

        git.add(self._repo, str(local_path))  # path must not be unicode. :(

        if self.save_script:
            git.add(self._repo, str(os.path.splitext(local_path)[0] + '.py'))

        self.log.debug("Notebook added %s" % local_path)
        git.commit(self._repo, "IPython Save",
                   committer=self.committer_fullname)
        return model

    def update_notebook(self, model, name, path=''):
        return super(GitNotebookManager, self
                     ).update_notebook(model, name, path)

    def delete_notebook(self, name, path=''):
        return super(GitNotebookManager, self).delete_notebook(name, path)

    def rename_notebook(self, old_name, old_path, new_name, new_path):
        return super(GitNotebookManager, self
                     ).rename_notebook(old_name, old_path, new_name, new_path)

    # Checkpoint-related utilities

    def get_checkpoint_path(self, checkpoint_id, name, path=''):
        return super(GitNotebookManager, self
                     ).get_checkpoint_path(checkpoint_id, name, path)

    def get_checkpoint_model(self, checkpoint_id, name, path=''):
        return super(GitNotebookManager, self
                     ).get_checkpoint_model(checkpoint_id, name, path)

    # public checkpoint API

    def create_checkpoint(self, name, path=''):
        return super(GitNotebookManager, self).create_checkpoint(name, path)

    def list_checkpoints(self, name, path=''):
        return super(GitNotebookManager, self).list_checkpoints(name, path)

    def restore_checkpoint(self, checkpoint_id, name, path=''):
        return super(GitNotebookManager,
                     self).restore_checkpoint(checkpoint_id, name, path)

    def delete_checkpoint(self, checkpoint_id, name, path=''):
        return super(GitNotebookManager, self).delete_checkpoint(checkpoint_id,
                                                                 name, path)

    def info_string(self):
        return "Serving notebooks from local git repository: %s" % self.notebook_dir
