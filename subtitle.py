import pysrt


if __name__ == "__main__":
  file = pysrt.SubRipFile()
  sub = pysrt.SubRipItem(1, start='00:02:04,000', end='00:02:08,000', text="Hello World!")
  file.append(sub)
  file.save('vocals.srt')