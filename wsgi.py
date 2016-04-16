
from flaskapp import app as application

virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR','.'), 'virtenv')
httpd.serve_forever()
