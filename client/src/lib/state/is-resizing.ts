import type { ResizeEvent } from "$lib/types/resize-event";
import { writable } from "svelte/store";

export const isResizing = writable(null as ResizeEvent);
