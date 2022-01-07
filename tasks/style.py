from invoke import task

@task
def reformat(ctx):
    """Format your code through `JuliaFormatter.jl`."""
    ctx.run('julia -e \'using DaemonMode; runexpr(raw"using JuliaFormatter; format(\\".\\")")\'')
