import sys

from invoke import task, run
from colorama import init, Fore
""" automatically set back to default color after every print """
init(autoreset=True)

if sys.platform == 'darwin':
    DEFAULT_ENV = 'local'
else:
    DEFAULT_ENV = 'development'


@task
def clean(ctx):
    """Remove all .pyc files."""
    print(Fore.GREEN + 'Clean up .pyc files')
    run("find . -name '*.py[co]' -exec rm -f '{}' ';'")


@task
def lint(ctx):
    """Check for lints"""
    print(Fore.GREEN + 'Checking for lints')
    result = run('flake8 src/h3 '
                 '--ignore=E501,E702,E712,C901', warn=True)
    if result.exited == 0:
        print(Fore.GREEN + 'Linty fresh!')
    else:
        print(Fore.RED + 'Too much lint :(')


@task
def bootstrap(ctx):
    """Bootstrap the environment."""
    print(Fore.GREEN + '\nInstalling requirements')
    run('pip install -r requirements-dev.txt')
    run('python setup.py develop')


@task
def test(ctx,
         args='',
         cov_report='term-missing',
         junit_xml=None,
         arc_cover=False):
    """Run the test suite."""
    lint(ctx)

    if cov_report:
        cmd = ('py.test tests/* -rs -s --tb short %s ' '--cov h3 --cov-report %s' % (args, cov_report))
    else:
        cmd = ("py.test tests -rs -s --tb short %s " % (args, ))

    if junit_xml:
        cmd = '%s --junit-xml %s' % (cmd, junit_xml)

    if arc_cover:
        run("mv coverage.xml coverage/cobertura-coverage.xml")

    result = run(cmd, warn=True)
    if result.exited == 0:
        print(Fore.GREEN + 'Tests finished running with success.')
    else:
        print(Fore.RED + 'Test finished running with errors.')
        sys.exit(1)


@task
def shell(ctx):
    """Run the shell in the environment."""
    run("ipython -i -c 'from h3 import h3;'")
