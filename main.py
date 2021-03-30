import pandas as pd

from scripts.onthemarket import crawl_onthemarket
from scripts.zoopla import crawl_zoopla

URL = ""
data = crawl_zoopla(URL)
df = pd.DataFrame.from_dict(data)
df.to_excel("zoopla.xlsx")