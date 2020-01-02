from argparse import ArgumentParser
from pathlib import Path
import os, sys

from .main import main as real_main

parser = ArgumentParser(description='Try to pull some git repositories, and update a docker image if there were changes')
parser.add_argument('root', metavar='DIR', default='.', nargs='?', help='Root directory containing `repos` and `Dockerfile`')
parser.add_argument('--image-name', metavar='NAME', default='breedbase', help='Name to tag the docker image with')
parser.add_argument('--write-logs', metavar='DIR', help='Write log files to DIR')
parser.add_argument('-c', '--update-compose', action='store_true', help='Update running container on docker-compose')
parser.add_argument('-v', '--verbose', action='store_true', help='Extra output')
parser.add_argument('-n', '--dry-run', action='store_true', help='Do not update trees or build the image, but otherwise pretend to')

def main(args=None):
  error = 0
  options = parser.parse_args(args)
  options.repos = os.path.join(options.root, 'repos')
  options.compose_root = Path(__file__).resolve().parent.parent.parent
  if sys.stdout.isatty():
    try:
      print(options)
      # error = real_main(options)
    except KeyboardInterrupt:
      error = 0
    except:
      import ipdb, traceback
      traceback.print_exc()
      extype, value, tb = sys.exc_info()
      ipdb.post_mortem(tb)
  else:
    error = real_main(options)
  sys.exit(error)