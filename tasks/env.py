from invoke import task

# https://github.com/pyinvoke/invoke/issues/682
@task
def julia_daemon(ctx):
    """Run julia server, that is responsible for running all julia scripts."""
    ctx.run("julia --project=@. --startup-file=no -e 'using Revise; using DaemonMode; serve()'", disown=True)

@task
def setup_pre_commit_hook(ctx):
    """Setup pre-commit hook to automate check before git commit and git push."""
    ctx.run("git init")
    ctx.run("pre-commit install -t pre-commit")
    ctx.run("pre-commit install -t pre-push")
    ctx.run("pre-commit install -t commit-msg")

@task
def julia_instantiate(ctx):
    """Download all dependencies of the current julia project and precompile all dependencies."""
    ctx.run("julia --project=@. -e 'using Pkg; Pkg.instantiate(); Pkg.precompile()'", pty=True)

@task(optional=["no-pre-commit"])
def init_dev(ctx, no_pre_commit=False):
    """Install development dependencies and setup pre-commit hooks."""
    julia_instantiate(ctx)
    if not no_pre_commit:
        setup_pre_commit_hook(ctx)
