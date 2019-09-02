from polyglot.transliteration import Transliterator
from polyglot.downloader import downloader
print(downloader.supported_languages_table("transliteration2"))

from polyglot.text import Text
blob = """We will meet at eight o'clock on Thursday morning."""
text = Text(blob)
for x in text.transliterate("ar"):
  print(x)

