#!/bin/bash
"{{ aiida_venv }}/bin/activate"
jupyter notebook --notebook-dir="{{ jupyter_base_folder }}" \
  --NotebookApp.default_url="/apps/apps/home/start.ipynb"
