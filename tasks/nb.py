from invoke import task

@task
def lab(ctx):
    """Run jupyter lab at notebooks directory."""
    ctx.run("jupyter lab --notebook-dir=notebooks --port=8888", pty=True)

@task
def pluto(ctx):
    """Run Pluto.jl at notebooks directory."""
    ctx.run("cd notebooks && julia --project=@. -e 'using Pluto; Pluto.run()'", pty=True)
