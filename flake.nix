{
  description = "lrt-plot";

  outputs = { self, nixpkgs }: let
    pkgs = import nixpkgs {
      system = "x86_64-linux";
    };
  in {
    devShell.x86_64-linux = pkgs.mkShell {
      name = "lrt-plot";
      buildInputs = (with pkgs; [
        cairo
        pkg-config
      ]) ++ (with pkgs.python3Packages; [
        python
        virtualenv
      ]);
      shellHook = ''
        if [ ! -d ./venv ]; then
          virtualenv ./venv
          ./venv/bin/pip install -r ./requirements.txt
        fi
        source ./venv/bin/activate
      '';
    };
  };
}
