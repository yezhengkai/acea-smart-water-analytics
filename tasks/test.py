from invoke import task
from tasks.common import JL_PROJECT_PKG_NAME

@task(default=True)
def run(ctx):
    """Run test cases."""
    ctx.run('julia --project=@. -e \'using Pkg; Pkg.activate("."); Pkg.test()\'', pty=True)

@task
def cov(ctx):
    """Run test coverage check."""
    ctx.run(
        'julia --project=@. -e'
        + f' \'using LocalCoverage; generate_coverage("{JL_PROJECT_PKG_NAME}");'
        + f' clean_coverage("{JL_PROJECT_PKG_NAME}"; rm_directory=false);\'',
        pty=True
    )
