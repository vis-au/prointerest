import { dispatch, select, pointer } from "d3";
import type { Selection } from "d3-selection";

export function lasso(): {
  (selection: Selection<any, any, any, any>): void;
  on(type: string, _: (e: unknown) => void): any;
} {
  const lassoDispatcher = dispatch("start", "lasso", "end");

  const trackPointer = function (e: any, { start, move, out, end }: Record<string, any>) {
    const tracker: Record<string, any> = {};
    const id = (tracker.id = e.pointerId);
    const target = e.target;

    tracker.point = pointer(e, target);
    target.setPointerCapture(id);

    select(target)
      .on(`pointerup.${id} pointercancel.${id}`, (e: any) => {
        if (e.pointerId !== id) return;
        tracker.sourceEvent = e;
        select(target).on(`.${id}`, null);
        target.releasePointerCapture(id);
        end && end(tracker);
      })
      .on(`pointermove.${id}`, (e: any) => {
        if (e.pointerId !== id) return;
        tracker.sourceEvent = e;
        tracker.prev = tracker.point;
        tracker.point = pointer(e, target);
        move && move(tracker);
      })
      .on(`pointerout.${id}`, (e: any) => {
        if (e.pointerId !== id) return;
        tracker.sourceEvent = e;
        tracker.point = null;
        out && out(tracker);
      });

    start && start(tracker);
  };

  const lasso = function (selection: Selection<any, any, any, any>) {
    const node = selection.node();
    const polygon: [number, number][] = [];

    selection
      .on("touchmove", (e) => e.preventDefault()) // prevent scrolling
      .on("pointerdown", (e) => {
        trackPointer(e, {
          start: () => {
            polygon.length = 0;
            lassoDispatcher.call("start", node, polygon);
          },
          move: (p: { point: [number, number] }) => {
            polygon.push(p.point);
            lassoDispatcher.call("lasso", node, polygon);
          },
          end: () => {
            lassoDispatcher.call("end", node, polygon);
          }
        });
      });
  };

  lasso.on = function (type: "start" | "move" | "out" | "end", callback: (e: unknown) => void) {
    lassoDispatcher.on(type, callback);
    return lasso;
  };

  return lasso;
}
