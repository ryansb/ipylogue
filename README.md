# pitted - IPython notebook storage backed by git

Like tracking checkpoints in your ipython notebooks? Perhaps you'd like better
control over their revisions. Then pitted is for you. Heavy duty VCS for your
ipython notebooks.


# Usage

*Note: Requires IPython 1.0.0+*

Add this to your ipython notebook profile (`ipython_notebook_config.py`):

```
# c.NotebookApp.notebook_manager_class = 'IPython.html.services.notebooks.filenbmanager.FileNotebookManager'
c.NotebookApp.notebook_manager_class = 'pitted.gitmanager.GitNotebookManager'
c.GitNotebookManager.commiter_name = u'COMMITTER_NAME'
c.GitNotebookManager.commiter_email = u'COMMITTER_EMAIL'
c.GitNotebookManager.git_repo = u'/home/yourname/code/fancydatathings'
c.GitNotebookManager.repo_subdir = u'notebooks' # OPTIONAL: a directory *inside* the repo where you want notebooks to put notebooks
```

It's easy to set up a notebook profile if you don't have one:

```
$ ipython profile create pitted
[ProfileCreate] Generating default config file: u'/home/yourname/.ipython/profile_pitted/ipython_config.py'
[ProfileCreate] Generating default config file: u'/home/yourname/.ipython/profile_pitted/ipython_notebook_config.py'
[ProfileCreate] Generating default config file: u'/home/yourname/.ipython/profile_pitted/ipython_nbconvert_config.py'
```

You can also use your default config, located at `~/.ipython/profile_default/ipython_notebook_config.py`


# Licensing

Affero GPLv3, see COPYING.txt for full license

Also see https://github.com/FriendCode/gittle for dulwich usage examples
