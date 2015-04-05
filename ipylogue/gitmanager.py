#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Ryan Brown <sb@ryansb.com>
#
# This file is part of ipylogue.
#
# ipylogue is free software: you can redistribute it and/or modify
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
from IPython.html.services.contents.filemanager import FileContentsManager

import os

#TODO Make checkpoints like here: https://github.com/rgbkrk/bookstore/blob/master/bookstore/swift.py

class GitNotebookManager(FileContentsManager):
    """Git-backed storage of ipython notebooks.
    """
    committer_name = Unicode('', config=True,
                             help="The name of the committer (probably your "
                             "name). Pulls from ~/.gitconfig if blank.")
    committer_email = Unicode('', config=True,
                              help="The email address the commits should come "
                              "from (probably yours). Pulls from ~/.gitconfig "
                              "if blank.")

    @property
    def committer_fullname(self):
        c = "{} <{}>".format(self.committer_name, self.committer_email)
        self.log.debug("Committing as " + c)
        return c

    _repo = None

    def __init__(self, **kwargs):
        super(GitNotebookManager, self).__init__(**kwargs)
        self._check_repo()
        if not self.committer_email:
            self.committer_email = self._repo.get_config_stack().get('user', 'email')
        if not self.committer_name:
            self.committer_name = self._repo.get_config_stack().get('user', 'name')

    def _check_repo(self):
        self.notebook_dir = super(GitNotebookManager, self)._get_os_path("")
        if self._repo is not None:
            return
        try:
            self._repo = git.Repo(self.notebook_dir)
        except NotGitRepository:
            git.Repo.init(self.notebook_dir)
            self._repo = git.Repo(self.notebook_dir)

    def save(self, model, path=''):
        self.notebook_dir = super(GitNotebookManager, self)._get_os_path("")
        self._check_repo()

        model = super(GitNotebookManager, self).save(
            model, path)

        os_path = super(GitNotebookManager, self)._get_os_path(
            model['path'])
        local_path = os_path[len(self.notebook_dir):].strip('/')

        git.add(self._repo, [str(local_path)])  # path must not be unicode. :(

        if self.save_script:
            git.add(self._repo, [str(os.path.splitext(local_path)[0] + '.py')])

        self.log.debug("Notebook added %s" % local_path)
        git.commit(self._repo, "IPython notebook save\n\n"
                   "Automated commit from IPython via ipylogue",
                   committer=self.committer_fullname)
        return model

    def update(self, model, path):
        #TODO
        return super(GitNotebookManager, self).update(model, path)

    def delete(self, path):
        #TODO
        return super(GitNotebookManager, self).delete(path)

    def rename_file(self, old_path, new_path):
        # paths must not be unicode. :(
        old_files = [old_path]
        new_files = [new_path]
        if self.save_script:
            old_files.append(old_files[0].replace('.ipynb', '.py'))
            new_files.append(new_files[0].replace('.ipynb', '.py'))

        git.rm(self._repo, [str(_) for _ in old_files])

        renamed = super(GitNotebookManager, self).rename_file(old_path, new_path)

        git.add(self._repo, [str(_) for _ in new_files])

        self.log.debug("Notebook renamed from '%s' to '%s'" % (old_files[0],
                                                               new_files[0]))
        git.commit(self._repo, "IPython notebook rename\n\n"
                   "Automated commit from IPython via ipylogue",
                   committer=self.committer_fullname)
        return renamed

    #def info_string(self):
    #    return "Serving notebooks from local git repository: %s" % self.notebook_dir
