export type ColorEncoding = "count" | "doi";
export const colorEncodings: ColorEncoding[] = ["count", "doi"];

export type SizeEncoding = "count" | "fixed";
export const sizeEncodings: SizeEncoding[] = ["count", "fixed"];

export interface Encodings {
  x: string;
  y: string;
  color: ColorEncoding;
  size: SizeEncoding;
}
