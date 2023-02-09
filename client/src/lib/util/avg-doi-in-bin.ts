import { mean } from "d3";
import type { HexbinBin } from "d3-hexbin";

import { doiValues } from "$lib/state/doi-values";
import type DataItem from "$lib/types/data-item";


let currentDoiValues: Map<number, number> = null;
doiValues.subscribe(($doiValues) => (currentDoiValues = $doiValues));


export function getAvgDoiInBin(bin: HexbinBin<DataItem>) {
  return mean(bin.map((d) => currentDoiValues.get(d.id)));
}