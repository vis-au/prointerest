// https://stackoverflow.com/a/2901298
export function separateThousands(x: number, separator=","): string {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, separator);
}