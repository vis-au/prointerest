export type ColorEncoding = "none" | "count" | "doi";
export const colorEncodings: ColorEncoding[] = ["count", "doi"];

export type SizeEncoding = "fixed" | "count" | "doi";
export const sizeEncodings: SizeEncoding[] = ["fixed", "count", "doi"];

export interface Encodings {
  x: string;
  y: string;
  color: ColorEncoding;
  size: SizeEncoding;
}
