// given the current progress of the computation, get the appropriate prior weight
export type DoiInterpolationFunction = (progress: number) => number;

const alpha = 0.01;
const beta = 2;

export const linear: DoiInterpolationFunction = (progress) => {
  return progress;
};
export const gaussian: DoiInterpolationFunction = (progress) => {
  return Math.exp(-(progress - alpha) / beta);
};
export const logarithmic: DoiInterpolationFunction = (progress) => {
  return Math.log10(progress);
};
export const exponential: DoiInterpolationFunction = (progress) => {
  return Math.exp(progress);
};
export const sigmoid: DoiInterpolationFunction = (progress) => {
  return 1 / (1 + Math.exp(-beta * (progress - alpha)));
};

export type FunctionName = "none"|"linear"|"gaussian"|"logarithmic"|"exponential"|"sigmoid";
export const functionNames: FunctionName[] = [
  "none", "linear", "gaussian", "logarithmic", "exponential", "sigmoid"
];

export const doiInterpolationFunctions: Map<FunctionName, DoiInterpolationFunction> = new Map();
doiInterpolationFunctions.set("none", null);
doiInterpolationFunctions.set("linear", linear);
doiInterpolationFunctions.set("gaussian", gaussian);
doiInterpolationFunctions.set("logarithmic", logarithmic);
doiInterpolationFunctions.set("exponential", exponential);
doiInterpolationFunctions.set("sigmoid", sigmoid);