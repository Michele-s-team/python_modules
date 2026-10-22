import os

# 1. root paths

# 1.1 root path for latex modules
latex_modules_root_path = '/Users/michelecastellana/Documents/latex_modules'

# 1.2 root path for latex_modules/finite_elements
root_path = os.path.join(latex_modules_root_path, 'finite_elements')

# 2. definitions

# 2.1 deinitions for latex_modules/finite_elements
definitions_path = os.path.join(root_path, 'definitions.tex')
packages_path = os.path.join(root_path, 'packages.tex')
figures_path = os.path.join(root_path, 'figures/')
modules_path = os.path.join(figures_path, 'modules/')

ale_definitions_path = os.path.join(root_path, 'ale', 'definitions.tex')

# 2.2 definitions for latex_modules
latex_module_definitions_path = os.path.join(latex_modules_root_path, 'definitions.tex')

