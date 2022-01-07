from invoke import Collection

from tasks import env, nb, style, test

ns = Collection()
ns.add_collection(env)
ns.add_collection(nb)
ns.add_collection(style)
ns.add_collection(test)
