export function bindKeyboardShortcuts({onToggleStopwatch,onResetStopwatch}) {
  document.addEventListener("keydown", event => {
    if(event.altKey||event.ctrlKey||event.metaKey) return;
    if(["INPUT","TEXTAREA","SELECT"].includes(document.activeElement?.tagName)) return;
    if(event.code==="Space"){event.preventDefault();onToggleStopwatch?.();}
    if(event.key.toLowerCase()==="r") onResetStopwatch?.();
  });
}
