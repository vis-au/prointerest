export function mapToRecord(map: Map<string, number | string>): Record<string, number | string> {
  const record: Record<string, number | string> = {};
  map.forEach((value, key) => (record[key] = value));
  return record;
}
