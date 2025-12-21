const protocol = location.protocol === "https:" ? "wss" : "ws";
const ws = new WebSocket(`${protocol}://${location.host}/ws`);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  setStatus("pump", data.pump, "ON", "OFF");
  setStatus("valve", data.valve, "OPEN", "CLOSED");

  document.getElementById("temp").textContent = data.temperature.toFixed(1);
  document.getElementById("pressure").textContent = data.pressure.toFixed(1);
};

function setStatus(id, state, onText, offText) {
  const el = document.getElementById(id);
  el.textContent = state ? onText : offText;
  el.className = state ? "on" : "off";
}
