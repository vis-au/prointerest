import { interpolateBrBG, interpolateCividis, interpolateCool, interpolateCubehelixDefault,
   interpolateInferno, interpolateMagma, interpolatePiYG, interpolatePlasma, interpolatePRGn,
   interpolatePuOr, interpolateRdBu, interpolateRdGy, interpolateRdYlBu, interpolateRdYlGn,
   interpolateViridis, interpolateWarm, interpolateYlGnBu } from "d3-scale-chromatic";
import { writable } from "svelte/store";

export const sequentialSchemes = [
  interpolateYlGnBu,
  interpolateInferno,
  interpolateMagma,
  interpolatePlasma,
  interpolateCividis,
  interpolateWarm,
  interpolateCool,
  interpolateCubehelixDefault,
  interpolateViridis,
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

export const sequentialScheme = writable(interpolateViridis);
export const divergingScheme = writable(interpolatePiYG);