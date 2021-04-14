{
  description = "lrt-plot";

  outputs = { self, nixpkgs }: let
    pkgs = import nixpkgs {
      system = "x86_64-linux";
    };
  in {
    devShell.x86_64-linux = pkgs.mkShell {
      name = "lrt-plot";
      buildInputs = with pkgs.python3Packages; [
        python
        pandas
        matplotlib
        numpy
      ];
    };
  };
}
