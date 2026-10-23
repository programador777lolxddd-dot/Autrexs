// Base experimental; todavía no está integrada en la interfaz.
export class CountdownTimer {
  constructor(durationMs) {
    if (!Number.isFinite(durationMs) || durationMs < 0) throw new TypeError("Duración inválida");
    this.durationMs = durationMs;
    this.deadline = null;
  }
  start(now = Date.now()) { this.deadline = now + this.durationMs; }
  remaining(now = Date.now()) { return this.deadline === null ? this.durationMs : Math.max(0, this.deadline - now); }
  stop() { this.deadline = null; }
}
