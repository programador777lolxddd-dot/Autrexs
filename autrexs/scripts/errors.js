export class AutrexsError extends Error {
  constructor(message, code = "AUTREXS_ERROR") {
    super(message);
    this.name = "AutrexsError";
    this.code = code;
  }
}
