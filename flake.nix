{
  description = "x-cli - CLI for X/Twitter API v2 using uv2nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      nixpkgs,
      pyproject-nix,
      uv2nix,
      pyproject-build-systems,
      ...
    }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;

      # Load workspace from uv.lock and pyproject.toml
      workspace = uv2nix.lib.workspace.loadWorkspace { workspaceRoot = ./.; };

      # Create overlay from lock file (builds packages as nix derivations)
      overlay = workspace.mkPyprojectOverlay {
        sourcePreference = "wheel";  # Use wheels for faster builds
      };

      # Editable overlay for development (points to src/)
      editableOverlay = workspace.mkEditablePyprojectOverlay {
        root = "$REPO_ROOT";
      };

      # Build Python sets for each system
      pythonSets = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python313;  # Match your Python version
        in
        (pkgs.callPackage pyproject-nix.build.packages {
          inherit python;
        }).overrideScope
          (
            lib.composeManyExtensions [
              pyproject-build-systems.overlays.wheel
              overlay
            ]
          )
      );

    in
    {
      # Development shell with editable install
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          pythonSet = pythonSets.${system}.overrideScope editableOverlay;
          virtualenv = pythonSet.mkVirtualEnv "x-cli-dev-env" workspace.deps.all;
        in
        {
          default = pkgs.mkShell {
            packages = [
              virtualenv
              pkgs.uv
              pkgs.basedpyright
              pkgs.ruff  # Keep ruff in nix for editor integration
            ];
            env = {
              UV_NO_SYNC = "1";  # Don't sync, use nix-built venv
              UV_PYTHON = pythonSet.python.interpreter;
              UV_PYTHON_DOWNLOADS = "never";
            };
            shellHook = ''
              unset PYTHONPATH
              export REPO_ROOT=$(git rev-parse --show-toplevel)
              echo "x-cli dev shell ready!"
              echo ""
              echo "Commands:"
              echo "  x-cli <command>           # Run the CLI"
              echo "  pytest                    # Run tests"
              echo "  ruff check .              # Run linter"
              echo "  ruff format .             # Run formatter"
              echo "  basedpyright src/         # Run type checker"
              echo "  uv add <package>          # Add dependency (then exit and re-enter shell)"
            '';
          };
        }
      );

      # Build package for distribution
      packages = forAllSystems (system: {
        default = pythonSets.${system}.mkVirtualEnv "x-cli-env" workspace.deps.default;
      });
    };
}
