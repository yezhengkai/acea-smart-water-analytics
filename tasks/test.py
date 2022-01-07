from invoke import task

@task(default=True)
def run(ctx):
    """Run test cases."""
    ctx.run('julia --project=@. -e \'using Pkg; Pkg.activate("."); Pkg.test()\'', pty=True)
