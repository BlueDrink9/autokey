Contributing
============
When you want to contribute new features or fix things, you are free to take virtually any task you wish. Just open a PR for discussion and I’ll try to answer any questions that arise. I suggest writing new features on top of develop.

Please make sure tests pass before you submit PRs. To ensure this happens automatically, I recommend adding the following lines to the file `.git/hooks/pre-push`:

.. code:: sh
    remote="$1"
    url="$2"

    python3 setup.py test
    exit $?

This will stop the push if tests fail.

Testing
=======
Running the tests is simple: Checkout `develop` and run `python3 setup.py test`. Running individual test files or folders, or using pytest arguments, can be done with `python3 -m pytest tests/[test file] [--opt]`


Testing requires pytest and PyHamcrest as new test-time only dependencies.

The current `master` tests are deprecated and won’t work. They are still on Python 2 and nobody cared to update them throughout the years, not even the original developer. They test things long gone in the project code…
The old tests are scheduled to be replaced by a new suite in the `develop` branch, which will be merged as 0.96.0.

The current situation is a bit unfortunate: The new suite lives in the develop branch, which accumulates new features, but which can't be backported to master without introducing merge conflicts later on. So until develop gets merged in, you’d have to switch to develop to run the tests.

