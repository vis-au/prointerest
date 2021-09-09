// https://stackoverflow.com/a/2901298
export function separateThousands(x: number, separator=","): string {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, separator);
}

export function abbreviate(x: number): string {
  if (x < 1000) {
    return `${x}`;
  } else if (x < 1000000) {
    return `${Math.floor(x / 100)/10}K`;
  } else if (x < 1000000000) {
    return `${Math.floor(x / 100000)/10}M`;
  } else {
    return `${Math.floor(x / 100000000)/10}B`;
  }
}