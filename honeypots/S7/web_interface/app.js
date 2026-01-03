const ws = new WebSocket(`ws://${location.host}/ws`);

ws.onmessage = (event) => {
  const d = JSON.parse(event.data);
  set("pump", d.pump, "ON", "OFF");
  set("valve", d.valve, "OPEN", "CLOSED");
  document.getElementById("temperature").textContent = d.temperature.toFixed(1);
  document.getElementById("pressure").textContent = d.pressure.toFixed(1);
};

function set(id, state, on, off) {
  const el = document.getElementById(id);
  el.textContent = state ? on : off;
  el.className = state ? "on" : "off";
}
