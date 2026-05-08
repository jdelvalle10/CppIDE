# =============================================================================
# Doral Academy / Miami Dade College — C++ IDE Container
# Base: code-server (VS Code in browser)
# Compiler: GCC 12, C++17 support
# Maintainer: Professor Del Valle
# =============================================================================

FROM codercom/code-server:4.23.1

USER root

# ── System packages ───────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    gcc \
    make \
    cmake \
    gdb \
    valgrind \
    git \
    curl \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Switch to non-root coder user ────────────────────────────────────────────
USER coder

# ── Install VS Code extensions ────────────────────────────────────────────────
RUN code-server --install-extension ms-vscode.cpptools
RUN code-server --install-extension ms-vscode.cpptools-extension-pack
RUN code-server --install-extension formulahendry.code-runner

# ── VS Code user settings ─────────────────────────────────────────────────────
RUN mkdir -p /home/coder/.local/share/code-server/User
COPY --chown=coder:coder settings.json \
     /home/coder/.local/share/code-server/User/settings.json

# ── Workspace ─────────────────────────────────────────────────────────────────
RUN mkdir -p /home/coder/project
WORKDIR /home/coder/project
COPY --chown=coder:coder hello.cpp /home/coder/project/hello.cpp

EXPOSE 8080
