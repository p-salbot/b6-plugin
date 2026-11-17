import sys

from reorder.cli import configure_output, main

configure_output(sys.stdout, sys.stderr)
sys.exit(main())
