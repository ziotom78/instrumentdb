# Contributing to InstrumentDB

If you want to give a hand, thanks! You're encouraged to submit [pull requests](https://github.com/ziotom78/instrumentdb/pulls), [propose features and discuss issues](https://github.com/ziotom78/instrumentdb/issues).

In the examples below, substitute your Github username for `YOUR-GITHUB-NAME-HERE` in URLs.

### Fork the Project

Fork the [project on Github](https://github.com/ziotom78/instrumentdb) and check out your copy.

```
git clone https://github.com/YOUR-GITHUB-NAME-HERE/instrumentdb.git
cd instrumentdb
git remote add upstream https://github.com/ziotom78/instrumentdb.git
```

### Install and Test

Ensure that you can build the project and run tests. Follow the Installation guide in the [README](./README.md), then run

```
python manage.py test
```

## Contribute Code

### Create a Topic Branch

Make sure your fork is up-to-date and create a topic branch for your feature or bug fix.

```
git checkout master
git pull upstream master
git checkout -b my-feature-branch
```

### Write Tests

Try to write a test that reproduces the problem you're trying to fix or describes a feature that you want to build.

We definitely appreciate pull requests that highlight or reproduce a problem, even without a fix.

### Write Code

Implement your feature or bug fix.

### Write Documentation

Document any external behavior in the [documentation](https://instrumentdb.readthedocs.io/en/latest/?badge=latest). (You will need to use [Sphinx](https://www.sphinx-doc.org/en/master/) for that…)

### Update Changelog

Add a line to [CHANGELOG](CHANGELOG.md) under *HEAD*.

Make it look like every other line, including a link to the issue being fixed, your name and link to your Github account.

### Commit Changes

Make sure git knows your name and email address:

```
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
```

Try to write a good, descriptive commit log.

```
git add ...
git commit
```

### Push

```
git push origin my-feature-branch
```

### Make a Pull Request

Go to https://github.com/YOUR-GITHUB-NAME-HERE/instrumentdb and select your feature branch. Click the 'Pull Request' button and fill out the form. Pull requests are usually reviewed within a few days.

### Update CHANGELOG Again

Update the [CHANGELOG](CHANGELOG.md) with the pull request number. A typical entry looks as follows.

```
* [#12345](https://github.com/ziotom78/instrumentdb/pull/12345): New awesome feature - [@YOUR-GITHUB-NAME-HERE](https://github.com/YOUR-GITHUB-NAME-HERE).
```

Amend your previous commit and force push the changes.

```
git commit --amend
git push origin my-feature-branch -f
```

### Rebase

If you've been working on a change for a while, rebase with `upstream/master`.

```
git fetch upstream
git rebase upstream/master
git push origin my-feature-branch -f
```

### Check on Your Pull Request

Go back to your pull request after a few minutes and see whether the tests passed. Everything should look green, otherwise fix issues and amend your commit as described above.
