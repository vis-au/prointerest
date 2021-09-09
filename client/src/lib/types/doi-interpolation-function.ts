export type DoiInterpolationFunction = (prior: number) => number;

const alpha = 0.01;
const beta = 2;

export const linear: DoiInterpolationFunction = (prior) => {
  return 1 - prior;
};
export const gaussian: DoiInterpolationFunction = (prior) => {
  return 1 - Math.exp(-(prior - alpha) / beta);
};
export const logarithmic: DoiInterpolationFunction = (prior) => {
  return 1 - Math.log10(prior);
};
export const exponential: DoiInterpolationFunction = (prior) => {
  return 1 - Math.exp(prior);
};
export const sigmoid: DoiInterpolationFunction = (prior) => {
  return 1 - 1 / (1 + Math.exp(-beta * (prior - alpha)));
};

export const doiInterpolationFunctions: DoiInterpolationFunction[] = [
  linear, gaussian, logarithmic, exponential, sigmoid
];
export const doiInterpolationFunctionNames = [
  "linear", "gaussian", "logarithmic", "exponential", "sigmoid"
];