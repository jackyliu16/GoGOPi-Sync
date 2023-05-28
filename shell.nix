{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    (python310.withPackages (ps: with ps; [
      opencv3
    ])) 
  ];
}
