import seaborn as sns
import pandas as pd


PALETTE = "Set2"


def _apply_styles():
  sns.set_style("whitegrid")
  sns.set_palette(PALETTE)


def histogram_matrix(df: pd.DataFrame, x: str, row: str, column: str, hue: str):
  matrix = sns.FacetGrid(
    data=df,
    row=row,
    col=column,
    margin_titles=True,
    hue=hue,
  )
  matrix.map_dataframe(
    sns.histplot,
    x=x,
    binwidth=0.1,
    binrange=[-1, 1],
    kde=True,
    kde_kws={"bw_adjust": 4}
  )
  matrix.add_legend()
  _apply_styles()
  return matrix


def boxplot(df: pd.DataFrame, x: str, y: str, hue: str):
  plot = sns.catplot(
    kind="box",
    data=df,
    x=x,
    y=y,
    hue=hue,
    linewidth=1,
    margin_titles=True
  )
  sns.despine(left=True, bottom=True)
  _apply_styles()
  return plot


def boxplot_matrix(df: pd.DataFrame, x: str, y: str, hue: str, row: str, column: str):
  plot = sns.catplot(
    kind="box",
    data=df,
    x=x,
    y=y,
    row=row,
    col=column,
    hue=hue,
    linewidth=1,
    margin_titles=True
  )
  sns.despine(left=True, bottom=True)
  _apply_styles()
  return plot
