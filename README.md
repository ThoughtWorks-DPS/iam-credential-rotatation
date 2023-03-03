# iami-credential-rotation
Pattern for automated rotation of IAM machine-user credentials





 setup
 1. basic folder structure

src/
- MAIN_SCRIPT_NAME.py
tests/
LICENSE
setup.py

2. setup venv
3. python setup.py develop
4. python -m build
5. python3 -m twine upload --repository testpypi dist/*

