# ipylogue - IPython notebook storage backed by git

Like tracking checkpoints in your ipython notebooks? Perhaps you'd like better
control over their revisions. Then ipylogue is for you. Heavy duty VCS for your
ipython notebooks.

For another way to share notebooks, check out [bookstore][bookstore]
([Rackspace's post about it][blogpost]), which lets you publish notebooks to
OpenStack Swift (or Rackspace Cloud Files) automatically.

[bookstore]: https://github.com/rgbkrk/bookstore
[blogpost]: https://developer.rackspace.com/blog/bookstore-for-ipython-notebooks/

# What does it do?

Interactive computing can yield super cool results. Like discovering a new
pattern in your data, or stumbling on a better way of doing your work.

Wouldn't it be cool to save your steps so you can see the evolution of your
notebooks over time? Thought so.

```
* 48dbea0 - (HEAD, master) IPython notebook rename [Ryan S. Brown]
* 7dff1f3 - IPython notebook save [Ryan S. Brown]
* 91b7e32 - IPython notebook save [Ryan S. Brown]
```

Each save (or rename) event creates a new git commit in the notebook directory.
By default, that's wherever you ran `ipython notebook`.

# Usage

*Note: Requires IPython 2.0.0+*

*Second Note: Doesn't work on IPython 3+ (development version)*

Install ipylogue by running `pip install ipylogue`.

Create a profile (or, if you insist, edit the default profile).  You can
also use your default config, located at
`~/.ipython/profile_default/ipython_notebook_config.py`

```
$ ipython profile create ipylogue
[ProfileCreate] Generating default config file: u'/home/yourname/.ipython/profile_ipylogue/ipython_config.py'
[ProfileCreate] Generating default config file: u'/home/yourname/.ipython/profile_ipylogue/ipython_notebook_config.py'
[ProfileCreate] Generating default config file: u'/home/yourname/.ipython/profile_ipylogue/ipython_nbconvert_config.py'
```

Replace "ipylogue" with another name if you like. It will print the location of
the profile on your hard drive.

Add these lines to your ipython notebook profile (`ipython_notebook_config.py`):

```
c.NotebookApp.notebook_manager_class = 'ipylogue.gitmanager.GitNotebookManager'
c.GitNotebookManager.commiter_name = u'COMMITTER_NAME' # this is optional
c.GitNotebookManager.commiter_email = u'COMMITTER_EMAIL' # this is optional
```

Then go to a directory and run `ipython notebook --profile ipylogue`

Each time you save a notebook, ipylogue will commit the changes to git so you
never lose any history.

# Advanced Usage

Because ipylogue makes a commit for every save/rename while you work on your
notebook, it may be a good idea to squash some of your commits and add a
descriptive message. For more information on squashing commits, check out this
[thigitready.com tutorial][gitready].

[gitready]: http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html)

# Troubleshooting

If you encounter an error that looks like:

```
ImportError: IPython.html requires pyzmq >= 2.1.11
```

Try running `pip install ipython[notebook] --upgrade --force`

# TODO

Add the option to have the root of your notebook folder be a subdir of your repository

```
c.GitNotebookManager.repo_subdir = u'notebooks' # OPTIONAL: a directory *inside* the repo where you want notebooks to put notebooks
```

Add the option to do all notebook commits on a specific branch to be squashed
later.


# Licensing

Affero GPLv3, see COPYING.txt for full license

Also see https://github.com/FriendCode/gittle for dulwich usage examples
