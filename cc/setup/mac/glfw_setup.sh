#!/usr/bin/env bash
# Idempotent setup script which installs glfw (and any other ccircle dependencies).

################## IDEMPOTENT HELPER FUNCTIONS #####################
# Install brew.
function ensure_brew() {
    command -v brew >/dev/null 2>&1 || { echo >&2 "Installing Homebrew Now..."; \
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; }

    echo >&2 "Homebrew install confirmed."
}

# Install GLFW (glfw3) shared library binary view Homebrew.
function ensure_glfw_shared_library() {
    brew list glfw >/dev/null 2>&1 || { echo >&2 "Installing glfw shared library..."; \
    brew install glfw; }

    # After glfw is installed we need to set an environment variable so it is picked up by pyglfw.
    # First, ensure the dylib is in the canonical install location.
    local required_dylib_name='libglfw3.dylib'
    local canonical_dylib_name='libglfw.3.3.dylib'
    local installed_dylib_base="/usr/local/Cellar/glfw/3.3/lib"
    local installed_dylib_file="$installed_dylib_base/$canonical_dylib_name"
    [[ -f $installed_dylib_file ]] || { echo >&2 "Was expecting glfw dylib at location $installed_dylib_file"; \
    exit 1;}

     # Check for the 'correctly' named dylib, and exit if exists.
    if [[ ! -f "$installed_dylib_base/$required_dylib_name" ]]; then
        local command="ln -sf $installed_dylib_base/$canonical_dylib_name $installed_dylib_base/$required_dylib_name"
        echo >&2 "Creating a symlink for expected pyGlfw filename: $command"
        eval "$command"
    fi

    echo >&2 "glfw shared library install confirmed."
}

# Install glfw: https://pypi.org/project/glfw/.
function ensure_pyglfw() {
    { pip freeze | grep glfw >/dev/null 2>&1; } || { echo >&2 "Installing python bindings for glfw..."; \
    pip install glfw; }

    echo >&2 "glfw (python bindings) install confirmed."
}

# Install pyOpenGL.
function ensure_pyopengl() {
    { pip freeze | grep PyOpenGL >/dev/null 2>&1; } || { echo >&2 "Installing PyOpenGL..."; \
    pip install PyOpenGL; }

    echo >&2 "PyOpenGL install confirmed."
}
################# MAIN #####################
ensure_brew # OSX Package manager.
ensure_glfw_shared_library # OS-specific shared library.
ensure_pyglfw # Python bindings for glfw.
ensure_pyopengl

echo -e >&2 "\n---Ccircle dependencies confirmed.---"