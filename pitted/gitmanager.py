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

from IPython.utils.traitlets import Unicode
from IPython.html.services.notebooks.filenbmanager import FileNotebookManager

import os


class PittedConfigurationException(Exception):
    pass


class GitNotebookManager(FileNotebookManager):
    """Git-backed storage of ipython notebooks.
    """
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
        #TODO
        return super(GitNotebookManager, self
                     ).update_notebook(model, name, path)

    def delete_notebook(self, name, path=''):
        #TODO
        return super(GitNotebookManager, self).delete_notebook(name, path)

    def rename_notebook(self, old_name, old_path, new_name, new_path):
        #TODO
        return super(GitNotebookManager, self
                     ).rename_notebook(old_name, old_path, new_name, new_path)

    def info_string(self):
        return "Serving notebooks from local git repository: %s" % self.notebook_dir
