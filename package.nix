{ lib
, python3Packages
}:

python3Packages.buildPythonApplication {
  pname = "cse412_backend";
  version = "0.0.1";
  pyproject = true;

  src = ./.;

  build-system = with python3Packages; [
    setuptools
    wheel
  ];

  dependencies = with python3Packages; [
    flask
    psycopg2
    flask-sqlalchemy
    flask-cors
  ];
}
