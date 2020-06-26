import os
import argparse

def get_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--source', dest="source", type=str, required=True, help='path of the audio files.')
  parser.add_argument('-l', '--size', dest="size", type=int, default=88, help='path of the audio files.')
  arguments = parser.parse_args()

  return arguments

def delete_file(source, limit):
  print("Source: {} and limit: {}".format(str(source), str(limit)))
  # r=root, d=directories, f = files
  for r, d, f in os.walk(source):
    for file in f:
        if file.endswith(".wav"):
            filepath = os.path.join(r, file)
            size = os.path.getsize(filepath)
            if(size < limit):
              print("name: {}, size: {}".format(str(filepath), str(size)))
              os.remove(filepath)

if __name__ == "__main__":
  args = get_arguments()
  delete_file(args.source, args.size)