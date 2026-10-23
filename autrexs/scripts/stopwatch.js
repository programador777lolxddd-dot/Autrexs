export class Stopwatch {
  #startedAt = null;
  #elapsedBeforeStart = 0;

  get running() { return this.#startedAt !== null; }

  start() {
    if (!this.running) this.#startedAt = performance.now();
  }

  pause() {
    if (this.running) {
      this.#elapsedBeforeStart += performance.now() - this.#startedAt;
      this.#startedAt = null;
    }
  }

  elapsed() {
    return this.#elapsedBeforeStart + (this.running ? performance.now() - this.#startedAt : 0);
  }

  reset() {
    this.#startedAt = null;
    this.#elapsedBeforeStart = 0;
  }
}
