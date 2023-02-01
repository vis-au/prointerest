export type ColorEncoding = "count" | "doi";
export const colorEncodings: ColorEncoding[] = ["count", "doi"];

export type SizeEncoding = "count" | "fixed" | "doi";
export const sizeEncodings: SizeEncoding[] = ["count", "fixed", "doi"];

export interface Encodings {
  x: string;
  y: string;
  color: ColorEncoding;
  size: SizeEncoding;
}
