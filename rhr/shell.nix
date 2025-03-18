with import <nixpkgs> {};
mkShell { 
    buildInputs = [ glibc.static gcc ];
}
