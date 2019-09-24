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
