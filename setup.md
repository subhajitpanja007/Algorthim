> git config --list   
> git credential-manager uninstall  
> git config --global --unset credential.helper
> git config --global --unset credential.https
> git config --global credential.useHttpPath true
> git config --global --unset remote.origin.url
> git config --global --unset remote.origin         
> git config --global --unset user.name  
> git config --global --unset user.email
> git remote remove origin
> git config user.name "abcdef" 
> git config user.email "abcdef@gmail.com"  
> git remote add origin https://github.com/abcdef 
> git push -u origin main

` pip install virtualenv `
` virtualenv .venv `
` .\.venv\Scripts\activate ` 
` pip list > requirement.txt `
` pip list `
` pip install -r requirement.txt `
` deactivate `

#### Steps to Use setup.py
Create a Virtual Environment: If you haven’t already, create a virtual environment:
`python -m venv .venv`
source `.venv/bin/activate ` # On Windows use `.venv\Scripts\activate`

Install Dependencies: Ensure all dependencies are installed in your virtual environment:
`pip install -r requirements.txt`

Build and Install Your Package:
`python setup.py sdist bdist_wheel`
`pip install .`

`[Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html)`   

Parent Directory:
Python

`sys.path.insert(0, '../')`

Specific Directory (e.g., my_directory):
Python

`sys.path.insert(0, '/path/to/my_directory')`

Sibling Directory (relative to the current file):
Python

`sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../sibling_directory'))`

Grandparent Directory:
Python

`sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))`