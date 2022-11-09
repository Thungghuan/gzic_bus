{
  description = "gzic_bus: 赶快坐上华南理工大学广州国际校区校巴";
  inputs = {
    nixpkgs.url = github:NixOS/nixpkgs/nixos-22.05;
    flake-utils.url = github:numtide/flake-utils;
    mach-nix.url = github:DavHau/mach-nix;
  };

  outputs = { self, nixpkgs, flake-utils, mach-nix, ... }@inputs:
    flake-utils.lib.eachDefaultSystem (system:
      let
        python = "python310";
        pkgs = (import nixpkgs {
          inherit system;
        }).pkgs;
        mach-nix-utils = import mach-nix {
          inherit pkgs;
          inherit python;
        };
        requirements = builtins.readFile ./requirements.txt;
      in
      {
        devShell = mach-nix-utils.mkPythonShell { inherit requirements; };
        packages.venv = mach-nix-utils.mkPython { inherit requirements; };
      });
}
