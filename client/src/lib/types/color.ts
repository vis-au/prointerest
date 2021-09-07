import {
  interpolateBuPu,
  interpolateBrBG,
  interpolateCividis,
  interpolateCool,
  interpolateCubehelixDefault,
  interpolateInferno,
  interpolateMagma,
  interpolatePiYG,
  interpolatePlasma,
  interpolatePRGn,
  interpolatePuOr,
  interpolateRdBu,
  interpolateRdGy,
  interpolateRdYlBu,
  interpolateRdYlGn,
  interpolateViridis,
  interpolateWarm,
  interpolateYlGnBu
} from "d3-scale-chromatic";

export const sequentialSchemes = [
  interpolateBuPu,
  interpolateYlGnBu,
  interpolateInferno,
  interpolateMagma,
  interpolatePlasma,
  interpolateCividis,
  interpolateWarm,
  interpolateCool,
  interpolateCubehelixDefault,
  interpolateViridis
];

export const divergingSchemes = [
  interpolateBrBG,
  interpolatePRGn,
  interpolatePiYG,
  interpolatePuOr,
  interpolateRdBu,
  interpolateRdGy,
  interpolateRdYlBu,
  interpolateRdYlGn
];

export type ColorScaleType = "log" | "linear";
export const colorScaleTypes: ColorScaleType[] = ["log", "linear"];
