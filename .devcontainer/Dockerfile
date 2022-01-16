# References:
# https://github.com/andferrari/julia_notebook/blob/master/Dockerfile
# https://github.com/marius311/CMBLensing.jl/blob/master/Dockerfile
# https://github.com/MalteBoehm/julia_docker-compose_template/blob/main/Dockerfile

FROM jupyter/minimal-notebook:python-3.9.7


USER root

# [Optional] Add sudo support. Omit if you don't need to install software after connecting.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        sudo \
        curl \
        bash-completion \
        lcov \
    && echo $NB_USER ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$NB_USER \
    && chmod 0440 /etc/sudoers.d/$NB_USER \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# Install Julia
ARG VARIANT="1.6.5"
RUN mkdir /opt/julia-${VARIANT} \
    && curl -L https://julialang-s3.julialang.org/bin/linux/x64/`echo ${VARIANT} | cut -d. -f 1,2`/julia-${VARIANT}-linux-x86_64.tar.gz | tar zxf - -C /opt/julia-${VARIANT} --strip=1 \
    && ln -fs /opt/julia-${VARIANT}/bin/julia /usr/local/bin/julia


USER $NB_USER

ARG PROJECT_DIR=/home/jovyan/julia-project
WORKDIR $PROJECT_DIR

# Add python packages and add invoke shell completion
RUN mamba install --quiet --yes \
        numpy=1.21 \
        pandas=1.3 \
        matplotlib=3.5 \
        scipy=1.7 \
        scikit-learn=1.0 \
        invoke=1.6 \
        pre-commit=2.16 \
        commitizen=2.20 \
        dvc-s3=2.9 \
        dvc-gdrive=2.9 \
    && mamba clean --all -f -y \
    && npm cache clean --force

# Add julia packages and precompile
RUN julia -e 'using Pkg; Pkg.update()' \
    && julia -e '\
        using Pkg; \
        Pkg.add( \
            [ \
                PackageSpec(name="Revise", version="3.3"), \
                PackageSpec(name="BenchmarkTools", version="1.2"), \
                PackageSpec(name="OhMyREPL", version="0.5"), \
                PackageSpec(name="JuliaFormatter", version="0.21"), \
                PackageSpec(name="Documenter", version="0.27"), \
                PackageSpec(name="LiveServer", version="0.7"), \
                PackageSpec(name="Pluto", version="0.17"), \
                PackageSpec(name="PlutoUI", version="0.7"), \
                PackageSpec(name="DaemonMode", version="0.1"), \
                PackageSpec(name="LocalCoverage", version="0.2"), \
            ] \
        ) \
    ' \
    && julia -e ' \
        using Pkg; \
        Pkg.add(name="IJulia", version="1.23"); \
        using IJulia \
    '

ENV JULIA_PROJECT=@.

# Avoid VS Code extension reinstalls
# https://code.visualstudio.com/remote/advancedcontainers/avoid-extension-reinstalls
RUN mkdir -p /home/$NB_USER/.vscode-server/extensions \
        /home/$NB_USER/.vscode-server-insiders/extensions \
    && chown -R $NB_USER \
        /home/$NB_USER/.vscode-server \
        /home/$NB_USER/.vscode-server-insiders

# Jupyterlab settings
RUN mkdir -p /home/$NB_USER/.jupyter/lab/user-settings/@jupyterlab/notebook-extension \
    && echo '{"codeCellConfig": {"lineNumbers": true}}' \
        >> /home/$NB_USER/.jupyter/lab/user-settings/@jupyterlab/notebook-extension/tracker.jupyterlab-settings \
    && mkdir -p /home/$NB_USER/.jupyter/lab/user-settings/@jupyterlab/shortcuts-extension \
    && echo '{"shortcuts": [{"command": "runmenu:restart-and-run-all", "keys": ["Alt R"], "selector": "[data-jp-code-runner]"}]}' \
        >> /home/$NB_USER/.jupyter/lab/user-settings/@jupyterlab/shortcuts-extension/shortcuts.jupyterlab-settings \
    && mkdir -p /home/$NB_USER/.jupyter/lab/user-settings/@jupyterlab/apputils-extension \
    && echo '{"modal": false}' \
        >> /home/$NB_USER/.jupyter/lab/user-settings/@jupyterlab/apputils-extension/palette.jupyterlab-settings

# Shell completion and alias
RUN inv --print-completion-script bash > ~/.invoke-completion.sh \
    && echo "source ~/.invoke-completion.sh" >> ~/.bashrc \
    && dvc completion -s bash | sudo tee /etc/bash_completion.d/dvc \
    && echo -e "alias juliaclient='julia --startup-file=no -e \"using DaemonMode; runargs()\"'" >> ~/.bashrc

# Install Starship
RUN sh -c "$(curl -fsSL https://starship.rs/install.sh)" -- -y \
    && echo 'eval "$(starship init bash)"' >> ~/.bashrc \
    && mkdir -p ~/.config \
    && echo -e '[conda]\nsymbol = "Conda "\nignore_base = false' > ~/.config/starship.toml

RUN fix-permissions /home/$NB_USER

# Pluto port
EXPOSE 1234
