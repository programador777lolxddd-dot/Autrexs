export function onVisibilityChange(callback) {
  const handler=()=>callback(document.visibilityState==="visible");
  document.addEventListener("visibilitychange",handler);
  return ()=>document.removeEventListener("visibilitychange",handler);
}
